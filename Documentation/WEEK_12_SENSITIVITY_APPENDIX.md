# Week 12 sensitivity appendix

## Status and research question

This is a post-submission diagnostic, not a replacement Week 12 experiment.
The canonical submission remains the eight GP-UCB proposals generated with
`kappa = 0.1`. No sensitivity recommendation has been submitted or added to the
immutable returned-pair ledger. The question is whether the recommendation is
stable to exploration weight, acquisition rule, GP hyperparameter bounds, and
candidate coverage.

## Experimental design

Each surrogate was reconstructed from the canonical post-Week-11 counts
`21, 21, 26, 41, 31, 31, 41, 51`. Two Matérn-5/2 GP profiles were fitted: the
canonical bounds and wider constant, length-scale, and noise bounds. Each profile
was evaluated with UCB at `kappa = 0.1, 0.5, 1.0, 2.0` and Expected Improvement
(`xi = 0.01`). Functions 1–5 use 20,000 deterministic uniform candidates.
Functions 6–8 use 32,768 scrambled Sobol candidates because 20,000 random points
leave increasingly sparse coverage in five to eight dimensions. All candidates
are bounded, rounded to six decimals, and checked against prior observations.

The complete 80-row result is in
[`Results/week12_sensitivity_analysis.csv`](../Results/week12_sensitivity_analysis.csv)
and is reproduced by [`Code/run_week12_sensitivity.py`](../Code/run_week12_sensitivity.py).

## Academic evaluation

UCB ranks `mean + kappa × standard deviation`. Therefore `kappa = 0.1`
prioritises exploitation of high predicted values, while `kappa = 2.0` gives the
uncertainty bonus twenty times as much weight. This distinction is visible in
the original like-for-like Week 12 comparison. F4 recommends exactly the same
point at both settings, suggesting the model's highest-mean region and its useful
uncertainty coincide. F7 behaves differently: `kappa = 0.1` selects
`0.108717-0.301229-0.470084-0.228030-0.331784-0.836498` with predicted mean
`2.100446` and standard deviation `0.113192`; `kappa = 2.0` moves to
`0.087492-0.296104-0.894458-0.260860-0.263170-0.806628`, accepting a lower mean
`1.950674` for greater uncertainty `0.214878`. That is a concrete exploitation
versus exploration trade-off rather than a claim that either point is better.

Within the new common-candidate sensitivity experiment, F4 and F5 select one
point under every acquisition and bound profile, so they are locally robust.
F6 produces three alternatives as kappa rises, showing controlled movement from
the predicted basin toward uncertainty. F1–F3 are sensitive to kappa and/or GP
bounds; F3 changes especially strongly under wider bounds. F8 has three standard-
bound alternatives, while its wider-bound fit collapses all five rules to one
candidate. F7 is invariant within the Sobol experiment, which does not contradict
the archived comparison: changing the candidate design changes the finite set
over which acquisition is maximised.

Several optimiser and kernel-bound warnings remain informative diagnostics.
They show that wider bounds do not automatically make a model better and that
scaling, repeated fits, and kernel alternatives deserve testing. Without returned
objective values, this appendix measures recommendation stability—not regret,
improvement, calibration, or global optimality.

## Decision

The submitted `kappa = 0.1` proposals remain unchanged. The sensitivity results
support reporting stability where it exists, treating unstable recommendations
as model-dependent, retaining space-filling candidates in high dimensions, and
using the next authoritative returns to evaluate rather than retrospectively
select among acquisition settings.
