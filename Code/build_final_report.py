"""Build the public, reader-first final report and its derived summary artifacts."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf
import pandas as pd
import matplotlib.pyplot as plt


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def build_tables(root: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    performance = pd.read_csv(root / "Results/performance_summary_weeks_01_to_13.csv")
    strategy = pd.read_csv(root / "Week_13/04_Results/week_13_strategy_summary.csv")
    metrics = pd.read_csv(root / "Results/gp_validation_metrics.csv")

    functions = [f"F{i}" for i in range(1, 9)]
    rows = []
    timeline_rows = []
    for function in functions:
        history = performance.loc[performance["Function"].eq(function)].sort_values("Week")
        changes = history.loc[history["Improvement"].fillna(0).gt(0)]
        strategy_row = strategy.loc[strategy["function"].eq(int(function[1:]))].iloc[0]
        metric_row = metrics.loc[metrics["function"].eq(int(function[1:]))].iloc[0]
        rows.append(
            {
                "function": function,
                "dimensions": int(history.iloc[0]["Dimensions"]),
                "initial_incumbent": history.iloc[0]["Previous best"],
                "final_incumbent": history.iloc[-1]["New best"],
                "incumbent_changes": len(changes),
                "change_weeks": ", ".join(map(str, changes["Week"].astype(int))) or "None",
                "week_13_return": history.iloc[-1]["New observation"],
                "week_13_improved": bool(history.iloc[-1]["Improvement"] > 0),
                "week_13_acquisition": strategy_row["method"],
                "rolling_rmse_skill": metric_row["rmse_skill_vs_naive"],
                "coverage_95": metric_row["coverage_95"],
            }
        )
        timeline_rows.append(
            {"function": function, "week": 0, "incumbent": history.iloc[0]["Previous best"], "source": "starter data"}
        )
        for _, change in changes.iterrows():
            timeline_rows.append(
                {"function": function, "week": int(change["Week"]), "incumbent": change["New best"], "source": "verified return"}
            )

    scoreboard = pd.DataFrame(rows)
    timeline = pd.DataFrame(timeline_rows)
    strategy_table = strategy[
        ["function", "dimensions", "method", "kappa", "xi_fraction_of_output_std", "candidate_source", "reason"]
    ].copy()
    strategy_table["function"] = strategy_table["function"].map(lambda value: f"F{value}")
    strategy_table.columns = [
        "function", "dimensions", "acquisition", "kappa", "xi_output_sd_fraction", "candidate_focus", "pre_outcome_rationale"
    ]
    return scoreboard, timeline, strategy_table


def build_notebook(root: Path) -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python"}
    nb.cells = [
        nbf.v4.new_markdown_cell(
            """# Start here: final BBO capstone report

## tl;dr

- The canonical ledger contains **104 verified query/return pairs**: 13 rounds for each of eight functions.
- **12 returns changed an incumbent**. Week 13 improved F5 and F6 after its eight proposals had been frozen from the 96-pair Week 12 boundary.
- Rolling chronological GP validation now contains **104 held-out predictions** (13 per function). All eight functions beat the historical-mean RMSE baseline, but calibration remains uneven.
- The function-specific UCB/EI/PI policy was adaptive and heuristic, not a statistically controlled acquisition comparison.

This is the single reader-first synthesis. The weekly folders remain historical records; the canonical source map is in `Documentation/ARTEFACT_GUIDE.md`."""
        ),
        nbf.v4.new_markdown_cell(
            """## Context & Methods

Eight unknown functions were maximised sequentially. Each round added one portal-returned observation per function. Gaussian Process surrogates and acquisition functions increasingly replaced manual exploration, while validation, provenance, and submission-format checks became stricter.

### Key assumptions and limitations

- Objective scales differ, so performance is compared within functions rather than pooled.
- The chronological folds respect time order but arise from an adaptive campaign, not an independent test set.
- Incumbent change means a strictly larger verified output; it is not proof of a global optimum.
- Week 13 acquisition choices were recorded before Week 13 outcomes. Their realised results do not make the policy a controlled experiment.
- Source-file modification dates are provenance metadata, not authoritative portal submission times."""
        ),
        nbf.v4.new_code_cell(
            """from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

ROOT = Path.cwd().resolve()
for candidate in (ROOT, *ROOT.parents):
    if (candidate / 'Results/query_output_ledger.csv').is_file():
        ROOT = candidate
        break
else:
    raise FileNotFoundError('Repository root not found')

