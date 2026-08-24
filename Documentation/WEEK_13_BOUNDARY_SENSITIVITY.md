# Week 13 Boundary-Generation Sensitivity

The canonical Week 13 proposals remain immutable pre-outcome evidence. Their query-file SHA-256 is `55e012ff2df6bd04fa8d78c527c3c5fe32634cdf9da0744ecfcf22cbd4537686`; this analysis cannot replace them.

## Method

For Functions 2, 5 and 6, the proposal generator was rerun with identical data, Gaussian Process fits, seeds, Sobol candidates, local centres, local scales and acquisition parameters. Only local boundary handling changed: Gaussian perturbations were reflected back into `[0, 0.999999]` instead of clipped. Diagnostics were recomputed at each six-decimal candidate.

## Results

| Function | Canonical clipped candidate | Reflected-local candidate | Interpretation |
| --- | --- | --- | --- |
| F2 | `[0.686305, 0.999999]` | `[0.703542, 0.090883]` | The exact boundary recommendation is not robust to boundary generation. |
| F5 | `[0.035438, 0.999999, 0.999999, 0.999999]` | `[0.018955, 0.999459, 0.996407, 0.988539]` | Exact boundary coordinates disappear, but the recommendation remains strongly near the same boundary corner; minimum distance to a boundary is about 0.00054. |
| F6 | `[0.395407, 0.091768, 0.662260, 0.806631, 0.000000]` | `[0.140862, 0.019269, 0.893176, 0.953696, 0.013258]` | The exact boundary recommendation is not robust, although the reflected alternative remains near several boundaries. |

The full machine-readable comparison is in [`week_13_boundary_generation_sensitivity.csv`](../Week_13/04_Results/week_13_boundary_generation_sensitivity.csv). This is a candidate-generation sensitivity check, not outcome evidence and not a reason to revise the frozen submissions. F5’s corner-seeking behaviour is the most persistent of the three, but unknown true optima and sparse high-dimensional coverage prevent a global-optimality claim.

When authoritative Week 13 outputs arrive, they must be appended prospectively to the ledger, incumbents and validation must then be updated, and realised values must never be used to choose retrospectively among the already recorded UCB/EI/PI alternatives.
