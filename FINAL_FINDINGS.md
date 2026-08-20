# Final findings

These four findings answer the capstone FAQ explicitly. They separate realised optimisation performance, surrogate quality, recommendation robustness, and data integrity so that a predicted query is never presented as a returned result.

## Finding 1 — Optimisation performance

Five of the 88 verified weekly returns established a new within-function incumbent, an observed improvement rate of 5.7%. The improvements occurred for F8 in Weeks 1 and 2, F4 and F7 in Week 3, and F5 in Week 8. The other returns were still informative because they reduced uncertainty or ruled out regions. The final recorded maxima are incumbents rather than proven global optima: the analytical functions and true optima are unknown, and no Week 12 returns are available.

## Finding 2 — Surrogate accuracy and uncertainty calibration

Rolling one-step-ahead validation produced 88 leakage-free historical folds. Seven of eight Gaussian Processes achieved positive RMSE skill relative to a historical-mean baseline; F2 did not. Calibration varied materially. F5–F7 under-covered at the nominal 95% level, with F7 covering only 63.6%, whereas F1 and F8 covered all folds and were conservative. Consequently, predictive means and intervals are useful diagnostic evidence but should not be treated as equally reliable across functions.

## Finding 3 — Recommendation robustness and exploration–exploitation

The submitted Week 12 method uses GP-UCB with `kappa = 0.1`, deliberately prioritising exploitation. The sensitivity appendix compares kappa values `0.1`, `0.5`, `1.0`, and `2.0`, Expected Improvement, standard and wider GP bounds, and Sobol candidates for F6–F8. F4 and F5 remain stable across every setting. F7 provides the clearest exploration example: high kappa gives substantially more weight to uncertainty than low kappa. Without Week 12 returns, robustness can be assessed but no acquisition rule can be declared the realised winner.

## Finding 4 — Data lineage, reproducibility, and limitation

The most consequential methodological result was recovery from a data-lineage failure. Starter arrays plus an immutable 88-row query/output ledger reconstruct the correct post-Week-11 counts: `21, 21, 26, 41, 31, 31, 41, 51`. Proposals remain separate from observations until an authoritative return exists. Checksums, fixed seeds, exact dependencies, strict portal formatting, dataset-size checks, rolling validation, and a frozen Git tag make the final analysis auditable. The remaining limitations—adaptive sampling, sparse high-dimensional coverage, missing Week 12 returns, and unknown global optima—are explicit rather than imputed away.
