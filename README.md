# Bayesian optimisation for black-box functions

An Imperial College London Machine Learning and Artificial Intelligence
capstone project exploring sequential optimisation of eight unknown objective
functions with Gaussian Process surrogate models and acquisition functions.

## Nontechnical summary

This project asks how Bayesian optimisation can search eight expensive, unknown functions efficiently. It begins with exploratory and manual query choices, then develops reproducible Gaussian Process models that balance promising predictions against uncertainty. A recovered, checksum-backed ledger preserves the verified history through Week 11 and prevents unreturned proposals from being treated as observations. Rolling validation tests prediction accuracy and uncertainty calibration, while sensitivity analysis shows how acquisition settings alter recommendations. The final Week 12 queries deliberately favour exploitation using UCB with kappa 0.1, but no global optimum or Week 12 improvement is claimed. The repository includes executed notebooks, figures, reflections, frozen dependencies and reproducibility checks.

## Project status

Weeks 1–11 contain a recovered and validated experiment history. The canonical
Week 12 notebook reconstructs the post-Week-11 arrays from the immutable ledger,
verifies counts of `21, 21, 26, 41, 31, 31, 41, 51`, and generates eight
deterministic GP-UCB proposals. The canonical Week 13 notebook now provides 
validated full EDA and deterministic
GP-UCB proposals while preserving the evidence boundary: no authoritative 
Week 13 returned outputs are available, so proposals are not observations.

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
| 12 | [Week 12](Week_12/02_Notebook/Week_12_Capstone.ipynb) | Executed canonical-ledger validation; [new GP-UCB proposals](Week_12/01_Queries/week_12_query_points.txt); returned outputs unavailable |
| 13 | [Week 13](Week_13/02_Notebook/Week_13_Capstone.ipynb) | Validated and executed; full EDA and [GP-UCB values](Results/week_13_gp_ucb_proposals.csv); [query points](Week_13/01_Queries/week_13_query_points.txt); returned outputs unavailable |

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
- Week 12 has validated GP-UCB proposals generated from the post-Week-11
  canonical state, but no returned outputs. Week 12 therefore carries
  the verified Week 11 evidence forward without inventing evaluations.
- Week 13 contains validated EDA and deterministic GP-UCB proposals generated
  from the canonical verified evidence through Week 11. No authoritative Week
  12 or Week 13 returned outputs are available.
- Objective values from different functions are not directly comparable because
  the black-box functions use different scales.

## Author

JP Amewu
Machine Learning & Artificial Intelligence Programme
Imperial College London, 2026
