"""Regenerate all deterministic week/function artifacts from the ledger."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from Code.weekly_function_review import write_review_artifacts
from Code.weekly_evidence import EVIDENCE_GAPS


def refresh_narrative(path: Path, prefix: str, replacement: str) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    updated = re.sub(
        rf"(?m)^{re.escape(prefix)}.*$",
        replacement,
        text,
    )
    path.write_text(updated, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--weeks", type=int, nargs="*")
    args = parser.parse_args()
    weeks = args.weeks or list(range(1, 14))
    for week in weeks:
        for function in range(1, 9):
            write_review_artifacts(week, function, args.repository.resolve())
            target = args.repository.resolve() / f"Week_{week:02d}" / f"Function_{function:02d}"
            gap = EVIDENCE_GAPS[week]
            quarantine = (
                " The original Week 11 arrays remain quarantined and are not used."
                if week >= 11 else ""
            )
            refresh_narrative(
                target / "06_Documentation" / "methodology.md",
                "At this review point,",
                f"At this review point, {gap}{quarantine} No value is imputed. Results are descriptive within Function {function:02d}; they do not imply causality, global optimality, or cross-function ranking.",
            )
            refresh_narrative(
                target / "07_Reflection" / "README.md",
                "At this checkpoint,",
                f"At this checkpoint, {gap}{quarantine} The trajectory is interpreted only from verified evidence.",
            )
        print(f"Generated Week {week:02d}", flush=True)


if __name__ == "__main__":
    main()
