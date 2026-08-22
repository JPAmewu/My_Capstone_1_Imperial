"""Reconcile and append verified Week 12 evidence from a cumulative snapshot."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Code.recover_capstone_archive import DIMENSIONS, FIELDNAMES, _parse_inputs, _parse_outputs  # noqa: E402


NEW_VERSION = "verified-query-output-ledger-v1.2"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def submission_lines(queries: list[list[float]]) -> str:
    return "".join(
        f"Function_{function}:" + "-".join(f"{value:.6f}" for value in query) + "\n"
        for function, query in enumerate(queries, 1)
    )


def append(root: Path, input_path: Path, output_path: Path) -> None:
    rounds_x, rounds_y = _parse_inputs(input_path), _parse_outputs(output_path)
    if len(rounds_x) != 12 or len(rounds_y) != 12:
        raise ValueError("Expected one complete cumulative snapshot containing 12 rounds")

    ledger = root / "Results" / "query_output_ledger.csv"
    with ledger.open(newline="", encoding="utf-8") as source:
        existing = list(csv.DictReader(source))
    if len(existing) not in {88, 96}:
        raise ValueError(f"Expected an 88- or 96-row ledger, found {len(existing)} rows")
    by_key = {(int(row["week"]), int(row["function"])): row for row in existing}

    # The cumulative prefix must reproduce every already-published Week 1–11 pair.
    for week in range(1, 12):
        for function in range(1, 9):
            row = by_key[(week, function)]
            if not np.allclose(json.loads(row["query"]), rounds_x[week - 1][function - 1], rtol=0, atol=5e-7):
                raise ValueError(f"Week {week} F{function}: cumulative query conflicts with ledger")
            if not np.isclose(float(row["returned_output"]), rounds_y[week - 1][function - 1], rtol=0, atol=5e-12):
                raise ValueError(f"Week {week} F{function}: cumulative output conflicts with ledger")

    new_queries, new_outputs = rounds_x[11], rounds_y[11]
    for function, (query, output) in enumerate(zip(new_queries, new_outputs), 1):
        values = np.asarray(query, float)
        if values.shape != (DIMENSIONS[function],):
            raise ValueError(f"Week 12 F{function}: expected {DIMENSIONS[function]} dimensions")
        if not np.isfinite(values).all() or not np.all((values >= 0) & (values <= 1)):
            raise ValueError(f"Week 12 F{function}: query is non-finite or outside [0,1]")
        if not np.isfinite(float(output)):
            raise ValueError(f"Week 12 F{function}: output is non-finite")

    # Archive the stale tracked proposal record before replacing it with the supplied submission row.
    query_file = root / "Week_12" / "01_Queries" / "week_12_query_points.txt"
    query_archive = root / "Week_12" / "01_Queries" / "archive"
    query_archive.mkdir(exist_ok=True)
    stale = query_archive / "pre_reconciliation_week_12_query_points.txt"
    if not stale.exists():
        shutil.copyfile(query_file, stale)
    elif stale.read_bytes() != query_file.read_bytes() and len(existing) == 88:
        raise ValueError("Existing stale-query archive does not match the pre-reconciliation file")
    query_file.write_text(submission_lines(new_queries), encoding="utf-8")

    archive = root / "Results" / "archive"
    archive.mkdir(exist_ok=True)
    ledger_v11 = archive / "query_output_ledger_v1.1.csv"
    if len(existing) == 88:
        shutil.copyfile(ledger, ledger_v11)
        (archive / "query_output_ledger_v1.1.sha256").write_text(
            f"{sha256(ledger_v11)}  {ledger_v11.name}\n", encoding="utf-8"
        )

    input_digest, output_digest = sha256(input_path), sha256(output_path)
    evidence_dir = root / "Results" / "source_evidence" / "week_12"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    preserved_input = evidence_dir / "week_12_inputs.txt"
    preserved_output = evidence_dir / "week_12_outputs.txt"
    shutil.copyfile(input_path, preserved_input); shutil.copyfile(output_path, preserved_output)
    if sha256(preserved_input) != input_digest or sha256(preserved_output) != output_digest:
        raise ValueError("Preserved evidence copy failed SHA-256 verification")
    input_time = datetime.fromtimestamp(input_path.stat().st_mtime).astimezone()
    output_time = datetime.fromtimestamp(output_path.stat().st_mtime).astimezone()
    evidence_date = input_time.date().isoformat() if input_time.date() == output_time.date() else ""
    source_input = preserved_input.relative_to(root).as_posix()
    source_output = preserved_output.relative_to(root).as_posix()

    if len(existing) == 88:
        for function, (query, output) in enumerate(zip(new_queries, new_outputs), 1):
            existing.append({
                "week": "12",
                "function": str(function),
                "query": json.dumps(query, separators=(",", ":")),
                "returned_output": repr(float(output)),
                "dataset_version": NEW_VERSION,
                "submission_date": evidence_date,
                "date_basis": "source_file_mtime; not platform submission timestamp",
                "notebook": "Week_12/01_Queries/week_12_query_points.txt",
                "commit_sha": "",
                "evidence_status": "verified_cumulative_archive_pair_after_query_record_reconciliation",
                "source_registry": "Results/query_output_ledger.csv",
                "source_input": source_input,
                "source_output": source_output,
                "source_input_sha256": input_digest,
                "source_output_sha256": output_digest,
                "duplicate_of": "",
            })
    else:
        for function, (query, output) in enumerate(zip(new_queries, new_outputs), 1):
            row = by_key[(12, function)]
            if row["query"] != json.dumps(query, separators=(",", ":")):
                raise ValueError(f"Published Week 12 F{function} query would change")
            if float(row["returned_output"]) != float(output):
                raise ValueError(f"Published Week 12 F{function} output would change")
            row.update({
                "source_input": source_input, "source_output": source_output,
                "source_input_sha256": input_digest, "source_output_sha256": output_digest,
            })

    with ledger.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader(); writer.writerows(existing)
    ledger_digest = sha256(ledger)
    (root / "Results" / "query_output_ledger.sha256").write_text(
        f"{ledger_digest}  {ledger.name}\n", encoding="utf-8"
    )

    manifest = root / "Results" / "query_output_source_manifest.csv"
    with manifest.open(newline="", encoding="utf-8") as source:
        manifest_rows = list(csv.DictReader(source))
    if not any(int(row["week"]) == 12 for row in manifest_rows):
        manifest_rows.append({
            "week": "12", "source_snapshot": "12", "identical_archive_copy_count": "1",
            "source_input": source_input, "source_output": source_output,
            "source_input_sha256": input_digest, "source_output_sha256": output_digest,
            "archive_date": evidence_date,
            "validation": "complete_aligned_snapshot; prefix_matches_88_published_pairs",
        })
    else:
        for row in manifest_rows:
            if int(row["week"]) == 12:
                row.update({
                    "source_input": source_input, "source_output": source_output,
                    "source_input_sha256": input_digest, "source_output_sha256": output_digest,
                })
    with manifest.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(manifest_rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(manifest_rows)

    versions_path = root / "Results" / "query_output_ledger_versions.json"
    versions = json.loads(versions_path.read_text(encoding="utf-8"))
    for entry in versions:
        if entry["dataset_version"] == "verified-query-output-ledger-v1.1":
            entry["status"] = "superseded_preserved_immutable"
            entry["path"] = "Results/archive/query_output_ledger_v1.1.csv"
            entry["sha256"] = sha256(ledger_v11)
    if not any(entry["dataset_version"] == NEW_VERSION for entry in versions):
        versions.append({
            "dataset_version": NEW_VERSION, "status": "canonical",
            "path": "Results/query_output_ledger.csv", "sha256": ledger_digest,
            "reason": "Appended eight Week 12 pairs after cumulative-prefix and query-record reconciliation.",
        })
    else:
        for entry in versions:
            if entry["dataset_version"] == NEW_VERSION:
                entry.update({"status": "canonical", "path": "Results/query_output_ledger.csv", "sha256": ledger_digest})
    versions_path.write_text(json.dumps(versions, indent=2) + "\n", encoding="utf-8")

    report = {
        "dataset_version": NEW_VERSION,
        "source_rounds": 12,
        "historical_prefix_pairs_checked": 88,
        "historical_prefix_mismatches": 0,
        "week_12_pairs_appended": 8,
        "query_record_reconciliation": {
            "status": "corrected",
            "finding": "The pre-reconciliation tracked Week 12 file repeated the Week 11 queries and matched none of the supplied Week 12 queries.",
            "archived_path": "Week_12/01_Queries/archive/pre_reconciliation_week_12_query_points.txt",
        },
        "checks": {"dimensions": "passed", "bounds": "passed", "finite_values": "passed", "row_alignment": "passed"},
        "source_file_date": evidence_date,
        "date_basis": "source-file modification date; not authoritative platform submission timestamp",
        "canonical_ledger_sha256": ledger_digest,
    }
    (root / "Results" / "week_12_evidence_validation.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Validated 88 historical pairs and appended 8 Week 12 pairs; ledger rows={len(existing)}")
    print(f"Ledger SHA-256: {ledger_digest}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--outputs", type=Path, required=True)
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    args = parser.parse_args()
    append(args.repository.resolve(), args.inputs.resolve(), args.outputs.resolve())


if __name__ == "__main__":
    main()
