"""Export the examiner-facing Week 01–13 optimisation trajectory.

Only exact returns recorded in ``Code.weekly_evidence`` are treated as new
weekly evidence. Missing returns remain blank; the previously verified best is
carried forward so the trajectory is visible without reconstructing results.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from Code.data_validation import validate_observations
    from Code.weekly_evidence import (
        DIMENSIONS,
        EARLY_OUTPUTS,
        WEEK_6_OUTPUTS,
        WEEK_9_OUTPUTS,
    )
except ModuleNotFoundError:  # Support direct execution from the repository root.
    from data_validation import validate_observations
    from weekly_evidence import (
        DIMENSIONS,
        EARLY_OUTPUTS,
        WEEK_6_OUTPUTS,
        WEEK_9_OUTPUTS,
    )


RETURN_BY_WEEK = {
    1: lambda function: EARLY_OUTPUTS[function][0],
    2: lambda function: EARLY_OUTPUTS[function][1],
    3: lambda function: EARLY_OUTPUTS[function][2],
    4: lambda function: EARLY_OUTPUTS[function][3],
    6: lambda function: WEEK_6_OUTPUTS[function],
    9: lambda function: WEEK_9_OUTPUTS[function],
}

MISSING_EVIDENCE = {
    5: "Week 5 return unavailable in the repository evidence.",
    7: "Week 7 return unavailable in the repository evidence.",
    8: "Week 8 return unavailable in the repository evidence.",
    10: "Week 10 return unavailable in the repository evidence.",
    11: "Week 11 arrays quarantined after provenance and corruption checks.",
    12: "No verified Week 12 return is present.",
    13: "No verified Week 13 return is present.",
}

COLUMNS = [
    "Week",
    "Function",
    "Dimensions",
    "Observation count",
    "Previous best",
    "New observation",
    "New best",
    "Improvement",
    "Fitted GP kernel",
    "Predictive std at selected query",
    "UCB score",
    "Evidence status",
    "Evidence note",
]


def repository_root(start: str | Path | None = None) -> Path:
    """Locate the repository from the current or supplied directory."""
    current = Path.cwd() if start is None else Path(start).expanduser().resolve()
    for candidate in (current, *current.parents):
        if (candidate / "Week_01").is_dir() and (candidate / "Code").is_dir():
            return candidate
    raise FileNotFoundError("Capstone repository root not found")


def build_performance_summary(root: str | Path | None = None) -> pd.DataFrame:
    """Build one audit row per week and function from verified evidence."""
    base = repository_root(root)
    rows: list[dict] = []

    for function in range(1, 9):
        data_folder = base / "Week_01" / f"Function_{function:02d}" / "03_Data"
        inputs = np.load(data_folder / "initial_inputs.npy", allow_pickle=False)
        outputs = np.load(data_folder / "initial_outputs.npy", allow_pickle=False)
        _, verified_outputs = validate_observations(
            inputs, outputs, dimensions=DIMENSIONS[function]
        )
        verified_outputs = verified_outputs.copy()

        for week in range(1, 14):
            previous_best = float(np.max(verified_outputs))
            return_loader = RETURN_BY_WEEK.get(week)

            if return_loader is None:
                new_observation = np.nan
                improvement = np.nan
                evidence_status = "Return unavailable"
                evidence_note = MISSING_EVIDENCE[week]
            else:
                new_observation = float(return_loader(function))
                verified_outputs = np.append(verified_outputs, new_observation)
                improvement = float(np.max(verified_outputs) - previous_best)
                evidence_status = "Confirmed return"
                evidence_note = "Exact query/return pair recorded in Code/weekly_evidence.py."

            rows.append(
                {
                    "Week": week,
                    "Function": f"F{function}",
                    "Dimensions": DIMENSIONS[function],
                    "Observation count": int(verified_outputs.size),
                    "Previous best": previous_best,
                    "New observation": new_observation,
                    "New best": float(np.max(verified_outputs)),
                    "Improvement": improvement,
                    "Fitted GP kernel": "Not recorded",
                    "Predictive std at selected query": np.nan,
                    "UCB score": np.nan,
                    "Evidence status": evidence_status,
                    "Evidence note": evidence_note,
                }
            )

    summary = pd.DataFrame(rows, columns=COLUMNS).sort_values(
        ["Week", "Function"], key=lambda values: values.str.extract(r"(\d+)")[0].astype(int)
        if values.name == "Function" else values
    )
    return summary.reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("Results/performance_summary_weeks_01_to_13.csv"),
    )
    args = parser.parse_args()
    summary = build_performance_summary()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output, index=False)
    print(f"Saved {len(summary)} rows to {args.output}")


if __name__ == "__main__":
    main()
