# Final reproducibility and version freeze

## Canonical release

The final submission version is identified by the annotated Git tag
`capstone-final-v1.0.2`. Resolve the exact commit with:

```bash
git rev-list -n 1 capstone-final-v1.0.2
git show --stat capstone-final-v1.0.2
```

The tag, rather than a mutable branch name, is the authoritative repository
version.

## Environment

- Interpreter: CPython `3.12.13`
- Exact dependency pins: [`requirements-lock.txt`](../requirements-lock.txt)
- Python selector: [`.python-version`](../.python-version)

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-lock.txt
```

Operating-system libraries, CPU architecture, and BLAS/LAPACK may still produce
small floating-point differences during GP optimisation.

## Deterministic settings

| Component | Seed rule | Other fixed settings |
| --- | --- | --- |
| Submitted Week 12 GP/candidates | `4200 + function` | Matérn-5/2, three restarts, 20,000 candidates, UCB kappa `0.1` |
| Rolling historical validation GP | `7300 + 100 × function + held-out week` | One restart per fold, 88 chronological folds |
| Sensitivity candidate design | `9100 + function` | 20,000 uniform candidates for F1–F5; 32,768 scrambled Sobol candidates for F6–F8 |
| Sensitivity GP | `9200 + function` | Three restarts, standard/wider bounds, UCB and EI |

Candidate points are rounded to six decimal places for duplicate checks and
submission formatting. Returned-pair rows remain immutable.

## Reproduction sequence

```bash
MPLCONFIGDIR=/tmp/capstone-matplotlib .venv/bin/python Code/run_gp_validation.py
MPLCONFIGDIR=/tmp/capstone-matplotlib .venv/bin/python Code/run_week12_sensitivity.py
.venv/bin/python Code/generate_evaluation_notebook.py
MPLCONFIGDIR=/tmp/capstone-matplotlib .venv/bin/python -m jupyter nbconvert --execute --to notebook --inplace Notebooks/GP_Evaluation_and_Calibration.ipynb
.venv/bin/python Code/freeze_submission.py
.venv/bin/python -m unittest discover -s Code/tests -v
```

The submitted Week 12 experiment remains unchanged; sensitivity artifacts are
explicitly non-submission.

## Checksums and evidence integrity

[`Results/submission_manifest.json`](../Results/submission_manifest.json) stores
the versions, seeds, canonical counts, release tag, and SHA-256 checksums for the
principal evidence and analysis artifacts. A checksum match establishes byte
identity with the frozen artifact; it does not independently authenticate the
original black-box platform response.
