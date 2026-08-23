# Week 01 Function 04 reflection

## Objective

Review Function 04 at the Week 1 checkpoint and decide what the
starter evidence establishes as the optimisation baseline.

## Strategy and work completed

I used grid search within the Week 1 workflow. I validated
all 30 starter observations, kept the
analysis within this function's 4-dimensional space, and
checked the response trace, running incumbent, bounds, and provenance.

## Evidence and result

The starter-sample incumbent occurs at query 28 with
input `[0.5777656143780968,0.4287717415443063,0.4258258674882194,0.24900741466191134]`. Progress is
defined only against earlier Function 04 values; objective magnitudes
are not ranked across functions.

## Critical reflection

Initial methods established coverage, but sparse samples made manual and random choices difficult to justify. For Function 04, the result shows that a
model-guided or plausible query is not evidence of improvement until its exact
return is recorded. The baseline alone does not justify choosing or judging an acquisition method.


## Data quality, limitations, and ethics

The authoritative Week 1 baseline contains the 30 starter observations. The response surface and global optimum remain unknown, the
sample is adaptive rather than representative, and sparse coverage becomes more
serious as dimension increases. I therefore avoid causal claims, imputation,
cross-function score comparisons, and retrospective selection of a method after
seeing its result.

## Next step

For a later checkpoint I would introduce a reproducible surrogate and acquisition function. I would append a point only
after its authoritative return is available and preserve the prior rows as an
immutable audit trail.
