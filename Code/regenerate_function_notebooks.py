"""Refresh and execute every focused weekly function notebook."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def regenerate(root: Path) -> None:
    notebooks = sorted(root.glob("Week_*/Function_*/01_Notebook/*.ipynb"))
    if len(notebooks) != 97:
        raise ValueError(f"Expected 97 function notebooks, found {len(notebooks)}")
    for index, path in enumerate(notebooks, 1):
        match = re.search(r"Week_(\d+)/Function_(\d+)", path.as_posix())
        if not match:
            raise ValueError(f"Cannot identify week/function for {path}")
        week, function = map(int, match.groups())
        notebook = nbformat.read(path, as_version=4)
        if week <= 11:
            note = f"Confirmed cumulative evidence is available through Week {week}."
        elif week == 12:
            note = "No verified Week 12 return is present; confirmed evidence is carried forward through Week 11."
        else:
            note = "No verified Week 12 or Week 13 return is present; confirmed evidence is carried forward through Week 11."
        notebook.cells[0].source = (
            f"# Week {week:02d} — Function {function:02d}\n\n"
            f"Focused review reconstructed from starter data plus the immutable ledger. {note}"
        )
        client = NotebookClient(
            notebook,
            timeout=180,
            kernel_name="python3",
            resources={"metadata": {"path": str(root)}},
        )
        client.execute()
        nbformat.write(notebook, path)
        print(f"[{index:02d}/{len(notebooks)}] executed {path.relative_to(root)}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    args = parser.parse_args()
    regenerate(args.repository.resolve())


if __name__ == "__main__":
    main()
