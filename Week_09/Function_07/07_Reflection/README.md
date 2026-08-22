# Week 09 Function 07 reflection

## Objective

Review Function 07 at the Week 9 checkpoint and decide what the
verified evidence implies for the next optimisation step.

## Strategy and work completed

I used Expected Improvement with an 80/20 local/global candidate mixture within the Week 9 workflow. I validated
all 39 cumulative observations, kept the
analysis within this function's 6-dimensional space, and
checked the response trace, running incumbent, bounds, and provenance.

## Evidence and result

The latest verified return `1.009894` did not exceed the incumbent `2.149905`. The verified incumbent occurs at query 33 with
input `[0.143585,0.302559,0.571101,0.194533,0.395561,0.815792]`. Progress is
defined only against earlier Function 07 values; objective magnitudes
are not ranked across functions.

## Critical reflection

Recovered rounds demonstrated that data lineage can change the modelling state; evidence must be reconciled before optimisation. For Function 07, the result shows that a
model-guided or plausible query is not evidence of improvement until its exact
return is recorded. The absence of improvement argues against overconfidence in the selected region, not against the acquisition method on the basis of one trial.


## Data quality, limitations, and ethics

Confirmed cumulative evidence is available through Week 9. The response surface and global optimum remain unknown, the
sample is adaptive rather than representative, and sparse coverage becomes more
serious as dimension increases. I therefore avoid causal claims, imputation,
cross-function score comparisons, and retrospective selection of a method after
seeing its result.

## Next step

For the next checkpoint I would return to GP-UCB with transparent normalisation and duplicate checks. I would append a point only
after its authoritative return is available and preserve the prior rows as an
immutable audit trail.
