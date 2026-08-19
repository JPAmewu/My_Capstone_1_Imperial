# Week 08 Function 04 reflection

## Objective

Review Function 04 at the Week 8 checkpoint and decide what the
verified evidence implies for the next optimisation step.

## Strategy and work completed

I used GP-UCB within the Week 8 workflow. I validated
all 38 cumulative observations, kept the
analysis within this function's 4-dimensional space, and
checked the response trace, running incumbent, bounds, and provenance.

## Evidence and result

The latest verified return `-28.73632` did not exceed the incumbent `-1.981075`. The verified incumbent occurs at query 33 with
input `[0.394519,0.361122,0.256803,0.461856]`. Progress is
defined only against earlier Function 04 values; objective magnitudes
are not ranked across functions.

## Critical reflection

A shared pipeline reduced cell-order leakage and made cross-function implementation consistent without comparing incompatible objective scales. For Function 04, the result shows that a
model-guided or plausible query is not evidence of improvement until its exact
return is recorded. The absence of improvement argues against overconfidence in the selected region, not against the acquisition method on the basis of one trial.


## Data quality, limitations, and ethics

Confirmed cumulative evidence is available through Week 8. The response surface and global optimum remain unknown, the
sample is adaptive rather than representative, and sparse coverage becomes more
serious as dimension increases. I therefore avoid causal claims, imputation,
cross-function score comparisons, and retrospective selection of a method after
seeing its result.

## Next step

For the next checkpoint I would use Expected Improvement on reconciled evidence and preserve per-function diagnostics. I would append a point only
after its authoritative return is available and preserve the prior rows as an
immutable audit trail.
