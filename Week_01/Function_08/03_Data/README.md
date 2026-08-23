# Week 01 – Function 08 Data

## Data description

| Attribute | Value |
| --- | --- |
| Function | Function 8 |
| Input | 8D array |
| Output | 1D array |
| Optimisation goal | Maximise |
| Description of sample application | An eight-variable high-dimensional optimisation problem. It can represent the tuning of a complex system, such as a machine-learning model with eight hyperparameters, using a single performance score. The large search space makes complete exploration impractical, so the objective is to find a strong parameter configuration with a high output value. |

## Files

This folder contains the canonical immutable starter observations:

- `initial_inputs.npy`: 40 observations with eight bounded input dimensions.
- `initial_outputs.npy`: 40 aligned scalar outputs.

`verified_cumulative_inputs.npy` and `verified_cumulative_outputs.npy` preserve
the starter rows plus the subsequently returned Week 1 ledger pair. The return
improves the starter incumbent, but it remains a lineage artifact for later
checkpoints and is not an input to the Week 1 starter-baseline notebook.
