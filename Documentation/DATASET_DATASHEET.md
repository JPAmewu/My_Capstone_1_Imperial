# Datasheet: BBO capstone sequential optimisation dataset

**Version:** 1.5 (function-level descriptions and frozen release)
**Creator and maintainer:** JP Amewu
**Programme:** Imperial College London Machine Learning and Artificial Intelligence Programme
**Repository:** <https://github.com/JPAmewu/My_Capstone_1_Imperial>

## Motivation

This dataset was created to support a capstone investigation of Bayesian optimisation for expensive, unknown black-box objective functions. The practical task is to maximise eight functions while using as few objective-function evaluations as possible. Each observation therefore has two linked components: a submitted query point and the scalar value returned by the corresponding black box.

The dataset supports sequential optimisation, exploratory data analysis, Gaussian Process (GP) surrogate modelling, acquisition-function comparison and critical reflection on exploration, exploitation, transparency and reproducibility. It was created by JP Amewu as programme coursework. No external commercial funding is known or claimed.

## Data description

### Unit of analysis and relationships

| Description item | Recorded definition |
| --- | --- |
| Functions | Eight independent numerical black-box functions, labelled F1–F8 |
| Analytical form | Unknown; the true functions and global optima are not available |
| Optimisation objective | Maximise the scalar output independently for each function |
| Input domain | Unit hypercube `[0, 1]^d` |
| Fundamental observed unit | One query/return pair for one function and round |
| Query | One `d`-dimensional input vector submitted to a function |
| Return | One scalar objective produced for that exact query |
| Recovered weekly key | `(week, function)` |
| Sampling design | Sequential and adaptive: later queries depend on earlier returns |
| Starter evidence | Initial aligned input/output arrays for each function |
| Historical evidence | One verified returned pair per function for Weeks 1–11 |
| Reconstructed state | Starter pairs plus immutable-ledger pairs through Week 11 |
| Week 12 evidence | Eight model proposals with diagnostics; returned outputs unavailable |
| Observation rule | A proposal is not an observation until its authoritative return is recorded |

### Principal data assets

| Asset | Grain and size | Description |
| --- | --- | --- |
| `Week_01/Function_XX/03_Data/initial_inputs.npy` | One row per starter query; 2–8 coordinate columns | Canonical initial input vectors for one function |
| `Week_01/Function_XX/03_Data/initial_outputs.npy` | One scalar per starter query | Objective returns aligned row-for-row with starter inputs |
| [`Results/query_output_ledger.csv`](../Results/query_output_ledger.csv) | 88 rows; one `(week, function)` pair for Weeks 1–11 | Append-only recovered queries and returned outputs |
| [`Results/bbo_query_ledger.csv`](../Results/bbo_query_ledger.csv) | 8 rows; one Week 12 proposal per function | Query recommendations and GP diagnostics; no returned objectives |
| [`Results/performance_summary_weeks_01_to_13.csv`](../Results/performance_summary_weeks_01_to_13.csv) | One row per week and function | Derived best-so-far and evidence-status trajectory |
| [`Results/gp_rolling_validation_predictions.csv`](../Results/gp_rolling_validation_predictions.csv) | 88 rows; one chronological held-out prediction per recovered pair | Derived GP accuracy, uncertainty, calibration, and fitted-fold diagnostics |
| [`Results/gp_final_hyperparameters.csv`](../Results/gp_final_hyperparameters.csv) | 8 rows; one final fit per function | Derived constants, length scales, noise estimates, warnings, and bound hits |
| [`Results/week12_sensitivity_analysis.csv`](../Results/week12_sensitivity_analysis.csv) | 80 rows; function × bound profile × strategy | Non-submission recommendation-robustness experiment |

| Asset class | Evidence status | Permitted interpretation |
| --- | --- | --- |
| Starter input/output arrays | Observed evidence | Initial aligned query/return pairs |
| Canonical returned-pair ledger | Observed evidence | Verified historical returns that may update cumulative arrays |
| Week 12 proposal ledger | Proposal evidence | Recommendations and model diagnostics only; must not update observed outputs |
| Performance summaries | Derived analysis | Best-so-far and improvement calculations from observed evidence |
| GP validation and hyperparameter files | Derived analysis | Surrogate diagnostics; not additional black-box observations |
| Sensitivity analysis | Derived, non-submission experiment | Recommendation robustness under alternative settings |

### Canonical returned-pair ledger fields

| Field | Type | Meaning |
| --- | --- | --- |
| `week` | integer | Sequential return round, 1–11 |
| `function` | integer | Function identifier, 1–8 |
| `query` | encoded numeric vector | Exact submitted coordinates in dimension order |
| `returned_output` | float | Scalar objective paired with the query |
| `dataset_version` | string | Version label assigned during recovery |
| `submission_date` | date-like string | Source-file date, not guaranteed platform submission time |
| `date_basis` | categorical string | Explains how the date was obtained |
| `notebook`, `commit_sha` | strings | Notebook and repository provenance where available |
| `evidence_status` | categorical string | Validation state of the recovered pair |
| `source_registry`, `source_input`, `source_output` | paths/identifiers | Evidence used to reconstruct and verify the row |
| `source_input_sha256`, `source_output_sha256` | hexadecimal strings | Byte-integrity hashes for source arrays |
| `duplicate_of` | nullable identifier | Reference if a row duplicates earlier evidence |

