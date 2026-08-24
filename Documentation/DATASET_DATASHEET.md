# Datasheet: BBO capstone sequential optimisation dataset

**Version:** 1.7 (portal bounds, size audit, and frozen release)
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
| Observed-data domain | Unit hypercube `[0, 1]^d`; source observations may include the endpoint `1.0` |
| Submission domain | `[0.000000, 0.999999]^d` after six-decimal rounding, matching the portal constraint |
| Fundamental observed unit | One query/return pair for one function and round |
| Query | One `d`-dimensional input vector submitted to a function |
| Return | One scalar objective produced for that exact query |
| Recovered weekly key | `(week, function)` |
| Sampling design | Sequential and adaptive: later queries depend on earlier returns |
| Starter evidence | Initial aligned input/output arrays for each function |
| Historical evidence | One verified returned pair per function for Weeks 1–13 |
| Reconstructed state | Starter pairs plus immutable-ledger pairs through Week 13 |
| Week 12 evidence | Eight reconciled model queries with verified returned outputs |
| Week 13 evidence | Eight authoritative returns matched prospectively to the frozen pre-outcome queries |
| Observation rule | A proposal is not an observation until its authoritative return is recorded |

### Function schemas and illustrative applications

The analytical forms and real-world origins of the eight functions are unknown. The examples below are therefore explanatory analogies: they show how optimisation problems with the same input dimensionality and scalar-output structure could arise in practice. They must not be interpreted as verified descriptions of the hidden functions.

| Function | Input | Output | Optimisation goal | Description of sample application |
| --- | --- | --- | --- | --- |
| Function 1 | 2D array (`n × 2`) | 1D array (`n`, one scalar per row) | Maximise | Detect likely contamination sources in a two-dimensional area, such as a radiation field, where only proximity produces a non-zero reading. Bayesian optimisation can tune detection locations or parameters to identify both strong and weak sources efficiently. |
| Function 2 | 2D array (`n × 2`) | 1D array (`n`, one scalar per row) | Maximise | Optimise a mystery machine-learning model that accepts two parameters and returns a noisy log-likelihood score. Bayesian optimisation balances exploration and exploitation to reduce the risk of becoming trapped at one of several local optima. |
| Function 3 | 3D array (`n × 3`) | 1D array (`n`, one scalar per row) | Maximise | Test combinations of three compounds in a drug-discovery experiment. If the measured quantity is adverse reactions, it can be transformed—for example, by negation—so maximising the recorded objective corresponds to minimising side effects. This is an illustrative interpretation; the repository stores only the transformed scalar response. |
| Function 4 | 4D array (`n × 4`) | 1D array (`n`, one scalar per row) | Maximise | Tune four hyperparameters of a fast surrogate used to approximate costly, biweekly warehouse product-placement calculations. A dynamic landscape with multiple local optima requires careful tuning and validation to identify reliable near-optimal settings. |
| Function 5 | 4D array (`n × 4`) | 1D array (`n`, one scalar per row) | Maximise | Optimise four chemical-process inputs to maximise factory yield. For a broadly unimodal response, systematic exploration can locate the combination near the single dominant peak while limiting expensive trials. |
| Function 6 | 5D array (`n × 5`) | 1D array (`n`, one scalar per row) | Maximise | Optimise a cake recipe using five ingredient quantities, such as flour, sugar, eggs, butter and milk. An expert score can combine flavour, consistency, calories, waste and cost as negative penalties; maximisation then seeks a total score as close to zero as possible. |
| Function 7 | 6D array (`n × 6`) | 1D array (`n`, one scalar per row) | Maximise | Tune six machine-learning hyperparameters, such as learning rate, regularisation strength and network depth, to maximise a performance score such as accuracy or F1. Prior literature can help define sensible bounds, while Bayesian optimisation searches the unknown response surface. |
| Function 8 | 8D array (`n × 8`) | 1D array (`n`, one scalar per row) | Maximise | Tune an eight-parameter system—for example, learning rate, batch size, layer count, dropout, regularisation, encoded activation, encoded optimiser and initial-weight range—to maximise performance, efficiency or validation accuracy. Because global search becomes difficult in eight dimensions, identifying strong local maxima is a practical objective. |

### Principal data assets

