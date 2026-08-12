# Function 02 methodology

## Purpose

Audit the immutable Function 02 starter observations and record the Random Search decision independently of notebook cell order.

## Provenance and validation

The supplied `initial_inputs.npy` and `initial_outputs.npy` are source evidence and are not rewritten. Checks require finite numeric arrays, matching row counts, a one-dimensional response, and inputs within the unit hypercube. The submitted query was `[0.37544,0.950714]`; its returned objective was `-0.03182956281754251`.

## Method and outputs

The standalone script identifies the maximum observed response, calculates descriptive statistics, compares the submitted return with that incumbent, and generates `observations.csv`, `summary.json`, and one consolidated Matplotlib diagnostic. The notebook imports the same code.

## Interpretation boundary

Results describe Function 02 only and do not establish causality or global optimality.

## Reproduction

```bash
.venv/bin/python Week_01/Function_02/02_Code/analyse_function_02.py --write-artifacts
.venv/bin/jupyter nbconvert --to notebook --execute Week_01/Function_02/01_Notebook/Week_01_Function_02.ipynb --inplace
```

