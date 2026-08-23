# Week 13 — Canonical adaptive optimisation strategy

Weeks 01–12 are observed, comprising 96 returned function/week pairs; Week 13 is proposed only. No Week 13 outputs are present in the supplied cumulative exports.

## Canonical methodology

[`02_Notebook/Week_13_Optimisation_Strategy.ipynb`](02_Notebook/Week_13_Optimisation_Strategy.ipynb) is the sole active Week 13 methodology. It uses function-specific UCB, Expected Improvement, and Probability of Improvement choices recorded before Week 13 outcomes. The adaptive policy is heuristic, not a statistically controlled comparison.

The obsolete uniform GP-UCB draft is retained only as pre-Week-12-evidence history and is not an active proposal source.

## Repository map

- [`01_Queries/week_13_query_points.txt`](01_Queries/week_13_query_points.txt): eight portal-valid proposals, capped at `0.999999` and formatted to six decimals.
- [`04_Results/week_13_strategy_summary.csv`](04_Results/week_13_strategy_summary.csv): function-specific acquisition diagnostics and pre-outcome reasons.
- `Function_01` through `Function_08`: focused reviews with the 96-return evidence boundary and Week 13 proposals kept separate.