ledger = pd.read_csv(ROOT / 'Results/query_output_ledger.csv')
scoreboard = pd.read_csv(ROOT / 'Final_Report/final_scoreboard.csv')
timeline = pd.read_csv(ROOT / 'Final_Report/incumbent_timeline.csv')
strategy = pd.read_csv(ROOT / 'Final_Report/function_strategy_table.csv')
metrics = pd.read_csv(ROOT / 'Results/gp_validation_metrics.csv')

assert len(ledger) == 104 and ledger.groupby('function').size().eq(13).all()
assert len(scoreboard) == len(strategy) == len(metrics) == 8
assert scoreboard['incumbent_changes'].sum() == 12
assert scoreboard.loc[scoreboard.week_13_improved, 'function'].tolist() == ['F5', 'F6']
print('Integrity checks passed: 104 returns, 8 functions, 12 incumbent changes.')"""
        ),
        nbf.v4.new_markdown_cell("## Data\n\nThe scoreboard and timeline below are derived from `Results/performance_summary_weeks_01_to_13.csv`, itself generated from the checksum-backed canonical ledger. The strategy table is derived from the frozen Week 13 strategy summary."),
        nbf.v4.new_markdown_cell("## Results\n\n### Final scoreboard"),
        nbf.v4.new_code_cell(
            """view = scoreboard[['function', 'dimensions', 'initial_incumbent', 'final_incumbent', 'incumbent_changes', 'change_weeks', 'week_13_improved', 'week_13_acquisition', 'rolling_rmse_skill', 'coverage_95']]
display(view.style.format({'initial_incumbent': '{:.6g}', 'final_incumbent': '{:.6g}', 'rolling_rmse_skill': '{:.3f}', 'coverage_95': '{:.1%}'}))"""
        ),
        nbf.v4.new_markdown_cell("### Campaign timeline: when incumbents changed"),
        nbf.v4.new_code_cell(
            """fig, ax = plt.subplots(figsize=(12, 5.5))
for index, function in enumerate([f'F{i}' for i in range(1, 9)]):
    points = timeline[timeline.function.eq(function)]
    ax.hlines(index, 0, 13, color='#CBD5E1', linewidth=1)
    ax.scatter(points.week, [index] * len(points), s=85, color='#1D4ED8', edgecolor='white', zorder=3)
    for row in points.itertuples(index=False):
        label = 'start' if row.week == 0 else f'W{row.week}'
        ax.annotate(label, (row.week, index), xytext=(0, 8), textcoords='offset points', ha='center', fontsize=8)
ax.set(yticks=range(8), yticklabels=[f'F{i}' for i in range(1, 9)], xticks=range(14), xlabel='Campaign week (0 = starter data)', title='Verified incumbent-change timeline')
ax.invert_yaxis(); ax.spines[['top', 'right', 'left']].set_visible(False); ax.grid(axis='x', alpha=.15)
fig.tight_layout()
display(fig)
plt.close(fig)"""
        ),
        nbf.v4.new_markdown_cell("### Function-by-function Week 13 strategy"),
        nbf.v4.new_code_cell("display(strategy)"),
        nbf.v4.new_markdown_cell(
            """### How the final workflow connects

```mermaid
flowchart LR
  A[Weekly inputs and portal returns] --> B[Canonical 104-pair ledger]
  B --> C[Per-function GP models]
  B --> D[Chronological rolling evaluation]
  D --> E[Calibration and hyperparameter diagnostics]
  C --> F[Week 13 acquisition policy: UCB / EI / PI]
  E --> F
  F --> G[Candidate generator]
  G --> H[Six-decimal portal validation]
  H --> I[Frozen Week 13 proposals]
  I -. prospective returns .-> B
```

The dashed edge is important: Week 13 outcomes entered the ledger only after the proposals were frozen."""
        ),
        nbf.v4.new_markdown_cell(
            """## Takeaways

