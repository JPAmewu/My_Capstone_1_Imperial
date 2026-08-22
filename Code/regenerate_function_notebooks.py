"""Build and execute the 104 systematic weekly function notebooks."""

from __future__ import annotations

import argparse
from pathlib import Path

import nbformat
from nbclient import NotebookClient


DIMENSIONS = {1: 2, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6, 8: 8}
STEPS = (
    "Create week's_dataset by appending the previous output results",
    "Extract the function",
    "Check shapes and missing values",
    "Calculate summary statistics",
    "Plot the output trend",
    "Plot the best-so-far trend",
    "Identify the best query point",
    "Plot the correlation heatmap",
    "Plot each input against the output",
    "Fit a Gaussian Process surrogate",
    "Apply UCB to generate the next query point",
)


def table_of_contents() -> nbformat.NotebookNode:
    """Return the canonical eleven-stage notebook contents list."""
    items = "\n".join(f"{number}. {title}" for number, title in enumerate(STEPS, 1))
    return nbformat.v4.new_markdown_cell(f"## Table of contents\n\n{items}")


def markdown_step(number: int) -> nbformat.NotebookNode:
    return nbformat.v4.new_markdown_cell(f"## {number}. {STEPS[number - 1]}")


def build_notebook(root: Path, week: int, function: int) -> nbformat.NotebookNode:
    """Return one reproducible notebook with the requested eleven-stage order."""
    cutoff = min(max(week - 1, 0), 12)
    dimension = DIMENSIONS[function]
    if cutoff:
        lineage = f"starter observations plus verified query–output pairs through Week {cutoff:02d}"
    else:
        lineage = "starter observations only; no earlier weekly return exists"

    notebook = nbformat.v4.new_notebook()
    notebook.metadata.kernelspec = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    notebook.metadata.language_info = {"name": "python", "version": "3"}
    notebook.cells = [
        nbformat.v4.new_markdown_cell(
            f"# Week {week:02d} — Function {function:02d}\n\n"
            "Systematic Bayesian optimisation review. The notebook follows the same "
            "eleven-stage sequence for every week and function. The proposal generated "
            "at the end is an unevaluated candidate, not a returned observation.\n\n"
            f"**Evidence used:** {lineage}."
        ),
        table_of_contents(),
        nbformat.v4.new_code_cell(
            "from pathlib import Path\n"
            "import sys, warnings\n"
            "import numpy as np\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n"
            "from scipy.stats import qmc\n"
            "from sklearn.gaussian_process import GaussianProcessRegressor\n"
            "from sklearn.gaussian_process.kernels import ConstantKernel, Matern, WhiteKernel\n"
            "from sklearn.exceptions import ConvergenceWarning\n\n"
            "ROOT = Path.cwd().resolve()\n"
            "if not (ROOT / 'Results' / 'query_output_ledger.csv').is_file():\n"
            "    raise FileNotFoundError('Run this notebook with the repository root as the working directory.')\n"
            "if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))\n"
            "from Code.weekly_evidence import pairs_through_week\n"
            "from Code.acquisition_function import upper_confidence_bound\n\n"
            f"WEEK, FUNCTION, DIMENSION, EVIDENCE_CUTOFF = {week}, {function}, {dimension}, {cutoff}\n"
            "KAPPA, CANDIDATE_COUNT = 2.0, 4096\n"
            "warnings.filterwarnings('ignore', category=ConvergenceWarning)\n"
            "plt.style.use('seaborn-v0_8-whitegrid')\n"
            "BLUE, GOLD, INK = '#2A6FBB', '#D69E2E', '#263238'"
        ),
        markdown_step(1),
        nbformat.v4.new_code_cell(
            "starter_dir = ROOT / f'Week_01/Function_{FUNCTION:02d}/03_Data'\n"
            "starter_inputs = np.load(starter_dir / 'initial_inputs.npy').astype(float)\n"
            "starter_outputs = np.load(starter_dir / 'initial_outputs.npy').astype(float).reshape(-1)\n"
            "previous_pairs = pairs_through_week(EVIDENCE_CUTOFF, FUNCTION)\n"
            "previous_inputs = np.asarray([query for query, _ in previous_pairs], dtype=float).reshape(-1, DIMENSION)\n"
            "previous_outputs = np.asarray([output for _, output in previous_pairs], dtype=float)\n"
            "cumulative_inputs = np.vstack([starter_inputs, previous_inputs])\n"
            "cumulative_outputs = np.concatenate([starter_outputs, previous_outputs])\n"
            "source = ['starter'] * len(starter_outputs) + [f'week_{index:02d}' for index in range(1, EVIDENCE_CUTOFF + 1)]\n"
            "week_dataset = pd.DataFrame(cumulative_inputs, columns=[f'x{i}' for i in range(1, DIMENSION + 1)])\n"
            "week_dataset.insert(0, 'source', source)\n"
            "week_dataset['output'] = cumulative_outputs\n"
            "week_dataset.index.name = 'observation'\n"
            "week_dataset.tail(min(10, len(week_dataset)))"
        ),
        markdown_step(2),
        nbformat.v4.new_code_cell(
            "function_inputs = week_dataset.filter(regex=r'^x').to_numpy(dtype=float)\n"
            "function_outputs = week_dataset['output'].to_numpy(dtype=float)\n"
            "print(f'Function {FUNCTION}: {DIMENSION} input dimensions, {len(function_outputs)} verified observations')"
        ),
        markdown_step(3),
        nbformat.v4.new_code_cell(
            "quality = pd.DataFrame({\n"
            "    'measure': ['input shape', 'output shape', 'missing inputs', 'missing outputs', 'non-finite inputs', 'non-finite outputs', 'out-of-bounds inputs'],\n"
            "    'value': [str(function_inputs.shape), str(function_outputs.shape), int(np.isnan(function_inputs).sum()), int(np.isnan(function_outputs).sum()), int((~np.isfinite(function_inputs)).sum()), int((~np.isfinite(function_outputs)).sum()), int(((function_inputs < 0) | (function_inputs > 1)).sum())],\n"
            "})\n"
            "assert function_inputs.shape == (len(function_outputs), DIMENSION)\n"
            "assert np.isfinite(function_inputs).all() and np.isfinite(function_outputs).all()\n"
            "assert np.all((function_inputs >= 0) & (function_inputs <= 1))\n"
            "quality"
        ),
        markdown_step(4),
        nbformat.v4.new_code_cell(
            "summary_statistics = week_dataset.drop(columns='source').describe().T\n"
            "summary_statistics"
        ),
        markdown_step(5),
        nbformat.v4.new_code_cell(
            "observation_number = np.arange(1, len(function_outputs) + 1)\n"
            "fig, ax = plt.subplots(figsize=(10, 4.5))\n"
            "ax.plot(observation_number, function_outputs, color=BLUE, marker='o', markersize=3.5, linewidth=1.4)\n"
            "if EVIDENCE_CUTOFF: ax.axvline(len(starter_outputs) + .5, color=GOLD, linestyle='--', label='Weekly evidence begins')\n"
            "ax.set(title=f'Week {WEEK:02d} Function {FUNCTION:02d}: observed output trend', xlabel='Cumulative observation', ylabel='Returned output')\n"
            "if EVIDENCE_CUTOFF: ax.legend(frameon=False)\n"
            "fig.tight_layout(); plt.show()"
        ),
        markdown_step(6),
        nbformat.v4.new_code_cell(
            "best_so_far = np.maximum.accumulate(function_outputs)\n"
            "fig, ax = plt.subplots(figsize=(10, 4.5))\n"
            "ax.step(observation_number, best_so_far, where='post', color=BLUE, linewidth=2)\n"
            "ax.scatter(observation_number, best_so_far, color=BLUE, s=18)\n"
            "ax.set(title=f'Week {WEEK:02d} Function {FUNCTION:02d}: best-so-far objective', xlabel='Cumulative observation', ylabel='Maximum observed output')\n"
            "fig.tight_layout(); plt.show()"
        ),
        markdown_step(7),
        nbformat.v4.new_code_cell(
            "best_index = int(np.argmax(function_outputs))\n"
            "best_query_point = pd.DataFrame([{\n"
            "    'observation': best_index + 1, 'source': week_dataset.iloc[best_index]['source'],\n"
            "    **{f'x{i + 1}': function_inputs[best_index, i] for i in range(DIMENSION)},\n"
            "    'output': function_outputs[best_index],\n"
            "}])\n"
            "best_query_point"
        ),
        markdown_step(8),
        nbformat.v4.new_code_cell(
            "correlation = week_dataset.drop(columns='source').corr(method='spearman')\n"
            "fig, ax = plt.subplots(figsize=(max(6, DIMENSION + 2), max(5, DIMENSION + 1)))\n"
            "image = ax.imshow(correlation, cmap='RdBu_r', vmin=-1, vmax=1)\n"
            "labels = correlation.columns.tolist(); ax.set_xticks(range(len(labels)), labels); ax.set_yticks(range(len(labels)), labels)\n"
            "for row in range(len(labels)):\n"
            "    for column in range(len(labels)):\n"
            "        value = correlation.iloc[row, column]\n"
            "        ax.text(column, row, f'{value:.2f}', ha='center', va='center', fontsize=8, color='white' if abs(value) > .55 else INK)\n"
            "ax.set_title(f'Week {WEEK:02d} Function {FUNCTION:02d}: Spearman correlation heatmap')\n"
            "fig.colorbar(image, ax=ax, label='Spearman correlation'); fig.tight_layout(); plt.show()"
        ),
        markdown_step(9),
        nbformat.v4.new_code_cell(
            "columns = min(3, DIMENSION); rows = int(np.ceil(DIMENSION / columns))\n"
            "fig, axes = plt.subplots(rows, columns, figsize=(5 * columns, 3.8 * rows), squeeze=False)\n"
            "for index, ax in enumerate(axes.ravel()):\n"
            "    if index >= DIMENSION: ax.axis('off'); continue\n"
            "    ax.scatter(function_inputs[:, index], function_outputs, color=BLUE, alpha=.78, edgecolor='white', linewidth=.4)\n"
            "    ax.scatter(function_inputs[best_index, index], function_outputs[best_index], marker='*', s=170, color=GOLD, edgecolor=INK, label='Best observed')\n"
            "    ax.set(xlabel=f'x{index + 1}', ylabel='Returned output', title=f'x{index + 1} against output')\n"
            "    ax.legend(frameon=False, fontsize=8)\n"
            "fig.suptitle(f'Week {WEEK:02d} Function {FUNCTION:02d}: input–output relationships', fontweight='bold')\n"
            "fig.tight_layout(); plt.show()"
        ),
        markdown_step(10),
        nbformat.v4.new_code_cell(
            "kernel = ConstantKernel(1.0, (1e-3, 1e3)) * Matern(length_scale=np.full(DIMENSION, .3), length_scale_bounds=(1e-2, 10), nu=2.5) + WhiteKernel(noise_level=1e-6, noise_level_bounds=(1e-10, 1e-1))\n"
            "gaussian_process = GaussianProcessRegressor(kernel=kernel, normalize_y=True, n_restarts_optimizer=2, random_state=1000 + WEEK * 10 + FUNCTION)\n"
            "gaussian_process.fit(function_inputs, function_outputs)\n"
            "training_r_squared = gaussian_process.score(function_inputs, function_outputs)\n"
            "print('Fitted kernel:', gaussian_process.kernel_)\n"
            "print(f'Training R²: {training_r_squared:.4f}')"
        ),
        markdown_step(11),
        nbformat.v4.new_code_cell(
            "sobol_power = int(np.log2(CANDIDATE_COUNT))\n"
            "candidate_points = qmc.Sobol(d=DIMENSION, scramble=True, seed=2000 + WEEK * 10 + FUNCTION).random_base2(sobol_power)\n"
            "candidate_mean, candidate_std = gaussian_process.predict(candidate_points, return_std=True)\n"
            "ucb_scores = upper_confidence_bound(candidate_mean, candidate_std, kappa=KAPPA)\n"
            "rounded_candidates = np.round(candidate_points, 6)\n"
            "observed_rounded = {tuple(row) for row in np.round(function_inputs, 6)}\n"
            "duplicate_mask = np.array([tuple(row) in observed_rounded for row in rounded_candidates])\n"
            "ucb_scores[duplicate_mask] = -np.inf\n"
            "selected_index = int(np.argmax(ucb_scores))\n"
            "next_query_point = rounded_candidates[selected_index]\n"
            "assert np.isfinite(next_query_point).all() and np.all((next_query_point >= 0) & (next_query_point <= 1))\n"
            "assert tuple(next_query_point) not in observed_rounded\n"
            "ucb_proposal = pd.DataFrame([{\n"
            "    'week': WEEK, 'function': FUNCTION, 'kappa': KAPPA,\n"
            "    **{f'x{i + 1}': next_query_point[i] for i in range(DIMENSION)},\n"
            "    'predicted_mean': candidate_mean[selected_index],\n"
            "    'predicted_std': candidate_std[selected_index],\n"
            "    'ucb_score': ucb_scores[selected_index],\n"
            "    'status': 'proposed_not_evaluated',\n"
            "}])\n"
            "print(f\"Function_{FUNCTION}:\" + '-'.join(f'{value:.6f}' for value in next_query_point))\n"
            "ucb_proposal"
        ),
    ]
    return notebook


