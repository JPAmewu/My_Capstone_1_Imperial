# Final reproducibility and version freeze

## Canonical release

Releases through `capstone-final-v1.0.8` preserve the pre-outcome Week 13 freeze.
The canonical prospective outcome update is identified by the immutable
annotated Git tag `capstone-final-v1.0.9`. Resolve it with:

```bash
git rev-list -n 1 capstone-final-v1.0.9
git show --stat capstone-final-v1.0.9
```

The tag, rather than a mutable branch name, is the authoritative repository
version.

## Environment

- Canonical interpreter: CPython `3.14.3`
- Exact dependency pins: [`requirements-lock.txt`](../requirements-lock.txt)
- Python selector: [`.python-version`](../.python-version)

```bash
python3.14 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-lock.txt
```

Operating-system libraries, CPU architecture, and BLAS/LAPACK may still produce
small floating-point differences during GP optimisation.

## Deterministic settings

| Component | Seed rule | Other fixed settings |
| --- | --- | --- |
| Submitted Week 12 GP/candidates | `4200 + function` | Matérn-5/2, three restarts, 20,000 candidates, UCB kappa `0.1` |
| Rolling historical validation GP | `7300 + 100 × function + held-out week` | One restart per fold, 104 chronological folds |
| Final diagnostic GP | `4200 + function` | Three restarts on all verified evidence through Week 13 |
| Week 13 proposal GP and Sobol design | `1300 + function` | Five GP optimiser restarts; 32,768 scrambled Sobol candidates |
| Week 13 local design | `2300 + function` | 4,096 Gaussian candidates around each of the three strongest observations (12,288 local; 45,056 total) |
| Sensitivity candidate design | `9100 + function` | 20,000 uniform candidates for F1–F5; 32,768 scrambled Sobol candidates for F6–F8 |
| Sensitivity GP | `9200 + function` | Three restarts, standard/wider bounds, UCB and EI |

The proposal-generating and diagnostic GP protocols are intentionally distinct.
Week 13 proposals use five optimiser restarts and seed `1300 + function` because
they drive the frozen decision. Rolling validation uses one restart and a unique
fold seed to keep 104 refits tractable and leakage-free. Final diagnostic fits use
three restarts and seed `4200 + function` for compatibility with the historical
Week 12 diagnostic protocol. These fits answer different questions and must not
be treated as numerically interchangeable.

### Week 13 function-specific policy

| Function | Acquisition | Kappa | Xi as output-SD fraction | Local scale |
| --- | --- | ---: | ---: | ---: |
| F1 | UCB | 3.00 | 0.010 | 0.120 |
| F2 | EI | 2.00 | 0.020 | 0.100 |
| F3 | PI | 1.50 | 0.005 | 0.035 |
| F4 | UCB | 2.75 | 0.020 | 0.140 |
| F5 | EI | 1.50 | 0.010 | 0.070 |
| F6 | EI | 1.75 | 0.010 | 0.080 |
| F7 | UCB | 2.00 | 0.010 | 0.090 |
| F8 | UCB | 3.00 | 0.020 | 0.120 |

All Week 13 reported mean, standard deviation, and acquisition diagnostics are
recomputed at the exact six-decimal submitted coordinate. The separate reflected-
boundary sensitivity is diagnostic only and cannot rewrite the immutable Week 13
query set.

Candidate points are restricted to `[0.000000, 0.999999]`, rounded to exactly
six decimal places, separated by hyphens, and strictly validated before portal
submission. Historical observations retain their source-domain validation over
`[0, 1]`. Returned-pair rows remain immutable.

The raw Week 13 cumulative files are preserved under
`Results/source_evidence/week_13/`. Their first 12 rounds match the published
ledger and their final inputs match the v1.0.8 frozen query set. The source
renderer displays submitted `0.999999` values as `1.0` in two functions; the
ledger retains the exact submitted coordinates and the validation report records
the one-micro-unit rendering tolerance.

## Reproduction sequence

Run the complete frozen pipeline with one command:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/capstone-matplotlib .venv/bin/python Code/run_frozen_repository.py
```

The runner audits dataset sizes, validates portal strings, rebuilds derived GP
results, regenerates and executes the three final notebooks, freezes checksums,
and runs the unit-test suite. Its machine-readable outcome is written to
`Results/frozen_run_report.json`.

The runner fixes Matplotlib to its non-interactive `Agg` backend and constrains
BLAS/OpenMP thread counts to one, preventing GUI and threaded linear-algebra
differences from destabilising the frozen macOS run.

The equivalent individual sequence is:

```bash
MPLCONFIGDIR=/tmp/capstone-matplotlib .venv/bin/python Code/run_gp_validation.py
MPLCONFIGDIR=/tmp/capstone-matplotlib .venv/bin/python Code/run_week12_sensitivity.py
.venv/bin/python Code/generate_evaluation_notebook.py
MPLCONFIGDIR=/tmp/capstone-matplotlib .venv/bin/python -m jupyter nbconvert --execute --to notebook --inplace Week_12/02_Notebook/Week_12_Capstone.ipynb
MPLCONFIGDIR=/tmp/capstone-matplotlib .venv/bin/python -m jupyter nbconvert --execute --to notebook --inplace Notebooks/GP_Evaluation_and_Calibration.ipynb
.venv/bin/python Code/generate_final_visual_results.py
MPLCONFIGDIR=/tmp/capstone-matplotlib .venv/bin/python -m jupyter nbconvert --execute --to notebook --inplace Notebooks/Final_Visual_Results.ipynb
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
