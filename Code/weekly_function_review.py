"""Stable, notebook-independent analysis for weekly black-box evidence."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .data_validation import validate_observations
from .weekly_evidence import DIMENSIONS, EVIDENCE_GAPS, pairs_through_week


def repository_root(start: str | Path | None = None) -> Path:
    """Locate the capstone root from any nested function folder."""
    current = Path.cwd() if start is None else Path(start).expanduser().resolve()
    for candidate in (current, *current.parents):
        if (candidate / "Week_01").is_dir() and (candidate / "Code").is_dir():
            return candidate
    raise FileNotFoundError("Capstone repository root not found")


def load_weekly_evidence(
    week: int,
    function: int,
    root: str | Path | None = None,
    *,
    evidence_through_week: int | None = None,
):
    """Load starter arrays and append only exact recoverable query/return pairs."""
    base = repository_root(root)
    data = base / "Week_01" / f"Function_{function:02d}" / "03_Data"
    X = np.asarray(np.load(data / "initial_inputs.npy", allow_pickle=False), dtype=float)
    y = np.asarray(np.load(data / "initial_outputs.npy", allow_pickle=False), dtype=float).reshape(-1)
    X, y = validate_observations(X, y, dimensions=DIMENSIONS[function])
    starter_count = len(y)
    cutoff = week if evidence_through_week is None else evidence_through_week
    for query, output in pairs_through_week(min(cutoff, 12), function):
        X = np.vstack((X, np.asarray(query, dtype=float)))
        y = np.append(y, float(output))
    X, y = validate_observations(X, y, dimensions=DIMENSIONS[function])
    return X, y, starter_count


def analyse_weekly_function(
    week: int,
    function: int,
    root: str | Path | None = None,
    *,
    evidence_through_week: int | None = None,
):
    """Return an observation table and within-function evidence summary."""
    X, y, starter_count = load_weekly_evidence(
        week, function, root, evidence_through_week=evidence_through_week
    )
    frame = pd.DataFrame(X, columns=[f"x{i + 1}" for i in range(X.shape[1])])
    frame.insert(0, "query", np.arange(1, len(y) + 1))
    frame.insert(1, "evidence", ["starter"] * starter_count + ["recorded"] * (len(y) - starter_count))
    frame["objective"] = y
    best = int(np.argmax(y))
    latest = len(y) - 1
    summary = {
        "week": week, "function": function, "dimensions": X.shape[1],
        "starter_observations": starter_count, "recorded_pairs": len(y) - starter_count,
        "total_verified_observations": len(y), "best_query": best + 1,
        "best_input": X[best].tolist(), "best_output": float(y[best]),
        "latest_verified_query": latest + 1, "latest_verified_input": X[latest].tolist(),
        "latest_verified_output": float(y[latest]),
        "latest_improves_previous_best": bool(y[latest] > np.max(y[:latest])) if latest else False,
        "minimum_output": float(np.min(y)), "mean_output": float(np.mean(y)),
        "standard_deviation": float(np.std(y)), "evidence_gap": EVIDENCE_GAPS[week],
        "interpretation": "Within-function descriptive evidence; no causal or cross-function ranking claim.",
    }
    if week >= 11:
        summary["archive_integrity"] = (
            "Original repository Week 11 arrays remain quarantined; analysis "
            "uses independently recovered pairs from the canonical ledger."
        )
    return frame, summary


def plot_weekly_function(frame: pd.DataFrame, summary: dict) -> plt.Figure:
    """Create a consolidated response trace and coordinate heatmap."""
    dims = [c for c in frame if c.startswith("x")]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    recorded = frame["evidence"].eq("recorded")
    axes[0].plot(frame["query"], frame["objective"], marker="o", lw=1.3)
    axes[0].scatter(frame.loc[recorded, "query"], frame.loc[recorded, "objective"], color="darkorange", label="recorded return", zorder=3)
    axes[0].scatter(summary["best_query"], summary["best_output"], color="crimson", marker="*", s=140, label="verified best", zorder=4)
    axes[0].set(title="Objective evidence", xlabel="Verified query", ylabel="Objective"); axes[0].legend()
    image = axes[1].imshow(frame[dims].to_numpy().T, aspect="auto", cmap="viridis", vmin=0, vmax=1)
    axes[1].set(title="Input coordinates", xlabel="Verified query", ylabel="Dimension")
    axes[1].set_yticks(range(len(dims)), dims); fig.colorbar(image, ax=axes[1], label="Coordinate value")
    fig.suptitle(f"Week {summary['week']:02d} Function {summary['function']:02d} — verified evidence")
    fig.tight_layout(rect=(0, 0, 1, .94)); return fig


def write_review_artifacts(week: int, function: int, root: str | Path | None = None):
    """Write deterministic CSV, JSON, PNG, and data-provenance artifacts."""
    base = repository_root(root); target = base / f"Week_{week:02d}" / f"Function_{function:02d}"
    frame, summary = analyse_weekly_function(week, function, base)
    results, figures, data = target / "04_Results", target / "05_Figures", target / "03_Data"
    for folder in (results, figures, data): folder.mkdir(parents=True, exist_ok=True)
    frame.to_csv(results / "observations.csv", index=False)
    (results / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    provenance = {
        "canonical_starter": f"Week_01/Function_{function:02d}/03_Data",
        "recorded_pairs_registry": "Results/query_output_ledger.csv",
        "review_context": f"Week_{week:02d}/02_Notebook",
        "data_policy": "Derived arrays are reconstructed from starter data plus the ledger; source arrays are never rewritten.",
        "evidence_gap": summary["evidence_gap"],
    }
    if week >= 11:
        provenance["excluded_archive"] = f"Week_11/Function_{function:02d}/03_Data/function_{function}_*.npy"
        provenance["exclusion_reason"] = "Duplicate sentinel values, cross-function outputs, altered coordinates, and unprovenanced rows."
    (data / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    np.save(data / "verified_cumulative_inputs.npy", frame[[c for c in frame if c.startswith("x")]].to_numpy())
    np.save(data / "verified_cumulative_outputs.npy", frame["objective"].to_numpy())
    fig = plot_weekly_function(frame, summary)
    fig.savefig(figures / f"week_{week:02d}_function_{function:02d}_diagnostics.png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    return summary
