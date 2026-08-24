# Week 13 queries and confirmed outputs

This folder preserves the eight Week 13 queries generated from the verified
Week 1–12 evidence and frozen before any Week 13 return was known:

- [`week_13_query_points.txt`](week_13_query_points.txt) — immutable portal-format queries;
- [`week_13_query_output_results.txt`](week_13_query_output_results.txt) — the same queries paired with their confirmed outputs.

The fitted models, UCB/EI/PI comparison, parameters and duplicate checks are in
the [executed strategy notebook](../02_Notebook/Week_13_Optimisation_Strategy.ipynb).
The machine-readable outcome analysis is in
[`week_13_confirmed_outcomes.csv`](../04_Results/week_13_confirmed_outcomes.csv).

The authoritative cumulative files contain 13 aligned rounds and are preserved
with SHA-256 provenance under `Results/source_evidence/week_13/`. Their final
inputs match the frozen query set. F5 and F6 improved their Week 12 incumbents;
the other six functions did not.

The original query file remains unchanged so that the repository continues to
distinguish the pre-outcome decision from the subsequently observed results.
