# Model Card: GP-UCB Bayesian Optimisation for the BBO Capstone

**Model name:** BBO Capstone GP-UCB Optimiser
**Type:** Sequential Bayesian optimisation with per-function Gaussian Process surrogates
**Version:** 1.7 (rolling validation, calibration, and frozen release)
**Developer:** JP Amewu
**Repository:** <https://github.com/JPAmewu/My_Capstone_1_Imperial>

## Overview

This approach proposes evaluation points for eight unknown numerical objective functions. It is not one persistent fitted model: a separate Gaussian Process is refitted for each function after every round using all confirmed observations available for that function. An acquisition function then ranks unevaluated candidate points and selects the next query.

The validated Week 12 implementation uses scikit-learn's `GaussianProcessRegressor`, a constant kernel multiplied by an anisotropic Matérn-5/2 kernel, a white-noise component, GP target normalisation, and Upper Confidence Bound (UCB) acquisition. It uses `kappa = 0.1`, three optimiser restarts, deterministic per-function random seeds, and 20,000 bounded candidate points per function. The previous `kappa = 2.0` proposals are archived for comparison.

## Intended use

The approach is suitable for:

- educational black-box optimisation where evaluations are limited or costly;
- bounded continuous search spaces with scalar objectives;
- sequential experiments where uncertainty should influence query selection;
- comparative study of manual, exploratory, exploitative, EI and UCB strategies;
- reproducible analysis of the eight capstone functions.

It should not be used as the sole decision mechanism in medical, financial, safety-critical or high-impact applications. It is not appropriate for unconstrained, categorical, strongly time-varying or adversarial objectives without substantial redesign. It should not be assumed to find a global optimum, particularly in high-dimensional or discontinuous spaces.

## Strategy and evolution across ten rounds

The optimisation strategy became progressively more systematic:

1. **Initial exploration:** starter observations were inspected through plots, descriptive statistics and manual query reasoning.
2. **Surrogate introduction:** early Gaussian Processes used RBF-style kernels and random candidate searches.
3. **Data reconstruction and validation:** uploaded arrays and returned outputs were reshaped and checked as new rounds were appended.
4. **Exploration/exploitation analysis:** manual choices were compared with GP recommendations, and dimensionality was recognised as a practical constraint.
5. **Acquisition-function expansion:** Matérn kernels and Expected Improvement were introduced.
6. **Robustness improvements:** GP target normalisation, EI/UCB comparison, and mixtures of global and local candidates were explored.
7. **Greater exploitation:** queries increasingly focused on strong observed regions, while malformed or misaligned arrays were investigated.
8. **Reusable per-function modelling:** repeated EDA and GP/UCB pipelines were applied consistently across all eight functions.
9. **Lineage repair:** query/output parsing and length mismatches were examined before producing later recommendations.
10. **Validated GP-UCB workflow:** the latest evidence-backed observation was appended to each function, unavailable returns were reported explicitly, and UCB selected the next point from 20,000 bounded candidates while excluding rounded duplicates.

Patterns from prior rounds influenced the balance between exploration and exploitation. Functions with weak or unstable recent outputs retained uncertainty-led exploration. Function 5's large positive values encouraged more exploitation. Higher-dimensional Functions 6–8 required broader uncertainty awareness because their observed points cover only a small fraction of their spaces.

## Inputs and outputs

**Input:** For Function `j`, an array `X_j` of previous points in `[0, 1]^{d_j}` and a paired vector `y_j` of observed scalar outputs.

**Output:** One new point for each function, rounded to six decimal places and formatted as a hyphen-separated submission string.

Function dimensions are:

| Function | Dimensions | Verified observations |
| --- | ---: | ---: |
| 1 | 2 | 21 |
| 2 | 2 | 21 |
| 3 | 3 | 26 |
| 4 | 4 | 41 |
| 5 | 4 | 31 |
| 6 | 5 | 31 |
| 7 | 6 | 41 |
| 8 | 8 | 51 |

## Performance

Because the true objective functions and global optima are unknown, conventional predictive accuracy is not the primary success criterion. The project uses:

- best observed objective value (best-so-far);
- improvement over the previous best;
- progression of best-so-far across rounds;
- number of objective evaluations;
- predictive mean, predictive standard deviation and acquisition value at a proposed point;
- validity checks for bounds, dimensionality, finite values and duplicate submissions.

At the corrected Week 11 state, verified best values are approximately `7.710875e-16`, `0.6112052`, `-0.03483531`, `-1.981075`, `1465.512`, `-0.7142649`, `2.149905`, and `9.939904` for Functions 1–8 respectively. These are best observed values, not proven global optima.

The canonical Week 12 notebook executed all code cells without error, verified the ledger checksum and observation counts, and generated one valid, non-duplicate, correctly dimensioned proposal for each function. A separate sensitivity appendix compares UCB at `kappa = 0.1, 0.5, 1.0, 2.0`, Expected Improvement, standard and wider GP bounds, and Sobol candidate sets for Functions 6–8. It does not modify the submitted experiment. F4's submitted recommendation is unchanged between `kappa = 0.1` and `2.0`, indicating local agreement between mean and uncertainty ranking. F7 changes substantially: the low-kappa point has higher predicted mean and lower uncertainty, whereas the high-kappa point accepts a lower mean for substantially greater uncertainty. These proposals are not observations until authoritative returns are received.

