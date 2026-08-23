"""Function-specific reviews for Weeks 3--13 with strict proposal boundaries."""

from __future__ import annotations

import ast
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .weekly_function_review import analyse_weekly_function, plot_weekly_function, repository_root


WEEK_METHODS = {
    3: {**{n: "GP-UCB" for n in range(1, 9)}, 5: "Manual reasoning"},
    4: {**{n: "GP-UCB" for n in range(1, 9)}, 5: "Manual reasoning"},
    5: {**{n: "GP-UCB" for n in range(1, 9)}, 5: "Expected Improvement"},
    6: {**{n: "GP-UCB" for n in range(1, 9)}, 5: "Expected Improvement", 8: "Expected Improvement"},
    7: {**{n: "GP-UCB exploitation" for n in range(1, 9)}, 5: "Local exploitation"},
    8: {n: "GP-UCB" for n in range(1, 9)},
    9: {n: "Expected Improvement" for n in range(1, 9)},
    10: {n: "GP-UCB" for n in range(1, 9)},
    11: {n: "GP-UCB" for n in range(1, 9)},
    12: {n: "GP-UCB" for n in range(1, 9)},
}

WEEK_KAPPA = {
    3: {1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 6: 5.0, 7: 2.0, 8: 5.0},
    4: {1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 6: 5.0, 7: 3.0, 8: 2.0},
    5: {1: 5.0, 2: 5.0, 3: 4.0, 4: 4.0, 6: 4.0, 7: 3.0, 8: 2.0},
    6: {1: 2.5, 2: 2.5, 3: 2.5, 4: 2.5, 6: 2.0, 7: 2.0},
    7: {n: 2.0 for n in range(1, 9) if n != 5},
    8: {1: 1.5, **{n: 2.0 for n in range(2, 9)}},
    10: {n: 2.0 for n in range(1, 9)},
    11: {n: 2.0 for n in range(1, 9)},
    12: {n: 0.1 for n in range(1, 9)},
}


