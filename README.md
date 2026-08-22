# Bayesian optimisation for black-box functions

An Imperial College London Machine Learning and Artificial Intelligence
capstone project exploring sequential optimisation of eight unknown objective
functions with Gaussian Process surrogate models and acquisition functions.

## Project status

Weeks 1–12 contain a recovered and validated experiment history. The Week 12
cumulative snapshot reproduces all 88 earlier ledger pairs and supplies eight
aligned Week 12 evaluations. The Week 13 strategy notebook refits the Gaussian
Processes on this evidence, compares UCB, EI and PI, and generates eight new
proposals for the 12th query submission.

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
| 11 | [Week 11](Week_11/02_Notebook/Week_11_Capstone.ipynb) | Executed corruption-aware review with verified Week 11 return |
| 12 | [Week 12 evidence](Week_12/01_Queries/week_12_query_points.txt) | Submitted queries reconciled and eight returned outputs verified |
| 13 | [Week 13 strategy](Week_13/02_Notebook/Week_13_Optimisation_Strategy.ipynb) | Executed UCB/EI/PI comparison with eight new proposals |

## Optimisation workflow

The weekly implementation evolves, but the validated workflow is:

1. Load the starter data and append only dimensionally valid query/output pairs
   with explicit provenance.
2. Validate shapes, bounds, finite values, and alignment before modelling.
3. Fit a Gaussian Process with built-in target normalisation.
4. Generate candidates reproducibly inside the unit hypercube `[0, 1]^d`.
5. Score candidates with an acquisition function such as Expected Improvement
   or Upper Confidence Bound.
6. Reject previously evaluated candidates at submission precision.
7. Record the proposal, uncertainty, fitted kernel, diagnostics, and evidence
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
- The pre-reconciliation Week 12 query file repeated Week 11 and is preserved
  under `Week_12/01_Queries/archive/`; the supplied cumulative snapshot is the
  reconciled source for the verified Week 12 pairs.
- Week 13 coordinates remain proposals and are not ledger observations until
  their returned outputs are received.
- Objective values from different functions are not directly comparable because
  the black-box functions use different scales.

## Author

JP Amewu
Machine Learning & Artificial Intelligence Programme
Imperial College London, 2026
