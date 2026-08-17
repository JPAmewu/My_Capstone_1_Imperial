# Datasheet: BBO capstone sequential optimisation dataset

**Version:** 1.3 (archive-reconciled ledger)
**Creator and maintainer:** JP Amewu
**Programme:** Imperial College London Machine Learning and Artificial Intelligence Programme
**Repository:** <https://github.com/JPAmewu/My_Capstone_1_Imperial>

## Motivation

This dataset was created to support a capstone investigation of Bayesian optimisation for expensive, unknown black-box objective functions. The practical task is to maximise eight functions while using as few objective-function evaluations as possible. Each observation therefore has two linked components: a submitted query point and the scalar value returned by the corresponding black box.

The dataset supports sequential optimisation, exploratory data analysis, Gaussian Process (GP) surrogate modelling, acquisition-function comparison and critical reflection on exploration, exploitation, transparency and reproducibility. It was created by JP Amewu as programme coursework. No external commercial funding is known or claimed.

## Composition

The verified project state covers eight independent objective functions with inputs constrained to the unit hypercube `[0, 1]^d`. Function dimensionalities are 2, 2, 3, 4, 4, 5, 6 and 8 respectively.

The corrected Week 11 analysis contains 263 verified paired observations. It
uses the Week 1 starter arrays plus one exact returned pair per function for
each of Weeks 1–11, recovered from aligned cumulative archive snapshots.

| Function | Dimensions | Verified observations | Verified maximum | Latest verified output |
| --- | ---: | ---: | ---: | ---: |
| 1 | 2 | 21 | `7.710875e-16` | `8.159220e-130` |
| 2 | 2 | 21 | `0.6112052` | `0.06529973` |
| 3 | 3 | 26 | `-0.03483531` | `-0.03844613` |
| 4 | 4 | 41 | `-1.981075` | `-14.99267` |
| 5 | 4 | 31 | `1465.512` | `210.0383` |
| 6 | 5 | 31 | `-0.7142649` | `-1.154424` |
| 7 | 6 | 41 | `2.149905` | `1.478174` |
| 8 | 8 | 51 | `9.939904` | `9.276069` |

Inputs and outputs are stored as NumPy `.npy` arrays. Query submissions are stored as plain-text `.txt` files, normally with six-decimal coordinates separated by hyphens. Jupyter/Colab `.ipynb` notebooks contain collection logic, validation, analysis, modelling and generated query points. Some weekly directories also contain Markdown documentation and placeholders.

The canonical append-only ledger is [`Results/query_output_ledger.csv`](../Results/query_output_ledger.csv). Version 1.1 contains 88 exact query/output pairs for all eight functions in Weeks 1–11. Each row records source paths and hashes, validation status, and the source-file date. [`Results/query_output_ledger.sha256`](../Results/query_output_ledger.sha256) provides a content-integrity checksum. The superseded version 1.0 remains immutable under `Results/archive/`. Dates are filesystem metadata and are not claimed as authoritative platform submission timestamps.

There are no human subjects, demographic groups, personal data or labels describing people. The outputs are numerical objective values rather than conventional supervised-learning class labels. A fixed train/test split is not recommended because observations are collected sequentially and every confirmed observation is used to update the surrogate.

### Known gaps and integrity concerns

- The immutable ledger covers the 88 exact pairs supported by the archive for Weeks 1–11; returns for Weeks 12–13 remain unavailable.
- Exact collection timestamps and software versions were not recorded for every observation.
- Weeks 12 and 13 remain placeholders and do not yet represent successive completed datasets.
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
- replacing Week 12 and Week 13 placeholders only when their genuine successive outputs are available;
- documenting corrections in Git history and this datasheet;
- archiving a final version when the capstone concludes.

Issues and corrections should be reported through the repository's GitHub issue tracker or directly to the repository owner.
