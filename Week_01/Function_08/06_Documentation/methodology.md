# Function 08 methodology

## Purpose

Audit the immutable Function 08 starter observations and record the Bayesian Optimisation decision independently of notebook cell order.

## Provenance and validation

The supplied `initial_inputs.npy` and `initial_outputs.npy` are source evidence and are not rewritten. Checks require finite numeric arrays, matching row counts, a one-dimensional response, and inputs within the unit hypercube. The submitted query was `[0.273673,0.2604,0.073937,0.078562,0.862321,0.230729,0.10688,0.352588]`; its returned objective was `9.8157087929671`.

## Method and outputs

The standalone script identifies the maximum observed response, calculates descriptive statistics, compares the submitted return with that incumbent, and generates `observations.csv`, `summary.json`, and one consolidated Matplotlib diagnostic. The notebook imports the same code.

## Interpretation boundary

Results describe Function 08 only and do not establish causality or global optimality.

## Reproduction

```bash
.venv/bin/python Week_01/Function_08/02_Code/analyse_function_08.py --write-artifacts
.venv/bin/jupyter nbconvert --to notebook --execute Week_01/Function_08/01_Notebook/Week_01_Function_08.ipynb --inplace
```