### Week 12 proposal fields

| Field group | Fields | Meaning |
| --- | --- | --- |
| Identity and shape | `week`, `function`, `dimensions`, `observation_count` | Proposal round and cumulative training-data shape |
| Query | `query`, `submission_query` | Numeric vector and six-decimal submission form |
| GP prediction | `predicted_mean`, `predictive_std`, `kernel` | Surrogate diagnostics at the candidate |
| Acquisition | `ucb_score`, `kappa`, `candidate_count` | UCB setting and finite candidate-search details |
| Reproducibility | `random_seed`, `duplicate_at_6dp` | Seed and submission-precision collision check |
| Evidence boundary | `status` | Marks the row as a proposal rather than an observation |

### Shapes, counts, and data types

| Property | Value | Interpretation or rule |
| --- | --- | --- |
| Input type | Floating-point numeric | Every coordinate must be finite and within `[0, 1]` |
| Input shape | `(n, d)` | `n` aligned observations and `d` function-specific dimensions |
| Output type | Floating-point scalar | One objective value per input row |
| Accepted raw output shapes | `(n,)` or `(n, 1)` | Validation standardises outputs to a one-dimensional vector |
| Function dimensions F1–F8 | `2, 2, 3, 4, 4, 5, 6, 8` | Dimension order is fixed by function identifier |
| Starter observations | 175 | Canonical Week 1 input/output pairs across all functions |
| Recovered weekly observations | 88 | Eight verified pairs per week for Weeks 1–11 |
| Total observations after Week 11 | 263 | 175 starter pairs plus 88 recovered pairs |
| Counts by function F1–F8 | `21, 21, 26, 41, 31, 31, 41, 51` | Required canonical reconstruction counts |
| Week 12 proposals | 8 | One proposal per function; zero verified Week 12 returns |
| Objective scale | Function-specific | Raw outputs may be compared within a function, not ranked or averaged across functions |

## Composition

The verified project state covers eight independent objective functions with inputs constrained to the unit hypercube `[0, 1]^d`. Function dimensionalities are 2, 2, 3, 4, 4, 5, 6 and 8 respectively.

The corrected Week 11 analysis contains 263 verified paired observations. It
uses the Week 1 starter arrays plus one exact returned pair per function for
each of Weeks 1–11, recovered from aligned cumulative archive snapshots.

The descriptions below summarise observed response and modelling behaviour in the project evidence. They are empirical descriptions, not claims about the unknown analytical forms of the black-box functions.

| Function | Description | Dimensions | Verified observations | Verified maximum | Latest verified output |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | Two-dimensional, near-zero-scale objective; observed responses are highly compressed and the recommendation is sensitive to acquisition weight and GP bounds. | 2 | 21 | `7.710875e-16` | `8.159220e-130` |
| 2 | Two-dimensional objective with a recurring first-coordinate region near 0.69–0.70; the second coordinate is less stable, suggesting ridge-like behaviour. | 2 | 21 | `0.6112052` | `0.06529973` |
| 3 | Three-dimensional, predominantly negative objective; the best observed region is narrow and recommendations are sensitive to GP hyperparameter bounds. | 3 | 26 | `-0.03483531` | `-0.03844613` |
| 4 | Four-dimensional, negative-valued objective; the preferred local region is unusually stable across kappa, Expected Improvement and GP-bound settings. | 4 | 41 | `-1.981075` | `-14.99267` |
| 5 | Four-dimensional, positive large-scale objective with a strong boundary-associated incumbent; the recommendation is locally robust across sensitivity settings. | 4 | 31 | `1465.512` | `210.0383` |
| 6 | Five-dimensional, negative-valued objective with sparse coverage; increasing exploration weight moves the recommendation through several distinct candidates. | 5 | 31 | `-0.7142649` | `-1.154424` |
| 7 | Six-dimensional positive objective with a recurring promising region; low kappa favours higher predicted mean while high kappa moves towards greater uncertainty. | 6 | 41 | `2.149905` | `1.478174` |
| 8 | Eight-dimensional positive objective with sparse high-dimensional coverage; recommendations depend on acquisition weight and GP-bound specification. | 8 | 51 | `9.939904` | `9.276069` |

Inputs and outputs are stored as NumPy `.npy` arrays. Query submissions are stored as plain-text `.txt` files, normally with six-decimal coordinates separated by hyphens. Jupyter/Colab `.ipynb` notebooks contain collection logic, validation, analysis, modelling and generated query points. Some weekly directories also contain Markdown documentation and placeholders.

The canonical append-only ledger is [`Results/query_output_ledger.csv`](../Results/query_output_ledger.csv). Version 1.1 contains 88 exact query/output pairs for all eight functions in Weeks 1–11. Each row records source paths and hashes, validation status, and the source-file date. [`Results/query_output_ledger.sha256`](../Results/query_output_ledger.sha256) provides a content-integrity checksum. The superseded version 1.0 remains immutable under `Results/archive/`. Dates are filesystem metadata and are not claimed as authoritative platform submission timestamps.

