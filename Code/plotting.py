"""Consolidated Matplotlib diagnostics for one objective function."""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from .data_validation import validate_observations
from .eda import running_best


def plot_function_diagnostics(
    inputs: object,
    outputs: object,
    *,
    title: str = "Function diagnostics",
    latest_label: str = "Latest observation",
) -> Figure:
    """Plot observations, running best, and every input/output relationship."""
    X, y = validate_observations(inputs, outputs)
    query_numbers = np.arange(1, len(y) + 1)
    best_index = int(np.argmax(y))
    panels, columns = X.shape[1] + 2, 3
    rows = math.ceil(panels / columns)
    figure, axes = plt.subplots(rows, columns, figsize=(15, 4 * rows), squeeze=False)
    axes = axes.ravel()

    axes[0].plot(query_numbers, y, color="#2a6fbb", marker="o", linewidth=1.8, markersize=4)
    axes[0].scatter(query_numbers[-1], y[-1], marker="D", color="#d62728", s=75, label=latest_label)
    axes[0].scatter(query_numbers[best_index], y[best_index], marker="*", color="#ffbf00", edgecolor="black", s=170, label="Best")
    axes[0].set(xlabel="Query number", ylabel="Objective value", title="Observed values")
    axes[0].legend()
    axes[0].xaxis.set_major_locator(MaxNLocator(integer=True))

    axes[1].step(query_numbers, running_best(y), where="post", color="#2ca02c", linewidth=2.2)
    axes[1].set(xlabel="Query number", ylabel="Best value so far", title="Running-best progress")
    axes[1].xaxis.set_major_locator(MaxNLocator(integer=True))

    colour_plot = None
    for column, axis in enumerate(axes[2 : 2 + X.shape[1]]):
        colour_plot = axis.scatter(X[:, column], y, c=query_numbers, cmap="viridis", s=44, alpha=0.85, edgecolor="white", linewidth=0.35)
        axis.scatter(X[-1, column], y[-1], marker="D", color="#d62728", s=70)
        axis.scatter(X[best_index, column], y[best_index], marker="*", color="#ffbf00", edgecolor="black", s=150)
        axis.set(xlabel=f"Input x{column + 1}", ylabel="Objective value", title=f"x{column + 1} vs objective")
    for axis in axes[panels:]:
        axis.set_visible(False)
    for axis in axes[:panels]:
        axis.grid(True, alpha=0.25)
    if colour_plot is not None:
        figure.colorbar(colour_plot, ax=axes[2 : 2 + X.shape[1]].tolist(), label="Query number", shrink=0.85)
    figure.suptitle(title, fontsize=16, fontweight="bold")
    figure.subplots_adjust(top=0.91, hspace=0.45, wspace=0.30)
    return figure


def plot_proposal_overview(
    labels: object,
    uncertainty: object,
    distance_from_best: object,
    *,
    title: str = "Proposal diagnostics",
) -> Figure:
    """Plot comparable proposal diagnostics without mixing objective scales."""
    names = np.asarray(labels)
    std = np.asarray(uncertainty, dtype=float)
    distance = np.asarray(distance_from_best, dtype=float)
    if not (len(names) == len(std) == len(distance)):
        raise ValueError("labels, uncertainty, and distance must align")
    figure, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].bar(names, std, color="#9467bd")
    axes[0].set(title="Uncertainty at proposal", ylabel="Predictive std")
    axes[1].bar(names, distance, color="#17becf")
    axes[1].set(title="Distance from observed best", ylabel="Euclidean distance")
    figure.suptitle(title, fontsize=16, fontweight="bold")
    figure.tight_layout()
    return figure
