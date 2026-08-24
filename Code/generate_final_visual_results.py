"""Generate the final consolidated visual-results notebook."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    notebook = nbf.v4.new_notebook()
    notebook["metadata"]["kernelspec"] = {
        "display_name": "Python 3", "language": "python", "name": "python3"
    }
    notebook["metadata"]["language_info"] = {"name": "python", "version": "3.14.3"}
    notebook["cells"] = [
        nbf.v4.new_markdown_cell(
            """# Final consolidated visual results

## tl;dr

1. Ten of 96 verified weekly returns set a new within-function incumbent (10.4%), including five in Week 12.
2. All eight GPs beat a historical-mean RMSE baseline, but calibration varies and F5–F7 under-cover at 95%.
3. The Week 13 UCB/EI/PI policy is adaptive and heuristic, not a controlled comparison.
4. The immutable ledger reconstructs the required post-Week-12 counts and keeps Week 13 proposals outside the observed dataset.

This notebook is the final reader-facing visual synthesis. Detailed methods remain in the weekly and GP-evaluation notebooks.
"""
        ),
        nbf.v4.new_markdown_cell(
            """## Context & Methods

The notebook reads only frozen repository artifacts: the returned-pair ledger, performance summary, rolling GP metrics, sensitivity analysis and Week 13 proposal ledger. It does not refit models or create new black-box evidence.

### Key assumptions

- Improvements are evaluated within each function because objective scales differ.
- Rolling folds are chronological but arise from adaptive queries, not an independent test set.
- Sensitivity rows are diagnostic experiments and were not submitted.
- Missing Week 13 returns remain missing; recommendations are not scored as realised outcomes.
"""
        ),
        nbf.v4.new_code_cell(
            """from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

ROOT = Path.cwd().resolve()
for candidate in (ROOT, *ROOT.parents):
    if (candidate / 'Results' / 'query_output_ledger.csv').is_file():
        ROOT = candidate
        break
else:
    raise FileNotFoundError('Repository root not found')

ledger = pd.read_csv(ROOT / 'Results' / 'query_output_ledger.csv')
performance = pd.read_csv(ROOT / 'Results' / 'performance_summary_weeks_01_to_13.csv')
metrics = pd.read_csv(ROOT / 'Results' / 'gp_validation_metrics.csv')
sensitivity = pd.read_csv(ROOT / 'Results' / 'week12_sensitivity_analysis.csv')
proposals = pd.read_csv(ROOT / 'Week_13' / '04_Results' / 'week_13_strategy_summary.csv')
print(f'Repository: {ROOT}')"""
        ),
        nbf.v4.new_markdown_cell("## Data\n\n### 1. Validate frozen evidence"),
        nbf.v4.new_code_cell(
            """EXPECTED_COUNTS = [22, 22, 27, 42, 32, 32, 42, 52]
assert len(ledger) == 96
assert ledger.groupby('function').size().eq(12).all()
assert len(metrics) == len(proposals) == 8
assert len(sensitivity) == 80
assert proposals['verified_observations'].tolist() == EXPECTED_COUNTS
print('Validated: 96 returned pairs, 80 sensitivity rows, 8 unreturned Week 13 proposals.')"""
        ),
        nbf.v4.new_markdown_cell("## Results\n\n### 2. Four-panel consolidated evidence"),
        nbf.v4.new_code_cell(
            """confirmed = performance[performance['Evidence status'].eq('Confirmed return')].copy()
improvements = confirmed.assign(improved=confirmed['Improvement'].fillna(0).gt(0)).groupby('Function')['improved'].sum()
improvements = improvements.reindex([f'F{i}' for i in range(1, 9)], fill_value=0)
distinct_recommendations = sensitivity.groupby('function')['submission_query'].nunique().reindex(range(1, 9))

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
colours = ['#4472C4' if value == 0 else '#D97706' for value in improvements]
axes[0, 0].bar(improvements.index, improvements.values, color=colours)
axes[0, 0].set(title='A. Verified incumbent improvements', xlabel='Function', ylabel='Improving returns (of 12)', ylim=(0, max(2, improvements.max() + 0.5)))

