"""Stable Gaussian Process construction and fitting interfaces."""

from __future__ import annotations

import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern, RBF, WhiteKernel

from .data_validation import validate_observations


def build_kernel(dimensions: int, *, family: str = "matern"):
    """Build the bounded kernel family used throughout the corrected notebooks."""
    if dimensions < 1:
        raise ValueError("dimensions must be positive")
    if family == "matern":
        base = Matern(np.full(dimensions, 0.2), length_scale_bounds=(0.01, 2.0), nu=2.5)
    elif family == "rbf":
        base = RBF(np.ones(dimensions), length_scale_bounds=(0.01, 100.0))
    else:
        raise ValueError("family must be 'matern' or 'rbf'")
    return ConstantKernel(1.0, (1e-3, 1e3)) * base + WhiteKernel(1e-6, (1e-10, 1e-2))


def fit_gaussian_process(
    inputs: object,
    outputs: object,
    *,
    kernel=None,
    kernel_family: str = "matern",
    normalize_y: bool = True,
    optimizer_restarts: int = 3,
    random_state: int = 42,
) -> GaussianProcessRegressor:
    """Validate observations and fit a reproducible scikit-learn GP."""
    X, y = validate_observations(inputs, outputs)
    if optimizer_restarts < 0:
        raise ValueError("optimizer_restarts cannot be negative")
    model = GaussianProcessRegressor(
        kernel=kernel if kernel is not None else build_kernel(X.shape[1], family=kernel_family),
        normalize_y=normalize_y,
        n_restarts_optimizer=optimizer_restarts,
        random_state=random_state,
    )
    return model.fit(X, y)


def predict_with_uncertainty(model: GaussianProcessRegressor, candidates: object):
    """Return one-dimensional predictive mean and standard deviation arrays."""
    points = np.asarray(candidates, dtype=float)
    if points.ndim != 2:
        raise ValueError("candidates must have shape (n, d)")
    mean, std = model.predict(points, return_std=True)
    return np.asarray(mean, dtype=float).reshape(-1), np.asarray(std, dtype=float).reshape(-1)
