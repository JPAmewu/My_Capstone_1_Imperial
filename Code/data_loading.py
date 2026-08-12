"""Safe local loading for repository-backed NumPy observation pairs."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from .data_validation import validate_observations


FUNCTION_DIMENSIONS = {1: 2, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6, 8: 8}


def find_repository_root(start: str | Path | None = None) -> Path:
    """Find the nearest parent containing the canonical Week 1 data tree."""
    current = Path.cwd() if start is None else Path(start).expanduser().resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "Week_01").is_dir() and (candidate / "Code").is_dir():
            return candidate
    raise FileNotFoundError("repository root containing Week_01 and Code was not found")


def load_numpy_pair(
    input_path: str | Path,
    output_path: str | Path,
    *,
    dimensions: int | None = None,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Load an ``X/y`` pair with pickle disabled and validate its structure."""
    input_file, output_file = Path(input_path), Path(output_path)
    if not input_file.is_file() or not output_file.is_file():
        missing = [str(p) for p in (input_file, output_file) if not p.is_file()]
        raise FileNotFoundError(f"missing NumPy data file(s): {', '.join(missing)}")
    X = np.load(input_file, allow_pickle=False)
    y = np.load(output_file, allow_pickle=False)
    return validate_observations(X, y, dimensions=dimensions)


def load_starter_data(
    function_number: int,
    *,
    repository_root: str | Path | None = None,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Load canonical Week 1 starter observations for Function 1–8."""
    if function_number not in FUNCTION_DIMENSIONS:
        raise ValueError("function_number must be an integer from 1 to 8")
    root = find_repository_root(repository_root)
    folder = root / "Week_01" / f"Function_{function_number:02d}" / "03_Data"
    return load_numpy_pair(
        folder / "initial_inputs.npy",
        folder / "initial_outputs.npy",
        dimensions=FUNCTION_DIMENSIONS[function_number],
    )


def append_observations(
    inputs: NDArray[np.float64],
    outputs: NDArray[np.float64],
    new_inputs: object,
    new_outputs: object,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Append evidence-backed pairs and revalidate the cumulative dataset."""
    X, y = validate_observations(inputs, outputs)
    added_X, added_y = validate_observations(new_inputs, new_outputs, dimensions=X.shape[1])
    return validate_observations(np.vstack((X, added_X)), np.concatenate((y, added_y)))
