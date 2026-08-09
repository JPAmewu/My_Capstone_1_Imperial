# Model Card: GP-UCB Bayesian Optimisation for the BBO Capstone

**Model name:** BBO Capstone GP-UCB Optimiser  
**Type:** Sequential Bayesian optimisation with per-function Gaussian Process surrogates  
**Version:** 1.0 (ten-round/Week 11 data state)  
**Developer:** JP Amewu  
**Repository:** <https://github.com/JPAmewu/My_Capstone_1_Imperial>

## Overview

This approach proposes evaluation points for eight unknown numerical objective functions. It is not one persistent fitted model: a separate Gaussian Process is refitted for each function after every round using all confirmed observations available for that function. An acquisition function then ranks unevaluated candidate points and selects the next query.

The current implementation uses scikit-learn's `GaussianProcessRegressor`, a constant kernel multiplied by an anisotropic Matérn-5/2 kernel, a white-noise component and Upper Confidence Bound (UCB) acquisition. The tenth-round implementation uses `kappa = 2.0`, ten optimiser restarts, deterministic random seeds and 100,000 uniform candidate points per function.

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
6. **Robustness improvements:** output scaling, EI/UCB comparison and mixtures of global and local candidates were explored.
7. **Greater exploitation:** queries increasingly focused on strong observed regions, while malformed or misaligned arrays were investigated.
8. **Reusable per-function modelling:** repeated EDA and GP/UCB pipelines were applied consistently across all eight functions.
9. **Lineage repair:** query/output parsing and length mismatches were examined before producing later recommendations.
10. **Validated GP-UCB workflow:** the confirmed latest observation was appended to each function, the Week 11 dataset was created, and UCB selected the next point from 100,000 bounded candidates while excluding rounded duplicates.

Patterns from prior rounds influenced the balance between exploration and exploitation. Functions with weak or unstable recent outputs retained uncertainty-led exploration. Function 5's large positive values encouraged more exploitation. Higher-dimensional Functions 6–8 required broader uncertainty awareness because their observed points cover only a small fraction of their spaces.

## Inputs and outputs

**Input:** For Function `j`, an array `X_j` of previous points in `[0, 1]^{d_j}` and a paired vector `y_j` of observed scalar outputs.

**Output:** One new point for each function, rounded to six decimal places and formatted as a hyphen-separated submission string.

Function dimensions are:

| Function | Dimensions | Week 11 observations |
| --- | ---: | ---: |
| 1 | 2 | 20 |
| 2 | 2 | 20 |
| 3 | 3 | 25 |
| 4 | 4 | 40 |
| 5 | 4 | 30 |
| 6 | 5 | 30 |
| 7 | 6 | 40 |
| 8 | 8 | 49 |

## Performance

Because the true objective functions and global optima are unknown, conventional predictive accuracy is not the primary success criterion. The project uses:

- best observed objective value (best-so-far);
- improvement over the previous best;
- progression of best-so-far across rounds;
- number of objective evaluations;
- predictive mean, predictive standard deviation and acquisition value at a proposed point;
- validity checks for bounds, dimensionality, finite values and duplicate submissions.

At the Week 11 dataset state, raw recorded maxima are `64` for Functions 1–4 and 6–8, and `1088.8596182` for Function 5. These values should be interpreted cautiously: repeated exact values of `64` across multiple functions require provenance review and must not be presented as verified global optima. The most recently appended outputs were approximately `0`, `0.0494064`, `-0.0818934`, `-23.4228031`, `430.8031250`, `-1.1717132`, `1.0098940` and `9.6998918` for Functions 1–8 respectively.

The tenth-round notebook executed all 27 code cells without error and generated one valid, non-duplicate, correctly dimensioned query for each function. GP optimisation emitted convergence warnings for some kernel parameters reaching specified bounds. These warnings are useful performance diagnostics rather than proof of failure, but they indicate that kernel choices and bounds merit sensitivity testing.

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

Another researcher can reproduce the latest recommendations if they use the same dataset, notebook, Python dependencies and random seeds. Full reconstruction of every earlier decision additionally requires the immutable round-by-round query ledger, returned outputs, exact software versions and explanations of any manual interventions. Adding those details would materially improve the card; the current structure is sufficient to describe the method, but not to guarantee bit-for-bit reproduction of every historical round.

## Assumptions

The approach assumes that:

- each objective is stationary during the project;
- nearby inputs tend to have related outputs, making a Matérn GP useful;
- observations are exact or contain only modest noise;
- all valid inputs lie within `[0, 1]^d`;
- the accumulated arrays preserve correct query-output pairing;
- a uniformly generated candidate set provides adequate coverage;
- six-decimal rounding is compatible with the evaluation platform;
- maximising UCB with `kappa = 2.0` provides an acceptable exploration/exploitation balance.

Violations can produce overconfident or misleading recommendations. Discontinuities, narrow peaks, heteroscedastic noise or incorrect pairing may be smoothed over by the surrogate.

## Limitations and failure modes

- **Curse of dimensionality:** 100,000 candidates are sparse in five to eight dimensions.
- **Sampling bias:** adaptive queries cluster near previously promising areas, leaving other regions underexplored.
- **Model misspecification:** one Matérn-family design may not represent every function.
- **Hyperparameter boundary warnings:** fitted values sometimes reach configured limits.
- **Sparse data:** observation counts are small relative to continuous search volumes.
- **Random candidate dependence:** recommendations depend on candidate generation and the chosen seed.
- **No known optimum:** absolute regret and optimality cannot be calculated.
- **Data-lineage risk:** early reconstruction steps and repeated `64` values require audit.
- **Limited robustness evaluation:** alternative kernels, acquisition functions and seeds have not been systematically compared under a common protocol.

Potential failures include repeated focus on a local optimum, missing narrow boundary peaks, overexploration of uncertain but unproductive areas or propagating an incorrectly paired observation into later rounds.

## Ethical considerations

The capstone contains no personal or demographic data, so conventional group-fairness analysis is not directly applicable. The relevant ethical duties are accurate provenance, honest reporting of uncertainty, avoidance of overstated optimality and reproducibility. A technically valid query can still be misleading if undocumented reconstruction decisions or suspicious values are concealed.

Transparency supports responsible adaptation by allowing reviewers to inspect assumptions, reproduce query generation, identify sampling bias and decide whether a different domain requires stronger safeguards. If adapted to real-world high-stakes optimisation, the approach would require domain-specific harm analysis, human oversight, constraints on unsafe experiments, audit logs, subgroup or distributional evaluation where people are affected and clear responsibility for deployment decisions.

## Recommended improvements

1. Preserve an immutable round-by-round ledger with timestamps and provenance.
2. Audit repeated `64` outputs against original platform responses.
3. Compare multiple kernels and acquisition functions using repeated seeds.
4. Replace uniform random candidates with Sobol/Latin hypercube designs or multi-start continuous acquisition optimisation.
5. Evaluate calibration, sensitivity and cumulative/best-so-far regret when a reference optimum becomes available.
6. Track fitted kernels, acquisition scores and reasons for manual overrides.
7. Add automated lineage and array-validation tests.

## Distribution and maintenance

The notebook, data and documentation are maintained by JP Amewu in the public GitHub repository. No explicit software or model licence was found when this card was prepared; reuse therefore requires permission unless a licence is added. Updates should increment the version, state the dataset round and record material changes to data, kernels, acquisition settings or limitations.