skill = metrics.set_index('function')['rmse_skill_vs_naive'].reindex(range(1, 9))
axes[0, 1].bar([f'F{i}' for i in skill.index], skill.values, color=np.where(skill >= 0, '#2E8B57', '#C44536'))
axes[0, 1].axhline(0, color='black', linewidth=0.8)
axes[0, 1].set(title='B. Rolling GP skill versus mean baseline', xlabel='Function', ylabel='RMSE skill (higher is better)')

coverage = metrics.set_index('function')[['coverage_50', 'coverage_80', 'coverage_95']].reindex(range(1, 9))
for column, colour, marker in [('coverage_50', '#4472C4', 'o'), ('coverage_80', '#D97706', 's'), ('coverage_95', '#7A284E', '^')]:
    axes[1, 0].plot([f'F{i}' for i in coverage.index], coverage[column], marker=marker, color=colour, label=column.replace('coverage_', '') + '% observed')
for nominal, colour in [(0.5, '#4472C4'), (0.8, '#D97706'), (0.95, '#7A284E')]:
    axes[1, 0].axhline(nominal, color=colour, alpha=0.25, linestyle='--')
axes[1, 0].set(title='C. Predictive-interval calibration', xlabel='Function', ylabel='Observed coverage', ylim=(0, 1.05))
axes[1, 0].legend(fontsize=8)

axes[1, 1].bar([f'F{i}' for i in distinct_recommendations.index], distinct_recommendations.values, color='#6A5ACD')
axes[1, 1].set(title='D. Recommendation sensitivity', xlabel='Function', ylabel='Distinct queries across 10 settings', ylim=(0, 10))

fig.suptitle('Bayesian optimisation capstone — final consolidated results', fontsize=16, fontweight='bold')
fig.tight_layout(rect=(0, 0, 1, 0.96))
figure_path = ROOT / 'Figures' / 'final_consolidated_results.png'
fig.savefig(figure_path, dpi=180, bbox_inches='tight')
display(fig)
plt.close(fig)
print(figure_path.relative_to(ROOT))"""
        ),
        nbf.v4.new_markdown_cell(
            """### 3. Interpretation

- **Panel A:** ten historical returns improved an incumbent; five of those improvements occurred in Week 12.
- **Panel B:** all functions have positive GP skill relative to the historical-mean RMSE baseline.
- **Panel C:** F5–F7 materially under-cover at 95%. Twelve folds per function make coverage estimates coarse.
- **Panel D:** one distinct query means stability across acquisition and bound settings (F4/F5/F7 in this appendix); many distinct queries indicate model or acquisition sensitivity, not necessarily poor realised performance.
"""
        ),
        nbf.v4.new_markdown_cell("### 4. Compact evidence table"),
        nbf.v4.new_code_cell(
            """summary = pd.DataFrame({
    'function': [f'F{i}' for i in range(1, 9)],
    'verified_observations': proposals['verified_observations'].to_numpy(),
    'improving_returns': improvements.to_numpy(dtype=int),
    'rmse_skill_vs_mean': skill.to_numpy(),
    'coverage_95': coverage['coverage_95'].to_numpy(),
    'distinct_sensitivity_queries': distinct_recommendations.to_numpy(dtype=int),
    'week13_return_available': False,
})
display(summary.round({'rmse_skill_vs_mean': 3, 'coverage_95': 3}))"""
        ),
        nbf.v4.new_markdown_cell(
            """## Takeaways

The project’s strongest conclusion is methodological rather than a claim of global optimality: progressively stronger Bayesian optimisation was paired with increasingly strict evidence controls. The final state distinguishes observed improvement, surrogate accuracy and calibration, recommendation robustness, and data lineage. Week 13 proposals are reproducible and portal-valid, but remain proposals until authoritative returns exist. The next scientifically valuable step is to obtain those returns, append them immutably, and evaluate realised improvement against the recorded pre-outcome recommendations.
"""
        ),
    ]
    output = root / "Notebooks" / "Final_Visual_Results.ipynb"
    nbf.write(notebook, output)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
