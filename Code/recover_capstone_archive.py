"""Recover verified weekly query/output pairs from cumulative local snapshots.

The source archive is read-only. Existing repository arrays are never used as
recovery evidence and are never overwritten by this script.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import math
import re
import shutil
from datetime import datetime
from pathlib import Path

import numpy as np


DIMENSIONS = {1: 2, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6, 8: 8}
FIELDNAMES = [
    "week", "function", "query", "returned_output", "dataset_version",
    "submission_date", "date_basis", "notebook", "commit_sha",
    "evidence_status", "source_registry", "source_input", "source_output",
    "source_input_sha256", "source_output_sha256", "duplicate_of",
]
DATASET_VERSION = "verified-query-output-ledger-v1.1"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _snapshot_number(path: Path) -> int | None:
    match = re.fullmatch(r"week_(\d+)_inputs\.txt", path.name.lower())
    return int(match.group(1)) if match else None


def _parse_inputs(path: Path) -> list[list[list[float]]]:
    arrays = re.findall(r"array\((\[[^\]]+\])\)", path.read_text(), flags=re.S)
    values = [
        [
            float(number)
            for number in re.findall(
                r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?", raw
            )
        ]
        for raw in arrays
    ]
    if len(values) % 8:
        raise ValueError(f"{path}: input count is not divisible by eight")
    return [values[index:index + 8] for index in range(0, len(values), 8)]


def _parse_outputs(path: Path) -> list[list[float]]:
    rows = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        cleaned = re.sub(r"np\.float64\(([^()]*)\)", r"\1", line.strip())
        rows.append([float(value) for value in ast.literal_eval(cleaned)])
    if any(len(row) != 8 for row in rows):
        raise ValueError(f"{path}: every output row must contain eight values")
    return rows


def _candidate_snapshots(archive: Path) -> list[dict]:
    candidates = []
    for directory in archive.iterdir():
        if not directory.is_dir():
            continue
        for input_path in directory.iterdir():
            if not input_path.is_file():
                continue
            snapshot = _snapshot_number(input_path)
            if snapshot is None:
                continue
            possible_names = {
                f"week_{snapshot}_outputs.txt", f"week_{snapshot:02d}_outputs.txt"
            }
            output_paths = [
                path for path in directory.iterdir()
                if path.is_file() and path.name.lower() in possible_names
            ]
            if len(output_paths) != 1:
                continue
            output_path = output_paths[0]
            try:
                inputs = _parse_inputs(input_path)
                outputs = _parse_outputs(output_path)
            except (SyntaxError, TypeError, ValueError):
                continue
            if len(inputs) != snapshot or len(outputs) != snapshot:
                continue
            candidates.append({
                "snapshot": snapshot,
                "input_path": input_path,
                "output_path": output_path,
                "inputs": inputs,
                "outputs": outputs,
                "input_sha256": _sha256(input_path),
                "output_sha256": _sha256(output_path),
            })
    return candidates


def recover_rows(archive: Path, repository: Path) -> tuple[list[dict], list[dict]]:
    """Recover Weeks 1–11 and return ledger rows plus source-manifest rows."""
    candidates = _candidate_snapshots(archive)
    ledger_rows: list[dict] = []
    manifest_rows: list[dict] = []
    seen_queries: dict[int, list[tuple[str, np.ndarray]]] = {}

    for function in range(1, 9):
        starter = np.load(
            repository / "Week_01" / f"Function_{function:02d}" /
            "03_Data" / "initial_inputs.npy", allow_pickle=False
        )
        seen_queries[function] = [
            (f"starter:{index + 1}", np.asarray(query, dtype=float))
            for index, query in enumerate(starter)
        ]

    for week in range(1, 12):
        eligible = [item for item in candidates if item["snapshot"] >= week]
        if not eligible:
            raise ValueError(f"No complete snapshot contains Week {week}")
        smallest_snapshot = min(item["snapshot"] for item in eligible)
        copies = [item for item in eligible if item["snapshot"] == smallest_snapshot]
        signatures = {
            (item["input_sha256"], item["output_sha256"]) for item in copies
        }
        if len(signatures) != 1:
            raise ValueError(f"Conflicting copies found for snapshot {smallest_snapshot}")
        source = min(copies, key=lambda item: str(item["input_path"]))
        queries = source["inputs"][week - 1]
        outputs = source["outputs"][week - 1]
        if len(queries) != 8 or len(outputs) != 8:
            raise ValueError(f"Week {week}: expected eight aligned pairs")

        input_date = datetime.fromtimestamp(source["input_path"].stat().st_mtime).astimezone()
        output_date = datetime.fromtimestamp(source["output_path"].stat().st_mtime).astimezone()
        archive_date = input_date.date().isoformat() if input_date.date() == output_date.date() else ""
        source_input = source["input_path"].relative_to(archive.parent).as_posix()
        source_output = source["output_path"].relative_to(archive.parent).as_posix()

        manifest_rows.append({
            "week": week,
            "source_snapshot": smallest_snapshot,
            "identical_archive_copy_count": len(copies),
            "source_input": source_input,
            "source_output": source_output,
            "source_input_sha256": source["input_sha256"],
            "source_output_sha256": source["output_sha256"],
            "archive_date": archive_date,
            "validation": "complete_aligned_snapshot",
        })

        for function, (query, output) in enumerate(zip(queries, outputs), 1):
            query_array = np.asarray(query, dtype=float)
            if query_array.shape != (DIMENSIONS[function],):
                raise ValueError(f"Week {week} F{function}: invalid dimensions")
            if not np.isfinite(query_array).all() or not np.all((query_array >= 0) & (query_array <= 1)):
                raise ValueError(f"Week {week} F{function}: invalid query values")
            if not math.isfinite(float(output)):
                raise ValueError(f"Week {week} F{function}: non-finite output")

            duplicate_of = ""
            for label, prior in seen_queries[function]:
                if np.allclose(query_array, prior, rtol=0.0, atol=5e-7):
                    duplicate_of = label
                    break
            seen_queries[function].append((f"week:{week}", query_array))

            ledger_rows.append({
                "week": str(week),
                "function": str(function),
                "query": json.dumps(query, separators=(",", ":")),
                "returned_output": repr(float(output)),
                "dataset_version": DATASET_VERSION,
                "submission_date": archive_date,
                "date_basis": "source_file_mtime; not platform submission timestamp",
                "notebook": f"Week_{week:02d}/02_Notebook/" + (
                    f"Week_{week}_Capstone.ipynb" if week <= 11 else ""
                ),
                "commit_sha": "",
                "evidence_status": "verified_cumulative_archive_pair",
                "source_registry": "Results/query_output_ledger.csv",
                "source_input": source_input,
                "source_output": source_output,
                "source_input_sha256": source["input_sha256"],
                "source_output_sha256": source["output_sha256"],
                "duplicate_of": duplicate_of,
            })

    if len(ledger_rows) != 88 or len({(row["week"], row["function"]) for row in ledger_rows}) != 88:
        raise ValueError("Expected 88 unique Week 1–11 function pairs")
    return ledger_rows, manifest_rows


def write_recovery(archive: Path, repository: Path) -> None:
    rows, manifest = recover_rows(archive, repository)
    results = repository / "Results"
    results.mkdir(exist_ok=True)
    output = results / "query_output_ledger.csv"
    checksum = results / "query_output_ledger.sha256"
    versions = results / "query_output_ledger_versions.json"
    archive_folder = results / "archive"
    old_digest = None
    if output.exists():
        with output.open(newline="", encoding="utf-8") as source:
            existing = list(csv.DictReader(source))
        versions_seen = {row.get("dataset_version", "") for row in existing}
        if versions_seen == {"verified-query-output-ledger-v1.0"}:
            archive_folder.mkdir(exist_ok=True)
            archived = archive_folder / "query_output_ledger_v1.0.csv"
            if archived.exists() and archived.read_bytes() != output.read_bytes():
                raise ValueError("Existing v1.0 archive differs from the published ledger")
            if not archived.exists():
                shutil.copyfile(output, archived)
            old_digest = _sha256(archived)
            (archive_folder / "query_output_ledger_v1.0.sha256").write_text(
                f"{old_digest}  {archived.name}\n", encoding="utf-8"
            )
        elif versions_seen != {DATASET_VERSION}:
            raise ValueError(f"Refusing to replace unexpected ledger versions: {versions_seen}")
    archived = archive_folder / "query_output_ledger_v1.0.csv"
    if archived.exists():
        old_digest = _sha256(archived)
    with output.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    digest = _sha256(output)
    checksum.write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    manifest_path = results / "query_output_source_manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(manifest[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(manifest)
    version_entries = []
    if old_digest:
        version_entries.append({
            "dataset_version": "verified-query-output-ledger-v1.0",
            "status": "superseded_preserved_immutable",
            "path": "Results/archive/query_output_ledger_v1.0.csv",
            "sha256": old_digest,
            "reason": "Superseded after reconciliation against the original cumulative Downloads archive.",
        })
    version_entries.append({
        "dataset_version": DATASET_VERSION,
        "status": "canonical",
        "path": "Results/query_output_ledger.csv",
        "sha256": digest,
        "reason": "Recovered from aligned cumulative source snapshots and validated programmatically.",
    })
    versions.write_text(json.dumps(version_entries, indent=2) + "\n", encoding="utf-8")
    quarantine_rows = []
    for function in range(1, 9):
        data = repository / "Week_11" / f"Function_{function:02d}" / "03_Data"
        for kind in ("inputs", "outputs"):
            path = data / f"function_{function}_{kind}.npy"
            if path.exists():
                values = np.load(path, allow_pickle=False)
                quarantine_rows.append({
                    "function": function,
                    "kind": kind,
                    "path": path.relative_to(repository).as_posix(),
                    "sha256": _sha256(path),
                    "shape": json.dumps(list(values.shape), separators=(",", ":")),
                    "status": "quarantined_read_only_historical_evidence",
                    "reason": "Failed prior provenance reconciliation; excluded from reconstructed evidence.",
                })
    if quarantine_rows:
        quarantine = results / "quarantined_week11_arrays.csv"
        with quarantine.open("w", newline="", encoding="utf-8") as target:
            writer = csv.DictWriter(target, fieldnames=list(quarantine_rows[0]), lineterminator="\n")
            writer.writeheader(); writer.writerows(quarantine_rows)
    target_weeks = {5, 7, 8, 10, 11}
    target_rows = [row for row in rows if int(row["week"]) in target_weeks]
    duplicate_rows = [
        {"week": int(row["week"]), "function": int(row["function"]), "duplicate_of": row["duplicate_of"]}
        for row in rows if row["duplicate_of"]
    ]
    report = {
        "dataset_version": DATASET_VERSION,
        "requested_weeks": sorted(target_weeks),
        "requested_pair_count": len(target_rows),
        "exactly_one_pair_per_function_per_requested_week": (
            len(target_rows) == 40
            and len({(row["week"], row["function"]) for row in target_rows}) == 40
        ),
        "checks": {
            "expected_dimensions": "passed",
            "finite_queries_and_outputs": "passed",
            "unit_hypercube_bounds": "passed",
            "query_output_row_alignment": "passed",
            "duplicate_detection": "passed_with_flagged_repeated_evaluation",
        },
        "flagged_duplicates": duplicate_rows,
        "date_validation": {
            "status": "source_metadata_only",
            "basis": "input/output source-file modification date agreement",
            "limitation": "No authoritative platform submission timestamps were present in the archive.",
        },
        "quarantined_array_count": len(quarantine_rows),
        "canonical_ledger_sha256": digest,
    }
    (results / "recovery_validation_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Recovered {len(rows)} verified pairs to {output}")
    print(f"SHA-256: {digest}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    args = parser.parse_args()
    write_recovery(args.archive.expanduser().resolve(), args.repository.resolve())


if __name__ == "__main__":
    main()
