# Week 01 – Function 05 Data

## Data description

| Attribute | Value |
| --- | --- |
| Function | Function 5 |
| Input | 4D array |
| Output | 1D array |
| Optimisation goal | Maximise |
| Description of sample application | A four-variable process-optimisation problem. It can represent the selection of chemical inputs that produces the greatest manufacturing yield. The response is expected to have one main peak, making the central task the efficient identification of that best operating point. |

## Files

This folder contains the canonical immutable starter observations:

- `initial_inputs.npy`: 20 observations with four bounded input dimensions.
- `initial_outputs.npy`: 20 aligned scalar outputs.

`verified_cumulative_inputs.npy` and `verified_cumulative_outputs.npy` preserve
the starter rows plus the subsequently returned Week 1 ledger pair. They are
lineage artifacts for later checkpoints and are not inputs to the Week 1
starter-baseline notebook.
