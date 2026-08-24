# Final findings

These four findings answer the capstone FAQ explicitly. They separate realised optimisation performance, surrogate quality, recommendation robustness, and data integrity so that a predicted query is never presented as a returned result.

## Finding 1 — Optimisation performance

Twelve of the 104 verified weekly returns established a new within-function incumbent, an observed improvement rate of 11.5%. Week 13 added two improvements: F5 (`+893.930245`) and F6 (`+0.131829`). The final recorded maxima are incumbents rather than proven global optima.

## Finding 2 — Surrogate accuracy and uncertainty calibration

Rolling one-step-ahead validation produced 104 chronological folds, thirteen per function. All eight Gaussian Processes achieved positive RMSE skill relative to a historical-mean baseline. Calibration remains imperfect: nominal 95% coverage is 61.5% for F5, 69.2% for F7, and 76.9% for F4 and F6. Predictive means and intervals are useful diagnostic evidence but should not be treated as equally reliable across functions.

## Finding 3 — Recommendation robustness and exploration–exploitation

The sole canonical Week 13 methodology compares UCB, EI, and PI and then applies a function-specific policy: UCB for F1/F4/F7/F8, EI for F2/F5/F6, and PI for F3. The reasons were recorded after observing Week 12 and before any Week 13 outcomes. This adaptive policy is heuristic, not a randomised or statistically controlled acquisition comparison, so no acquisition rule is declared a winner.

## Finding 4 — Data lineage, reproducibility, and limitation

The most consequential methodological result was recovery from a data-lineage failure. Starter arrays plus an immutable 104-row query/output ledger reconstruct the post-Week-13 counts: `23, 23, 28, 43, 33, 33, 43, 53`. Tag v1.0.8 preserves the proposals as pre-outcome evidence; authoritative outcomes were appended prospectively in ledger v1.3. Adaptive sampling, sparse high-dimensional coverage, imperfect calibration, boundary estimates and unknown global optima remain explicit limitations.
