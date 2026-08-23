# Week 01 – Function 07 Data

## Data description

| Attribute | Value |
| --- | --- |
| Function | Function 7 |
| Input | 6D array |
| Output | 1D array |
| Optimisation goal | Maximise |
| Description of sample application | A six-variable hyperparameter-tuning problem for a machine-learning model. Each input controls one aspect of model training or structure, while the output measures predictive performance. The aim is to identify a configuration that gives the highest reliable performance without knowing the mathematical form of the response. |

## Files

This folder contains the canonical immutable starter observations:

- `initial_inputs.npy`: 30 observations with six bounded input dimensions.
- `initial_outputs.npy`: 30 aligned scalar outputs.

`verified_cumulative_inputs.npy` and `verified_cumulative_outputs.npy` preserve
the starter rows plus the subsequently returned Week 1 ledger pair. They are
lineage artifacts for later checkpoints and are not inputs to the Week 1
starter-baseline notebook.
