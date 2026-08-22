# Week 10 Function 05 reflection

## Objective

Review Function 05 at the Week 10 checkpoint and decide what the
verified evidence implies for the next optimisation step.

## Strategy and work completed

I used GP-UCB within the Week 10 workflow. I validated
all 30 cumulative observations, kept the
analysis within this function's 4-dimensional space, and
checked the response trace, running incumbent, bounds, and provenance.

## Evidence and result

The latest verified return `1424.637` did not exceed the incumbent `1465.512`. The verified incumbent occurs at query 28 with
input `[0.08123,0.992582,0.156202,0.988421]`. Progress is
defined only against earlier Function 05 values; objective magnitudes
are not ranked across functions.

## Critical reflection

One transparent target-normalisation path made GP diagnostics easier to interpret and reproduce. For Function 05, the result shows that a
model-guided or plausible query is not evidence of improvement until its exact
return is recorded. The absence of improvement argues against overconfidence in the selected region, not against the acquisition method on the basis of one trial.


## Data quality, limitations, and ethics

Confirmed cumulative evidence is available through Week 10. The response surface and global optimum remain unknown, the
sample is adaptive rather than representative, and sparse coverage becomes more
serious as dimension increases. I therefore avoid causal claims, imputation,
cross-function score comparisons, and retrospective selection of a method after
seeing its result.

## Next step

For the next checkpoint I would quarantine unverified arrays and reconstruct the modelling state from canonical evidence. I would append a point only
after its authoritative return is available and preserve the prior rows as an
immutable audit trail.