def regenerate(root: Path, weeks: list[int] | None = None, execute: bool = True) -> None:
    selected_weeks = sorted(set(weeks or range(1, 14)))
    invalid = [week for week in selected_weeks if week not in range(1, 14)]
    if invalid:
        raise ValueError(f"Weeks must be in 1..13; received {invalid}")

    targets = [(week, function) for week in selected_weeks for function in range(1, 9)]
    for index, (week, function) in enumerate(targets, 1):
        path = root / f"Week_{week:02d}/Function_{function:02d}/01_Notebook/Week_{week:02d}_Function_{function:02d}.ipynb"
        path.parent.mkdir(parents=True, exist_ok=True)
        notebook = build_notebook(root, week, function)
        if execute:
            client = NotebookClient(
                notebook,
                timeout=240,
                kernel_name="python3",
                resources={"metadata": {"path": str(root)}},
            )
            client.execute()
        nbformat.write(notebook, path)
        action = "built and executed" if execute else "built"
        print(f"[{index:03d}/{len(targets)}] {action} {path.relative_to(root)}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--weeks", type=int, nargs="*")
    parser.add_argument("--no-execute", action="store_true")
    args = parser.parse_args()
    regenerate(args.repository.resolve(), args.weeks, execute=not args.no_execute)


if __name__ == "__main__":
    main()
