"""Canonical function-specific Week 2 evidence and proposal workflow."""

from __future__ import annotations

import json
from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, RBF, WhiteKernel

from .weekly_function_review import (
    analyse_weekly_function,
    plot_weekly_function,
    repository_root,
)

STRATEGY = {n: "Bayesian Optimisation" for n in range(1, 9)}
STRATEGY[5] = "Manual Reasoning"
KAPPA = {1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 5: None, 6: 5.0, 7: 3.0, 8: 2.0}


def _manual_query(X: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> dict:
    best_x = X[int(np.argmax(y))]
    for _ in range(100):
        candidate = np.clip(best_x + rng.normal(0.0, 0.05, size=best_x.shape), 0.0, 1.0)
        if not np.any(np.all(np.isclose(X, candidate, rtol=0.0, atol=1e-12), axis=1)):
            return {"query": candidate, "kernel": "Manual reasoning", "predictive_std": None, "ucb_score": None}
    raise RuntimeError("Could not generate a distinct manual-search query")


def _ucb_query(
    X: np.ndarray, y: np.ndarray, kappa: float, rng: np.random.Generator
) -> dict:
    dimension = X.shape[1]
    kernel = (
        ConstantKernel(1.0, (1e-3, 1e3))
        * RBF(np.ones(dimension), (1e-2, 1e2))
        + WhiteKernel(1e-5, (1e-10, 1e1))
    )
    gp = GaussianProcessRegressor(
        kernel=kernel, normalize_y=True, n_restarts_optimizer=3, random_state=42
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConvergenceWarning)
        gp.fit(X, y)
    candidates = rng.uniform(0.0, 1.0, size=(5000, dimension))
    mean, std = gp.predict(candidates, return_std=True)
    ucb = mean + kappa * std
    selected = int(np.argmax(ucb))
    return {
        "query": candidates[selected],
        "kernel": str(gp.kernel_),
        "predictive_std": float(std[selected]),
        "ucb_score": float(ucb[selected]),
    }


def analyse_week_02_function(function: int, root: str | Path | None = None):
    """Return observed evidence, summary, proposal, and diagnostic figure."""
    base = repository_root(root)
    frame, summary = analyse_weekly_function(
        2, function, base, evidence_through_week=1
    )
    input_columns = [column for column in frame if column.startswith("x")]
    X = frame[input_columns].to_numpy(float)
    y = frame["objective"].to_numpy(float)
    rng = np.random.default_rng(42 + function)
    kappa = KAPPA[function]
    result = _manual_query(X, y, rng) if function == 5 else _ucb_query(X, y, kappa, rng)
    query = np.asarray(result.pop("query"), dtype=float)
    if np.any(np.all(np.isclose(X, query, rtol=0.0, atol=1e-12), axis=1)):
        raise AssertionError("Week 2 proposal duplicates observed evidence")
    proposal = {
        "method": STRATEGY[function],
        "kappa": kappa,
        "query": query.tolist(),
        **result,
        "status": "proposed_only",
    }
    summary.update(
        {
            "evidence_boundary": "Week 1 starter data and Week 1 return observed; Week 2 query proposed only.",
            "evidence_gap": "Confirmed observed evidence is available through Week 1; Week 2 is proposed only at this checkpoint.",
            "proposal": proposal,
        }
    )
    return frame, summary, proposal, plot_weekly_function(frame, summary)


def write_week_02_artifacts(function: int, root: str | Path | None = None) -> dict[str, Path]:
    """Write deterministic Week 2 evidence, proposal, figures, and provenance."""
    base = repository_root(root)
    target = base / "Week_02" / f"Function_{function:02d}"
    frame, summary, _, figure = analyse_week_02_function(function, base)
    results = target / "04_Results"
    figures = target / "05_Figures"
    data = target / "03_Data"
    for folder in (results, figures, data):
        folder.mkdir(parents=True, exist_ok=True)
    observations_path = results / "observations.csv"
    summary_path = results / "summary.json"
    canonical_figure = figures / f"function_{function:02d}_diagnostics.png"
    compatibility_figure = figures / f"week_02_function_{function:02d}_diagnostics.png"
    frame.to_csv(observations_path, index=False)
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    input_columns = [column for column in frame if column.startswith("x")]
    np.save(data / "verified_cumulative_inputs.npy", frame[input_columns].to_numpy())
    np.save(data / "verified_cumulative_outputs.npy", frame["objective"].to_numpy())
    provenance = {
        "canonical_starter": f"Week_01/Function_{function:02d}/03_Data",
        "recorded_pairs_registry": "Results/query_output_ledger.csv",
        "review_context": "Week_02/02_Notebook",
        "observed_scope": "Starter observations plus the returned Week 1 pair.",
        "proposal_scope": "The Week 2 query is proposed only and excluded from observed arrays and results.",
        "data_policy": "Derived arrays are reconstructed from starter data plus the ledger; source arrays are never rewritten.",
        "evidence_gap": "Confirmed observed evidence is available through Week 1; Week 2 is proposed only at this checkpoint.",
    }
    (data / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    figure.savefig(canonical_figure, dpi=160, bbox_inches="tight")
    figure.savefig(compatibility_figure, dpi=160, bbox_inches="tight")
    plt.close(figure)
    return {
        "observations": observations_path,
        "summary": summary_path,
        "figure": canonical_figure,
        "compatibility_figure": compatibility_figure,
    }
