# Bayesian optimisation for black-box functions

An Imperial College London Machine Learning and Artificial Intelligence
capstone project exploring sequential optimisation of eight unknown objective
functions with Gaussian Process surrogate models and acquisition functions.

## Nontechnical summary

This project asks how Bayesian optimisation can search eight expensive, unknown functions efficiently. It begins with exploratory and manual query choices, then develops reproducible Gaussian Process models that balance promising predictions against uncertainty. A checksum-backed 96-pair ledger preserves the verified history through Week 12 and prevents Week 13 proposals from being treated as observations. Rolling validation tests prediction accuracy and uncertainty calibration. Week 13 uses a pre-outcome, function-specific UCB/EI/PI policy that is adaptive and heuristic rather than statistically controlled.

## Project status

Weeks 1–12 now contain a recovered, reconciled, and validated experiment
history. Canonical ledger v1.2 appends eight verified Week 12 query/output pairs
after cumulative-prefix and query-record reconciliation, extending the
per-function observation counts to `22, 22, 27, 42, 32, 32, 42, 52`. The
executed Week 13 optimisation-strategy notebook uses this updated evidence,
performs full EDA, compares UCB, Expected Improvement, and Probability of
Improvement, and generates one bounded, non-duplicate proposal for each
function. These Week 13 coordinates remain proposals rather than observations
until eight aligned platform outputs are returned and validated.

## Repository structure

| Location | Purpose |
| --- | --- |
| [`Code/`](Code/) | Reusable Python scripts and functions shared across weeks |
| [`Documentation/`](Documentation/) | Datasheet, model card, methodology, project guide, and technical documentation |
| [`Notebooks/`](Notebooks/) | Final consolidated notebooks, not duplicate weekly notebooks |
| [`Reflections/`](Reflections/) | Consolidated academic reflections and learning summaries |
| [`Resources/`](Resources/) | References, links, reading lists, and supporting materials |
| `Week_01/`–`Week_13/` | Detailed weekly notebooks, queries, data, results, and reflection scaffolding |

## Project documentation

- [Dataset datasheet](Documentation/DATASET_DATASHEET.md)
- [Model card](Documentation/MODEL_CARD.md)
- [Evaluation chapter](Documentation/EVALUATION.md)
- [Week 12 sensitivity appendix](Documentation/WEEK_12_SENSITIVITY_APPENDIX.md)
- [Final reproducibility and version freeze](Documentation/REPRODUCIBILITY.md)
- [Four final findings](FINAL_FINDINGS.md)
- [Dataset-size audit](Documentation/DATA_SIZE_AUDIT.md)
- [Final consolidated visual results](Notebooks/Final_Visual_Results.ipynb)
- [Canonical notebook index](Notebooks/README.md)
- [Reflection index](Reflections/README.md)

## Canonical weekly notebooks

| Week | Notebook | Evidence status |
| --- | --- | --- |
| 1 | [Week 1](Week_01/02_Notebook/Week_1_Capstone.ipynb) | Corrected and executed |
| 2 | [Week 2](Week_02/02_Notebook/Week_2_Capstone.ipynb) | Corrected and executed |
| 3 | [Week 3](Week_03/02_Notebook/Week_3_Capstone.ipynb) | Corrected and executed |
| 4 | [Week 4](Week_04/02_Notebook/Week_4_Capstone.ipynb) | Corrected and executed |
| 5 | [Week 5](Week_05/02_Notebook/Week_5_Capstone.ipynb) | Corrected, reconciled, and executed |
| 6 | [Week 6](Week_06/02_Notebook/Week_6_Capstone.ipynb) | Corrected and executed |
| 7 | [Week 7](Week_07/02_Notebook/Week_7_Capstone.ipynb) | Corrected, reconciled, and executed |
| 8 | [Week 8](Week_08/02_Notebook/Week_8_Capstone.ipynb) | Corrected and executed |
| 9 | [Week 9](Week_09/02_Notebook/Week_9_Capstone.ipynb) | Corrected and executed |
| 10 | [Week 10](Week_10/02_Notebook/Week_10_Capstone.ipynb) | Corrected and executed |
| 11 | [Week 11](Week_11/02_Notebook/Week_11_Capstone.ipynb) | Executed corruption-aware review; returned pairs recovered and verified in the canonical ledger |
| 12 | [Week 12](Week_12/02_Notebook/Week_12_Capstone.ipynb) | Observed and reconciled; eight returned outputs are in the canonical ledger |
| 13 | [Week 13](Week_13/02_Notebook/Week_13_Optimisation_Strategy.ipynb) | Sole canonical methodology; validated UCB/EI/PI [query points](Week_13/01_Queries/week_13_query_points.txt); outcomes unavailable |

## Optimisation workflow

The weekly implementation evolves, but the validated workflow is:

1. Load the starter data and append only dimensionally valid query/output pairs
   with explicit provenance.
2. Validate shapes, bounds, finite values, and alignment before modelling.
3. Fit a Gaussian Process with built-in target normalisation.
4. Generate submission candidates reproducibly inside `[0.000000, 0.999999]^d`.
5. Score candidates with an acquisition function such as Expected Improvement
   or Upper Confidence Bound.
6. Reject previously evaluated candidates at submission precision.
7. Validate the exact six-decimal, hyphen-separated portal format.
8. Record the proposal, uncertainty, fitted kernel, diagnostics, and evidence
   gaps for the next round.

The corrected notebooks avoid active Google Drive mounts, `/content` dependencies,
external writes, environment-dependent `display()` calls, and manual target
scaling. Matplotlib figures are embedded in the executed Week 1–11 notebooks.

## Running the notebooks

Create a Python environment with:

```text
numpy
pandas
matplotlib
scipy
scikit-learn
jupyter
```

Run a notebook from the repository root so its root-discovery logic can locate
the Week 1 starter arrays. Execute cells from top to bottom. The final cell in
each corrected notebook contains reproducibility and integrity
assertions.

## Evidence limitations

- Exact query/output pairs for Weeks 1–12 were recovered from the original
  cumulative snapshots in the local capstone archive and recorded with hashes.
- Snapshot file modification dates are retained as provenance metadata, but are
  not represented as authoritative platform submission timestamps.
- Weeks 1–12 are observed and contain 96 verified returned pairs in total.
- Week 13 contains validated proposals generated from that 96-pair state. No
  Week 13 returned outputs are available.
- Objective values from different functions are not directly comparable because
  the black-box functions use different scales.

## Author

JP Amewu
Machine Learning & Artificial Intelligence Programme
Imperial College London, 2026
