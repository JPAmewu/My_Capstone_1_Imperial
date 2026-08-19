# Week 04 Function 08 reflection

## Objective

Review Function 08 at the Week 4 checkpoint and decide what the
verified evidence implies for the next optimisation step.

## Strategy and work completed

I used GP-UCB within the Week 4 workflow. I validated
all 44 cumulative observations, kept the
analysis within this function's 8-dimensional space, and
checked the response trace, running incumbent, bounds, and provenance.

## Evidence and result

The latest verified return `9.254064` did not exceed the incumbent `9.939904`. The verified incumbent occurs at query 42 with
input `[0.16316,0.184786,0.152644,0.083802,0.999322,0.544113,0.184124,0.123846]`. Progress is
defined only against earlier Function 08 values; objective magnitudes
are not ranked across functions.

## Critical reflection

Repairing the evidence chain mattered as much as fitting the model; unverified rows could otherwise move the apparent incumbent. For Function 08, the result shows that a
model-guided or plausible query is not evidence of improvement until its exact
return is recorded. The absence of improvement argues against overconfidence in the selected region, not against the acquisition method on the basis of one trial.


## Data quality, limitations, and ethics

Confirmed cumulative evidence is available through Week 4. The response surface and global optimum remain unknown, the
sample is adaptive rather than representative, and sparse coverage becomes more
serious as dimension increases. I therefore avoid causal claims, imputation,
cross-function score comparisons, and retrospective selection of a method after
seeing its result.

## Next step

For the next checkpoint I would use only reconciled evidence and compare UCB with an improvement-based acquisition. I would append a point only
after its authoritative return is available and preserve the prior rows as an
immutable audit trail.
