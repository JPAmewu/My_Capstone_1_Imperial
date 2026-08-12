# Week 1 Function 1 methodology

## Objective

Maximise the unknown two-dimensional Function 1 using the ten starter
observations and propose a defensible direction for the following round.

## Data

The canonical inputs and outputs are stored in `../03_Data`. Inputs must have
shape `(n, 2)`, outputs must align one-to-one, all values must be finite, and
inputs must lie inside `[0, 1]^2`.

## Week 1 method

The recorded strategy was random search. The focused analysis validates the
data, identifies the best observed query, calculates a running-best sequence,
and plots both input dimensions against the objective. It does not claim that
the best observed point is a global optimum.

## Reproducibility

`../02_Code/analyse_function_01.py` imports stable loaders, EDA, and plotting
functions from the repository-level `Code` package. It has no dependency on
notebook cell order. Run it from the repository root with:

```bash
.venv/bin/python Week_01/Function_01/02_Code/analyse_function_01.py --write-artifacts
```

The command deterministically recreates `observations.csv`, `summary.json`, and
`function_01_diagnostics.png` from the immutable starter arrays.
