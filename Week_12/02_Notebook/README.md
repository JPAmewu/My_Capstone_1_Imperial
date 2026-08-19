# Week 12 notebook

[`Week_12_Capstone.ipynb`](Week_12_Capstone.ipynb) is the executed canonical
Week 12 analysis. It verifies the immutable ledger checksum, reconstructs the
post-Week-11 datasets, checks the expected observation counts, fits deterministic
GP-UCB models, and generates one bounded non-duplicate proposal per function.

The proposals are stored in [`../01_Queries/week_12_query_points.txt`](../01_Queries/week_12_query_points.txt)
and `Results/bbo_query_ledger.csv`. No verified returned outputs are available,
so the proposals are not appended to the query/output ledger.
