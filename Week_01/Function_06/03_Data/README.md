# Week 01 – Function 06 Data

## Data description

| Attribute | Value |
| --- | --- |
| Function | Function 6 |
| Input | 5D array |
| Output | 1D array |
| Optimisation goal | Maximise |
| Description of sample application | A five-variable multi-criteria design problem. It can represent recipe development in which ingredient quantities affect quality, nutrition, waste and cost. These competing criteria are combined into one negative score, so the best solution is the one with the largest value, typically the value closest to zero. |

## Files

This folder contains the canonical immutable starter observations:

- `initial_inputs.npy`: 20 observations with five bounded input dimensions.
- `initial_outputs.npy`: 20 aligned scalar outputs.

`verified_cumulative_inputs.npy` and `verified_cumulative_outputs.npy` preserve
the starter rows plus the subsequently returned Week 1 ledger pair. They are
lineage artifacts for later checkpoints and are not inputs to the Week 1
starter-baseline notebook.
