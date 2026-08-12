# Function 07 methodology

## Purpose

Audit the immutable Function 07 starter observations and record the Bayesian Optimisation decision independently of notebook cell order.

## Provenance and validation

The supplied `initial_inputs.npy` and `initial_outputs.npy` are source evidence and are not rewritten. Checks require finite numeric arrays, matching row counts, a one-dimensional response, and inputs within the unit hypercube. The submitted query was `[0.045091,0.528666,0.329265,0.10535,0.434667,0.641164]`; its returned objective was `1.0510148516295004`.

## Method and outputs

The standalone script identifies the maximum observed response, calculates descriptive statistics, compares the submitted return with that incumbent, and generates `observations.csv`, `summary.json`, and one consolidated Matplotlib diagnostic. The notebook imports the same code.

## Interpretation boundary

Results describe Function 07 only and do not establish causality or global optimality.

## Reproduction

```bash
.venv/bin/python Week_01/Function_07/02_Code/analyse_function_07.py --write-artifacts
.venv/bin/jupyter nbconvert --to notebook --execute Week_01/Function_07/01_Notebook/Week_01_Function_07.ipynb --inplace
```

