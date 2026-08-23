"""Build one focused Week 2 function notebook from the canonical workflow."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

from .week_02_function_review import KAPPA, STRATEGY, analyse_week_02_function
from .weekly_function_review import repository_root


def build(function: int, root: str | Path | None = None) -> Path:
    base = repository_root(root)
    frame, summary, proposal, figure = analyse_week_02_function(function, base)
    figure.clear()
    dimensions = summary["dimensions"]
    observed = summary["total_verified_observations"]
    method = STRATEGY[function]
    query = proposal["query"]
    notebook = nbf.v4.new_notebook()
    notebook.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
    notebook.metadata.language_info = {"name": "python", "version": "3"}
    notebook.cells = [
        nbf.v4.new_markdown_cell(
            f"# Week 02 — Function {function:02d}\n\n## Table of contents\n\n"
            "1. [Overview](#overview)\n2. [Objectives](#objectives)\n3. [Evidence provenance](#evidence-provenance)\n"
            "4. [Environment and setup](#environment-setup)\n5. [Data validation](#data-validation)\n"
            "6. [Descriptive EDA](#descriptive-eda)\n7. [Visual EDA](#visual-eda)\n"
            "8. [Model and acquisition](#model-acquisition)\n9. [Week 2 proposal](#week-2-proposal)\n"
            "10. [Reproducibility checks](#reproducibility-checks)\n11. [Conclusions and next steps](#conclusions-next-steps)"
        ),
        nbf.v4.new_markdown_cell(
            f'<a id="overview"></a>\n## 1. Overview\n\nThis focused notebook mirrors the canonical Week 2 main notebook for Function {function:02d}. It observes the starter data plus the returned Week 1 point and keeps the Week 2 query proposal separate.'
        ),
        nbf.v4.new_markdown_cell(
            f'<a id="objectives"></a>\n## 2. Objectives\n\nValidate the {dimensions}-dimensional cumulative evidence, assess the latest returned point within Function {function:02d}, and reproduce the Week 2 {method} proposal without look-ahead.'
        ),
        nbf.v4.new_markdown_cell(
            '<a id="evidence-provenance"></a>\n## 3. Evidence provenance\n\nStarter arrays come from `Week_01/Function_nn/03_Data`; the exact Week 1 query/return comes from the canonical ledger. The Week 2 return is excluded because it was unknown when this proposal was made.'
        ),
        nbf.v4.new_markdown_cell('<a id="environment-setup"></a>\n## 4. Environment and setup'),
        nbf.v4.new_code_cell(
            f"from pathlib import Path\nimport sys\nimport numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\nROOT=Path.cwd().resolve()\nfor candidate in (ROOT,*ROOT.parents):\n    if (candidate/'Week_02'/'Function_{function:02d}').is_dir(): ROOT=candidate; break\nelse: raise FileNotFoundError('Could not locate repository root')\nif str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))\nfrom Code.week_02_function_review import analyse_week_02_function\n"
        ),
        nbf.v4.new_markdown_cell('<a id="data-validation"></a>\n## 5. Data validation'),
        nbf.v4.new_code_cell(
            f"observations, summary, proposal, diagnostic_figure = analyse_week_02_function({function}, ROOT)\ninput_columns=[f'x{{i}}' for i in range(1,{dimensions + 1})]\ninputs=observations[input_columns].to_numpy(float)\noutputs=observations['objective'].to_numpy(float)\nassert inputs.shape==({observed},{dimensions}) and outputs.shape==({observed},)\nassert np.isfinite(inputs).all() and np.isfinite(outputs).all()\nassert np.all((inputs>=0)&(inputs<=1))\nobservations"
        ),
        nbf.v4.new_markdown_cell('<a id="descriptive-eda"></a>\n## 6. Descriptive EDA\n\nAll comparisons are within-function; no causal, global-optimum, or cross-function ranking claim is made.'),
        nbf.v4.new_code_cell("pd.Series({k:v for k,v in summary.items() if k!='proposal'}, name='verified evidence')"),
        nbf.v4.new_markdown_cell('<a id="visual-eda"></a>\n## 7. Visual EDA\n\nThe orange marker is the returned Week 1 observation and the star is the verified incumbent.'),
        nbf.v4.new_code_cell("display(diagnostic_figure)\nplt.close(diagnostic_figure)"),
        nbf.v4.new_markdown_cell(
            f'<a id="model-acquisition"></a>\n## 8. Model and acquisition\n\nMethod: **{method}**. ' + (f'For GP-UCB, `kappa={KAPPA[function]}` and a seeded 5,000-point candidate set reproduce the main notebook.' if function != 5 else 'A seeded local perturbation around the incumbent reproduces the main notebook manual-search policy.')
        ),
        nbf.v4.new_markdown_cell(f'<a id="week-2-proposal"></a>\n## 9. Week 2 proposal\n\nProposed only: `{query}`. This point is not included in `observations`.'),
        nbf.v4.new_markdown_cell('<a id="reproducibility-checks"></a>\n## 10. Reproducibility checks'),
        nbf.v4.new_code_cell(
            f"candidate=np.asarray(proposal['query'],dtype=float)\nassert proposal['status']=='proposed_only'\nassert candidate.shape==({dimensions},) and np.all((candidate>=0)&(candidate<=1))\nassert not np.any(np.all(np.isclose(inputs,candidate,rtol=0,atol=1e-12),axis=1))\nassert summary['total_verified_observations']=={observed}\nassert summary['recorded_pairs']==1\nprint('Function {function:02d} Week 2 checks passed.')"
        ),
        nbf.v4.new_markdown_cell(
            f'<a id="conclusions-next-steps"></a>\n## 11. Conclusions and next steps\n\nThe evidence boundary is locked at {observed} verified observations. The Week 2 proposal remains unobserved until its authoritative return is appended at the next checkpoint.'
        ),
    ]
    output = base / "Week_02" / f"Function_{function:02d}" / "01_Notebook" / f"Week_02_Function_{function:02d}.ipynb"
    nbf.write(notebook, output)
    return output
