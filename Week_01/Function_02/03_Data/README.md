# Week 01 – Function 02 Data

## Data description

| Attribute | Value |
| --- | --- |
| Function | Function 2 |
| Input | 2D array |
| Output | 1D array |
| Optimisation goal | Maximise |
| Description of sample application | A two-variable noisy optimisation problem with several possible peaks. It can represent the tuning of a statistical or machine-learning model using a log-likelihood score. A good method must manage measurement noise and avoid settling too early on a weak local optimum. |

## Files

This folder contains the canonical immutable starter observations:

- `initial_inputs.npy`: 10 observations with two bounded input dimensions.
- `initial_outputs.npy`: 10 aligned scalar outputs.

`verified_cumulative_inputs.npy` and `verified_cumulative_outputs.npy` preserve
the starter rows plus the subsequently returned Week 1 ledger pair. They are
lineage artifacts for later checkpoints and are not inputs to the Week 1
starter-baseline notebook.
