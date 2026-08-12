# Function 06 methodology

## Purpose

Audit the immutable Function 06 starter observations and record the Manual Reasoning decision independently of notebook cell order.

## Provenance and validation

The supplied `initial_inputs.npy` and `initial_outputs.npy` are source evidence and are not rewritten. Checks require finite numeric arrays, matching row counts, a one-dimensional response, and inputs within the unit hypercube. The submitted query was `[0.728186,0.154693,0.732552,0.693997,0.564013]`; its returned objective was `-1.1520351120911565`.

## Method and outputs

The standalone script identifies the maximum observed response, calculates descriptive statistics, compares the submitted return with that incumbent, and generates `observations.csv`, `summary.json`, and one consolidated Matplotlib diagnostic. The notebook imports the same code.

## Interpretation boundary

Results describe Function 06 only and do not establish causality or global optimality.

## Reproduction

```bash
.venv/bin/python Week_01/Function_06/02_Code/analyse_function_06.py --write-artifacts
.venv/bin/jupyter nbconvert --to notebook --execute Week_01/Function_06/01_Notebook/Week_01_Function_06.ipynb --inplace
```

