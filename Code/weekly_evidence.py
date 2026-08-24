"""Verified capstone evidence loaded from the canonical immutable ledger."""

from __future__ import annotations

import csv
import json
from functools import lru_cache
from pathlib import Path


DIMENSIONS = {1: 2, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6, 8: 8}

EVIDENCE_GAPS = {
    week: f"Confirmed cumulative evidence is available through Week {week}."
    for week in range(1, 13)
}
EVIDENCE_GAPS[13] = "Confirmed cumulative evidence is available through Week 13."


def _repository_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in (current.parent, *current.parents):
        if (candidate / "Results" / "query_output_ledger.csv").is_file():
            return candidate
    raise FileNotFoundError("Canonical query/output ledger not found")


@lru_cache(maxsize=1)
def ledger_rows() -> tuple[dict, ...]:
    path = _repository_root() / "Results" / "query_output_ledger.csv"
    with path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    parsed = []
    for row in rows:
        parsed.append({
            **row,
            "week": int(row["week"]),
            "function": int(row["function"]),
            "query": json.loads(row["query"]),
            "returned_output": float(row["returned_output"]),
        })
    return tuple(parsed)


def pairs_through_week(submission_week: int, function: int):
    """Return verified pairs through a submission week, inclusive."""
    if not 0 <= submission_week <= 13 or function not in DIMENSIONS:
        raise ValueError("submission_week must be 0..13 and function must be 1..8")
    return [
        (row["query"], row["returned_output"])
        for row in ledger_rows()
        if row["function"] == function and row["week"] <= submission_week
    ]


def recorded_pairs(review_week: int, function: int):
    """Return evidence available at the start of a weekly review."""
    if review_week not in range(2, 14):
        raise ValueError("review_week must be 2..13")
    return pairs_through_week(min(review_week - 1, 12), function)
