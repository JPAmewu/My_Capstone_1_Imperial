# Public reproducibility guide

## Quick start

Use Python 3.14 and run commands from the repository root:

```bash
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/capstone-matplotlib \
  .venv/bin/python Code/run_frozen_repository.py
```

The frozen runner rebuilds the ledger-derived analyses, regenerates and executes
the final notebooks, validates Week 13 portal strings, refreshes checksums, and
runs the tests. A machine-readable result is saved to
`Results/frozen_run_report.json`.

To rebuild only the reader-facing report after its source CSV files are current:

```bash
.venv/bin/python Code/build_final_report.py
.venv/bin/python -m jupyter nbconvert --execute --to notebook --inplace \
  Final_Report/START_HERE_Final_Report.ipynb
```

## Verify the evidence

```bash
shasum -a 256 -c Results/query_output_ledger.sha256
.venv/bin/python -m unittest discover -s Code/tests -v
```

Expected final invariants are 104 ledger rows, 13 verified rounds per function,
104 chronological held-out predictions, and eight Week 13 portal strings with
exactly six decimals and no coordinate above `0.999999`.

The full environment, seed rules, individual commands, platform caveats, and
release-tag policy are documented in
[`Documentation/REPRODUCIBILITY.md`](Documentation/REPRODUCIBILITY.md).
