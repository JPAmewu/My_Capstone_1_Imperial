# Week 1 Function 4 methodology

## Objective

Describe the unknown four-dimensional Function 4 using the 30 starter
observations and preserve the Grid Search baseline for later rounds.

## Data and evidence boundary

The canonical starter arrays are stored in `../03_Data`. Inputs must have shape
`(30, 4)`, outputs must align one-to-one, all values must be finite, and inputs
must lie in `[0, 1]^4`. The cumulative arrays add the returned Week 1 ledger
pair for later checkpoints and are not inputs to this baseline.

## Week 1 method

As in the Week 1 main notebook, the focused analysis validates the data,
identifies the best observed query, calculates a running-best sequence, and
plots all four input dimensions against the objective. It does not claim a
global optimum, fit a GP, or claim a GP-UCB proposal.

## Reproducibility

From the repository root, run:

```bash
.venv/bin/python Week_01/Function_04/02_Code/analyse_function_04.py --write-artifacts --write-figure
.venv/bin/python Week_01/Function_04/02_Code/build_notebook.py
```

The figure uses six panels: ordered output history, running best, and one
scatter plot for each input. Every output uses the 30 starter rows.
