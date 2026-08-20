"""Strict formatting and validation for BBO portal query strings."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np


SUBMISSION_LOWER_BOUND = 0.000000
SUBMISSION_UPPER_BOUND = 0.999999
SUBMISSION_DECIMALS = 6
_COORDINATE = re.compile(r"(?:0\.\d{6})")


def format_portal_query(values: object, *, dimensions: int | None = None) -> str:
    """Return a strict six-decimal, hyphen-separated portal query."""
    query = np.asarray(values, dtype=float).reshape(-1)
    if dimensions is not None and query.size != dimensions:
        raise ValueError(f"expected {dimensions} coordinates; got {query.size}")
    if not query.size or not np.isfinite(query).all():
        raise ValueError("query coordinates must be non-empty and finite")
    rounded = np.round(query, SUBMISSION_DECIMALS)
    if np.any((rounded < SUBMISSION_LOWER_BOUND) | (rounded > SUBMISSION_UPPER_BOUND)):
        raise ValueError(
            "submission coordinates must lie in [0.000000, 0.999999] after rounding"
        )
    return "-".join(f"{value:.6f}" for value in rounded)


def validate_portal_query(text: str, *, dimensions: int) -> np.ndarray:
    """Validate exact portal syntax and return its numeric coordinates."""
    if not isinstance(text, str) or text != text.strip():
        raise ValueError("portal query must not contain surrounding whitespace")
    parts = text.split("-")
    if len(parts) != dimensions or any(_COORDINATE.fullmatch(part) is None for part in parts):
        raise ValueError(
            f"expected {dimensions} hyphen-separated coordinates in exact 0.000000 format"
        )
    values = np.asarray([float(part) for part in parts], dtype=float)
    if np.any((values < SUBMISSION_LOWER_BOUND) | (values > SUBMISSION_UPPER_BOUND)):
        raise ValueError("portal coordinates must lie in [0.000000, 0.999999]")
    return values


def validate_query_file(path: Path, dimensions: dict[int, int]) -> int:
    """Validate repository query-file lines of ``Function_N:<portal query>``."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        raise ValueError("query file is empty")
    seen: set[int] = set()
    for line_number, line in enumerate(lines, 1):
        match = re.fullmatch(r"Function_([1-8]):(.+)", line)
        if match is None:
            raise ValueError(f"line {line_number}: expected Function_N:<portal query>")
        function = int(match.group(1))
        if function in seen:
            raise ValueError(f"line {line_number}: duplicate Function_{function}")
        validate_portal_query(match.group(2), dimensions=dimensions[function])
        seen.add(function)
    if seen != set(dimensions):
        raise ValueError(f"query file functions are {sorted(seen)}; expected {sorted(dimensions)}")
    return len(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", help="portal query to validate")
    parser.add_argument("--dimensions", type=int, help="expected coordinate count")
    parser.add_argument("--file", type=Path, help="repository Function_N query file")
    args = parser.parse_args()
    if args.file:
        from Code.weekly_evidence import DIMENSIONS

        count = validate_query_file(args.file, DIMENSIONS)
        print(f"Valid: {count} function queries")
    elif args.query is not None and args.dimensions is not None:
        validate_portal_query(args.query, dimensions=args.dimensions)
        print("Valid portal query")
    else:
        parser.error("provide QUERY with --dimensions, or provide --file")


if __name__ == "__main__":
    main()
