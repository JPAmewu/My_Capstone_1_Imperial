# Week 1 Function 3 methodology

## Objective

Describe the unknown three-dimensional Function 3 using the 15 starter
observations and preserve the Grid Search baseline for later rounds.

## Data and evidence boundary

The canonical starter arrays are stored in `../03_Data`. Inputs must have shape
`(15, 3)`, outputs must align one-to-one, all values must be finite, and inputs
must lie in `[0, 1]^3`. The cumulative arrays add the returned Week 1 ledger
pair for later checkpoints and are not inputs to this baseline.

## Week 1 method

As in the Week 1 main notebook, the focused analysis validates the data,
identifies the best observed query, calculates a running-best sequence, and
plots all three input dimensions against the objective. It does not claim a
global optimum, fit a GP, or claim a GP-UCB proposal.

## Reproducibility

From the repository root, run:

```bash
.venv/bin/python Week_01/Function_03/02_Code/analyse_function_03.py --write-artifacts --write-figure
.venv/bin/python Week_01/Function_03/02_Code/build_notebook.py
```

The figure uses five panels: ordered output history, running best, and one
scatter plot for each input. Every output uses the 15 starter rows.