There are no human subjects, demographic groups, personal data or labels describing people. The outputs are numerical objective values rather than conventional supervised-learning class labels. A fixed train/test split is not recommended because observations are collected sequentially and every confirmed observation is used to update the surrogate.

### Known gaps and integrity concerns

- The immutable ledger covers the 88 exact pairs supported by the archive for Weeks 1–11; returns for Weeks 12–13 remain unavailable.
- Exact collection timestamps and software versions were not recorded for every observation.
- Week 12 is an executed proposal round with no verified returned outputs; only Week 13 remains a placeholder.
- The original Week 11 repository arrays failed provenance reconciliation and remain hash-recorded, quarantined historical evidence; reconstructed arrays are generated only from starter data plus the ledger.
- Sampling is sparse relative to the volume of the higher-dimensional search spaces.
- Earlier notebook versions sometimes reconstructed arrays from uploaded text and could encounter input/output length mismatches. Later validation stops rather than silently truncating data.

## Collection process

Data was accumulated through sequential optimisation rounds during the 2026 capstone project. In each round, one query was proposed for each of the eight functions, submitted to the programme's black-box evaluation platform and paired with the returned scalar output. Only pairs supported by repository evidence are included in the corrected analyses.

The strategy evolved across rounds:

1. Early rounds used exploratory analysis, plotting and manual heuristics.
2. Gaussian Process regression was introduced to estimate objective values and predictive uncertainty.
3. RBF and later Matérn kernels were used; corrected GP fits use `normalize_y=True` rather than manual target scaling.
4. Expected Improvement and Upper Confidence Bound (UCB) acquisition functions were explored.
5. Later rounds increasingly used UCB to balance exploitation of predicted high-value regions with exploration of uncertain regions.
6. The corrected later workflows use anisotropic Matérn GPs, deterministic seeds, bounded candidate generation, and duplicate exclusion after six-decimal rounding. Candidate counts are recorded in each notebook rather than assumed to be identical across weeks.

The process is adaptive, not an independent random sample: later query locations depend on earlier observations and modelling choices. This creates deliberate concentration near apparently promising regions and can leave other regions underexplored.

## Preprocessing, cleaning and labelling

The following processing has been applied in later notebooks:

- conversion to floating-point NumPy arrays;
- reshaping inputs to `(n, d)` and outputs to `(n, 1)` or `(n,)`;
- exact filename matching for each function's input and output arrays;
- checks for matching input/output counts, expected dimensionality, finite values and `[0, 1]` input bounds;
- preservation of source datasets while writing derived weekly datasets separately;
- GP target normalisation with `normalize_y=True` in corrected notebooks;
- rounding submitted coordinates to six decimal places;
- exclusion of duplicate candidate points at submission precision.

No missing-value imputation is used. A failed structural validation should stop processing and trigger comparison with the original query history. Raw weekly data should be retained alongside processed weekly arrays whenever available.

## Intended uses

Appropriate uses include:

- reproducing the capstone's sequential black-box optimisation experiments;
- comparing acquisition functions or GP kernels on the same observation history;
- studying exploration/exploitation decisions and sampling bias;
- teaching Bayesian optimisation, uncertainty-aware modelling and reproducible experimentation;
- auditing how query histories were constructed.

Inappropriate uses include:

- claiming that the recorded maxima are proven global optima;
- treating the adaptively sampled observations as an unbiased representation of each full function;
- benchmarking unrelated optimisation methods without controlling for the inherited query history;
- using the data for safety-critical, medical, financial or operational decisions;
- inferring real-world human behaviour or demographic effects;
- training a generally applicable predictor without additional data and validation.

## Distribution and terms of use

The dataset and notebooks are intended to be distributed through the public GitHub repository listed above. Files are versioned with Git. No API or paid distribution channel is provided.

No explicit licence file was found in the repository when this datasheet was prepared. Consequently, public visibility should not be interpreted as permission for unrestricted reuse. Copyright remains with the repository owner unless a licence is added. Users should cite the repository and comply with Imperial College London and Emeritus programme rules, including any restrictions on sharing assessment materials or black-box outputs.

## Maintenance

JP Amewu maintains the dataset. Maintenance should include:

- appending only confirmed query-output pairs;
- treating existing rows in `Results/query_output_ledger.csv` as immutable and verifying its SHA-256 checksum;
- preserving immutable copies of each previous week's dataset;
- recording provenance, submission round, timestamp and code version for every new observation;
- validating shape, bounds, finiteness and duplicates before publication;
- preserving explicit evidence-gap reporting for unavailable returned pairs;
- retaining Week 12 as an executed proposal round while clearly marking its returned outputs unavailable, and replacing only the Week 13 placeholder when genuine evidence becomes available;
- documenting corrections in Git history and this datasheet;
- archiving a final version when the capstone concludes.

Issues and corrections should be reported through the repository's GitHub issue tracker or directly to the repository owner.
