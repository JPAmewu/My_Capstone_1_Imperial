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
    if len(rows) != 88 or len(keys) != 88:
        raise ValueError("Canonical ledger must contain 88 unique Week 1–11/function pairs")
    if {row["dataset_version"] for row in rows} != {"verified-query-output-ledger-v1.1"}:
        raise ValueError("Unexpected canonical ledger version")
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
