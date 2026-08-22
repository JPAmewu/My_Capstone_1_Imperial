"""Verify the published canonical ledger without rewriting it.

Ledger recovery is intentionally performed only by recover_capstone_archive.py
because it requires the original read-only Downloads evidence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


def verify_ledger(path: Path, checksum: Path) -> None:
    with path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    keys = {(row["week"], row["function"]) for row in rows}
    if len(rows) != 96 or len(keys) != 96:
        raise ValueError("Canonical ledger must contain 96 unique Week 1–12/function pairs")
    versions = {row["dataset_version"] for row in rows}
    if versions != {"verified-query-output-ledger-v1.1", "verified-query-output-ledger-v1.2"}:
        raise ValueError(f"Unexpected row-version set: {versions}")
    if sum(row["dataset_version"] == "verified-query-output-ledger-v1.2" for row in rows) != 8:
        raise ValueError("Exactly eight appended Week 12 rows must carry ledger version v1.2")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = checksum.read_text(encoding="utf-8").split()[0]
    if digest != expected:
        raise ValueError("Ledger checksum mismatch")
    print(f"Verified {len(rows)} immutable rows; SHA-256: {digest}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=Path("Results/query_output_ledger.csv"))
    parser.add_argument("--checksum", type=Path, default=Path("Results/query_output_ledger.sha256"))
    args = parser.parse_args()
    verify_ledger(args.ledger, args.checksum)


if __name__ == "__main__":
    main()
