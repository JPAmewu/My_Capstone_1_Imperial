"""Structural validation shared by the weekly optimisation workflows."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def validate_observations(
    inputs: ArrayLike,
    outputs: ArrayLike,
    *,
    dimensions: int | None = None,
    lower_bound: float = 0.0,
    upper_bound: float = 1.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Return validated floating-point ``(X, y)`` arrays.

    Inputs must be a non-empty two-dimensional matrix. Outputs are flattened to
    one dimension and must align one-to-one with the rows of ``X``.
    """
    X = np.asarray(inputs, dtype=float)
    y = np.asarray(outputs, dtype=float).reshape(-1)
    if X.ndim != 2 or not X.shape[0]:
        raise ValueError(f"inputs must have non-empty shape (n, d); got {X.shape}")
    if dimensions is not None and X.shape[1] != dimensions:
        raise ValueError(f"expected {dimensions} dimensions; got {X.shape[1]}")
    if y.size != X.shape[0]:
        raise ValueError(f"input/output count mismatch: {X.shape[0]} != {y.size}")
    if not np.isfinite(X).all() or not np.isfinite(y).all():
        raise ValueError("inputs and outputs must contain only finite values")
    if np.any((X < lower_bound) | (X > upper_bound)):
        raise ValueError(f"inputs must lie in [{lower_bound}, {upper_bound}]")
    return X, y


def validate_candidates(
    candidates: ArrayLike,
    *,
    dimensions: int,
    lower_bound: float = 0.0,
    upper_bound: float = 1.0,
) -> NDArray[np.float64]:
    """Validate a non-empty candidate matrix without requiring outputs."""
    points = np.asarray(candidates, dtype=float)
    if points.ndim != 2 or points.shape[1] != dimensions or not len(points):
        raise ValueError(f"candidates must have non-empty shape (n, {dimensions})")
    if not np.isfinite(points).all():
        raise ValueError("candidates must contain only finite values")
    if np.any((points < lower_bound) | (points > upper_bound)):
        raise ValueError(f"candidates must lie in [{lower_bound}, {upper_bound}]")
    return points


def duplicate_mask(
    candidates: ArrayLike,
    observed: ArrayLike,
    *,
    decimals: int = 6,
) -> NDArray[np.bool_]:
    """Return ``True`` for candidates duplicating observed points after rounding."""
    points = np.round(np.asarray(candidates, dtype=float), decimals)
    existing = np.round(np.asarray(observed, dtype=float), decimals)
    if points.ndim != 2 or existing.ndim != 2 or points.shape[1] != existing.shape[1]:
        raise ValueError("candidate and observed matrices must have matching dimensions")
    return np.any(np.all(points[:, None, :] == existing[None, :, :], axis=2), axis=1)
