# Week 01 – Function 03 Data

## Data description

| Attribute | Value |
| --- | --- |
| Function | Function 3 |
| Input | 3D array |
| Output | 1D array |
| Optimisation goal | Maximise |
| Description of sample application | A three-variable formulation problem. It can represent experiments that combine three compounds while seeking to reduce harmful effects. Because the competition requires maximisation, an undesirable outcome such as the number of side effects can be converted into a score whose larger values represent safer combinations. |

## Files

This folder contains the canonical immutable starter observations:

- `initial_inputs.npy`: 15 observations with three bounded input dimensions.
- `initial_outputs.npy`: 15 aligned scalar outputs.

`verified_cumulative_inputs.npy` and `verified_cumulative_outputs.npy` preserve
the starter rows plus the subsequently returned Week 1 ledger pair. They are
lineage artifacts for later checkpoints and are not inputs to the Week 1
starter-baseline notebook.
