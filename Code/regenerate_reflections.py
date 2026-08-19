"""Regenerate evidence-specific function and consolidated weekly reflections."""

from __future__ import annotations

import json
from pathlib import Path


WEEK_METHOD = {
    1: "baseline manual, random, grid, and Bayesian strategies",
    2: "GP-UCB for F1–F4 and F6–F8, with manual local search for F5",
    3: "reproducible GP-UCB for F1–F4 and F6–F8, with local exploration for F5",
    4: "GP-UCB for modelled functions and bounded local exploration for F5",
    5: "GP-UCB for F1–F4 and F6–F8, with Expected Improvement for F5",
    6: "hybrid global/local candidates, UCB for F1–F4/F6–F7, and EI for F5/F8",
    7: "an exploitation-focused round with local search around verified incumbents",
    8: "a consistent reusable GP-UCB workflow across all eight functions",
    9: "80% local / 20% global Expected Improvement after evidence recovery",
    10: "normalised Gaussian Processes with reproducible GP-UCB",
    11: "corruption-aware GP-UCB using only canonical-ledger evidence",
    12: "validated GP-UCB with kappa 0.1 and a separate sensitivity appendix",
}

WEEK_LEARNING = {
    1: "Initial methods established coverage, but sparse samples made manual and random choices difficult to justify.",
    2: "Introducing a surrogate made uncertainty explicit and exposed the need for reproducible, function-specific random streams.",
    3: "Repeated UCB use showed that a plausible model recommendation still needs a returned value before it counts as progress.",
    4: "Repairing the evidence chain mattered as much as fitting the model; unverified rows could otherwise move the apparent incumbent.",
    5: "Comparing UCB with Expected Improvement clarified that acquisition rules express different attitudes to improvement and uncertainty.",
    6: "Hybrid candidates linked global coverage with local refinement and reduced dependence on a single uniform random search.",
    7: "Stronger exploitation did not reliably improve incumbents, demonstrating the risk of repeatedly searching one attractive basin.",
    8: "A shared pipeline reduced cell-order leakage and made cross-function implementation consistent without comparing incompatible objective scales.",
    9: "Recovered rounds demonstrated that data lineage can change the modelling state; evidence must be reconciled before optimisation.",
    10: "One transparent target-normalisation path made GP diagnostics easier to interpret and reproduce.",
    11: "Quarantining suspicious arrays prevented corrupted or unprovenanced rows from becoming model evidence.",
    12: "The immutable ledger separated observations from proposals, while low-kappa sensitivity made the exploration/exploitation choice explicit.",
}

WEEK_NEXT = {
    1: "replace uninformed search with a reproducible surrogate and acquisition function",
    2: "compare returned performance with the incumbent before refining the acquisition rule",
    3: "retain uncertainty diagnostics and verify every appended query/return pair",
    4: "use only reconciled evidence and compare UCB with an improvement-based acquisition",
    5: "test a global/local candidate mixture rather than relying on one search geometry",
    6: "evaluate whether deliberate exploitation improves on the verified incumbent",
    7: "restore broader exploration where local concentration has not produced improvement",
    8: "use Expected Improvement on reconciled evidence and preserve per-function diagnostics",
    9: "return to GP-UCB with transparent normalisation and duplicate checks",
    10: "quarantine unverified arrays and reconstruct the modelling state from canonical evidence",
    11: "generate Week 12 proposals only after ledger checksum and count validation",
    12: "wait for authoritative returns, then evaluate realised improvement without retrospectively changing the submission",
}

WEEK1_FUNCTION_METHOD = {
    1: "random search", 2: "random search", 3: "grid search", 4: "grid search",
    5: "manual reasoning", 6: "manual reasoning", 7: "Bayesian optimisation",
    8: "Bayesian optimisation",
}

WEEK12_SENSITIVITY = {
    1: "Nine distinct sensitivity candidates show dependence on kappa and GP bounds.",
    2: "The first coordinate stays near 0.69 while the second moves as uncertainty weight increases, suggesting a ridge rather than one settled point.",
    3: "Seven distinct candidates and a strong wider-bound shift make the recommendation hyperparameter-sensitive.",
    4: "Every appendix setting selects one point; the submitted kappa 0.1 and archived kappa 2.0 recommendations also agree.",
    5: "Every appendix setting selects one point, indicating local robustness without proving outcome quality.",
    6: "Sobol coverage produces three candidates as kappa rises, giving a controlled exploration path in five dimensions.",
    7: "The submitted comparison is diagnostic: kappa 0.1 selects higher mean and lower uncertainty, whereas kappa 2.0 accepts lower mean for greater uncertainty.",
    8: "Sobol sampling yields three standard-bound candidates, while wider bounds make all strategies agree, revealing model-specification sensitivity.",
}


def fmt(value: float) -> str:
    """Format objective values compactly without hiding very small magnitudes."""
    return f"{value:.7g}"


def strategy(week: int, function: int) -> str:
    if week == 1:
        return WEEK1_FUNCTION_METHOD[function]
    if week in (2, 3, 4) and function == 5:
        return "manual bounded local exploration"
    if week == 5 and function == 5:
        return "Expected Improvement"
    if week == 6:
        return "Expected Improvement with hybrid candidates" if function in (5, 8) else "GP-UCB with hybrid candidates"
    if week == 7:
        return "local exploitation around the verified incumbent"
    if week == 9:
        return "Expected Improvement with an 80/20 local/global candidate mixture"
    if week == 12:
        return "GP-UCB with kappa 0.1"
    return "GP-UCB"


