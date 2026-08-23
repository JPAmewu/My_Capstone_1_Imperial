"""Build the focused Function 06 notebook from the Week 1 baseline contract."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf


def build(repository_root: Path) -> Path:
    notebook = nbf.v4.new_notebook()
    notebook.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
    notebook.metadata.language_info = {"name": "python", "version": "3"}
    notebook.cells = [
        nbf.v4.new_markdown_cell(
            "# Week 01 — Function 06\n\n## Table of contents\n\n"
            "1. [Overview](#overview)\n2. [Objectives](#objectives)\n3. [Evidence provenance](#evidence-provenance)\n"
            "4. [Environment and setup](#environment-setup)\n5. [Data validation](#data-validation)\n"
            "6. [Descriptive EDA](#descriptive-eda)\n7. [Visual EDA](#visual-eda)\n"
            "8. [GP model configuration](#gp-model-configuration)\n9. [GP-UCB values](#gp-ucb-values)\n"
            "10. [Reproducibility checks](#reproducibility-checks)\n11. [Conclusions and next steps](#conclusions-next-steps)"
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"overview\"></a>\n## 1. Overview\n\nThis focused notebook mirrors the authoritative Week 1 main notebook for Function 06. It analyses the 20 immutable starter observations as a model-free Manual Reasoning baseline."
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"objectives\"></a>\n## 2. Objectives\n\nValidate the five-dimensional starter dataset, report its descriptive baseline, and preserve a reproducible starting point for later optimisation rounds."
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"evidence-provenance\"></a>\n## 3. Evidence provenance\n\nThe authoritative Week 1 inputs are `initial_inputs.npy` and `initial_outputs.npy`. The ledger-derived Week 1 return is later cumulative evidence and is deliberately excluded from this starter-baseline analysis. No proposal is promoted to an observation here."
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"environment-setup\"></a>\n## 4. Environment and setup\n\nLocate the repository and import the stable Function 06 analysis interface."
        ),
        nbf.v4.new_code_cell(
            "from pathlib import Path\nimport sys\nimport numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\n"
            "ROOT = Path.cwd().resolve()\nfor candidate in (ROOT, *ROOT.parents):\n"
            "    if (candidate / 'Week_01' / 'Function_06').is_dir(): ROOT = candidate; break\n"
            "else: raise FileNotFoundError('Could not locate the repository root.')\n"
            "CODE_DIR = ROOT / 'Week_01/Function_06/02_Code'\n"
            "if str(CODE_DIR) not in sys.path: sys.path.insert(0, str(CODE_DIR))\n"
            "from analyse_function_06 import analyse_function_06"
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"data-validation\"></a>\n## 5. Data validation\n\nLoad the 20 starter rows and validate alignment, dimensionality, finiteness, and unit-cube bounds."
        ),
        nbf.v4.new_code_cell(
            "observations, summary, diagnostic_figure = analyse_function_06(ROOT)\n"
            "inputs = observations[['x1', 'x2', 'x3', 'x4', 'x5']].to_numpy(float)\noutputs = observations['output'].to_numpy(float)\n"
            "assert inputs.shape == (20, 5) and outputs.shape == (20,)\n"
            "assert np.isfinite(inputs).all() and np.isfinite(outputs).all()\n"
            "assert np.all((inputs >= 0) & (inputs <= 1))\n"
            "pd.DataFrame({'measure':['input shape','output shape','missing values','out-of-bounds inputs'],"
            "'value':[str(inputs.shape),str(outputs.shape),int(np.isnan(inputs).sum()+np.isnan(outputs).sum()),int(((inputs<0)|(inputs>1)).sum())]})"
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"descriptive-eda\"></a>\n## 6. Descriptive EDA\n\nFunction 06 is assessed only in its own objective scale. Its negative maximum is valid: the least-negative observed value is the incumbent, not a global optimum."
        ),
        nbf.v4.new_code_cell("display(observations)\npd.Series(summary, name='Function 06 baseline')"),
        nbf.v4.new_markdown_cell(
            "<a id=\"visual-eda\"></a>\n## 7. Visual EDA\n\nShow the observation trace, running best, and all five input/output relationships."
        ),
        nbf.v4.new_code_cell("display(diagnostic_figure)\nplt.close(diagnostic_figure)"),
        nbf.v4.new_markdown_cell(
            "<a id=\"gp-model-configuration\"></a>\n## 8. GP model configuration\n\nWeek 1 establishes the model-free baseline; Gaussian Process configuration is introduced in later rounds."
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"gp-ucb-values\"></a>\n## 9. GP-UCB values\n\nNo GP-UCB proposal is claimed for the Week 1 baseline. The 20 starter values remain the authoritative evidence for this analysis."
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"reproducibility-checks\"></a>\n## 10. Reproducibility checks\n\nConfirm the starter count, best row, and exact agreement with the Function 06 summary."
        ),
        nbf.v4.new_code_cell(
            "best_index = int(np.argmax(outputs))\n"
            "assert summary['observations'] == 20 and summary['dimensions'] == 5\n"
            "assert summary['best_query_number'] == best_index + 1 == 1\n"
            "assert np.isclose(summary['best_output'], outputs[best_index])\n"
            "assert np.allclose(summary['best_input'], inputs[best_index])\n"
            "print('Function 06 Week 1 baseline checks passed.')"
        ),
        nbf.v4.new_markdown_cell(
            "<a id=\"conclusions-next-steps\"></a>\n## 11. Conclusions and next steps\n\nThe 20 starter observations establish a reproducible Manual Reasoning baseline. Query 1 is the observed incumbent at `-0.71426494782`; later returned evidence belongs to the sequential ledger and later checkpoints."
        ),
    ]
    output = repository_root / "Week_01/Function_06/01_Notebook/Week_01_Function_06.ipynb"
    nbf.write(notebook, output)
    return output


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[3]
    print(build(root))
