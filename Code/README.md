# Reusable code

This folder contains stable, notebook-independent Python interfaces shared by
the corrected Week 1–11 optimisation workflows. Weeks 12–13 are historical
placeholders and were not used as implementation sources.

| Module | Purpose |
| --- | --- |
| [`data_loading.py`](data_loading.py) | Repository discovery, safe `.npy` loading, starter-data access, and evidence-backed appends |
| [`data_validation.py`](data_validation.py) | Shape, alignment, bounds, finiteness, candidate, and duplicate validation |
| [`eda.py`](eda.py) | Function-specific summaries, running best, and tidy observation frames |
| [`gaussian_process.py`](gaussian_process.py) | Bounded RBF/Matérn kernels, reproducible GP fitting, and uncertainty prediction |
| [`acquisition_function.py`](acquisition_function.py) | Validated Upper Confidence Bound and Expected Improvement scoring |
| [`candidate_generation.py`](candidate_generation.py) | Seeded global, local, and hybrid candidate generation |
| [`query_selection.py`](query_selection.py) | UCB/EI acquisition scoring and rounded non-duplicate selection |
| [`plotting.py`](plotting.py) | Consolidated Matplotlib function and proposal diagnostics |

The requested labels `data.loading.np`, `gaussian_proccess.py`,
`acquisition _funnction.py`, `candidates_generation.py`, and
`querry_selection.py` are represented using the standard Python spellings above
so the files are importable and searchable.

## Design rules

- Functions accept their dependencies explicitly; none rely on notebook globals
  or cell execution order.
- Loaders disable pickle and validate data immediately.
- GP fitting uses `normalize_y=True` by default instead of manual scaling.
- Candidate generation requires an explicit NumPy random generator.
- Query selection rejects duplicates after submission-precision rounding.
- EDA never ranks raw outputs across different black-box functions.
- Plotting functions return Matplotlib `Figure` objects and do not call
  `plt.show()`, leaving display and saving decisions to the caller.

## Example

```python
import numpy as np

from Code.candidate_generation import uniform_candidates
from Code.data_loading import load_starter_data
from Code.gaussian_process import fit_gaussian_process, predict_with_uncertainty
from Code.query_selection import select_query

X, y = load_starter_data(1)
rng = np.random.default_rng(101)
points = uniform_candidates(X.shape[1], 5_000, rng=rng)
model = fit_gaussian_process(X, y)
mean, std = predict_with_uncertainty(model, points)
selection = select_query(points, X, mean, std, method="ucb", kappa=2.0)
print(selection.query)
```

Run the independent checks from the repository root with:

```bash
.venv/bin/python -m unittest discover -s Code/tests -v
```
