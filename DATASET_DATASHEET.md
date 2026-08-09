Datasheet: BBO Capstone Sequential Optimisation Dataset

**Version:** 1.0 (ten-round project state)  
**Creator and maintainer:** JP Amewu  
**Programme:** Imperial College London Machine Learning and Artificial Intelligence Programme  
**Repository:** <https://github.com/JPAmewu/My_Capstone_1_Imperial>

## Motivation

This dataset was created to support a capstone investigation of Bayesian optimisation for expensive, unknown black-box objective functions. The practical task is to maximise eight functions while using as few objective-function evaluations as possible. Each observation therefore has two linked components: a submitted query point and the scalar value returned by the corresponding black box.

The dataset supports sequential optimisation, exploratory data analysis, Gaussian Process (GP) surrogate modelling, acquisition-function comparison and critical reflection on exploration, exploitation, transparency and reproducibility. It was created by JP Amewu as programme coursework. No external commercial funding is known or claimed.

## Composition

The ten-round project state covers eight independent objective functions with inputs constrained to the unit hypercube `[0, 1]^d`. Function dimensionalities are 2, 2, 3, 4, 4, 5, 6 and 8 respectively.

At the completed Week 11 dataset state, the repository contains 254 paired observations:

| Function | Dimensions | Paired observations | Raw recorded maximum | Latest appended output |
| --- | ---: | ---: | ---: | ---: |
| 1 | 2 | 20 | 64 | approximately 0 |
| 2 | 2 | 20 | 64 | 0.0494064 |
| 3 | 3 | 25 | 64 | -0.0818934 |
| 4 | 4 | 40 | 64 | -23.4228031 |
| 5 | 4 | 30 | 1088.8596182 | 430.8031250 |
| 6 | 5 | 30 | 64 | -1.1717132 |
| 7 | 6 | 40 | 64 | 1.0098940 |
| 8 | 8 | 49 | 64 | 9.6998918 |

Inputs and outputs are stored as NumPy `.npy` arrays. Query submissions are stored as plain-text `.txt` files, normally with six-decimal coordinates separated by hyphens. Jupyter/Colab `.ipynb` notebooks contain collection logic, validation, analysis, modelling and generated query points. Some weekly directories also contain Markdown documentation and placeholders.

There are no human subjects, demographic groups, personal data or labels describing people. The outputs are numerical objective values rather than conventional supervised-learning class labels. A fixed train/test split is not recommended because observations are collected sequentially and every confirmed observation is used to update the surrogate.

### Known gaps and integrity concerns

- The complete, immutable query-and-response ledger is not consistently available for every early round.
- Exact collection timestamps and software versions were not recorded for every observation.
- Weeks 12 and 13 remain placeholders and do not yet represent successive completed datasets.
- Several functions contain repeated values of exactly `64`. These may be legitimate evaluations, but their repeated occurrence across functions is unusual and should be checked against the original submission history before treating every raw maximum as a verified optimisation result.
- Sampling is sparse relative to the volume of the higher-dimensional search spaces.
- Earlier notebook versions sometimes reconstructed arrays from uploaded text and could encounter input/output length mismatches. Later validation stops rather than silently truncating data.

## Collection process

Data was accumulated over ten sequential optimisation rounds during the 2026 capstone project. In each round, one query was proposed for each of the eight functions, submitted to the programme's black-box evaluation platform and paired with the returned scalar output. The confirmed pairs were appended to the next dataset; original source arrays were intended to remain unchanged.

The strategy evolved across rounds:

1. Early rounds used exploratory analysis, plotting and manual heuristics.
2. Gaussian Process regression was introduced to estimate objective values and predictive uncertainty.
3. RBF and later Matérn kernels were used, with target scaling where appropriate.
4. Expected Improvement and Upper Confidence Bound (UCB) acquisition functions were explored.
5. Later rounds increasingly used UCB to balance exploitation of predicted high-value regions with exploration of uncertain regions.
6. In the tenth-round workflow, each function used an anisotropic Matérn GP, `kappa = 2.0`, a fixed random seed and 100,000 uniformly sampled candidates. Candidates duplicating an existing point after six-decimal rounding were excluded.

The process is adaptive, not an independent random sample: later query locations depend on earlier observations and modelling choices. This creates deliberate concentration near apparently promising regions and can leave other regions underexplored.

## Preprocessing, cleaning and labelling

The following processing has been applied in later notebooks:

- conversion to floating-point NumPy arrays;
- reshaping inputs to `(n, d)` and outputs to `(n, 1)` or `(n,)`;
- exact filename matching for each function's input and output arrays;
- checks for matching input/output counts, expected dimensionality, finite values and `[0, 1]` input bounds;
- preservation of source datasets while writing derived weekly datasets separately;
- standardisation of objective values before some GP fits;
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
- preserving immutable copies of each previous week's dataset;
- recording provenance, submission round, timestamp and code version for every new observation;
- validating shape, bounds, finiteness and duplicates before publication;
- resolving the repeated-`64` provenance question;
- replacing Week 12 and Week 13 placeholders only when their genuine successive outputs are available;
- documenting corrections in Git history and this datasheet;
- archiving a final version when the capstone concludes.

Issues and corrections should be reported through the repository's GitHub issue tracker or directly to the repository owner.
