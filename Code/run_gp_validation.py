"""Rolling-origin GP validation, calibration, and hyperparameter diagnostics."""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm
from sklearn.exceptions import ConvergenceWarning

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Code.data_loading import append_observations, load_starter_data
from Code.gaussian_process import fit_gaussian_process
from Code.weekly_evidence import DIMENSIONS, pairs_through_week


RANDOM_SEED_BASE = 7300
COVERAGE_LEVELS = (0.50, 0.80, 0.95)


def repository_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    if not (root / "Results" / "query_output_ledger.csv").is_file():
        raise FileNotFoundError("canonical ledger not found")
    return root


def kernel_parameters(model) -> dict:
    """Extract fitted Matérn GP parameters and configured-bound diagnostics."""
    kernel = model.kernel_
    constant = float(kernel.k1.k1.constant_value)
    length_scales = np.atleast_1d(kernel.k1.k2.length_scale).astype(float)
    noise = float(kernel.k2.noise_level)
    constant_bounds = np.asarray(kernel.k1.k1.constant_value_bounds, dtype=float)
    length_bounds = np.asarray(kernel.k1.k2.length_scale_bounds, dtype=float)
    noise_bounds = np.asarray(kernel.k2.noise_level_bounds, dtype=float)

    def at_bound(value: float, bounds: np.ndarray) -> str:
        low, high = float(bounds[0]), float(bounds[1])
        tolerance = 1e-6
        if np.isclose(value, low, rtol=tolerance, atol=0.0):
            return "lower"
        if np.isclose(value, high, rtol=tolerance, atol=0.0):
            return "upper"
        return "none"

    length_flags = [at_bound(value, length_bounds) for value in length_scales]
    return {
        "constant_value": constant,
        "length_scales": json.dumps(length_scales.tolist(), separators=(",", ":")),
        "min_length_scale": float(length_scales.min()),
        "max_length_scale": float(length_scales.max()),
        "noise_level": noise,
        "constant_bound_status": at_bound(constant, constant_bounds),
        "length_scale_bound_status": json.dumps(length_flags, separators=(",", ":")),
        "length_scales_at_lower_bound": int(length_flags.count("lower")),
        "length_scales_at_upper_bound": int(length_flags.count("upper")),
        "noise_bound_status": at_bound(noise, noise_bounds),
        "any_parameter_at_bound": bool(
            at_bound(constant, constant_bounds) != "none"
            or any(flag != "none" for flag in length_flags)
            or at_bound(noise, noise_bounds) != "none"
        ),
        "fitted_kernel": str(kernel),
    }


def rolling_predictions(root: Path) -> pd.DataFrame:
    rows: list[dict] = []
    for function in range(1, 9):
        X, y = load_starter_data(function, repository_root=root)
        for week, (query, returned) in enumerate(pairs_through_week(12, function), start=1):
            train_count = len(y)
            train_mean = float(np.mean(y))
            train_scale = float(np.std(y))
            if train_scale <= 0:
                train_scale = 1.0
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always", ConvergenceWarning)
                model = fit_gaussian_process(
                    X,
                    y,
                    optimizer_restarts=1,
                    random_state=RANDOM_SEED_BASE + function * 100 + week,
                )
            point = np.asarray(query, dtype=float).reshape(1, -1)
            mean, std = model.predict(point, return_std=True)
            predicted = float(mean[0])
            predictive_std = max(float(std[0]), np.finfo(float).eps)
            residual = float(returned - predicted)
            z_score = residual / predictive_std
            row = {
                "function": function,
                "dimensions": DIMENSIONS[function],
                "held_out_week": week,
                "training_observations": train_count,
                "actual": float(returned),
                "predicted_mean": predicted,
                "predictive_std": predictive_std,
                "residual": residual,
                "absolute_error": abs(residual),
                "squared_error": residual**2,
                "standardized_residual": z_score,
                "absolute_standardized_error": abs(residual) / train_scale,
                "naive_training_mean": train_mean,
                "naive_squared_error": float((returned - train_mean) ** 2),
                "negative_log_predictive_density": float(
                    0.5 * np.log(2 * np.pi * predictive_std**2) + 0.5 * z_score**2
                ),
                "convergence_warning_count": sum(
                    issubclass(item.category, ConvergenceWarning) for item in caught
                ),
            }
            for level in COVERAGE_LEVELS:
                critical = float(norm.ppf((1 + level) / 2))
                row[f"covered_{int(level * 100)}"] = abs(z_score) <= critical
            row.update(kernel_parameters(model))
            rows.append(row)
            X, y = append_observations(X, y, [query], [returned])
    return pd.DataFrame(rows)


