"""Reconcile cumulative weekly exports into auditable query/result records."""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
from pathlib import Path

DIMS = {1: 2, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6, 8: 8}


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _parse_export(path: Path) -> list[list]:
    """Parse lists of numpy reprs without executing source-file contents."""
    class NumpyReprStripper(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call):
            node = self.generic_visit(node)
            is_array = isinstance(node.func, ast.Name) and node.func.id == "array"
            is_float = (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "np"
                and node.func.attr == "float64"
            )
            if (is_array or is_float) and len(node.args) == 1 and not node.keywords:
                return node.args[0]
            raise ValueError(f"Unsupported expression in {path.name}")

    module = ast.parse(path.read_text(encoding="utf-8"), mode="exec")
    module = NumpyReprStripper().visit(module)
    return [ast.literal_eval(node.value) for node in module.body if isinstance(node, ast.Expr)]


def _ledger(base: Path) -> dict[tuple[int, int], tuple[list[float], float]]:
    records = {}
    with (base / "Results" / "query_output_ledger.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            records[(int(row["week"]), int(row["function"]))] = (
                [float(value) for value in ast.literal_eval(row["query"])],
                float(row["returned_output"]),
            )
    return records


def _round_source_week(week: int) -> int:
    # The supplied Week 10 export repeats Week 09; Week 11 contains both new rounds.
    return 11 if week == 10 else week


def reconcile(source: Path, base: Path) -> dict[int, dict]:
    ledger = _ledger(base)
    reconciled = {}
    for week in range(1, 13):
        source_week = _round_source_week(week)
        input_path = source / f"week_{source_week:02d}_inputs.txt"
        output_path = source / f"week_{source_week:02d}_outputs.txt"
        input_blocks = _parse_export(input_path)
        output_blocks = _parse_export(output_path)
        if len(input_blocks) != len(output_blocks) or len(input_blocks) <= week - 1:
            raise ValueError(f"Week {week:02d} source does not contain cumulative block {week}")
        queries, outputs = input_blocks[week - 1], output_blocks[week - 1]
        if len(queries) != 8 or len(outputs) != 8:
            raise ValueError(f"Week {week:02d} must contain eight aligned functions")
        rows = []
        for function, (query, output) in enumerate(zip(queries, outputs), start=1):
            query = [float(value) for value in query]
            output = float(output)
            expected_query, expected_output = ledger[(week, function)]
            if query != expected_query or output != expected_output:
                raise ValueError(f"Week {week:02d} Function {function:02d} conflicts with canonical ledger")
            rows.append((function, query, output))
        reconciled[week] = {
            "rows": rows,
            "input_source": input_path,
            "output_source": output_path,
            "input_sha256": _hash(input_path),
            "output_sha256": _hash(output_path),
        }
    return reconciled


def write_records(source: Path, base: Path) -> None:
    records = reconcile(source, base)
    for week, record in records.items():
        folder = base / f"Week_{week:02d}" / "01_Queries"
        folder.mkdir(parents=True, exist_ok=True)
        lines = [
            f"# Week {week:02d} verified query/output record",
            "# Historical returned evidence; not a future portal submission file.",
        ]
        for function, query, output in record["rows"]:
            # Historical sources include an exact 1.0 in Week 09, so format directly.
            portal = "-".join(f"{value:.6f}" for value in query)
            lines.append(f"Function_{function}:{portal} | output={output!r}")
        (folder / f"week_{week:02d}_query_results.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        source_note = (
            "The supplied Week 10 export duplicates Week 09, so this round is recovered "
            "from cumulative block 10 of the supplied Week 11 files."
            if week == 10
            else f"This round is cumulative block {week} of the supplied Week {record['input_source'].stem[5:7]} files."
        )
        compatibility = (
            "\nThe older `week1_queries.text` file is retained for compatibility; the zero-padded query/result file above is canonical.\n"
            if week == 1
            else "\nThe older `week2_queries.txt` file is retained for compatibility; the zero-padded query/result file above is canonical.\n"
            if week == 2
            else ""
        )
        proposal_note = (
            "\n`week_12_query_points.txt` remains the pre-return proposal artifact. The query/result file records the subsequently verified submitted coordinates and outputs from the supplied export.\n"
            if week == 12
            else ""
        )
        readme = f"""# Week {week:02d} queries

[`week_{week:02d}_query_results.txt`](week_{week:02d}_query_results.txt) records the eight aligned queries and returned outputs recovered from the supplied cumulative exports. {source_note}
{compatibility}{proposal_note}

Evidence provenance:

- input SHA-256: `{record['input_sha256']}`
- output SHA-256: `{record['output_sha256']}`
- reconciliation registry: `Results/query_output_ledger.csv`

Coordinates are rendered with six decimals for readability; returned outputs retain their verified numeric precision. This is a historical evidence record, not a claim that the acquisition policy was statistically controlled.
"""
        (folder / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    args = parser.parse_args()
    write_records(args.source.resolve(), args.repository.resolve())


if __name__ == "__main__":
    main()
