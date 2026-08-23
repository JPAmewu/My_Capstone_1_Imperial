# Week 02 — Bayesian optimisation with a Function 05 exception

Decision-time evidence consists of the starter arrays and returned Week 01 points. The Week 02 query remains separate from those observations; its later verified return is recorded in [`01_Queries/week_02_query_results.txt`](01_Queries/week_02_query_results.txt).

## Acquisition policy

Functions 01–04 and 06–08 use GP-UCB. Function 05 uses seeded local manual reasoning around its incumbent. The choices are function-specific adaptive heuristics, not a controlled comparison.

## Repository map

- [`02_Notebook/Week_2_Capstone.ipynb`](02_Notebook/Week_2_Capstone.ipynb): canonical Week 02 methodology.
- [`01_Queries`](01_Queries): proposal-era files plus the reconciled query/output record.
- `Function_01` through `Function_08`: reproducible focused reviews with Week 01 observed and Week 02 proposed only.
