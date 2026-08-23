"""Regenerate focused Week 03--13 reviews and their documentation."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import matplotlib.pyplot as plt

from Code.build_historical_function_notebook import build
from Code.historical_function_review import analyse_historical_function, write_historical_artifacts


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _wrapper(week: int, function: int, builder: bool = False) -> str:
    action = "build" if builder else "write_historical_artifacts"
    module = "Code.build_historical_function_notebook" if builder else "Code.historical_function_review"
    call = f"{action}({week}, {function}, ROOT)"
    return f'''"""Canonical Week {week:02d} Function {function:02d} entry point."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from {module} import {action}
if __name__ == "__main__":
    print({call})
'''


def refresh_narrative(base: Path, week: int, function: int, summary: dict) -> None:
    target = base / f"Week_{week:02d}" / f"Function_{function:02d}"
    count, dims = summary["total_verified_observations"], summary["dimensions"]
    proposal = summary["proposal"]
    method, query, source = proposal["method"], proposal["query"], proposal["source"]
    boundary = summary["evidence_boundary"]
    portal = "-".join(f"{value:.6f}" for value in query)
    reason = proposal.get("reason", proposal["decision_timing"])
    archive = " Legacy Week 11 arrays remain quarantined." if week >= 11 else ""
    _write(target / "README.md", f"""# Week {week:02d} — Function {function:02d}

Function-specific review aligned to the canonical Week {week} methodology.

- Evidence boundary: **{boundary}**
- Verified observations: **{count}** in **{dims} dimensions**
- Acquisition: **{method}**
- Portal-formatted proposal: `{portal}`

The seven numbered folders contain the executable notebook, reusable code, verified derived data, results, figures, methodology, and reflection. The current-week proposal is never included in observed arrays, summaries, or plots.
""")
    _write(target / "01_Notebook" / "README.md", f"# Notebook\n\n`Week_{week:02d}_Function_{function:02d}.ipynb` mirrors `{source}`, validates {count} observations, records the {method} proposal separately, and checks six-decimal portal formatting.")
    _write(target / "02_Code" / "README.md", f"# Code\n\nThe analysis and notebook-builder entry points delegate to shared canonical modules. They enforce the Week {week - 1} evidence cutoff, proposal bounds, duplicate checks, and deterministic outputs.")
    _write(target / "02_Code" / f"analyse_week_{week:02d}_function_{function:02d}.py", _wrapper(week, function))
    _write(target / "02_Code" / "build_notebook.py", _wrapper(week, function, True))
    _write(target / "03_Data" / "README.md", f"# Data\n\nDerived verified arrays contain starter observations plus returned Weeks 1–{week - 1} pairs: {count} rows by {dims} dimensions. `provenance.json` records canonical sources. The Week {week} proposal is excluded.{archive}")
    _write(target / "04_Results" / "README.md", f"# Results\n\n`observations.csv` contains {count} verified observations through Week {week - 1}. `summary.json` holds within-function statistics and the distinct proposed-only Week {week} record `{portal}`.")
    _write(target / "05_Figures" / "README.md", f"# Figures\n\n`function_{function:02d}_diagnostics.png` is the canonical evidence trace and coordinate heatmap; the week-prefixed compatibility file is identical. Orange points identify returned rounds through Week {week - 1}; the Week {week} proposal is excluded. Additional existing Week 13 diagnostics are retained.")
    _write(target / "06_Documentation" / "README.md", "# Documentation\n\n`methodology.md` defines the evidence boundary, acquisition provenance, interpretation limits, and reproducibility policy.")
    _write(target / "06_Documentation" / "methodology.md", f"""# Methodology

## Evidence boundary

{boundary} The analysis reconstructs {count} observations from immutable starter arrays and the canonical ledger. The Week {week} query is held separately as a proposal. No outcome is imputed.{archive}

## Function-specific acquisition

Function {function:02d} uses **{method}**, as documented in `{source}`. Decision record: {reason}

This policy is adaptive and heuristic. It was selected using evidence available through Week {week - 1}; it is not a randomized or statistically controlled acquisition comparison. For Week 13, the reason was recorded before Week 13 outcomes existed.

## Validation

Inputs are finite and bounded; the proposal is distinct, capped at `0.999999`, and formatted as `{portal}` with six decimals per coordinate. Results are descriptive within Function {function:02d} and imply neither causality nor global optimality.
""")
    _write(target / "07_Reflection" / "README.md", f"# Reflection\n\nAt this checkpoint, **{boundary}** The latest return is interpreted only against prior Function {function:02d} evidence. The {method} proposal is an adaptive choice, not proof of acquisition superiority. Keeping it outside observed arrays prevents look-ahead.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--weeks", type=int, nargs="*", default=list(range(3, 14)))
    args = parser.parse_args()
    base = args.repository.resolve()
    for week in args.weeks:
        for function in range(1, 9):
            write_historical_artifacts(week, function, base)
            _, summary, _, figure = analyse_historical_function(week, function, base)
            plt.close(figure)
            refresh_narrative(base, week, function, summary)
            build(week, function, base)
        print(f"Generated Week {week:02d}", flush=True)


if __name__ == "__main__":
    main()