def function_reflection(summary: dict) -> str:
    week = summary["week"]
    function = summary["function"]
    latest = fmt(summary["latest_verified_output"])
    best = fmt(summary["best_output"])
    improved = summary["latest_improves_previous_best"]
    return_label = "latest canonical-ledger return" if week == 12 else "latest verified return"
    outcome = (
        f"The {return_label} `{latest}` established a new within-function best."
        if improved
        else f"The {return_label} `{latest}` did not exceed the incumbent `{best}`."
    )
    evidence = summary["evidence_gap"]
    if week == 12:
        evidence += " The Week 12 point is a proposal, not an observation."
    sensitivity = ""
    if week == 12:
        sensitivity = f"\n\n## Sensitivity and interpretation\n\n{WEEK12_SENSITIVITY[function]}"
    archive = ""
    if week >= 11:
        archive = " The original Week 11 arrays remain quarantined; reconstruction uses the immutable ledger."
    return f"""# Week {week:02d} Function {function:02d} reflection

## Objective

Review Function {function:02d} at the Week {week} checkpoint and decide what the
verified evidence implies for the next optimisation step.

## Strategy and work completed

I used {strategy(week, function)} within the Week {week} workflow. I validated
all {summary['total_verified_observations']} cumulative observations, kept the
analysis within this function's {summary['dimensions']}-dimensional space, and
checked the response trace, running incumbent, bounds, and provenance.

## Evidence and result

{outcome} The verified incumbent occurs at query {summary['best_query']} with
input `{json.dumps(summary['best_input'], separators=(',', ':'))}`. Progress is
defined only against earlier Function {function:02d} values; objective magnitudes
are not ranked across functions.

## Critical reflection

{WEEK_LEARNING[week]} For Function {function:02d}, the result shows that a
model-guided or plausible query is not evidence of improvement until its exact
return is recorded. {'The improvement supports the selected region, but one success does not prove the strategy or a global optimum.' if improved else 'The absence of improvement argues against overconfidence in the selected region, not against the acquisition method on the basis of one trial.'}
{sensitivity}

## Data quality, limitations, and ethics

{evidence}{archive} The response surface and global optimum remain unknown, the
sample is adaptive rather than representative, and sparse coverage becomes more
serious as dimension increases. I therefore avoid causal claims, imputation,
cross-function score comparisons, and retrospective selection of a method after
seeing its result.

## Next step

For the next checkpoint I would {WEEK_NEXT[week]}. I would append a point only
after its authoritative return is available and preserve the prior rows as an
immutable audit trail.
"""


def weekly_section(week: int, summaries: list[dict]) -> str:
    improvements = [f"F{s['function']}" for s in summaries if s["latest_improves_previous_best"]]
    improved_text = ", ".join(improvements) if improvements else "none"
    rows = "\n".join(
        f"| F{s['function']} | {s['total_verified_observations']} | `{fmt(s['latest_verified_output'])}` | "
        f"`{fmt(s['best_output'])}` | {'Yes' if s['latest_improves_previous_best'] else 'No'} |"
        for s in summaries
    )
    week12 = ""
    if week == 12:
        week12 = (
            "\nThe submitted proposals use `kappa = 0.1`, deliberately favouring "
            "predicted mean over uncertainty. The non-submission appendix compares "
            "kappa values `0.1`, `0.5`, `1.0`, and `2.0`, Expected Improvement, wider "
            "GP bounds, and Sobol candidates for F6–F8. F4 remains stable; F7's "
            "original common-candidate comparison clearly separates low-kappa "
            "exploitation from high-kappa uncertainty seeking.\n"
        )
    return f"""## Week {week}

### Strategy and evidence position

The week used {WEEK_METHOD[week]}. The latest verified observations produced new
within-function incumbents for: **{improved_text}**. {WEEK_LEARNING[week]}
{week12}
| Function | Verified observations | Latest return | Incumbent | New best? |
| --- | ---: | ---: | ---: | :---: |
{rows}

### Reflection and next step

The main lesson is to judge each strategy through verified within-function
improvement, not raw cross-function values or model predictions alone. The next
step was to {WEEK_NEXT[week]}. Evidence gaps remain explicit, and proposals are
kept separate from observations until authoritative returns arrive.
"""


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    weekly: dict[int, list[dict]] = {}
    for week in range(1, 13):
        weekly[week] = []
        for function in range(1, 9):
            path = root / f"Week_{week:02d}" / f"Function_{function:02d}"
            summary = json.loads((path / "04_Results" / "summary.json").read_text())
            weekly[week].append(summary)
            (path / "07_Reflection" / "README.md").write_text(
                function_reflection(summary), encoding="utf-8"
            )

    introduction = """# Consolidated academic reflections: Weeks 1–12

This document consolidates the function-level reflections by week. Each table
uses cumulative evidence available at that checkpoint and compares results only
within the same black-box function. A proposal is never counted as an observed
result until its authoritative objective value is recorded.

The learning sequence is: manual/random baselines, Gaussian Process surrogates,
acquisition functions, exploration/exploitation control, data-lineage failure
and recovery, an immutable ledger, and a low-kappa sensitivity experiment.

"""
    content = introduction + "\n".join(
        weekly_section(week, weekly[week]) for week in range(1, 13)
    )
    (root / "Reflections" / "README.md").write_text(content, encoding="utf-8")
    print("Regenerated 96 function reflections and 12 consolidated week sections")


if __name__ == "__main__":
    main()
