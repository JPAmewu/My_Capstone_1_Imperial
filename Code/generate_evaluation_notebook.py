"""Generate the reader-facing GP evaluation and calibration notebook."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    notebook = nbf.v4.new_notebook()
    notebook["metadata"]["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    notebook["metadata"]["language_info"] = {"name": "python", "version": "3.12.14"}
    notebook["cells"] = [
        nbf.v4.new_markdown_cell(
            """# Historical GP validation and uncertainty calibration

## tl;dr

- This notebook evaluates the surrogate **out of sample** using 96 rolling one-step-ahead folds: each historical return is predicted using only evidence available before that return.
- Seven functions beat a historical-mean baseline on RMSE; F2 does not.
- Calibration is heterogeneous. F5–F7 under-cover at the nominal 95% level, while F1 and F8 are conservative.
- Final GP hyperparameters are fitted to all verified evidence through Week 12, and kernel-bound warnings are reported as evidence rather than suppressed.
- These results assess surrogate prediction and calibration. They do not replace optimisation-performance or recommendation-robustness evaluation.
"""
        ),
        nbf.v4.new_markdown_cell(
            """## Context & Methods

The evaluation has three distinct questions:

1. **Optimisation performance:** did submitted queries improve the best observed objective within each function?
2. **Surrogate accuracy and calibration:** did a GP trained on the historical prefix predict the next returned value, and did its intervals cover at their nominal rates?
3. **Recommendation robustness:** does the proposed point remain stable under acquisition, GP-bound, and candidate-design changes?

### Key assumptions

The Matérn-5/2 GP, target normalisation, configured bounds, and canonical ledger pairing are held fixed. Each function has twelve rolling folds. Hyperparameters are re-estimated inside every fold with one optimiser restart; final diagnostics use all evidence through Week 12, three restarts and fixed seeds. Adaptive historical queries are not an independent random test set, so the results are conditional predictive checks rather than generalisation guarantees.
"""
        ),
        nbf.v4.new_code_cell(
            """from pathlib import Path
import subprocess
import sys
import pandas as pd
from IPython.display import Image, display

ROOT = Path.cwd()
if not (ROOT / 'Results' / 'query_output_ledger.csv').is_file():
    for candidate in Path.cwd().parents:
        if (candidate / 'Results' / 'query_output_ledger.csv').is_file():
            ROOT = candidate
            break
assert (ROOT / 'Results' / 'query_output_ledger.csv').is_file()
print(f'Repository: {ROOT}')"""
        ),
        nbf.v4.new_markdown_cell("## Data\n\n### 1. Recompute rolling validation from the immutable ledger"),
        nbf.v4.new_code_cell(
            """subprocess.run(
    [sys.executable, str(ROOT / 'Code' / 'run_gp_validation.py')],
    cwd=ROOT,
    check=True,
)
predictions = pd.read_csv(ROOT / 'Results' / 'gp_rolling_validation_predictions.csv')
metrics = pd.read_csv(ROOT / 'Results' / 'gp_validation_metrics.csv')
hyperparameters = pd.read_csv(ROOT / 'Results' / 'gp_final_hyperparameters.csv')
assert len(predictions) == 96
assert len(metrics) == len(hyperparameters) == 8
assert predictions.groupby('function').size().eq(12).all()
print('Validated 96 rolling folds: 12 per function.')"""
        ),
        nbf.v4.new_markdown_cell("## Results\n\n### 2. Surrogate accuracy and interval calibration"),
        nbf.v4.new_code_cell(
            """display(metrics.round({
    'mae': 6, 'rmse': 6, 'naive_mean_rmse': 6, 'rmse_skill_vs_naive': 3,
    'coverage_50': 3, 'coverage_80': 3, 'coverage_95': 3,
    'mean_abs_z': 3, 'hyperparameter_bound_hit_rate': 3,
}))"""
        ),
        nbf.v4.new_code_cell(
            """display(Image(filename=str(ROOT / 'Figures' / 'gp_rolling_validation_diagnostics.png')))"""
        ),
        nbf.v4.new_markdown_cell(
            """Coverage should be interpreted against nominal 50%, 80%, and 95% rates. With only twelve folds per function, one fold changes coverage by 8.3 percentage points. The uncertainty/error panel uses symmetric-log axes because objective scales differ sharply across functions; it is not a cross-function ranking of raw errors.
"""
        ),
        nbf.v4.new_markdown_cell("### 3. Final fitted GP hyperparameters"),
        nbf.v4.new_code_cell(
            """columns = [
    'function', 'observation_count', 'constant_value', 'length_scales',
    'noise_level', 'constant_bound_status', 'length_scale_bound_status',
    'noise_bound_status', 'convergence_warning_count',
]
display(hyperparameters[columns])"""
        ),
        nbf.v4.new_markdown_cell(
            """Longer fitted length scales imply slower variation along a coordinate under this kernel; a value at the upper bound means the data support a smoother direction than the configured search permitted. Near-zero noise estimates indicate that the fitted model attributes little independent noise, not that the black box is proven noiseless. Boundary estimates and convergence warnings indicate weak identification or restrictive bounds and motivate the separate wider-bound sensitivity analysis.
"""
        ),
        nbf.v4.new_markdown_cell(
            """## Takeaways

1. The 96-fold history includes all verified returns through Week 12; Week 13 remains proposal-only.
2. Rolling validation and calibration are diagnostic checks, not controlled acquisition comparisons.
3. Interval coverage and baseline skill vary by function and should be interpreted from the regenerated metric table.
4. Recommendation robustness is a separate property. The Week 13 function-specific UCB/EI/PI policy is adaptive and heuristic and was selected before Week 13 outcomes.
5. All findings are conditional on twelve adaptive folds per function, the recovered ledger, the Matérn model family, and the frozen environment. They do not establish global optimality or independent-test-set generalisation.
"""
        ),
    ]
    output = root / "Notebooks" / "GP_Evaluation_and_Calibration.ipynb"
    output.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(notebook, output)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
