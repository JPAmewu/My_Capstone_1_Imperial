"""Generate Week 13 proposals from the 12 completed Week 1–12 rounds."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import warnings
from pathlib import Path

import numpy as np
from scipy.stats import qmc
from sklearn.exceptions import ConvergenceWarning

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Code.acquisition_function import expected_improvement, probability_improvement, upper_confidence_bound  # noqa: E402
from Code.candidate_generation import reflected_local_candidates  # noqa: E402
from Code.data_validation import duplicate_mask, validate_observations  # noqa: E402
from Code.gaussian_process import fit_gaussian_process, predict_with_uncertainty  # noqa: E402
from Code.portal_format import SUBMISSION_UPPER_BOUND, format_portal_query, validate_portal_query  # noqa: E402
from Code.weekly_evidence import DIMENSIONS, pairs_through_week  # noqa: E402


POLICY = {
    1: {"method": "ucb", "kappa": 3.0, "xi_fraction": 0.01, "local_scale": 0.12,
        "reason": "Sparse near-zero responses still justify uncertainty-led exploration."},
    2: {"method": "ei", "kappa": 2.0, "xi_fraction": 0.02, "local_scale": 0.10,
        "reason": "The strong Week 12 return supports balanced improvement around a promising region."},
    3: {"method": "pi", "kappa": 1.5, "xi_fraction": 0.005, "local_scale": 0.035,
        "reason": "The new best reinforces a stable structure and supports controlled exploitation."},
    4: {"method": "ucb", "kappa": 2.75, "xi_fraction": 0.02, "local_scale": 0.14,
        "reason": "The large Week 12 improvement is promising, while high kappa tests its surrounding uncertainty."},
    5: {"method": "ei", "kappa": 1.5, "xi_fraction": 0.01, "local_scale": 0.07,
        "reason": "The much stronger Week 12 incumbent warrants focused expected improvement."},
    6: {"method": "ei", "kappa": 1.75, "xi_fraction": 0.01, "local_scale": 0.08,
        "reason": "The Week 12 best supports exploitation with uncertainty protection."},
    7: {"method": "ucb", "kappa": 2.0, "xi_fraction": 0.01, "local_scale": 0.09,
        "reason": "The new best supports local focus while moderate UCB preserves exploration."},
    8: {"method": "ucb", "kappa": 3.0, "xi_fraction": 0.02, "local_scale": 0.12,
        "reason": "A near-best Week 12 result does not remove eight-dimensional sparsity, so exploration remains strong."},
}

SOBOL_COUNT = 32768
LOCAL_CENTRES = 3
LOCAL_COUNT_PER_CENTRE = 4096
FROZEN_QUERY_SHA256 = "55e012ff2df6bd04fa8d78c527c3c5fe32634cdf9da0744ecfcf22cbd4537686"


def load_evidence(root: Path, function: int) -> tuple[np.ndarray, np.ndarray]:
    data = root / "Week_01" / f"Function_{function:02d}" / "03_Data"
    inputs = np.load(data / "initial_inputs.npy", allow_pickle=False)
    outputs = np.load(data / "initial_outputs.npy", allow_pickle=False).reshape(-1)
    pairs = pairs_through_week(12, function)
    inputs = np.vstack([inputs] + [np.asarray(query, float)[None, :] for query, _ in pairs])
    outputs = np.r_[outputs, [value for _, value in pairs]]
    return validate_observations(inputs, outputs, dimensions=DIMENSIONS[function])


def candidate_pool(
    inputs: np.ndarray,
    outputs: np.ndarray,
    function: int,
    local_scale: float,
    *,
    boundary_method: str = "clip",
):
    dimensions = inputs.shape[1]
    global_points = qmc.Sobol(dimensions, scramble=True, seed=1300 + function).random_base2(
        int(np.log2(SOBOL_COUNT))
    )
    top = np.argsort(outputs)[-min(LOCAL_CENTRES, len(outputs)):]
    rng = np.random.default_rng(2300 + function)
    if boundary_method == "clip":
        local_points = np.vstack([
            np.clip(
                inputs[index] + rng.normal(0, local_scale, (LOCAL_COUNT_PER_CENTRE, dimensions)),
                0,
                SUBMISSION_UPPER_BOUND,
            )
            for index in top
        ])
    elif boundary_method == "reflect":
        local_points = np.vstack([
            reflected_local_candidates(
                inputs[index], LOCAL_COUNT_PER_CENTRE, rng=rng, scale=local_scale
            )
            for index in top
        ])
    else:
        raise ValueError("boundary_method must be 'clip' or 'reflect'")
    points = np.vstack((global_points, local_points))
    sources = np.array(["sobol"] * len(global_points) + ["local"] * len(local_points))
    return points, sources


def acquisition_scores(
    method: str,
    mean: np.ndarray,
    std: np.ndarray,
    *,
    best: float,
    kappa: float,
    xi: float,
) -> np.ndarray:
    if method == "UCB":
        return upper_confidence_bound(mean, std, kappa=kappa)
    if method == "EI":
        return expected_improvement(mean, std, best=best, xi=xi)
    if method == "PI":
        return probability_improvement(mean, std, best=best, xi=xi)
    raise ValueError(f"unsupported acquisition method: {method}")


def diagnostics_at_rounded_point(model, point: np.ndarray, method: str, policy: dict, best: float, xi: float):
    rounded = np.clip(np.round(point, 6), 0.0, SUBMISSION_UPPER_BOUND)
    mean, std = predict_with_uncertainty(model, rounded[None, :])
    score = acquisition_scores(
        method, mean, std, best=best, kappa=policy["kappa"], xi=xi
    )
    return rounded, float(mean[0]), float(std[0]), float(score[0])


def generate(root: Path) -> tuple[list[dict], list[dict], list[dict]]:
    selected_rows, comparison_rows, boundary_rows = [], [], []
    for function in range(1, 9):
        policy = POLICY[function]
        inputs, outputs = load_evidence(root, function)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ConvergenceWarning)
            model = fit_gaussian_process(inputs, outputs, optimizer_restarts=5, random_state=1300 + function)
        points, sources = candidate_pool(inputs, outputs, function, policy["local_scale"])
        mean, std = predict_with_uncertainty(model, points)
        output_scale = max(float(np.std(outputs)), np.finfo(float).eps)
        xi = policy["xi_fraction"] * output_scale
        score_map = {
            "UCB": upper_confidence_bound(mean, std, kappa=policy["kappa"]),
            "EI": expected_improvement(mean, std, best=float(np.max(outputs)), xi=xi),
            "PI": probability_improvement(mean, std, best=float(np.max(outputs)), xi=xi),
        }
        duplicates = duplicate_mask(points, inputs, decimals=6)
        for scores in score_map.values():
            scores[duplicates] = -np.inf
        indices = {method: int(np.argmax(scores)) for method, scores in score_map.items()}
        length_scales = np.atleast_1d(model.kernel_.k1.k2.length_scale).tolist()
        for method, index in indices.items():
            rounded, rounded_mean, rounded_std, rounded_score = diagnostics_at_rounded_point(
                model, points[index], method, policy, float(np.max(outputs)), xi
            )
            comparison_rows.append({
                "function": function, "method": method,
                "candidate": json.dumps(rounded.tolist(), separators=(",", ":")),
                "candidate_source": sources[index], "acquisition_score": rounded_score,
                "predicted_mean": rounded_mean, "predicted_std": rounded_std,
                "kappa": policy["kappa"], "xi": xi,
                "xi_fraction_of_output_std": policy["xi_fraction"],
                "diagnostic_coordinate": "rounded_submission_6dp",
            })
        chosen_method = policy["method"].upper()
        index = indices[chosen_method]
        query, query_mean, query_std, query_score = diagnostics_at_rounded_point(
            model, points[index], chosen_method, policy, float(np.max(outputs)), xi
        )
        if duplicate_mask(query[None, :], inputs, decimals=6)[0]:
            raise RuntimeError(f"F{function}: selected an observed duplicate")
        selected_rows.append({
            "function": function, "dimensions": DIMENSIONS[function],
            "query": json.dumps(query.tolist(), separators=(",", ":")),
            "method": chosen_method, "kernel": str(model.kernel_),
            "fitted_length_scales": json.dumps(length_scales, separators=(",", ":")),
            "kappa": policy["kappa"], "xi": xi,
            "xi_fraction_of_output_std": policy["xi_fraction"],
            "local_scale": policy["local_scale"], "candidate_source": sources[index],
            "candidate_count": len(points), "predicted_mean": query_mean,
            "predicted_std": query_std, "selected_acquisition": query_score,
            "diagnostic_coordinate": "rounded_submission_6dp",
            "distance_from_incumbent": float(np.linalg.norm(query - inputs[int(np.argmax(outputs))])),
            "verified_observations": len(outputs), "verified_best": float(np.max(outputs)),
            "week_12_output": float(outputs[-1]),
            "week_12_improvement": float(outputs[-1] - np.max(outputs[:-1])),
            "reason": policy["reason"],
        })
        if function in (2, 5, 6):
            frozen_query = query.copy()
            for boundary_method in ("clip", "reflect"):
                sensitivity_points, sensitivity_sources = candidate_pool(
                    inputs, outputs, function, policy["local_scale"], boundary_method=boundary_method
                )
                sensitivity_mean, sensitivity_std = predict_with_uncertainty(model, sensitivity_points)
                sensitivity_score = acquisition_scores(
                    chosen_method,
                    sensitivity_mean,
                    sensitivity_std,
                    best=float(np.max(outputs)),
                    kappa=policy["kappa"],
                    xi=xi,
                )
                sensitivity_score[duplicate_mask(sensitivity_points, inputs, decimals=6)] = -np.inf
                sensitivity_index = int(np.argmax(sensitivity_score))
                sensitivity_query, sensitivity_mu, sensitivity_sigma, sensitivity_acquisition = diagnostics_at_rounded_point(
                    model,
                    sensitivity_points[sensitivity_index],
                    chosen_method,
                    policy,
                    float(np.max(outputs)),
                    xi,
                )
                boundary_rows.append({
                    "function": function,
                    "method": chosen_method,
                    "boundary_generation": boundary_method,
                    "query": json.dumps(sensitivity_query.tolist(), separators=(",", ":")),
                    "candidate_source": sensitivity_sources[sensitivity_index],
                    "is_boundary_recommendation": bool(
                        np.any((sensitivity_query == 0.0) | (sensitivity_query == SUBMISSION_UPPER_BOUND))
                    ),
                    "matches_frozen_week13_query": bool(np.array_equal(sensitivity_query, frozen_query)),
                    "distance_from_frozen_query": float(np.linalg.norm(sensitivity_query - frozen_query)),
                    "predicted_mean": sensitivity_mu,
                    "predicted_std": sensitivity_sigma,
                    "selected_acquisition": sensitivity_acquisition,
                    "candidate_count": len(sensitivity_points),
                    "local_scale": policy["local_scale"],
                    "sobol_seed": 1300 + function,
                    "local_seed": 2300 + function,
                    "status": "diagnostic_only_frozen_query_unchanged",
                })
    return selected_rows, comparison_rows, boundary_rows


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def write_outputs(root: Path, selected: list[dict], comparison: list[dict], boundary: list[dict]) -> None:
    query_dir, result_dir = root / "Week_13" / "01_Queries", root / "Week_13" / "04_Results"
    query_dir.mkdir(parents=True, exist_ok=True); result_dir.mkdir(parents=True, exist_ok=True)
    query_file = query_dir / "week_13_query_points.txt"
    lines = []
    for row in selected:
        values = json.loads(row["query"])
        portal = format_portal_query(values, dimensions=int(row["dimensions"]))
        validate_portal_query(portal, dimensions=int(row["dimensions"]))
        lines.append(f"Function_{row['function']}:{portal}\n")
    generated = "".join(lines).encode("utf-8")
    generated_hash = hashlib.sha256(generated).hexdigest()
    if generated_hash != FROZEN_QUERY_SHA256:
        raise RuntimeError(
            "generated Week 13 query set differs from immutable pre-outcome evidence: "
            f"{generated_hash}"
        )
    if query_file.exists() and query_file.read_bytes() != generated:
        raise RuntimeError("refusing to overwrite immutable Week 13 query evidence")
    if not query_file.exists():
        query_file.write_bytes(generated)
    write_csv(result_dir / "week_13_strategy_summary.csv", selected)
    write_csv(result_dir / "week_13_acquisition_comparison.csv", comparison)
    write_csv(result_dir / "week_13_boundary_generation_sensitivity.csv", boundary)
    print(query_file.read_text(), end="")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    args = parser.parse_args(); root = args.repository.resolve()
    write_outputs(root, *generate(root))


if __name__ == "__main__":
    main()
