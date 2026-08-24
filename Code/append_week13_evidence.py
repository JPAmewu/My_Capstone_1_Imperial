"""Validate and prospectively append authoritative Week 13 cumulative evidence."""

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

from Code.recover_capstone_archive import DIMENSIONS, FIELDNAMES, _parse_inputs, _parse_outputs


NEW_VERSION = "verified-query-output-ledger-v1.3"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_queries(root: Path) -> list[list[float]]:
    rows = []
    for line in (root / "Week_13/01_Queries/week_13_query_points.txt").read_text().splitlines():
        rows.append([float(value) for value in line.split(":", 1)[1].split("-")])
    if len(rows) != 8:
        raise ValueError("Frozen Week 13 query file must contain eight functions")
    return rows


def append(root: Path, input_path: Path, output_path: Path) -> None:
    rounds_x, rounds_y = _parse_inputs(input_path), _parse_outputs(output_path)
    if len(rounds_x) != 13 or len(rounds_y) != 13:
        raise ValueError("Expected one complete cumulative snapshot containing 13 rounds")

    ledger = root / "Results/query_output_ledger.csv"
    with ledger.open(newline="", encoding="utf-8") as source:
        existing = list(csv.DictReader(source))
    if len(existing) not in {96, 104}:
        raise ValueError(f"Expected a 96- or 104-row ledger, found {len(existing)} rows")
    by_key = {(int(row["week"]), int(row["function"])): row for row in existing}

    for week in range(1, 13):
        for function in range(1, 9):
            row = by_key[(week, function)]
            if not np.allclose(json.loads(row["query"]), rounds_x[week - 1][function - 1], rtol=0, atol=5e-7):
                raise ValueError(f"Week {week} F{function}: cumulative query conflicts with ledger")
            if not np.isclose(float(row["returned_output"]), rounds_y[week - 1][function - 1], rtol=0, atol=5e-12):
                raise ValueError(f"Week {week} F{function}: cumulative output conflicts with ledger")

    submitted = frozen_queries(root)
    exported, outputs = rounds_x[12], rounds_y[12]
    for function, (seen, exact, output) in enumerate(zip(exported, submitted, outputs), 1):
        seen_values, exact_values = np.asarray(seen, float), np.asarray(exact, float)
        if seen_values.shape != (DIMENSIONS[function],):
            raise ValueError(f"Week 13 F{function}: incorrect dimensions")
        if not np.isfinite(seen_values).all() or not np.isfinite(float(output)):
            raise ValueError(f"Week 13 F{function}: non-finite evidence")
        # NumPy's source rendering displays submitted 0.999999 coordinates as 1.
        if not np.allclose(seen_values, exact_values, rtol=0, atol=1.0000001e-6):
            raise ValueError(f"Week 13 F{function}: source input does not match frozen submission")

    input_digest, output_digest = sha256(input_path), sha256(output_path)
    evidence_dir = root / "Results/source_evidence/week_13"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    preserved_input, preserved_output = evidence_dir / "week_13_inputs.txt", evidence_dir / "week_13_outputs.txt"
    for source, target in ((input_path, preserved_input), (output_path, preserved_output)):
        if target.exists() and target.read_bytes() != source.read_bytes():
            raise ValueError(f"Published source evidence would change: {target}")
        shutil.copyfile(source, target)
    if sha256(preserved_input) != input_digest or sha256(preserved_output) != output_digest:
        raise ValueError("Preserved evidence copy failed SHA-256 verification")

    if len(existing) == 96:
        archive = root / "Results/archive"
        archive.mkdir(exist_ok=True)
        prior = archive / "query_output_ledger_v1.2.csv"
        shutil.copyfile(ledger, prior)
        (archive / "query_output_ledger_v1.2.sha256").write_text(f"{sha256(prior)}  {prior.name}\n")
        evidence_date = datetime.fromtimestamp(input_path.stat().st_mtime).astimezone().date().isoformat()
        for function, (query, output) in enumerate(zip(submitted, outputs), 1):
            existing.append({
                "week": "13", "function": str(function),
                "query": json.dumps(query, separators=(",", ":")),
                "returned_output": repr(float(output)), "dataset_version": NEW_VERSION,
                "submission_date": evidence_date,
                "date_basis": "source_file_mtime; not platform submission timestamp",
                "notebook": "Week_13/01_Queries/week_13_query_points.txt", "commit_sha": "",
                "evidence_status": "verified_cumulative_archive_pair_matches_frozen_pre_outcome_query",
                "source_registry": "Results/query_output_ledger.csv",
                "source_input": "Results/source_evidence/week_13/week_13_inputs.txt",
                "source_output": "Results/source_evidence/week_13/week_13_outputs.txt",
                "source_input_sha256": input_digest, "source_output_sha256": output_digest,
                "duplicate_of": "",
            })
    else:
        for function, (query, output) in enumerate(zip(submitted, outputs), 1):
            row = by_key[(13, function)]
            if row["query"] != json.dumps(query, separators=(",", ":")) or float(row["returned_output"]) != float(output):
                raise ValueError(f"Published Week 13 F{function} evidence would change")

    with ledger.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader(); writer.writerows(existing)
    ledger_digest = sha256(ledger)
    (root / "Results/query_output_ledger.sha256").write_text(f"{ledger_digest}  {ledger.name}\n")

    manifest_path = root / "Results/query_output_source_manifest.csv"
    with manifest_path.open(newline="", encoding="utf-8") as source:
        manifest = list(csv.DictReader(source))
    if not any(int(row["week"]) == 13 for row in manifest):
        manifest.append({
            "week": "13", "source_snapshot": "13", "identical_archive_copy_count": "1",
            "source_input": "Results/source_evidence/week_13/week_13_inputs.txt",
            "source_output": "Results/source_evidence/week_13/week_13_outputs.txt",
            "source_input_sha256": input_digest, "source_output_sha256": output_digest,
            "archive_date": datetime.fromtimestamp(input_path.stat().st_mtime).astimezone().date().isoformat(),
            "validation": "complete_aligned_snapshot; prefix_matches_96_published_pairs; final_inputs_match_frozen_week13_queries",
        })
    with manifest_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(manifest[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(manifest)

    versions_path = root / "Results/query_output_ledger_versions.json"
    versions = json.loads(versions_path.read_text())
    for entry in versions:
        if entry["dataset_version"] == "verified-query-output-ledger-v1.2":
            entry.update(status="superseded_preserved_immutable", path="Results/archive/query_output_ledger_v1.2.csv", sha256=sha256(root / "Results/archive/query_output_ledger_v1.2.csv"))
    if not any(entry["dataset_version"] == NEW_VERSION for entry in versions):
        versions.append({"dataset_version": NEW_VERSION, "status": "canonical", "path": "Results/query_output_ledger.csv", "sha256": ledger_digest, "reason": "Prospectively appended eight authoritative Week 13 pairs matching the frozen pre-outcome query set."})
    versions_path.write_text(json.dumps(versions, indent=2) + "\n")

    prior_best = {function: max(float(row["returned_output"]) for row in existing if int(row["function"]) == function and int(row["week"]) <= 12) for function in range(1, 9)}
    outcome_path = root / "Week_13/04_Results/week_13_confirmed_outcomes.csv"
    with outcome_path.open("w", newline="", encoding="utf-8") as target:
        fields = ["function", "submitted_query", "returned_output", "week_12_incumbent", "improvement", "new_incumbent", "improved"]
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n"); writer.writeheader()
        for function, (query, output) in enumerate(zip(submitted, outputs), 1):
            improvement = max(0.0, float(output) - prior_best[function])
            writer.writerow({"function": function, "submitted_query": json.dumps(query, separators=(",", ":")), "returned_output": repr(float(output)), "week_12_incumbent": repr(prior_best[function]), "improvement": repr(improvement), "new_incumbent": repr(max(prior_best[function], float(output))), "improved": improvement > 0})

    report = {"dataset_version": NEW_VERSION, "source_rounds": 13, "historical_prefix_pairs_checked": 96, "week_13_pairs_appended": 8, "exact_frozen_queries_recorded": True, "source_rendering_tolerance": "1e-6 only for displayed 1.0 versus submitted 0.999999", "source_input_sha256": input_digest, "source_output_sha256": output_digest, "canonical_ledger_sha256": ledger_digest, "checks": {"prefix": "passed", "dimensions": "passed", "finite_values": "passed", "frozen_query_alignment": "passed"}}
    (root / "Results/week_13_evidence_validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"Validated 96 historical pairs and appended 8 Week 13 pairs; ledger rows={len(existing)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, required=True); parser.add_argument("--outputs", type=Path, required=True)
    parser.add_argument("--repository", type=Path, default=Path.cwd()); args = parser.parse_args()
    append(args.repository.resolve(), args.inputs.resolve(), args.outputs.resolve())


if __name__ == "__main__":
    main()
