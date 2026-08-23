"""Reproduce the Week 1 Function 1 summary and diagnostic figure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from Code.data_loading import find_repository_root, load_starter_data
from Code.eda import observation_summary, observations_frame
from Code.plotting import plot_function_diagnostics


def analyse_function_01(repository_root: str | Path | None = None):
    """Return validated Function 1 observations, summary, and Matplotlib figure."""
    root = find_repository_root(repository_root)
    inputs, outputs = load_starter_data(1, repository_root=root)
    summary = observation_summary(inputs, outputs)
    summary.update({"function": "F1", "week": 1, "strategy": "Random Search"})
    figure = plot_function_diagnostics(
        inputs,
        outputs,
        title="Week 1 Function 1 — Random Search",
    )
    figure.set_layout_engine("constrained")
    return observations_frame(inputs, outputs), summary, figure


def write_artifacts(
    repository_root: str | Path | None = None, *, write_figure: bool = False
) -> dict[str, Path]:
    """Write the Week 1 baseline tables and optionally refresh the figure."""
    root = find_repository_root(repository_root)
    function_root = root / "Week_01" / "Function_01"
    results, summary, figure = analyse_function_01(root)
    results_dir, figures_dir = function_root / "04_Results", function_root / "05_Figures"
    results_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    observations_path = results_dir / "observations.csv"
    summary_path = results_dir / "summary.json"
    results.to_csv(observations_path, index=False)
    serializable = {
        key: value.tolist() if hasattr(value, "tolist") else value
        for key, value in summary.items()
    }
    summary_path.write_text(json.dumps(serializable, indent=2) + "\n", encoding="utf-8")
    written = {"observations": observations_path, "summary": summary_path}
    if write_figure:
        figure_path = figures_dir / "function_01_diagnostics.png"
        compatibility_path = figures_dir / "week_01_function_01_diagnostics.png"
        figure.savefig(figure_path, dpi=160, bbox_inches="tight")
        figure.savefig(compatibility_path, dpi=160, bbox_inches="tight")
        written["figure"] = figure_path
        written["compatibility_figure"] = compatibility_path
    plt.close(figure)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-artifacts", action="store_true", help="write CSV and JSON outputs")
    parser.add_argument("--write-figure", action="store_true", help="also refresh the optional diagnostic PNG")
    args = parser.parse_args()
    frame, summary, figure = analyse_function_01()
    if args.write_artifacts:
        for name, path in write_artifacts(write_figure=args.write_figure).items():
            print(f"{name}: {path}")
    else:
        print(pd.Series(summary).to_string())
        print(frame.to_string(index=False))
        plt.close(figure)


if __name__ == "__main__":
    main()
