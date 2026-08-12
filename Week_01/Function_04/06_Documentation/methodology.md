# Function 04 methodology

## Purpose

Audit the immutable Function 04 starter observations and record the Grid Search decision independently of notebook cell order.

## Provenance and validation

The supplied `initial_inputs.npy` and `initial_outputs.npy` are source evidence and are not rewritten. Checks require finite numeric arrays, matching row counts, a one-dimensional response, and inputs within the unit hypercube. The submitted query was `[0.555555,0.444444,0.222222,0.111111]`; its returned objective was `-8.727516493155957`.

## Method and outputs

The standalone script identifies the maximum observed response, calculates descriptive statistics, compares the submitted return with that incumbent, and generates `observations.csv`, `summary.json`, and one consolidated Matplotlib diagnostic. The notebook imports the same code.

## Interpretation boundary

Results describe Function 04 only and do not establish causality or global optimality.

## Reproduction

```bash
.venv/bin/python Week_01/Function_04/02_Code/analyse_function_04.py --write-artifacts
.venv/bin/jupyter nbconvert --to notebook --execute Week_01/Function_04/01_Notebook/Week_01_Function_04.ipynb --inplace
```