1. **Optimisation:** F5 achieved the largest absolute gain on its own scale; F4, F6, F7, and F8 also finished above their starter incumbents. F1 and F2 never exceeded strong starter values.
2. **Learning:** model-guided search improved the campaign, but function-specific behaviour justified different acquisition choices rather than one universal setting.
3. **Evaluation:** positive RMSE skill across all functions supports using the GPs as predictive aids, while uneven interval coverage argues against overconfident interpretation.
4. **Evidence discipline:** the proposal freeze, canonical ledger, derived evaluation, checksums, and historical archive separate decisions from later outcomes.
5. **Reproducibility:** run `Code/run_frozen_repository.py` for the complete pipeline or follow the shorter public guide in `REPRODUCIBILITY.md`."""
        ),
    ]
    return nb


def render_scoreboard(scoreboard: pd.DataFrame, output: Path) -> None:
    """Render a single-page, scale-aware scorecard for quick review."""
    fig = plt.figure(figsize=(16, 9), facecolor="#F8FAFC")
    fig.text(0.05, 0.92, "BBO capstone — final scoreboard", fontsize=25, weight="bold", color="#0F172A")
    fig.text(0.05, 0.875, "Weeks 1–13 observed • 104 verified returns • values compared within functions", fontsize=12, color="#475569")
    fig.text(0.05, 0.79, "12", fontsize=32, weight="bold", color="#1D4ED8")
    fig.text(0.05, 0.75, "incumbent changes", fontsize=11, color="#475569")
    fig.text(0.25, 0.79, "8 / 8", fontsize=32, weight="bold", color="#15803D")
    fig.text(0.25, 0.75, "GPs beat mean-RMSE baseline", fontsize=11, color="#475569")
    fig.text(0.54, 0.79, "F5, F6", fontsize=32, weight="bold", color="#B45309")
    fig.text(0.54, 0.75, "Week 13 incumbent gains", fontsize=11, color="#475569")
    fig.text(0.81, 0.79, "104", fontsize=32, weight="bold", color="#6D28D9")
    fig.text(0.81, 0.75, "chronological GP folds", fontsize=11, color="#475569")

    ax = fig.add_axes([0.04, 0.08, 0.92, 0.60]); ax.axis("off")
    table_data = []
    for row in scoreboard.itertuples(index=False):
        table_data.append([
            row.function, row.dimensions, f"{row.initial_incumbent:.6g}", f"{row.final_incumbent:.6g}",
            row.incumbent_changes, row.change_weeks, row.week_13_acquisition,
            "Yes" if row.week_13_improved else "No", f"{row.rolling_rmse_skill:.3f}", f"{row.coverage_95:.0%}",
        ])
    columns = ["Function", "Dim", "Starter best", "Final best", "Changes", "Change weeks", "W13 policy", "W13 gain", "RMSE skill", "95% cover"]
    table = ax.table(cellText=table_data, colLabels=columns, cellLoc="center", colLoc="center", loc="center", colWidths=[.07,.05,.12,.12,.07,.12,.09,.09,.10,.10])
    table.auto_set_font_size(False); table.set_fontsize(9.5); table.scale(1, 2.05)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#CBD5E1")
        if row == 0:
            cell.set_facecolor("#1E3A8A"); cell.set_text_props(color="white", weight="bold")
        else:
            cell.set_facecolor("#FFFFFF" if row % 2 else "#EFF6FF")
            if col == 7 and cell.get_text().get_text() == "Yes":
                cell.set_facecolor("#DCFCE7"); cell.set_text_props(color="#166534", weight="bold")
    fig.text(0.05, 0.025, "RMSE skill = 1 − GP RMSE / historical-mean baseline RMSE. Positive values favour the GP. Coverage is empirical across 13 folds per function.", fontsize=9, color="#64748B")
    fig.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(fig)


def render_timeline(timeline: pd.DataFrame, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(13, 6))
    for index, function in enumerate([f"F{i}" for i in range(1, 9)]):
        points = timeline.loc[timeline["function"].eq(function)]
        ax.hlines(index, 0, 13, color="#CBD5E1", linewidth=1)
        ax.scatter(points["week"], [index] * len(points), s=85, color="#1D4ED8", edgecolor="white", zorder=3)
        for row in points.itertuples(index=False):
            ax.annotate("start" if row.week == 0 else f"W{row.week}", (row.week, index), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8)
    ax.set(yticks=range(8), yticklabels=[f"F{i}" for i in range(1, 9)], xticks=range(14), xlabel="Campaign week (0 = starter data)", title="Verified incumbent-change timeline")
    ax.invert_yaxis(); ax.spines[["top", "right", "left"]].set_visible(False); ax.grid(axis="x", alpha=.15)
    fig.tight_layout(); fig.savefig(output, dpi=180, bbox_inches="tight"); plt.close(fig)


def main() -> None:
    root = repository_root()
    output = root / "Final_Report"
    output.mkdir(exist_ok=True)
    scoreboard, timeline, strategy = build_tables(root)
    scoreboard.to_csv(output / "final_scoreboard.csv", index=False)
    timeline.to_csv(output / "incumbent_timeline.csv", index=False)
    strategy.to_csv(output / "function_strategy_table.csv", index=False)
    render_scoreboard(scoreboard, output / "final_scoreboard.png")
    render_timeline(timeline, output / "incumbent_timeline.png")
    nbf.write(build_notebook(root), output / "START_HERE_Final_Report.ipynb")
    print(f"Built final report artifacts in {output}")


if __name__ == "__main__":
    main()
