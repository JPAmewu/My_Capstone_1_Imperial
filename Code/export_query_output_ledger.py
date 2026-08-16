"""Create the append-only ledger of verified capstone query/output pairs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

try:
    from Code.weekly_evidence import (
        EARLY_OUTPUTS,
        EARLY_QUERIES,
        WEEK_6_OUTPUTS,
        WEEK_6_QUERIES,
        WEEK_9_OUTPUTS,
        WEEK_9_QUERIES,
    )
except ModuleNotFoundError:  # Support direct execution from the repository root.
    from weekly_evidence import (
        EARLY_OUTPUTS,
        EARLY_QUERIES,
        WEEK_6_OUTPUTS,
        WEEK_6_QUERIES,
        WEEK_9_OUTPUTS,
        WEEK_9_QUERIES,
    )


DATASET_VERSION = "verified-query-output-ledger-v1.0"
EVIDENCE_COMMIT = "18b008567a3d283d854f36e260c77e06e3721aa9"
SOURCE_REGISTRY = "Code/weekly_evidence.py"

NOTEBOOK_BY_WEEK = {
    1: "Week_02/02_Notebook/Week_2_Capstone.ipynb",
    2: "Week_03/02_Notebook/Week_3_Capstone.ipynb",
    3: "Week_05/02_Notebook/Week_5_Capstone.ipynb",
    4: "Week_05/02_Notebook/Week_5_Capstone.ipynb",
    6: "Week_09/02_Notebook/Week_9_Capstone.ipynb",
    9: "Week_10/02_Notebook/Week_10_Capstone.ipynb",
}

FIELDNAMES = [
    "week",
    "function",
    "query",
    "returned_output",
    "dataset_version",
    "submission_date",
    "notebook",
    "commit_sha",
    "evidence_status",
    "source_registry",
]


def _row(week: int, function: int, query: list[float], output: float) -> dict[str, str]:
    return {
        "week": str(week),
        "function": str(function),
        "query": json.dumps(query, separators=(",", ":")),
        "returned_output": repr(float(output)),
        "dataset_version": DATASET_VERSION,
        "submission_date": "",
        "notebook": NOTEBOOK_BY_WEEK[week],
        "commit_sha": EVIDENCE_COMMIT,
        "evidence_status": "verified_exact_pair",
        "source_registry": SOURCE_REGISTRY,
    }


def build_ledger() -> list[dict[str, str]]:
    """Return all exact query/output pairs in chronological order."""
    rows: list[dict[str, str]] = []
    for week in range(1, 5):
        for function in range(1, 9):
            rows.append(
                _row(
                    week,
                    function,
                    EARLY_QUERIES[function][week - 1],
                    EARLY_OUTPUTS[function][week - 1],
                )
            )
    for week, queries, outputs in (
        (6, WEEK_6_QUERIES, WEEK_6_OUTPUTS),
        (9, WEEK_9_QUERIES, WEEK_9_OUTPUTS),
    ):
        for function in range(1, 9):
            rows.append(_row(week, function, queries[function], outputs[function]))
    return rows


def _validate_append_only(output: Path, rows: list[dict[str, str]]) -> None:
    """Reject any attempt to modify or remove a previously published row."""
    if not output.exists():
        return
    with output.open(newline="", encoding="utf-8") as source:
        existing = list(csv.DictReader(source))
    new_by_key = {(row["week"], row["function"]): row for row in rows}
    for old_row in existing:
        key = (old_row["week"], old_row["function"])
        if key not in new_by_key:
            raise ValueError(f"Published ledger row {key} would be removed.")
        if old_row != new_by_key[key]:
            raise ValueError(f"Published ledger row {key} would be modified.")


def write_ledger(output: Path, checksum: Path) -> None:
    rows = build_ledger()
    if len(rows) != 48 or len({(row["week"], row["function"]) for row in rows}) != 48:
        raise ValueError("Ledger must contain 48 unique verified week/function pairs.")
    _validate_append_only(output, rows)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    checksum.write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    print(f"Saved {len(rows)} immutable rows to {output}")
    print(f"SHA-256: {digest}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("Results/query_output_ledger.csv"),
    )
    parser.add_argument(
        "--checksum",
        type=Path,
        default=Path("Results/query_output_ledger.sha256"),
    )
    args = parser.parse_args()
    write_ledger(args.output, args.checksum)


if __name__ == "__main__":
    main()
