"""Export the examiner-facing Week 01–13 optimisation trajectory.

Only exact returns in the canonical ledger are treated as weekly evidence.
Missing returns remain blank and the previously verified best is carried
forward.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from Code.data_validation import validate_observations
    from Code.weekly_evidence import DIMENSIONS, ledger_rows
except ModuleNotFoundError:  # Support direct execution from the repository root.
    from data_validation import validate_observations
    from weekly_evidence import DIMENSIONS, ledger_rows


MISSING_EVIDENCE = {13: "Week 13 return is unavailable."}

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
    returns = {
        (row["week"], row["function"]): row for row in ledger_rows()
    }
    proposal_path = base / "Results" / "bbo_query_ledger.csv"
    proposals = {}
    if proposal_path.is_file():
        proposal_frame = pd.read_csv(proposal_path)
        proposals = {
            (int(row.week), int(row.function)): row
            for row in proposal_frame.itertuples(index=False)
        }
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
            return_row = returns.get((week, function))
            proposal_row = proposals.get((week, function))

            if return_row is None:
                new_observation = np.nan
                improvement = np.nan
                evidence_status = "Return unavailable"
                evidence_note = MISSING_EVIDENCE[week]
            else:
                new_observation = float(return_row["returned_output"])
                verified_outputs = np.append(verified_outputs, new_observation)
                improvement = float(np.max(verified_outputs) - previous_best)
                evidence_status = "Confirmed return"
                evidence_note = "Exact query/return pair recorded in Results/query_output_ledger.csv."

            fitted_kernel = "Not recorded"
            predictive_std = np.nan
            ucb_score = np.nan
            if proposal_row is not None:
                fitted_kernel = proposal_row.kernel
                predictive_std = float(proposal_row.predictive_std)
                ucb_score = float(proposal_row.ucb_score)
                evidence_note += " A validated proposal is recorded in Results/bbo_query_ledger.csv."

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
                    "Fitted GP kernel": fitted_kernel,
                    "Predictive std at selected query": predictive_std,
                    "UCB score": ucb_score,
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
