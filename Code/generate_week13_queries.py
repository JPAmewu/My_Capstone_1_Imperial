"""Generate reproducible 12th-round queries for the Week 13 strategy."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import warnings
from pathlib import Path

import numpy as np
from scipy.stats import qmc
from sklearn.exceptions import ConvergenceWarning

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Code.acquisition_function import expected_improvement, probability_improvement, upper_confidence_bound  # noqa: E402
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


def load_evidence(root: Path, function: int) -> tuple[np.ndarray, np.ndarray]:
    data = root / "Week_01" / f"Function_{function:02d}" / "03_Data"
    inputs = np.load(data / "initial_inputs.npy", allow_pickle=False)
    outputs = np.load(data / "initial_outputs.npy", allow_pickle=False).reshape(-1)
    pairs = pairs_through_week(12, function)
    inputs = np.vstack([inputs] + [np.asarray(query, float)[None, :] for query, _ in pairs])
    outputs = np.r_[outputs, [value for _, value in pairs]]
    return validate_observations(inputs, outputs, dimensions=DIMENSIONS[function])


def candidate_pool(inputs: np.ndarray, outputs: np.ndarray, function: int, local_scale: float):
    dimensions = inputs.shape[1]
    global_points = qmc.Sobol(dimensions, scramble=True, seed=1300 + function).random_base2(15)
    top = np.argsort(outputs)[-min(3, len(outputs)):]
    rng = np.random.default_rng(2300 + function)
    local_points = np.vstack([
        np.clip(inputs[index] + rng.normal(0, local_scale, (4096, dimensions)), 0, SUBMISSION_UPPER_BOUND)
        for index in top
    ])
    points = np.vstack((global_points, local_points))
    sources = np.array(["sobol"] * len(global_points) + ["local"] * len(local_points))
    return points, sources


def generate(root: Path) -> tuple[list[dict], list[dict]]:
    selected_rows, comparison_rows = [], []
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
            comparison_rows.append({
                "function": function, "method": method,
                "candidate": json.dumps(np.round(points[index], 6).tolist(), separators=(",", ":")),
                "candidate_source": sources[index], "acquisition_score": float(score_map[method][index]),
                "predicted_mean": float(mean[index]), "predicted_std": float(std[index]),
                "kappa": policy["kappa"], "xi": xi,
                "xi_fraction_of_output_std": policy["xi_fraction"],
            })
        chosen_method = policy["method"].upper()
        index = indices[chosen_method]
        query = np.clip(np.round(points[index], 6), 0.0, SUBMISSION_UPPER_BOUND)
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
            "candidate_count": len(points), "predicted_mean": float(mean[index]),
            "predicted_std": float(std[index]), "selected_acquisition": float(score_map[chosen_method][index]),
            "distance_from_incumbent": float(np.linalg.norm(query - inputs[int(np.argmax(outputs))])),
            "verified_observations": len(outputs), "verified_best": float(np.max(outputs)),
            "week_12_output": float(outputs[-1]),
            "week_12_improvement": float(outputs[-1] - np.max(outputs[:-1])),
            "reason": policy["reason"],
        })
    return selected_rows, comparison_rows


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def write_outputs(root: Path, selected: list[dict], comparison: list[dict]) -> None:
    query_dir, result_dir = root / "Week_13" / "01_Queries", root / "Week_13" / "04_Results"
    query_dir.mkdir(parents=True, exist_ok=True); result_dir.mkdir(parents=True, exist_ok=True)
    query_file = query_dir / "week_13_query_points.txt"
    lines = []
    for row in selected:
        values = json.loads(row["query"])
        portal = format_portal_query(values, dimensions=int(row["dimensions"]))
        validate_portal_query(portal, dimensions=int(row["dimensions"]))
        lines.append(f"Function_{row['function']}:{portal}\n")
    query_file.write_text("".join(lines), encoding="utf-8")
    write_csv(result_dir / "week_13_strategy_summary.csv", selected)
    write_csv(result_dir / "week_13_acquisition_comparison.csv", comparison)
    print(query_file.read_text(), end="")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    args = parser.parse_args(); root = args.repository.resolve()
    write_outputs(root, *generate(root))


if __name__ == "__main__":
    main()
