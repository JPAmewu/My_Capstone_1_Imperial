# Final findings

These four findings answer the capstone FAQ explicitly. They separate realised optimisation performance, surrogate quality, recommendation robustness, and data integrity so that a predicted query is never presented as a returned result.

## Finding 1 — Optimisation performance

Ten of the 96 verified weekly returns established a new within-function incumbent, an observed improvement rate of 10.4%. The first five occurred for F8 in Weeks 1 and 2, F4 and F7 in Week 3, and F5 in Week 8. Week 12 added five improvements: F3 (`+0.012206`), F4 (`+2.351050`), F5 (`+2081.120`), F6 (`+0.176443`), and F7 (`+0.116896`). The final recorded maxima are incumbents rather than proven global optima; Week 13 remains proposal-only.

## Finding 2 — Surrogate accuracy and uncertainty calibration

Rolling one-step-ahead validation produced 96 chronological folds, twelve per function. All eight Gaussian Processes achieved positive RMSE skill relative to a historical-mean baseline. Calibration varied materially: nominal 95% coverage was 66.7% for F5 and F7, 75.0% for F6, and 83.3% for F4, whereas F1, F2, and F8 covered all folds. Predictive means and intervals are useful diagnostic evidence but should not be treated as equally reliable across functions.

## Finding 3 — Recommendation robustness and exploration–exploitation

The sole canonical Week 13 methodology compares UCB, EI, and PI and then applies a function-specific policy: UCB for F1/F4/F7/F8, EI for F2/F5/F6, and PI for F3. The reasons were recorded after observing Week 12 and before any Week 13 outcomes. This adaptive policy is heuristic, not a randomised or statistically controlled acquisition comparison, so no acquisition rule is declared a winner.

## Finding 4 — Data lineage, reproducibility, and limitation

The most consequential methodological result was recovery from a data-lineage failure. Starter arrays plus an immutable 96-row query/output ledger reconstruct the post-Week-12 counts: `22, 22, 27, 42, 32, 32, 42, 52`. Week 13 proposals remain separate from observations until authoritative returns exist. Checksums, fixed seeds, exact dependencies, strict portal formatting, dataset-size checks, and rolling validation make the analysis auditable. The remaining limitations—adaptive sampling, sparse high-dimensional coverage, missing Week 13 returns, and unknown global optima—are explicit.
