# Week 05 Function 03 reflection

## Objective

Review Function 03 at the Week 5 checkpoint and decide what the
verified evidence implies for the next optimisation step.

## Strategy and work completed

I used GP-UCB within the Week 5 workflow. I validated
all 20 cumulative observations, kept the
analysis within this function's 3-dimensional space, and
checked the response trace, running incumbent, bounds, and provenance.

## Evidence and result

The latest verified return `-0.0573971` did not exceed the incumbent `-0.03483531`. The verified incumbent occurs at query 4 with
input `[0.49258141463713434,0.6115931882759961,0.3401763860035727]`. Progress is
defined only against earlier Function 03 values; objective magnitudes
are not ranked across functions.

## Critical reflection

Comparing UCB with Expected Improvement clarified that acquisition rules express different attitudes to improvement and uncertainty. For Function 03, the result shows that a
model-guided or plausible query is not evidence of improvement until its exact
return is recorded. The absence of improvement argues against overconfidence in the selected region, not against the acquisition method on the basis of one trial.


## Data quality, limitations, and ethics

Confirmed cumulative evidence is available through Week 5. The response surface and global optimum remain unknown, the
sample is adaptive rather than representative, and sparse coverage becomes more
serious as dimension increases. I therefore avoid causal claims, imputation,
cross-function score comparisons, and retrospective selection of a method after
seeing its result.

## Next step

For the next checkpoint I would test a global/local candidate mixture rather than relying on one search geometry. I would append a point only
after its authoritative return is available and preserve the prior rows as an
immutable audit trail.
