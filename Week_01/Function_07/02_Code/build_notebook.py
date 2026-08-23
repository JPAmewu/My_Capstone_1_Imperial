"""Build the focused Function 07 notebook from the Week 1 baseline contract."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf


def build(repository_root: Path) -> Path:
    notebook = nbf.v4.new_notebook()
    notebook.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
    notebook.metadata.language_info = {"name": "python", "version": "3"}
    notebook.cells = [
        nbf.v4.new_markdown_cell(
            "# Week 01 — Function 07\n\n## Table of contents\n\n"
            "1. [Overview](#overview)\n2. [Objectives](#objectives)\n3. [Evidence provenance](#evidence-provenance)\n"
            "4. [Environment and setup](#environment-setup)\n5. [Data validation](#data-validation)\n"
            "6. [Descriptive EDA](#descriptive-eda)\n7. [Visual EDA](#visual-eda)\n"
            "8. [GP model configuration](#gp-model-configuration)\n9. [GP-UCB values](#gp-ucb-values)\n"
            "10. [Reproducibility checks](#reproducibility-checks)\n11. [Conclusions and next steps](#conclusions-next-steps)"
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"overview\"></a>\n## 1. Overview\n\nThis focused notebook mirrors the authoritative Week 1 main notebook for Function 07. It analyses the 30 immutable starter observations and preserves the recorded Bayesian Optimisation strategy label as a descriptive baseline."
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"objectives\"></a>\n## 2. Objectives\n\nValidate the six-dimensional starter dataset, report its descriptive baseline, and preserve a reproducible starting point for later optimisation rounds."
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"evidence-provenance\"></a>\n## 3. Evidence provenance\n\nThe authoritative Week 1 inputs are `initial_inputs.npy` and `initial_outputs.npy`. The ledger-derived Week 1 return is later cumulative evidence and is deliberately excluded from this starter-baseline analysis. The repository records the strategy as Bayesian Optimisation but does not preserve a Week 1 GP fit or acquisition calculation, so none is reconstructed here."
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"environment-setup\"></a>\n## 4. Environment and setup\n\nLocate the repository and import the stable Function 07 analysis interface."
        ),
        nbf.v4.new_code_cell(
            "from pathlib import Path\nimport sys\nimport numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\n"
            "ROOT = Path.cwd().resolve()\nfor candidate in (ROOT, *ROOT.parents):\n"
            "    if (candidate / 'Week_01' / 'Function_07').is_dir(): ROOT = candidate; break\n"
            "else: raise FileNotFoundError('Could not locate the repository root.')\n"
            "CODE_DIR = ROOT / 'Week_01/Function_07/02_Code'\n"
            "if str(CODE_DIR) not in sys.path: sys.path.insert(0, str(CODE_DIR))\n"
            "from analyse_function_07 import analyse_function_07"
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"data-validation\"></a>\n## 5. Data validation\n\nLoad the 30 starter rows and validate alignment, dimensionality, finiteness, and unit-cube bounds."
        ),
        nbf.v4.new_code_cell(
            "observations, summary, diagnostic_figure = analyse_function_07(ROOT)\n"
            "input_columns = [f'x{i}' for i in range(1, 7)]\n"
            "inputs = observations[input_columns].to_numpy(float)\noutputs = observations['output'].to_numpy(float)\n"
            "assert inputs.shape == (30, 6) and outputs.shape == (30,)\n"
            "assert np.isfinite(inputs).all() and np.isfinite(outputs).all()\n"
            "assert np.all((inputs >= 0) & (inputs <= 1))\n"
            "pd.DataFrame({'measure':['input shape','output shape','missing values','out-of-bounds inputs'],"
            "'value':[str(inputs.shape),str(outputs.shape),int(np.isnan(inputs).sum()+np.isnan(outputs).sum()),int(((inputs<0)|(inputs>1)).sum())]})"
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"descriptive-eda\"></a>\n## 6. Descriptive EDA\n\nFunction 07 is assessed only in its own objective scale. The observed maximum is an incumbent within the starter sample, not evidence of a global optimum."
        ),
        nbf.v4.new_code_cell("display(observations)\npd.Series(summary, name='Function 07 baseline')"),
        nbf.v4.new_markdown_cell(
            "<a id=\"visual-eda\"></a>\n## 7. Visual EDA\n\nShow the observation trace, running best, and all six input/output relationships."
        ),
        nbf.v4.new_code_cell("display(diagnostic_figure)\nplt.close(diagnostic_figure)"),
        nbf.v4.new_markdown_cell(
            "<a id=\"gp-model-configuration\"></a>\n## 8. GP model configuration\n\nThe Week 1 evidence preserves no reproducible GP configuration for Function 07. The recorded strategy label is retained without inventing kernel, scaling, noise, or fitting choices."
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"gp-ucb-values\"></a>\n## 9. GP-UCB values\n\nNo reproducible Week 1 acquisition values are available. No GP-UCB proposal is inferred from the starter rows or promoted to observed evidence."
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"reproducibility-checks\"></a>\n## 10. Reproducibility checks\n\nConfirm the starter count, best row, and exact agreement with the Function 07 summary."
        ),
        nbf.v4.new_code_cell(
            "best_index = int(np.argmax(outputs))\n"
            "assert summary['observations'] == 30 and summary['dimensions'] == 6\n"
            "assert summary['best_query_number'] == best_index + 1 == 7\n"
            "assert np.isclose(summary['best_output'], outputs[best_index])\n"
            "assert np.allclose(summary['best_input'], inputs[best_index])\n"
            "print('Function 07 Week 1 baseline checks passed.')"
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"conclusions-next-steps\"></a>\n## 11. Conclusions and next steps\n\nThe 30 starter observations establish a reproducible descriptive baseline under the recorded Bayesian Optimisation label. Query 7 is the observed incumbent at `1.3649683045`; later returned evidence belongs to the sequential ledger and later checkpoints."
        ),
    ]
    output = repository_root / "Week_01/Function_07/01_Notebook/Week_01_Function_07.ipynb"
    nbf.write(notebook, output)
    return output


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[3]
    print(build(root))
