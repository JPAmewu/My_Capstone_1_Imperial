# Week 1 Function 8 methodology

## Objective

Describe the unknown eight-dimensional Function 8 using the 40 starter
observations and preserve the recorded Bayesian Optimisation strategy label.

## Data and evidence boundary

The canonical starter arrays are stored in `../03_Data`. Inputs must have shape
`(40, 8)`, outputs must align one-to-one, all values must be finite, and inputs
must lie in `[0, 1]^8`. The cumulative arrays add an improving returned Week 1
ledger pair for later checkpoints and are not inputs to this baseline.

## Week 1 method

As in the Week 1 main notebook, the focused analysis validates the data,
identifies the best observed starter query, calculates a running-best sequence,
and plots all eight input dimensions against the objective. The repository
records the strategy as Bayesian Optimisation, but does not preserve a
reproducible Week 1 GP configuration or acquisition calculation. Those details
are not retrospectively invented, and no global optimum is claimed.

## Reproducibility

From the repository root, run:

```bash
.venv/bin/python Week_01/Function_08/02_Code/analyse_function_08.py --write-artifacts --write-figure
.venv/bin/python Week_01/Function_08/02_Code/build_notebook.py
```

The figure uses ten panels: ordered output history, running best, and one
scatter plot for each input. Every output uses the 40 starter rows.
