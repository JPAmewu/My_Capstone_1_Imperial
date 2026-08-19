"""Generate the canonical Week 12 validation notebook."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "Week_12" / "02_Notebook" / "Week_12_Capstone.ipynb"


def build_notebook() -> None:
    nb = nbf.v4.new_notebook()
    nb["metadata"]["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb["metadata"]["language_info"] = {"name": "python", "version": "3"}
    nb["cells"] = [
        nbf.v4.new_markdown_cell(
            "# Week 12 Capstone — validated GP-UCB proposals\n\n"
            "## tl;dr\n\n"
            "This notebook reconstructs the post-Week-11 dataset from the immutable "
            "88-row canonical ledger, validates the required observation counts, and "
            "generates one deterministic, bounded, non-duplicate BBO proposal per function. "
            "No Week 12 returned outputs are available, so the proposals are not observations."
        ),
        nbf.v4.new_markdown_cell(
            "## Context & Methods\n\n"
            "The source of truth is `Results/query_output_ledger.csv` plus the pristine "
            "starter arrays under `Week_01/Function_XX/03_Data`. Each function uses a "
            "Matérn-5/2 Gaussian Process with target normalisation and UCB (`kappa=0.1`). "
            "Twenty thousand candidates are generated from a fixed per-function seed.\n\n"
            "### Key assumptions\n\n"
            "- The canonical ledger is correctly paired and immutable.\n"
            "- All objectives are maximised over `[0, 1]^d`.\n"
            "- Six-decimal duplicate checks match submission precision."
        ),
        nbf.v4.new_code_cell(
            "from pathlib import Path\n"
            "import hashlib\n"
            "import json\n"
            "import sys\n"
            "import numpy as np\n"
            "import pandas as pd\n\n"
            "ROOT = Path.cwd().resolve()\n"
            "for candidate in (ROOT, *ROOT.parents):\n"
            "    if (candidate / 'Results' / 'query_output_ledger.csv').is_file():\n"
            "        ROOT = candidate\n"
            "        break\n"
            "else:\n"
            "    raise FileNotFoundError('Repository root not found')\n"
            "sys.path.insert(0, str(ROOT))\n\n"
            "from Code.data_loading import load_starter_data, append_observations\n"
            "from Code.gaussian_process import fit_gaussian_process, predict_with_uncertainty\n"
            "from Code.candidate_generation import make_rng, uniform_candidates\n"
            "from Code.query_selection import select_query\n"
            "from Code.weekly_evidence import DIMENSIONS, pairs_through_week\n\n"
            "LEDGER = ROOT / 'Results' / 'query_output_ledger.csv'\n"
            "CHECKSUM = ROOT / 'Results' / 'query_output_ledger.sha256'\n"
            "expected_hash = CHECKSUM.read_text().split()[0]\n"
            "actual_hash = hashlib.sha256(LEDGER.read_bytes()).hexdigest()\n"
            "assert actual_hash == expected_hash\n"
            "print(f'Canonical ledger checksum verified: {actual_hash}')"
        ),
        nbf.v4.new_markdown_cell("## Data\n\n### 1. Reconstruct and validate cumulative observations"),
        nbf.v4.new_code_cell(
            "EXPECTED_COUNTS = {1: 21, 2: 21, 3: 26, 4: 41, 5: 31, 6: 31, 7: 41, 8: 51}\n"
            "datasets = {}\n"
            "validation_rows = []\n"
            "for function in range(1, 9):\n"
            "    X, y = load_starter_data(function, repository_root=ROOT)\n"
            "    pairs = pairs_through_week(11, function)\n"
            "    new_X = np.asarray([query for query, _ in pairs], dtype=float)\n"
            "    new_y = np.asarray([value for _, value in pairs], dtype=float)\n"
            "    X, y = append_observations(X, y, new_X, new_y)\n"
            "    assert X.shape == (EXPECTED_COUNTS[function], DIMENSIONS[function])\n"
            "    assert y.shape == (EXPECTED_COUNTS[function],)\n"
            "    assert np.isfinite(X).all() and np.isfinite(y).all()\n"
            "    assert ((X >= 0) & (X <= 1)).all()\n"
            "    datasets[function] = (X, y)\n"
            "    validation_rows.append({'Function': f'F{function}', 'Dimensions': X.shape[1], "
            "'Observations': len(X), 'Best observed': float(np.max(y))})\n"
            "validation = pd.DataFrame(validation_rows)\n"
            "validation"
        ),
        nbf.v4.new_markdown_cell(
            "### 2. Export validated figures by function\n\n"
            "For every function, this section displays data-quality checks, summary "
            "statistics, and six figures. Each figure is also written as an individual "
            "PNG under `Week_12/Function_XX/05_Figures`. Orange points are canonical "
            "ledger returns; starter observations are blue."
        ),
        nbf.v4.new_code_cell(
            "import matplotlib.pyplot as plt\n"
            "from IPython.display import display, Markdown\n\n"
            "figure_manifest = []\n"
            "for function, (X, y) in datasets.items():\n"
            "    starter_count = len(y) - 11\n"
            "    query_index = np.arange(1, len(y) + 1)\n"
            "    best_so_far = np.maximum.accumulate(y)\n"
            "    figure_dir = ROOT / 'Week_12' / f'Function_{function:02d}' / '05_Figures'\n"
            "    figure_dir.mkdir(parents=True, exist_ok=True)\n\n"
            "    display(Markdown(f'#### Function {function:02d}'))\n"
            "    quality = pd.DataFrame([{\n"
            "        'input_shape': str(X.shape), 'output_shape': str(y.shape),\n"
            "        'missing_values': int(np.isnan(X).sum() + np.isnan(y).sum()),\n"
            "        'infinite_values': int(np.isinf(X).sum() + np.isinf(y).sum()),\n"
            "        'out_of_bounds_inputs': int(((X < 0) | (X > 1)).sum()),\n"
            "        'duplicate_input_rows_6dp': int(len(X) - len(np.unique(np.round(X, 6), axis=0))),\n"
            "        'best_observation': int(np.argmax(y) + 1), 'best_output': float(np.max(y)),\n"
            "    }])\n"
            "    display(Markdown('**Data-quality checks**')); display(quality)\n"
            "    summary_frame = pd.DataFrame(X, columns=[f'x{i + 1}' for i in range(X.shape[1])])\n"
            "    summary_frame['objective'] = y\n"
            "    display(Markdown('**Summary statistics**')); display(summary_frame.describe().T)\n\n"
            "    fig, ax = plt.subplots(figsize=(8, 4.5))\n"
            "    ax.plot(query_index, y, marker='o', linewidth=1.3, label='objective')\n"
            "    ax.scatter(query_index[starter_count:], y[starter_count:], color='darkorange', "
            "label='canonical return', zorder=3)\n"
            "    ax.set(title=f'Week 12 Function {function:02d} — objective trace', "
            "xlabel='Verified observation', ylabel='Objective')\n"
            "    ax.legend(); fig.tight_layout()\n"
            "    path = figure_dir / f'week_12_function_{function:02d}_objective_trace.png'\n"
            "    fig.savefig(path, dpi=160, bbox_inches='tight'); display(fig); plt.close(fig)\n"
            "    figure_manifest.append({'function': function, 'figure': 'objective_trace', 'path': str(path.relative_to(ROOT))})\n\n"
            "    fig, ax = plt.subplots(figsize=(8, 4.5))\n"
            "    ax.step(query_index, best_so_far, where='post', color='crimson', linewidth=1.8)\n"
            "    ax.set(title=f'Week 12 Function {function:02d} — verified best so far', "
            "xlabel='Verified observation', ylabel='Best objective')\n"
            "    fig.tight_layout()\n"
            "    path = figure_dir / f'week_12_function_{function:02d}_best_so_far.png'\n"
            "    fig.savefig(path, dpi=160, bbox_inches='tight'); display(fig); plt.close(fig)\n"
            "    figure_manifest.append({'function': function, 'figure': 'best_so_far', 'path': str(path.relative_to(ROOT))})\n\n"
            "    fig, ax = plt.subplots(figsize=(9, max(3.5, 0.55 * X.shape[1])))\n"
            "    image = ax.imshow(X.T, aspect='auto', cmap='viridis', vmin=0, vmax=1)\n"
            "    ax.set(title=f'Week 12 Function {function:02d} — input coordinates', "
            "xlabel='Verified observation', ylabel='Dimension')\n"
            "    ax.set_yticks(range(X.shape[1]), [f'x{i + 1}' for i in range(X.shape[1])])\n"
            "    fig.colorbar(image, ax=ax, label='Coordinate value'); fig.tight_layout()\n"
            "    path = figure_dir / f'week_12_function_{function:02d}_input_heatmap.png'\n"
            "    fig.savefig(path, dpi=160, bbox_inches='tight'); display(fig); plt.close(fig)\n"
            "    figure_manifest.append({'function': function, 'figure': 'input_heatmap', 'path': str(path.relative_to(ROOT))})\n\n"
            "    fig, ax = plt.subplots(figsize=(7, 4.5))\n"
            "    ax.hist(y, bins=min(12, max(6, int(np.sqrt(len(y))))), color='#4472C4', "
            "edgecolor='#243447', alpha=0.85)\n"
            "    ax.axvline(np.mean(y), color='#D97706', linestyle='--', label=f'mean = {np.mean(y):.4g}')\n"
            "    ax.axvline(np.median(y), color='#7A284E', linestyle=':', label=f'median = {np.median(y):.4g}')\n"
            "    ax.set(title=f'Week 12 Function {function:02d} — objective distribution', "
            "xlabel='Objective', ylabel='Frequency'); ax.legend(); fig.tight_layout()\n"
            "    path = figure_dir / f'week_12_function_{function:02d}_output_distribution.png'\n"
            "    fig.savefig(path, dpi=160, bbox_inches='tight'); display(fig); plt.close(fig)\n"
            "    figure_manifest.append({'function': function, 'figure': 'output_distribution', 'path': str(path.relative_to(ROOT))})\n\n"
            "    columns = min(3, X.shape[1]); rows = int(np.ceil(X.shape[1] / columns))\n"
            "    fig, axes = plt.subplots(rows, columns, figsize=(4 * columns, 3 * rows), squeeze=False)\n"
            "    for dimension, ax in enumerate(axes.flat):\n"
            "        if dimension < X.shape[1]:\n"
            "            ax.hist(X[:, dimension], bins=10, range=(0, 1), color='#4472C4', "
            "edgecolor='#243447', alpha=0.85)\n"
            "            ax.set(title=f'x{dimension + 1}', xlabel='Coordinate', ylabel='Frequency', xlim=(0, 1))\n"
            "        else:\n"
            "            ax.axis('off')\n"
            "    fig.suptitle(f'Week 12 Function {function:02d} — input distributions')\n"
            "    fig.tight_layout(rect=(0, 0, 1, 0.96))\n"
            "    path = figure_dir / f'week_12_function_{function:02d}_input_distributions.png'\n"
            "    fig.savefig(path, dpi=160, bbox_inches='tight'); display(fig); plt.close(fig)\n"
            "    figure_manifest.append({'function': function, 'figure': 'input_distributions', 'path': str(path.relative_to(ROOT))})\n\n"
            "    correlation = summary_frame.corr(numeric_only=True)\n"
            "    fig, ax = plt.subplots(figsize=(max(5, 0.8 * len(correlation)), max(4, 0.7 * len(correlation))))\n"
            "    image = ax.imshow(correlation, cmap='coolwarm', vmin=-1, vmax=1)\n"
            "    labels = correlation.columns.tolist()\n"
            "    ax.set_xticks(range(len(labels)), labels, rotation=45, ha='right')\n"
            "    ax.set_yticks(range(len(labels)), labels)\n"
            "    ax.set_title(f'Week 12 Function {function:02d} — Pearson correlation')\n"
            "    fig.colorbar(image, ax=ax, label='Correlation', shrink=0.85); fig.tight_layout()\n"
            "    path = figure_dir / f'week_12_function_{function:02d}_correlation_heatmap.png'\n"
            "    fig.savefig(path, dpi=160, bbox_inches='tight'); display(fig); plt.close(fig)\n"
            "    figure_manifest.append({'function': function, 'figure': 'correlation_heatmap', 'path': str(path.relative_to(ROOT))})\n\n"
            "figure_manifest = pd.DataFrame(figure_manifest)\n"
            "figure_manifest"
        ),
        nbf.v4.new_markdown_cell("## Results\n\n### 3. Fit GP-UCB models and select new queries"),
        nbf.v4.new_code_cell(
            "proposal_rows = []\n"
            "for function, (X, y) in datasets.items():\n"
            "    model = fit_gaussian_process(X, y, optimizer_restarts=3, random_state=4200 + function)\n"
            "    candidates = uniform_candidates(DIMENSIONS[function], 20_000, "
            "rng=make_rng(4200 + function))\n"
            "    mean, std = predict_with_uncertainty(model, candidates)\n"
            "    selected = select_query(candidates, X, mean, std, method='ucb', kappa=0.1, decimals=6)\n"
            "    duplicate = np.any(np.all(np.round(X, 6) == selected.query, axis=1))\n"
            "    assert not duplicate and ((selected.query >= 0) & (selected.query <= 1)).all()\n"
            "    proposal_rows.append({\n"
            "        'week': 12, 'function': function, 'dimensions': DIMENSIONS[function],\n"
            "        'observation_count': len(X), 'query': json.dumps(selected.query.tolist(), separators=(',', ':')),\n"
            "        'submission_query': '-'.join(f'{value:.6f}' for value in selected.query),\n"
            "        'predicted_mean': selected.predicted_mean, 'predictive_std': selected.predicted_std,\n"
            "        'ucb_score': selected.acquisition, 'kernel': str(model.kernel_),\n"
            "        'candidate_count': 20_000, 'kappa': 0.1, 'random_seed': 4200 + function,\n"
            "        'duplicate_at_6dp': duplicate, 'status': 'proposal_only_return_unavailable'\n"
            "    })\n"
            "proposals = pd.DataFrame(proposal_rows)\n"
            "proposals[['function', 'observation_count', 'submission_query', 'predictive_std', 'ucb_score']]"
        ),
        nbf.v4.new_markdown_cell("### 4. Save the proposal ledger and submission file"),
        nbf.v4.new_code_cell(
            "proposal_path = ROOT / 'Results' / 'bbo_query_ledger.csv'\n"
            "archive_path = ROOT / 'Results' / 'archive' / 'bbo_query_ledger_kappa_2.0.csv'\n"
            "if proposal_path.is_file():\n"
            "    previous = pd.read_csv(proposal_path)\n"
            "    if len(previous) == 8 and previous['kappa'].eq(2.0).all():\n"
            "        archive_path.parent.mkdir(parents=True, exist_ok=True)\n"
            "        previous.to_csv(archive_path, index=False)\n"
            "proposals.to_csv(proposal_path, index=False)\n"
            "if archive_path.is_file():\n"
            "    baseline = pd.read_csv(archive_path)\n"
            "    comparison = baseline[['function', 'submission_query', 'predicted_mean', 'predictive_std', 'ucb_score']].merge(\n"
            "        proposals[['function', 'submission_query', 'predicted_mean', 'predictive_std', 'ucb_score']],\n"
            "        on='function', suffixes=('_kappa_2.0', '_kappa_0.1'))\n"
            "    comparison.to_csv(ROOT / 'Results' / 'bbo_query_kappa_comparison.csv', index=False)\n"
            "query_path = ROOT / 'Week_12' / '01_Queries' / 'week_12_query_points.txt'\n"
            "query_path.write_text(''.join(f\"Function_{row.function}:{row.submission_query}\\n\" "
            "for row in proposals.itertuples()), encoding='utf-8')\n"
            "print(query_path.read_text())\n"
            "comparison"
        ),
        nbf.v4.new_markdown_cell(
            "## Takeaways\n\n"
            "- The canonical post-Week-11 counts are `21, 21, 26, 41, 31, 31, 41, 51`.\n"
            "- Every proposed point is finite, within bounds, correctly dimensioned, and distinct "
            "from observed points at six-decimal precision.\n"
            "- These are Week 12 submission proposals only. They must not be appended to the "
            "query/output ledger until authoritative returned outputs are available."
        ),
    ]
    NOTEBOOK.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, NOTEBOOK)


if __name__ == "__main__":
    build_notebook()
    print(NOTEBOOK)
