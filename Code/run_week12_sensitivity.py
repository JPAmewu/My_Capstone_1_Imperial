"""Run a non-submission Week 12 acquisition and GP-bound sensitivity study."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import qmc
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern, WhiteKernel

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Code.candidate_generation import make_rng, uniform_candidates
from Code.data_loading import append_observations, load_starter_data
from Code.gaussian_process import predict_with_uncertainty
from Code.query_selection import select_query
from Code.portal_format import SUBMISSION_LOWER_BOUND, SUBMISSION_UPPER_BOUND, format_portal_query
from Code.weekly_evidence import DIMENSIONS, pairs_through_week


KAPPAS = (0.1, 0.5, 1.0, 2.0)
BOUND_PROFILES = {
    "standard": {
        "constant": (1e-3, 1e3),
        "length_scale": (0.01, 2.0),
        "noise": (1e-10, 1e-2),
    },
    "wide": {
        "constant": (1e-5, 1e5),
        "length_scale": (1e-3, 10.0),
        "noise": (1e-12, 1e-1),
    },
}


def repository_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    if not (root / "Results" / "query_output_ledger.csv").is_file():
        raise FileNotFoundError("canonical ledger not found")
    return root


def cumulative_data(function: int, root: Path) -> tuple[np.ndarray, np.ndarray]:
    X, y = load_starter_data(function, repository_root=root)
    pairs = pairs_through_week(11, function)
    return append_observations(
        X,
        y,
        [query for query, _ in pairs],
        [value for _, value in pairs],
    )


def candidate_set(function: int) -> tuple[np.ndarray, str, int]:
    dimensions = DIMENSIONS[function]
    seed = 9100 + function
    if function >= 6:
        exponent = 15
        unit_candidates = qmc.Sobol(dimensions, scramble=True, seed=seed).random_base2(exponent)
        candidates = qmc.scale(
            unit_candidates,
            SUBMISSION_LOWER_BOUND,
            SUBMISSION_UPPER_BOUND,
        )
        return candidates, "sobol", 2**exponent
    count = 20_000
    candidates = uniform_candidates(dimensions, count, rng=make_rng(seed))
    return candidates, "uniform_random", count


def kernel_for(dimensions: int, profile: dict):
    return (
        ConstantKernel(1.0, profile["constant"])
        * Matern(
            np.full(dimensions, 0.2),
            length_scale_bounds=profile["length_scale"],
            nu=2.5,
        )
        + WhiteKernel(1e-6, profile["noise"])
    )


def run(root: Path) -> pd.DataFrame:
    rows: list[dict] = []
    for function in range(1, 9):
        X, y = cumulative_data(function, root)
        candidates, scheme, count = candidate_set(function)
        for profile_name, bounds in BOUND_PROFILES.items():
            model = GaussianProcessRegressor(
                kernel=kernel_for(X.shape[1], bounds),
                normalize_y=True,
                n_restarts_optimizer=3,
                random_state=9200 + function,
            ).fit(X, y)
            mean, std = predict_with_uncertainty(model, candidates)
            strategies = [(f"ucb_kappa_{kappa:g}", "ucb", kappa) for kappa in KAPPAS]
            strategies.append(("expected_improvement_xi_0.01", "ei", None))
            for strategy, method, kappa in strategies:
                selected = select_query(
                    candidates,
                    X,
                    mean,
                    std,
                    method=method,
                    kappa=0.0 if kappa is None else kappa,
                    best=float(np.max(y)),
                    xi=0.01,
                    decimals=6,
                )
                rows.append(
                    {
                        "function": function,
                        "dimensions": X.shape[1],
                        "observation_count": len(X),
                        "bound_profile": profile_name,
                        "candidate_scheme": scheme,
                        "candidate_count": count,
                        "strategy": strategy,
                        "kappa": np.nan if kappa is None else kappa,
                        "xi": 0.01 if method == "ei" else np.nan,
                        "query": json.dumps(selected.query.tolist(), separators=(",", ":")),
                        "submission_query": format_portal_query(
                            selected.query, dimensions=X.shape[1]
                        ),
                        "predicted_mean": selected.predicted_mean,
                        "predictive_std": selected.predicted_std,
                        "acquisition_score": selected.acquisition,
                        "fitted_kernel": str(model.kernel_),
                        "duplicate_at_6dp": False,
                        "experiment_status": "sensitivity_only_not_submitted",
                    }
                )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("Results/week12_sensitivity_analysis.csv"),
    )
    args = parser.parse_args()
    root = repository_root()
    result = run(root)
    output = args.output if args.output.is_absolute() else root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False)
    print(f"Saved {len(result)} sensitivity rows to {output}")


if __name__ == "__main__":
    main()
