"""Non-duplicate query selection from precomputed candidate predictions."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .acquisition_function import expected_improvement, upper_confidence_bound
from .data_validation import duplicate_mask, validate_candidates
from .portal_format import SUBMISSION_LOWER_BOUND, SUBMISSION_UPPER_BOUND


@dataclass(frozen=True)
class QuerySelection:
    query: np.ndarray
    index: int
    acquisition: float
    predicted_mean: float
    predicted_std: float
    source: str | None = None


def select_query(
    candidates: object,
    observed: object,
    mean: object,
    std: object,
    *,
    method: str = "ucb",
    best: float | None = None,
    kappa: float = 2.0,
    xi: float = 0.01,
    decimals: int = 6,
    sources: object | None = None,
) -> QuerySelection:
    """Select the best rounded candidate after excluding observed duplicates."""
    X = np.asarray(observed, dtype=float)
    points = validate_candidates(
        candidates,
        dimensions=X.shape[1],
        lower_bound=SUBMISSION_LOWER_BOUND,
        upper_bound=SUBMISSION_UPPER_BOUND,
    )
    mu, sigma = np.asarray(mean, float).reshape(-1), np.asarray(std, float).reshape(-1)
    if len(points) != len(mu) or mu.shape != sigma.shape:
        raise ValueError("candidate predictions must align with candidate rows")
    if method == "ucb":
        scores = upper_confidence_bound(mu, sigma, kappa=kappa)
    elif method == "ei":
        if best is None:
            raise ValueError("best is required for expected improvement")
        scores = expected_improvement(mu, sigma, best=best, xi=xi)
    else:
        raise ValueError("method must be 'ucb' or 'ei'")
    scores = np.asarray(scores, float)
    scores[duplicate_mask(points, X, decimals=decimals)] = -np.inf
    if not np.isfinite(scores).any():
        raise RuntimeError("no distinct candidate is available")
    index = int(np.argmax(scores))
    source_values = None if sources is None else np.asarray(sources, dtype=object)
    if source_values is not None and len(source_values) != len(points):
        raise ValueError("sources must align with candidate rows")
    return QuerySelection(
        query=np.round(points[index], decimals),
        index=index,
        acquisition=float(scores[index]),
        predicted_mean=float(mu[index]),
        predicted_std=float(sigma[index]),
        source=None if source_values is None else str(source_values[index]),
    )
