# Final report.

Start with [`START_HERE_Final_Report.ipynb`](START_HERE_Final_Report.ipynb). It
combines the final scoreboard, incumbent-change timeline, function-level Week 13
strategy, evaluation caveats, and workflow diagram in one executable narrative.

The PNG scoreboard is the one-page examiner-facing summary. The three CSV files
are generated, reviewable companions:

- `final_scoreboard.csv` — one row per function with starting/final incumbents,
  change counts, Week 13 status, acquisition, RMSE skill, and 95% coverage.
- `incumbent_timeline.csv` — starter incumbents and every verified change point.
- `function_strategy_table.csv` — the pre-outcome Week 13 acquisition choice and
  rationale for each function.

Rebuild them with `python Code/build_final_report.py`. They are summaries, not
new experimental evidence; their sources remain the canonical ledger and frozen
Week 13 strategy artefacts documented in `Documentation/ARTEFACT_GUIDE.md`.