def _ledger_query(base: Path, week: int, function: int) -> list[float]:
    with (base / "Results" / "query_output_ledger.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if int(row["week"]) == week and int(row["function"]) == function:
                return [float(value) for value in ast.literal_eval(row["query"])]
    raise KeyError(f"No Week {week} Function {function} query in canonical ledger")


def _week_13_metadata(base: Path, function: int) -> dict:
    path = base / "Week_13" / "04_Results" / "week_13_strategy_summary.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if int(row["function"]) == function:
                query = [float(value) for value in ast.literal_eval(row["query"])]
                return {
                    "query": query,
                    "method": row["method"],
                    "kappa": float(row["kappa"]),
                    "xi": float(row["xi"]),
                    "candidate_source": row["candidate_source"],
                    "candidate_count": int(row["candidate_count"]),
                    "predicted_mean": float(row["predicted_mean"]),
                    "predictive_std": float(row["predicted_std"]),
                    "selected_acquisition": float(row["selected_acquisition"]),
                    "reason": row["reason"],
                    "decision_timing": "Chosen after Week 12 evidence and before any Week 13 outcome.",
                    "policy_scope": "Adaptive heuristic; not a statistically controlled acquisition comparison.",
                    "source": "Week_13/02_Notebook/Week_13_Optimisation_Strategy.ipynb",
                }
    raise KeyError(f"No Function {function} row in Week 13 strategy summary")


def proposal_for_week(week: int, function: int, root: str | Path | None = None) -> dict:
    """Return the recorded query as a proposal, never as current-week evidence."""
    base = repository_root(root)
    if week == 13:
        proposal = _week_13_metadata(base, function)
    else:
        proposal = {
            "query": _ledger_query(base, week, function),
            "method": WEEK_METHODS[week][function],
            "kappa": WEEK_KAPPA.get(week, {}).get(function),
            "source": f"Week_{week:02d}/02_Notebook/Week_{week}_Capstone.ipynb",
            "decision_timing": f"Chosen using evidence through Week {week - 1}, before the Week {week} return.",
            "policy_scope": "Adaptive heuristic; not a statistically controlled acquisition comparison.",
        }
    source_query = list(proposal["query"])
    proposal["query"] = np.clip(np.asarray(source_query, dtype=float), 0.0, 0.999999).tolist()
    if proposal["query"] != source_query:
        proposal["source_query"] = source_query
        proposal["portal_normalization"] = "Coordinates at 1.0 were capped at 0.999999 for valid six-decimal submission."
    proposal["status"] = "proposed_only"
    return proposal


def analyse_historical_function(week: int, function: int, root: str | Path | None = None):
    if week not in range(3, 14):
        raise ValueError("Historical focused reviews cover Weeks 3 through 13")
    base = repository_root(root)
    frame, summary = analyse_weekly_function(
        week, function, base, evidence_through_week=week - 1
    )
    proposal = proposal_for_week(week, function, base)
    candidate = np.asarray(proposal["query"], dtype=float)
    observed = frame[[column for column in frame if column.startswith("x")]].to_numpy(float)
    if candidate.shape != (summary["dimensions"],):
        raise AssertionError("Proposal dimension does not match function")
    if np.any((candidate < 0.0) | (candidate > 0.999999)):
        raise AssertionError("Proposal violates the validated [0, 0.999999] portal bounds")
    duplicates_observed = bool(np.any(np.all(np.isclose(observed, candidate, rtol=0.0, atol=5e-7), axis=1)))
    proposal["duplicates_observed_evidence"] = duplicates_observed
    if duplicates_observed:
        proposal["duplicate_note"] = "Historical proposal duplicated evidence available at the decision boundary; retained for fidelity, not endorsed."
    summary.update({
        "recorded_pairs": week - 1,
        "evidence_boundary": f"Weeks 1-{week - 1} observed; Week {week} proposed only.",
        "evidence_gap": f"Confirmed observed evidence is available through Week {week - 1}; Week {week} is proposed only at this checkpoint.",
        "proposal": proposal,
    })
    return frame, summary, proposal, plot_weekly_function(frame, summary)


def write_historical_artifacts(week: int, function: int, root: str | Path | None = None) -> dict[str, Path]:
    base = repository_root(root)
    target = base / f"Week_{week:02d}" / f"Function_{function:02d}"
    frame, summary, _, figure = analyse_historical_function(week, function, base)
    results, figures, data = target / "04_Results", target / "05_Figures", target / "03_Data"
    for folder in (results, figures, data):
        folder.mkdir(parents=True, exist_ok=True)
    observations_path = results / "observations.csv"
    summary_path = results / "summary.json"
    canonical_figure = figures / f"function_{function:02d}_diagnostics.png"
    compatibility_figure = figures / f"week_{week:02d}_function_{function:02d}_diagnostics.png"
    frame.to_csv(observations_path, index=False)
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    inputs = frame[[column for column in frame if column.startswith("x")]].to_numpy()
    np.save(data / "verified_cumulative_inputs.npy", inputs)
    np.save(data / "verified_cumulative_outputs.npy", frame["objective"].to_numpy())
    provenance = {
        "canonical_starter": f"Week_01/Function_{function:02d}/03_Data",
        "recorded_pairs_registry": "Results/query_output_ledger.csv",
        "review_context": summary["proposal"]["source"],
        "observed_scope": f"Starter observations plus returned Weeks 1-{week - 1} pairs.",
        "proposal_scope": f"The Week {week} query is proposed only and excluded from observed arrays and plots.",
        "data_policy": "Derived arrays are reconstructed from starter data plus the ledger; source arrays are never rewritten.",
        "evidence_gap": summary["evidence_gap"],
    }
    if week >= 11:
        provenance["excluded_archive"] = f"Week_11/Function_{function:02d}/03_Data/function_{function}_*.npy"
        provenance["exclusion_reason"] = "Unverified legacy arrays remain quarantined; the canonical ledger is used instead."
    (data / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    figure.savefig(canonical_figure, dpi=160, bbox_inches="tight")
    figure.savefig(compatibility_figure, dpi=160, bbox_inches="tight")
    plt.close(figure)
    return {"observations": observations_path, "summary": summary_path, "figure": canonical_figure}
