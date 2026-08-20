"""Audit repository dataset files against common Git hosting size limits."""

from __future__ import annotations

import csv
from pathlib import Path


DATASET_EXTENSIONS = {".npy", ".npz", ".csv", ".tsv", ".parquet", ".pkl", ".pickle", ".joblib"}
WARNING_BYTES = 50 * 1024 * 1024
HARD_LIMIT_BYTES = 100 * 1024 * 1024


def audit(root: Path) -> list[dict[str, object]]:
    rows = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if (
            not path.is_file()
            or any(part.startswith(".") for part in relative.parts)
            or path.suffix.lower() not in DATASET_EXTENSIONS
        ):
            continue
        if path == root / "Results" / "dataset_size_audit.csv":
            continue
        size = path.stat().st_size
        rows.append(
            {
                "path": path.relative_to(root).as_posix(),
                "extension": path.suffix.lower(),
                "bytes": size,
                "mib": round(size / 1024**2, 6),
                "status": "hard_limit" if size >= HARD_LIMIT_BYTES else "warning" if size >= WARNING_BYTES else "pass",
            }
        )
    return sorted(rows, key=lambda row: int(row["bytes"]), reverse=True)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    rows = audit(root)
    output = root / "Results" / "dataset_size_audit.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["path", "extension", "bytes", "mib", "status"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    violations = [row for row in rows if row["status"] != "pass"]
    total = sum(int(row["bytes"]) for row in rows)
    largest = rows[0] if rows else {"path": "none", "bytes": 0}
    print(
        f"Audited {len(rows)} dataset files ({total} bytes total); "
        f"largest={largest['path']} ({largest['bytes']} bytes); violations={len(violations)}"
    )
    if violations:
        raise SystemExit("dataset size audit failed")


if __name__ == "__main__":
    main()