def aggregate_metrics(predictions: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    for function, frame in predictions.groupby("function", sort=True):
        rmse = float(np.sqrt(frame["squared_error"].mean()))
        naive_rmse = float(np.sqrt(frame["naive_squared_error"].mean()))
        rows.append(
            {
                "function": int(function),
                "dimensions": int(frame["dimensions"].iloc[0]),
                "rolling_folds": len(frame),
                "mae": float(frame["absolute_error"].mean()),
                "rmse": rmse,
                "naive_mean_rmse": naive_rmse,
                "rmse_skill_vs_naive": float(1 - rmse / naive_rmse) if naive_rmse else np.nan,
                "mean_absolute_standardized_error": float(
                    frame["absolute_standardized_error"].mean()
                ),
                "mean_negative_log_predictive_density": float(
                    frame["negative_log_predictive_density"].mean()
                ),
                "coverage_50": float(frame["covered_50"].mean()),
                "coverage_80": float(frame["covered_80"].mean()),
                "coverage_95": float(frame["covered_95"].mean()),
                "mean_predictive_std": float(frame["predictive_std"].mean()),
                "mean_abs_z": float(frame["standardized_residual"].abs().mean()),
                "hyperparameter_bound_hit_rate": float(
                    frame["any_parameter_at_bound"].mean()
                ),
                "convergence_warning_folds": int(
                    (frame["convergence_warning_count"] > 0).sum()
                ),
            }
        )
    return pd.DataFrame(rows)


def final_hyperparameters(root: Path) -> pd.DataFrame:
    rows: list[dict] = []
    for function in range(1, 9):
        X, y = load_starter_data(function, repository_root=root)
        pairs = pairs_through_week(12, function)
        X, y = append_observations(
            X, y, [query for query, _ in pairs], [value for _, value in pairs]
        )
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ConvergenceWarning)
            model = fit_gaussian_process(
                X,
                y,
                optimizer_restarts=3,
                random_state=4200 + function,
            )
        row = {
            "function": function,
            "dimensions": DIMENSIONS[function],
            "observation_count": len(y),
            "optimizer_restarts": 3,
            "random_seed": 4200 + function,
            "convergence_warning_count": sum(
                issubclass(item.category, ConvergenceWarning) for item in caught
            ),
        }
        row.update(kernel_parameters(model))
        rows.append(row)
    return pd.DataFrame(rows)


def plot_diagnostics(predictions: pd.DataFrame, metrics: pd.DataFrame, output: Path) -> None:
    """Plot empirical interval coverage and uncertainty/error alignment."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    functions = metrics["function"].to_numpy()
    offsets = (-0.22, 0.0, 0.22)
    colors = ("#9ecae1", "#4292c6", "#08519c")
    for offset, level, color in zip(offsets, COVERAGE_LEVELS, colors):
        values = metrics[f"coverage_{int(level * 100)}"].to_numpy()
        axes[0].bar(functions + offset, values, width=0.2, color=color,
                    edgecolor="#263238", linewidth=0.5, label=f"{int(level * 100)}% interval")
        axes[0].axhline(level, color="#263238", lw=0.8, ls="--", alpha=0.45)
    axes[0].set(
        title="Rolling predictive-interval coverage",
        xlabel="Function",
        ylabel="Empirical coverage",
        xticks=functions,
        ylim=(0, 1.08),
    )
    axes[0].legend(
        frameon=False, ncol=3, fontsize=8, loc="upper center",
        bbox_to_anchor=(0.5, -0.16),
    )
    axes[0].grid(axis="y", color="#d9e1e5", linewidth=0.6)

    for function, frame in predictions.groupby("function"):
        axes[1].scatter(
            frame["predictive_std"], frame["absolute_error"],
            s=28, alpha=0.75, label=f"F{function}", edgecolors="none"
        )
    maximum = float(max(predictions["predictive_std"].max(), predictions["absolute_error"].max()))
    axes[1].plot([0, maximum], [0, maximum], color="#263238", ls="--", lw=1,
                 label="absolute error = predicted std")
    axes[1].set_xscale("symlog", linthresh=1e-4)
    axes[1].set_yscale("symlog", linthresh=1e-4)
    axes[1].set(
        title="Uncertainty versus realised absolute error",
        xlabel="Predictive standard deviation (symlog)",
        ylabel="Absolute one-step-ahead error (symlog)",
    )
    axes[1].grid(color="#d9e1e5", linewidth=0.6)
    axes[1].legend(frameon=False, ncol=3, fontsize=8, loc="upper left")
    fig.suptitle("Historical GP validation — 96 rolling one-step-ahead folds", fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("Results"))
    args = parser.parse_args()
    root = repository_root()
    output = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    predictions = rolling_predictions(root)
    metrics = aggregate_metrics(predictions)
    hyperparameters = final_hyperparameters(root)
    predictions.to_csv(output / "gp_rolling_validation_predictions.csv", index=False)
    metrics.to_csv(output / "gp_validation_metrics.csv", index=False)
    hyperparameters.to_csv(output / "gp_final_hyperparameters.csv", index=False)
    plot_diagnostics(
        predictions,
        metrics,
        root / "Figures" / "gp_rolling_validation_diagnostics.png",
    )
    print(
        f"Saved {len(predictions)} rolling folds, {len(metrics)} metric rows, "
        f"and {len(hyperparameters)} final hyperparameter rows"
    )


if __name__ == "__main__":
    main()
