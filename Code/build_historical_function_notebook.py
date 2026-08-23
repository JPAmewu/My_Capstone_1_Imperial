"""Build focused Function 01--08 notebooks for Weeks 3--13."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import nbformat as nbf

from .historical_function_review import analyse_historical_function
from .weekly_function_review import repository_root


def build(week: int, function: int, root: str | Path | None = None) -> Path:
    base = repository_root(root)
    frame, summary, proposal, figure = analyse_historical_function(week, function, base)
    plt.close(figure)
    dimensions = summary["dimensions"]
    observed = summary["total_verified_observations"]
    method = proposal["method"]
    notebook = nbf.v4.new_notebook()
    notebook.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
    notebook.metadata.language_info = {"name": "python", "version": "3"}
    notebook.cells = [
        nbf.v4.new_markdown_cell(
            f"# Week {week:02d} — Function {function:02d}\n\n## Table of contents\n\n"
            "1. [Overview](#overview)\n2. [Objectives](#objectives)\n3. [Evidence provenance](#evidence-provenance)\n"
            "4. [Environment and setup](#environment-setup)\n5. [Data validation](#data-validation)\n"
            "6. [Descriptive EDA](#descriptive-eda)\n7. [Visual EDA](#visual-eda)\n"
            f"8. [Model and acquisition](#model-acquisition)\n9. [Week {week} proposal](#week-{week}-proposal)\n"
            "10. [Reproducibility checks](#reproducibility-checks)\n11. [Conclusions and next steps](#conclusions-next-steps)"
        ),
        nbf.v4.new_markdown_cell(f'<a id="overview"></a>\n## 1. Overview\n\nThis focused review mirrors the canonical Week {week} methodology for Function {function:02d}, with Weeks 1–{week - 1} observed and Week {week} proposed only.'),
        nbf.v4.new_markdown_cell(f'<a id="objectives"></a>\n## 2. Objectives\n\nValidate the {dimensions}-dimensional evidence, assess the latest returned point, and reproduce the recorded {method} proposal without look-ahead.'),
        nbf.v4.new_markdown_cell(f'<a id="evidence-provenance"></a>\n## 3. Evidence provenance\n\nStarter arrays come from `Week_01/Function_nn/03_Data`; exact returned pairs come from `Results/query_output_ledger.csv`. The Week {week} return is excluded because it was unknown when the proposal was selected.'),
        nbf.v4.new_markdown_cell('<a id="environment-setup"></a>\n## 4. Environment and setup'),
        nbf.v4.new_code_cell(f"from pathlib import Path\nimport sys\nimport numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\nROOT=Path.cwd().resolve()\nfor candidate in (ROOT,*ROOT.parents):\n    if (candidate/'Week_{week:02d}'/'Function_{function:02d}').is_dir(): ROOT=candidate; break\nelse: raise FileNotFoundError('Could not locate repository root')\nif str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))\nfrom Code.historical_function_review import analyse_historical_function"),
        nbf.v4.new_markdown_cell('<a id="data-validation"></a>\n## 5. Data validation'),
        nbf.v4.new_code_cell(f"observations, summary, proposal, diagnostic_figure = analyse_historical_function({week}, {function}, ROOT)\ninput_columns=[f'x{{i}}' for i in range(1,{dimensions + 1})]\ninputs=observations[input_columns].to_numpy(float)\noutputs=observations['objective'].to_numpy(float)\nassert inputs.shape==({observed},{dimensions}) and outputs.shape==({observed},)\nassert np.isfinite(inputs).all() and np.isfinite(outputs).all()\nassert np.all((inputs>=0)&(inputs<=1))\nobservations"),
        nbf.v4.new_markdown_cell('<a id="descriptive-eda"></a>\n## 6. Descriptive EDA\n\nAll comparisons are descriptive and within-function; no causal, global-optimum, or cross-function ranking claim is made.'),
        nbf.v4.new_code_cell("pd.Series({k:v for k,v in summary.items() if k!='proposal'}, name='verified evidence')"),
        nbf.v4.new_markdown_cell(f'<a id="visual-eda"></a>\n## 7. Visual EDA\n\nOrange markers are returned Weeks 1–{week - 1} observations; the star is the verified incumbent. The Week {week} proposal is deliberately absent.'),
        nbf.v4.new_code_cell("display(diagnostic_figure)\nplt.close(diagnostic_figure)"),
        nbf.v4.new_markdown_cell(f'<a id="model-acquisition"></a>\n## 8. Model and acquisition\n\nMethod: **{method}**. This adaptive policy is a heuristic chosen from the evidence available at the decision boundary; it is not a statistically controlled acquisition comparison.'),
        nbf.v4.new_markdown_cell(f'<a id="week-{week}-proposal"></a>\n## 9. Week {week} proposal\n\nProposed only: `{proposal["query"]}`. Decision record: {proposal.get("reason", proposal["decision_timing"])}'),
        nbf.v4.new_markdown_cell('<a id="reproducibility-checks"></a>\n## 10. Reproducibility checks'),
        nbf.v4.new_code_cell(f"candidate=np.asarray(proposal['query'],dtype=float)\nassert proposal['status']=='proposed_only'\nassert candidate.shape==({dimensions},) and np.all((candidate>=0)&(candidate<=0.999999))\nduplicate=bool(np.any(np.all(np.isclose(inputs,candidate,rtol=0,atol=5e-7),axis=1)))\nassert duplicate==proposal['duplicates_observed_evidence']\nassert summary['recorded_pairs']=={week - 1}\nportal='-'.join(f'{{value:.6f}}' for value in candidate)\nassert all(len(part.split('.')[-1])==6 for part in portal.split('-'))\nprint('Function {function:02d} Week {week} checks passed:', portal, 'duplicate:', duplicate)"),
        nbf.v4.new_markdown_cell(f'<a id="conclusions-next-steps"></a>\n## 11. Conclusions and next steps\n\nThe evidence boundary is locked at {observed} verified observations. The Week {week} proposal remains unobserved until its authoritative return is appended at the next checkpoint.'),
    ]
    output = base / f"Week_{week:02d}" / f"Function_{function:02d}" / "01_Notebook" / f"Week_{week:02d}_Function_{function:02d}.ipynb"
    nbf.write(notebook, output)
    return output
