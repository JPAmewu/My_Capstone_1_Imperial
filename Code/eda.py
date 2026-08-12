"""Scale-safe descriptive summaries for black-box optimisation histories."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .data_validation import validate_observations


def running_best(outputs: object) -> np.ndarray:
    """Return the maximisation best-so-far sequence."""
    y = np.asarray(outputs, dtype=float).reshape(-1)
    if not y.size or not np.isfinite(y).all():
        raise ValueError("outputs must be a non-empty finite vector")
    return np.maximum.accumulate(y)


def observation_summary(inputs: object, outputs: object) -> dict[str, object]:
    """Summarise one function without comparing incompatible objective scales."""
    X, y = validate_observations(inputs, outputs)
    best_index = int(np.argmax(y))
    return {
        "observations": len(y),
        "dimensions": X.shape[1],
        "best_index": best_index,
        "best_query_number": best_index + 1,
        "best_input": X[best_index].copy(),
        "best_output": float(y[best_index]),
        "latest_output": float(y[-1]),
        "latest_percentile": 100.0 * float(np.mean(y <= y[-1])),
        "input_min": X.min(axis=0),
        "input_max": X.max(axis=0),
    }


def observations_frame(inputs: object, outputs: object) -> pd.DataFrame:
    """Return validated observations as columns ``x1..xd``, output, and query."""
    X, y = validate_observations(inputs, outputs)
    frame = pd.DataFrame(X, columns=[f"x{i + 1}" for i in range(X.shape[1])])
    frame["output"] = y
    frame["query"] = np.arange(1, len(y) + 1)
    frame["running_best"] = running_best(y)
    return frame
