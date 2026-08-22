"""Assemble the 13 consolidated weekly notebooks from executed function reviews."""

from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path

import nbformat
from nbclient import NotebookClient

try:
    from Code.regenerate_function_notebooks import STEPS, table_of_contents
except ModuleNotFoundError:  # Direct execution from the repository root.
    from regenerate_function_notebooks import STEPS, table_of_contents


def consolidated_path(root: Path, week: int) -> Path:
    if week == 13:
        name = "Week_13_Optimisation_Strategy.ipynb"
    else:
        name = f"Week_{week}_Capstone.ipynb"
    return root / f"Week_{week:02d}" / "02_Notebook" / name


def build(root: Path, week: int) -> nbformat.NotebookNode:
    """Combine all eight executed function notebooks for one week."""
    notebook = nbformat.v4.new_notebook()
    notebook.metadata.kernelspec = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    notebook.metadata.language_info = {"name": "python", "version": "3"}
    cutoff = min(week - 1, 12)
    evidence = (
        "starter observations only"
        if cutoff == 0
        else f"starter observations plus immutable-ledger returns through Week {cutoff:02d}"
    )
    notebook.cells = [
        nbformat.v4.new_markdown_cell(
            f"# Week {week:02d} consolidated Bayesian optimisation notebook\n\n"
            "This notebook presents Functions 1–8 in one systematic analytical record. "
            "Every function follows the same eleven-stage sequence below. UCB results are "
            "unevaluated proposals and are never appended as returned observations.\n\n"
            f"**Evidence used:** {evidence}."
        ),
        table_of_contents(),
    ]
    for function in range(1, 9):
        source = root / f"Week_{week:02d}/Function_{function:02d}/01_Notebook/Week_{week:02d}_Function_{function:02d}.ipynb"
        focused = nbformat.read(source, as_version=4)
        section_cells = deepcopy(focused.cells[2:])
        if not section_cells or section_cells[0].cell_type != "code":
            raise ValueError(f"Unexpected focused notebook structure: {source}")
        notebook.cells.append(
            nbformat.v4.new_markdown_cell(
                f"# Function {function}\n\n"
                f"Function {function} uses the verified evidence available before Week {week:02d}."
            )
        )
        notebook.cells.extend(section_cells)
    return notebook


def regenerate(root: Path, weeks: list[int] | None = None, execute: bool = True) -> None:
    selected = sorted(set(weeks or range(1, 14)))
    if any(week not in range(1, 14) for week in selected):
        raise ValueError("Weeks must be in 1..13")
    for index, week in enumerate(selected, 1):
        output = consolidated_path(root, week)
        output.parent.mkdir(parents=True, exist_ok=True)
        notebook = build(root, week)
        if execute:
            NotebookClient(
                notebook,
                timeout=1200,
                kernel_name="python3",
                resources={"metadata": {"path": str(root)}},
            ).execute()
        nbformat.write(notebook, output)
        action = "assembled and executed" if execute else "assembled"
        print(f"[{index:02d}/{len(selected)}] {action} {output.relative_to(root)}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--weeks", type=int, nargs="*")
    parser.add_argument("--no-execute", action="store_true")
    args = parser.parse_args()
    regenerate(args.repository.resolve(), args.weeks, execute=not args.no_execute)


if __name__ == "__main__":
    main()
