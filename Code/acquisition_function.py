"""Acquisition functions for maximising Gaussian Process surrogates."""

from __future__ import annotations

import numpy as np
from scipy.stats import norm


def _validated_predictions(mean: object, std: object) -> tuple[np.ndarray, np.ndarray]:
    """Return aligned, finite, one-dimensional predictive arrays."""
    mu = np.asarray(mean, dtype=float).reshape(-1)
    sigma = np.asarray(std, dtype=float).reshape(-1)
    if mu.shape != sigma.shape:
        raise ValueError("mean and standard deviation must have matching shapes")
    if not mu.size or not np.isfinite(mu).all() or not np.isfinite(sigma).all():
        raise ValueError("predictions must be non-empty and finite")
    if np.any(sigma < 0):
        raise ValueError("predictive standard deviation cannot be negative")
    return mu, sigma


def upper_confidence_bound(
    mean: object,
    std: object,
    *,
    kappa: float = 2.0,
) -> np.ndarray:
    """Return UCB scores ``mean + kappa * std`` for maximisation."""
    mu, sigma = _validated_predictions(mean, std)
    if not np.isfinite(kappa) or kappa < 0:
        raise ValueError("kappa must be finite and non-negative")
    return mu + kappa * sigma


def expected_improvement(
    mean: object,
    std: object,
    *,
    best: float,
    xi: float = 0.01,
) -> np.ndarray:
    """Return Expected Improvement scores for maximising an objective.

    Candidates with zero predictive uncertainty receive zero improvement.
    ``xi`` controls the minimum improvement margin and must be non-negative.
    """
    mu, sigma = _validated_predictions(mean, std)
    if not np.isfinite(best):
        raise ValueError("best must be finite")
    if not np.isfinite(xi) or xi < 0:
        raise ValueError("xi must be finite and non-negative")
    positive = sigma > 0
    scores = np.zeros_like(mu)
    improvement = mu[positive] - float(best) - xi
    z = improvement / sigma[positive]
    scores[positive] = improvement * norm.cdf(z) + sigma[positive] * norm.pdf(z)
    return scores


def probability_improvement(
    mean: object,
    std: object,
    *,
    best: float,
    xi: float = 0.01,
) -> np.ndarray:
    """Return Probability of Improvement scores for maximisation."""
    mu, sigma = _validated_predictions(mean, std)
    if not np.isfinite(best):
        raise ValueError("best must be finite")
    if not np.isfinite(xi) or xi < 0:
        raise ValueError("xi must be finite and non-negative")
    positive = sigma > 0
    scores = np.zeros_like(mu)
    scores[positive] = norm.cdf((mu[positive] - float(best) - xi) / sigma[positive])
    return scores
