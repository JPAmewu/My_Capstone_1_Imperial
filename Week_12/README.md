# Week 12 — Exploitation-weighted GP-UCB

Weeks 01–11 are observed; Week 12 is proposed only at the decision boundary. [`01_Queries/week_12_query_points.txt`](01_Queries/week_12_query_points.txt) preserves the pre-return proposal, while [`01_Queries/week_12_query_results.txt`](01_Queries/week_12_query_results.txt) records the subsequently verified submitted coordinates and returns.

All functions use GP-UCB with `kappa = 0.1` to emphasize exploitation. The policy is adaptive and heuristic, not a statistically controlled comparison.

- [`02_Notebook/Week_12_Capstone.ipynb`](02_Notebook/Week_12_Capstone.ipynb): canonical Week 12 methodology.
- [`01_Queries`](01_Queries): proposal and reconciled returned evidence.
- `Function_01` through `Function_08`: focused reviews with Weeks 01–11 observed.

The Week 12 returns include five incumbent improvements, which become observed evidence at the Week 13 checkpoint.
