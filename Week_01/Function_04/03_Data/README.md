# Week 01 – Function 04 Data

## Data description

| Attribute | Value |
| --- | --- |
| Function | Function 4 |
| Input | 4D array |
| Output | 1D array |
| Optimisation goal | Maximise |
| Description of sample application | A four-variable model-tuning problem. It can represent a fast predictive model used to support costly decisions, such as allocating products across warehouses. The objective is complex and may contain several local optima, so candidate solutions require careful search and validation. |

## Files

This folder contains the canonical immutable starter observations:

- `initial_inputs.npy`: 30 observations with four bounded input dimensions.
- `initial_outputs.npy`: 30 aligned scalar outputs.

`verified_cumulative_inputs.npy` and `verified_cumulative_outputs.npy` preserve
the starter rows plus the subsequently returned Week 1 ledger pair. They are
lineage artifacts for later checkpoints and are not inputs to the Week 1
starter-baseline notebook.