| Asset | Grain and size | Description |
| --- | --- | --- |
| `Week_01/Function_XX/03_Data/initial_inputs.npy` | One row per starter query; 2–8 coordinate columns | Canonical initial input vectors for one function |
| `Week_01/Function_XX/03_Data/initial_outputs.npy` | One scalar per starter query | Objective returns aligned row-for-row with starter inputs |
| [`Results/query_output_ledger.csv`](../Results/query_output_ledger.csv) | 104 rows; one `(week, function)` pair for Weeks 1–13 | Append-only verified queries and returned outputs |
| [`Week_13/04_Results/week_13_strategy_summary.csv`](../Week_13/04_Results/week_13_strategy_summary.csv) | 8 rows; one frozen Week 13 proposal per function | Pre-outcome query recommendations and GP diagnostics |
| [`Week_13/04_Results/week_13_confirmed_outcomes.csv`](../Week_13/04_Results/week_13_confirmed_outcomes.csv) | 8 rows; one Week 13 outcome per function | Prospective realised outcomes and incumbent changes |
| [`Results/performance_summary_weeks_01_to_13.csv`](../Results/performance_summary_weeks_01_to_13.csv) | One row per week and function | Derived best-so-far and evidence-status trajectory |
| [`Results/gp_rolling_validation_predictions.csv`](../Results/gp_rolling_validation_predictions.csv) | 104 rows; one chronological held-out prediction per recovered pair | Derived GP accuracy, uncertainty, calibration, and fitted-fold diagnostics |
| [`Results/gp_final_hyperparameters.csv`](../Results/gp_final_hyperparameters.csv) | 8 rows; one final fit per function | Derived constants, length scales, noise estimates, warnings, and bound hits |
| [`Results/week12_sensitivity_analysis.csv`](../Results/week12_sensitivity_analysis.csv) | 80 rows; function × bound profile × strategy | Non-submission recommendation-robustness experiment |

| Asset class | Evidence status | Permitted interpretation |
| --- | --- | --- |
| Starter input/output arrays | Observed evidence | Initial aligned query/return pairs |
| Canonical returned-pair ledger | Observed evidence | Verified historical returns that may update cumulative arrays |
| Week 13 proposal ledger | Pre-outcome proposal evidence | Recommendations and diagnostics remain immutable; outcomes are stored separately |
| Performance summaries | Derived analysis | Best-so-far and improvement calculations from observed evidence |
| GP validation and hyperparameter files | Derived analysis | Surrogate diagnostics; not additional black-box observations |
| Sensitivity analysis | Derived, non-submission experiment | Recommendation robustness under alternative settings |

### Canonical returned-pair ledger fields

| Field | Type | Meaning |
| --- | --- | --- |
| `week` | integer | Sequential return round, 1–13 |
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

### Week 13 proposal fields

| Field group | Fields | Meaning |
| --- | --- | --- |
| Identity and shape | `week`, `function`, `dimensions`, `observation_count` | Proposal round and cumulative training-data shape |
| Query | `query`, `submission_query` | Numeric vector and strict six-decimal, hyphen-separated submission form |
| GP prediction | `predicted_mean`, `predictive_std`, `kernel` | Surrogate diagnostics at the candidate |
| Acquisition policy | `method`, `selected_acquisition`, `kappa`, `xi`, `xi_fraction_of_output_std` | Function-specific UCB, EI, or PI choice and its method-appropriate score and parameters |
| Candidate search | `candidate_source`, `candidate_count`, `local_scale` | Finite global or local candidate-search design |
| Reproducibility | `random_seed`, `duplicate_at_6dp` | Seed and submission-precision collision check |
| Evidence boundary | `status` | Marks the row as a proposal rather than an observation |

### Shapes, counts, and data types

| Property | Value | Interpretation or rule |
| --- | --- | --- |
| Observed-input type | Floating-point numeric | Every historical coordinate must be finite and within `[0, 1]` |
| New submission input | Floating-point numeric | Every proposed coordinate must be within `[0.000000, 0.999999]` after rounding |
| Input shape | `(n, d)` | `n` aligned observations and `d` function-specific dimensions |
| Output type | Floating-point scalar | One objective value per input row |
| Accepted raw output shapes | `(n,)` or `(n, 1)` | Validation standardises outputs to a one-dimensional vector |
| Function dimensions F1–F8 | `2, 2, 3, 4, 4, 5, 6, 8` | Dimension order is fixed by function identifier |
| Starter observations | 175 | Canonical Week 1 input/output pairs across all functions |
| Recovered weekly observations | 104 | Eight verified pairs per week for Weeks 1–13 |
| Total observations after Week 13 | 279 | 175 starter pairs plus 104 recovered pairs |
| Counts by function F1–F8 | `23, 23, 28, 43, 33, 33, 43, 53` | Required canonical reconstruction counts |
| Week 13 proposals and returns | 8 each | Frozen proposals followed by prospectively appended returns |
| Objective scale | Function-specific | Raw outputs may be compared within a function, not ranked or averaged across functions |

