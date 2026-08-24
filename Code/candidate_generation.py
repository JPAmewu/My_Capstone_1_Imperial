"""Deterministic bounded candidate generation for acquisition searches."""

from __future__ import annotations

import numpy as np

from .data_validation import validate_candidates
from .portal_format import SUBMISSION_LOWER_BOUND, SUBMISSION_UPPER_BOUND


def make_rng(seed: int | None = None) -> np.random.Generator:
    """Create an explicit generator so results do not depend on global state."""
    return np.random.default_rng(seed)


def uniform_candidates(
    dimensions: int,
    count: int,
    *,
    rng: np.random.Generator,
    lower_bound: float = SUBMISSION_LOWER_BOUND,
    upper_bound: float = SUBMISSION_UPPER_BOUND,
) -> np.ndarray:
    """Generate reproducible uniform candidates inside a bounded hypercube."""
    if dimensions < 1 or count < 1 or lower_bound >= upper_bound:
        raise ValueError("dimensions/count must be positive and bounds ordered")
    return rng.uniform(lower_bound, upper_bound, size=(count, dimensions))


def local_candidates(
    centre: object,
    count: int,
    *,
    rng: np.random.Generator,
    scale: float = 0.08,
    lower_bound: float = SUBMISSION_LOWER_BOUND,
    upper_bound: float = SUBMISSION_UPPER_BOUND,
) -> np.ndarray:
    """Generate clipped Gaussian candidates near a known strong point."""
    origin = np.asarray(centre, dtype=float).reshape(-1)
    if not origin.size or count < 1 or scale <= 0:
        raise ValueError("centre/count/scale must be non-empty and positive")
    points = np.clip(origin + rng.normal(0.0, scale, (count, origin.size)), lower_bound, upper_bound)
    return validate_candidates(points, dimensions=origin.size, lower_bound=lower_bound, upper_bound=upper_bound)


def reflected_local_candidates(
    centre: object,
    count: int,
    *,
    rng: np.random.Generator,
    scale: float = 0.08,
    lower_bound: float = SUBMISSION_LOWER_BOUND,
    upper_bound: float = SUBMISSION_UPPER_BOUND,
) -> np.ndarray:
    """Generate Gaussian perturbations reflected into the bounded domain.

    Reflection avoids the artificial point masses at exact boundaries created
    by clipping while retaining the same centre, scale, count, and random seed.
    """
    origin = np.asarray(centre, dtype=float).reshape(-1)
    if not origin.size or count < 1 or scale <= 0 or lower_bound >= upper_bound:
        raise ValueError("centre/count/scale must be valid and bounds ordered")
    width = upper_bound - lower_bound
    raw = origin + rng.normal(0.0, scale, (count, origin.size))
    shifted = np.mod(raw - lower_bound, 2 * width)
    points = lower_bound + np.where(shifted <= width, shifted, 2 * width - shifted)
    return validate_candidates(
        points,
        dimensions=origin.size,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
    )


def hybrid_candidates(
    centre: object,
    *,
    rng: np.random.Generator,
    global_count: int = 8000,
    local_count: int = 3000,
    local_scale: float = 0.08,
) -> tuple[np.ndarray, np.ndarray]:
    """Combine global and local candidates and return parallel source labels."""
    origin = np.asarray(centre, dtype=float).reshape(-1)
    global_points = uniform_candidates(origin.size, global_count, rng=rng)
    local_points = local_candidates(origin, local_count, rng=rng, scale=local_scale)
    return np.vstack((global_points, local_points)), np.array(
        ["global"] * global_count + ["local"] * local_count,
        dtype=object,
    )
