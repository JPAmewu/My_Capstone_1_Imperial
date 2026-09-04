# Week 13 — Canonical adaptive optimisation strategy

Weeks 01–12 are observed, comprising 96 returned function/week pairs. The eight Week 13 proposals below were generated and frozen from that 96-pair boundary before any Week 13 outcome was known; the eight authoritative Week 13 returns were subsequently appended prospectively to the canonical ledger (`Results/query_output_ledger.csv`, now 104 rows) without altering the frozen proposals. F5 and F6 improved their Week 12 incumbents; the other six functions did not. See [`01_Queries/README.md`](01_Queries/README.md) for the confirmed outputs and [`04_Results/week_13_confirmed_outcomes.csv`](04_Results/week_13_confirmed_outcomes.csv) for the machine-readable outcome analysis.

## Canonical methodology

[`02_Notebook/Week_13_Optimisation_Strategy.ipynb`](02_Notebook/Week_13_Optimisation_Strategy.ipynb) is the sole active Week 13 methodology. It uses function-specific UCB, Expected Improvement, and Probability of Improvement choices recorded before Week 13 outcomes. The adaptive policy is heuristic, not a statistically controlled comparison.

The obsolete uniform GP-UCB draft is retained only as pre-Week-12-evidence history and is not an active proposal source.

## Repository map

- [`01_Queries/week_13_query_points.txt`](01_Queries/week_13_query_points.txt): eight portal-valid proposals, capped at `0.999999` and formatted to six decimals.
- [`01_Queries/week_13_query_output_results.txt`](01_Queries/week_13_query_output_results.txt): the same eight queries paired with their confirmed outputs.
- [`04_Results/week_13_strategy_summary.csv`](04_Results/week_13_strategy_summary.csv): function-specific acquisition diagnostics and pre-outcome reasons.
- [`04_Results/week_13_confirmed_outcomes.csv`](04_Results/week_13_confirmed_outcomes.csv): confirmed outputs compared against each Week 12 incumbent.
- `Function_01` through `Function_08`: focused reviews that intentionally keep the frozen 96-return pre-outcome evidence boundary separate from the Week 13 proposal, preserving the audit trail described in [`Documentation/ARTEFACT_GUIDE.md`](../Documentation/ARTEFACT_GUIDE.md).