## Composition

The verified project state covers eight independent objective functions with inputs constrained to the unit hypercube `[0, 1]^d`. Function dimensionalities are 2, 2, 3, 4, 4, 5, 6 and 8 respectively.

The corrected Week 13 analysis contains 279 verified paired observations. It
uses the Week 1 starter arrays plus one exact returned pair per function for
each of Weeks 1–13, recovered from aligned cumulative archive snapshots.

| Function | Dimensions | Verified observations | Verified maximum | Latest verified output |
| --- | ---: | ---: | ---: | ---: |
| 1 | 2 | 23 | `7.710875e-16` | `-4.447271e-102` |
| 2 | 2 | 23 | `0.6112052` | `0.5566816` |
| 3 | 3 | 28 | `-0.02262932` | `-0.02958929` |
| 4 | 4 | 43 | `0.3699753` | `-0.8263105` |
| 5 | 4 | 33 | `4440.562` | `4440.562` |
| 6 | 5 | 33 | `-0.4059929` | `-0.4059929` |
| 7 | 6 | 43 | `2.266802` | `1.961320` |
| 8 | 8 | 53 | `9.939904` | `9.653468` |
The descriptions below summarise observed response and modelling behaviour in the project evidence. They are empirical descriptions, not claims about the unknown analytical forms of the black-box functions.

| Function | Description | Dimensions | Verified observations | Verified maximum | Latest verified output |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | Two-dimensional, near-zero-scale objective; observed responses are highly compressed and the recommendation is sensitive to acquisition weight and GP bounds. | 2 | 23 | `7.710875e-16` | `-4.447271e-102` |
| 2 | Two-dimensional objective with a recurring first-coordinate region near 0.69–0.70; the second coordinate is less stable, suggesting ridge-like behaviour. | 2 | 23 | `0.6112052` | `0.5566816` |
| 3 | Three-dimensional, predominantly negative objective; the best observed region is narrow and recommendations are sensitive to GP hyperparameter bounds. | 3 | 28 | `-0.02262932` | `-0.02958929` |
| 4 | Four-dimensional objective with a Week 12 incumbent improvement. | 4 | 43 | `0.3699753` | `-0.8263105` |
| 5 | Four-dimensional, positive large-scale objective with a strong boundary-associated incumbent improved again in Week 13. | 4 | 33 | `4440.562` | `4440.562` |
| 6 | Five-dimensional, negative-valued objective with sparse coverage and a Week 13 incumbent improvement. | 5 | 33 | `-0.4059929` | `-0.4059929` |
| 7 | Six-dimensional positive objective with a recurring promising region. | 6 | 43 | `2.266802` | `1.961320` |
| 8 | Eight-dimensional positive objective with sparse high-dimensional coverage. | 8 | 53 | `9.939904` | `9.653468` |

Inputs and outputs are stored as NumPy `.npy` arrays. Query submissions are stored as plain-text `.txt` files with exactly six decimal places per coordinate, hyphen separators, and values in `[0.000000, 0.999999]`. Jupyter/Colab `.ipynb` notebooks contain collection logic, validation, analysis, modelling and generated query points. Some weekly directories also contain Markdown documentation and placeholders.

The canonical append-only ledger is [`Results/query_output_ledger.csv`](../Results/query_output_ledger.csv). Version 1.3 contains 104 exact query/output pairs for all eight functions in Weeks 1–13. Each row records source paths and hashes, validation status, and the source-file date. [`Results/query_output_ledger.sha256`](../Results/query_output_ledger.sha256) provides a content-integrity checksum. Superseded versions remain immutable under `Results/archive/`. Dates are filesystem metadata and are not claimed as authoritative platform submission timestamps.

There are no human subjects, demographic groups, personal data or labels describing people. The outputs are numerical objective values rather than conventional supervised-learning class labels. A fixed train/test split is not recommended because observations are collected sequentially and every confirmed observation is used to update the surrogate.

### Known gaps and integrity concerns

- The immutable ledger covers 104 exact pairs through Week 13; raw Week 13 source files and validation hashes are preserved.
- Exact collection timestamps and software versions were not recorded for every observation.
- Week 13 proposals remain preserved as pre-outcome evidence and the round is now complete.
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
- appending Week 13 outputs only after exact reconciliation with its submitted queries;
- preserving the frozen Week 13 proposals and acquisition rationales as pre-outcome evidence, separately from the prospectively appended returns;
- documenting corrections in Git history and this datasheet;
- archiving a final version when the capstone concludes.

Issues and corrections should be reported through the repository's GitHub issue tracker or directly to the repository owner.