Rolling one-step-ahead validation adds 88 chronological held-out predictions
(eleven per function). Seven functions improve on a historical-mean RMSE
baseline; F2 does not. Nominal 95% interval coverage is only 72.7%, 72.7%, and
63.6% for F5, F6, and F7, respectively, so uncertainty is not uniformly
calibrated. All eight final GP fits place at least one length scale or noise
estimate at a configured bound. The full separation between optimisation
performance, surrogate calibration, and recommendation robustness is reported
in the [evaluation chapter](EVALUATION.md).

## Decision process and transparency

The process is transparent at the procedural level. The repository records:

- input and output arrays;
- appended query-output pairs;
- input bounds and expected dimensions;
- kernel construction and hyperparameter bounds;
- acquisition formula and `kappa`;
- candidate count, random seeds and six-decimal rounding;
- duplicate exclusion and validation checks;
- notebook outputs, warnings and selected query strings.

The canonical [`Results/query_output_ledger.csv`](../Results/query_output_ledger.csv) records 88 exact returned pairs recovered for Weeks 1–11, with source paths, hashes, date basis, and validation status. Its SHA-256 checksum detects unintended changes. The separate [`Results/bbo_query_ledger.csv`](../Results/bbo_query_ledger.csv) records Week 12 proposals and model diagnostics without representing them as returned observations. The superseded version 1.0 and the suspicious Week 11 arrays remain preserved as immutable historical evidence.

The full sensitivity protocol, interpretation, and limitations are documented in
the [`Week 12 sensitivity appendix`](WEEK_12_SENSITIVITY_APPENDIX.md), with its
machine-readable results kept separate from both ledgers.

Another researcher can reproduce the latest recommendations if they use the same dataset, notebook, Python dependencies and random seeds. The ledger supports deterministic reconstruction through Week 11, but unavailable Week 12–13 returns, authoritative platform submission timestamps, historical software versions and explanations of some manual interventions still prevent bit-for-bit reproduction of every original round.

The final computational stack is pinned in `requirements-lock.txt`; seeds,
canonical counts, release tag, and SHA-256 checksums are recorded in
`Results/submission_manifest.json`. The annotated tag `capstone-final-v1.0.3`
identifies the frozen repository version.

## Assumptions

The approach assumes that:

- each objective is stationary during the project;
- nearby inputs tend to have related outputs, making a Matérn GP useful;
- observations are exact or contain only modest noise;
- all valid inputs lie within `[0, 1]^d`;
- the accumulated arrays preserve correct query-output pairing;
- a uniformly generated candidate set provides adequate coverage;
- six-decimal rounding is compatible with the evaluation platform;
- maximising UCB with `kappa = 0.1` intentionally favours exploitation; the archived `kappa = 2.0` run provides the more exploratory comparison.

Violations can produce overconfident or misleading recommendations. Discontinuities, narrow peaks, heteroscedastic noise or incorrect pairing may be smoothed over by the surrogate.

## Limitations and failure modes

- **Curse of dimensionality:** 20,000 candidates are sparse in five to eight dimensions.
- **Sampling bias:** adaptive queries cluster near previously promising areas, leaving other regions underexplored.
- **Model misspecification:** one Matérn-family design may not represent every function.
- **Hyperparameter boundary warnings:** fitted values sometimes reach configured limits.
- **Sparse data:** observation counts are small relative to continuous search volumes.
- **Random candidate dependence:** recommendations depend on candidate generation and the chosen seed.
- **No known optimum:** absolute regret and optimality cannot be calculated.
- **Data-lineage risk:** recovered dates are source-file metadata rather than authoritative platform timestamps, and the original Week 11 arrays remain quarantined.
- **Sensitivity is diagnostic, not outcome evidence:** alternative acquisition settings and GP bounds have now been compared under one deterministic protocol, but none can be ranked by realised performance until authoritative returns exist.

Potential failures include repeated focus on a local optimum, missing narrow boundary peaks, overexploration of uncertain but unproductive areas or propagating an incorrectly paired observation into later rounds.

## Ethical considerations

The capstone contains no personal or demographic data, so conventional group-fairness analysis is not directly applicable. The relevant ethical duties are accurate provenance, honest reporting of uncertainty, avoidance of overstated optimality and reproducibility. A technically valid query can still be misleading if undocumented reconstruction decisions or suspicious values are concealed.

Transparency supports responsible adaptation by allowing reviewers to inspect assumptions, reproduce query generation, identify sampling bias and decide whether a different domain requires stronger safeguards. If adapted to real-world high-stakes optimisation, the approach would require domain-specific harm analysis, human oversight, constraints on unsafe experiments, audit logs, subgroup or distributional evaluation where people are affected and clear responsibility for deployment decisions.

## Recommended improvements

1. Append future confirmed pairs to the immutable ledger with authoritative timestamps and provenance; never alter an existing published row.
2. Recover missing returned pairs only from authoritative platform records.
3. Extend the sensitivity appendix to multiple kernels and repeated seeds.
4. Retain Sobol or Latin-hypercube designs for high-dimensional candidate coverage and compare them with multi-start continuous acquisition optimisation.
5. Evaluate calibration, sensitivity and cumulative/best-so-far regret when a reference optimum becomes available.
6. Track fitted kernels, acquisition scores and reasons for manual overrides.
7. Add automated lineage and array-validation tests.

## Distribution and maintenance

The notebook, data and documentation are maintained by JP Amewu in the public GitHub repository. No explicit software or model licence was found when this card was prepared; reuse therefore requires permission unless a licence is added. Updates should increment the version, state the dataset round and record material changes to data, kernels, acquisition settings or limitations.
