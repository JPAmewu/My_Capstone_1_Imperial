# Week 03 Function 04 reflection

## Objective

Review Function 04 at the Week 3 checkpoint and decide what the
verified evidence implies for the next optimisation step.

## Strategy and work completed

I used GP-UCB within the Week 3 workflow. I validated
all 33 cumulative observations, kept the
analysis within this function's 4-dimensional space, and
checked the response trace, running incumbent, bounds, and provenance.

## Evidence and result

The latest verified return `-1.981075` established a new within-function best. The verified incumbent occurs at query 33 with
input `[0.394519,0.361122,0.256803,0.461856]`. Progress is
defined only against earlier Function 04 values; objective magnitudes
are not ranked across functions.

## Critical reflection

Repeated UCB use showed that a plausible model recommendation still needs a returned value before it counts as progress. For Function 04, the result shows that a
model-guided or plausible query is not evidence of improvement until its exact
return is recorded. The improvement supports the selected region, but one success does not prove the strategy or a global optimum.


## Data quality, limitations, and ethics

Confirmed cumulative evidence is available through Week 3. The response surface and global optimum remain unknown, the
sample is adaptive rather than representative, and sparse coverage becomes more
serious as dimension increases. I therefore avoid causal claims, imputation,
cross-function score comparisons, and retrospective selection of a method after
seeing its result.

## Next step

For the next checkpoint I would retain uncertainty diagnostics and verify every appended query/return pair. I would append a point only
after its authoritative return is available and preserve the prior rows as an
immutable audit trail.
