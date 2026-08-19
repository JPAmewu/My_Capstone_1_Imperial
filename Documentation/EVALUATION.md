# Evaluation: optimisation, surrogate calibration, and robustness

## Evaluation questions

The capstone has three related but non-interchangeable evaluation targets.

| Evaluation target | Question | Evidence | What it cannot establish |
| --- | --- | --- | --- |
| Optimisation performance | Did a returned query improve the within-function incumbent? | Immutable returned-pair ledger and best-so-far trajectory | Predictive accuracy, calibrated uncertainty, or global optimality |
| Surrogate accuracy and calibration | Does a GP trained on the historical prefix predict the next return, and do predictive intervals cover at nominal rates? | 88 one-step-ahead rolling folds | Independent-distribution generalisation or recommendation quality |
| Recommendation robustness | Does the selected point persist under kappa, acquisition, GP-bound, and candidate-design changes? | Week 12 sensitivity appendix | Which recommendation produces the best realised objective without returns |

Keeping these targets separate prevents a high predicted value from being called
an optimisation success and prevents a stable recommendation from being called
an accurate model.

## Optimisation performance

Across the 88 recovered weekly returned pairs, five established a new
within-function incumbent: F8 in Weeks 1 and 2, F4 and F7 in Week 3, and F5 in
Week 8. The remaining 83 returns still add information but did not increase the
best observed value. The resulting raw improvement rate is `5/88 = 5.7%`.
This descriptive rate is conditional on different functions, strategies, and
adaptive histories; it is not a controlled comparison of acquisition methods.

Best observed values after Week 11 remain approximately `7.710875e-16`,
`0.6112052`, `-0.03483531`, `-1.981075`, `1465.512`, `-0.7142649`, `2.149905`,
and `9.939904` for F1–F8. They are incumbents, not proven global optima.

## Rolling historical GP validation

For each function, the starter data train the first GP. Each historical returned
query is then predicted using only observations available before that return;
the true value is held out, scored, appended, and the process repeats. This
creates eleven chronological folds per function and 88 folds in total without
look-ahead leakage. Every fold refits a Matérn-5/2 GP with target normalisation,
the canonical kernel bounds, one optimiser restart, and a deterministic seed.

| Function | RMSE | Mean-baseline RMSE | RMSE skill | 50% coverage | 80% coverage | 95% coverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| F1 | 0.000176 | 0.000258 | 0.317 | 1.000 | 1.000 | 1.000 |
| F2 | 0.149677 | 0.136705 | -0.095 | 0.455 | 0.818 | 1.000 |
| F3 | 0.033313 | 0.047272 | 0.295 | 0.455 | 0.727 | 0.909 |
| F4 | 2.458890 | 8.550055 | 0.712 | 0.364 | 0.818 | 0.909 |
| F5 | 382.005320 | 680.252537 | 0.438 | 0.455 | 0.727 | 0.727 |
| F6 | 0.250453 | 0.513140 | 0.512 | 0.455 | 0.545 | 0.727 |
| F7 | 0.456669 | 0.904467 | 0.495 | 0.273 | 0.545 | 0.636 |
| F8 | 0.138411 | 1.347948 | 0.897 | 0.818 | 1.000 | 1.000 |

Seven functions have positive RMSE skill relative to predicting the historical
training mean; F2 is worse than that baseline. Raw RMSE is reported within each
function only because objective scales differ. With eleven folds, one miss moves
coverage by 9.1 percentage points. F5–F7 materially under-cover at 95%, especially
F7 at 63.6%, indicating overconfident intervals. F1 and F8 over-cover, indicating
conservative intervals. These are calibration diagnostics, not claims that one
function is easier or more important.

![Rolling GP coverage and uncertainty diagnostics](../Figures/gp_rolling_validation_diagnostics.png)

## Fitted GP hyperparameters

Final models use the canonical post-Week-11 counts and three optimiser restarts.
The length-scale vector is anisotropic and follows input-coordinate order.

| Function | Constant | Length scales | Noise | Parameters at bounds |
| --- | ---: | --- | ---: | --- |
| F1 | 1.49396 | `[2.000, 0.0498]` | `1e-10` | L1 upper; noise lower |
| F2 | 0.99006 | `[0.0444, 2.000]` | `1e-2` | L2 upper; noise upper |
| F3 | 1.94159 | `[0.496, 2.000, 0.139]` | `0.00197` | L2 upper |
| F4 | 19.1710 | `[1.957, 1.896, 2.000, 2.000]` | `0.00134` | L3–L4 upper |
| F5 | 2.13616 | `[2.000, 0.557, 0.756, 0.416]` | `1e-10` | L1 upper; noise lower |
| F6 | 4.70835 | `[1.153, 0.810, 1.120, 1.902, 2.000]` | `0.00122` | L5 upper |
| F7 | 0.82866 | `[0.644, 0.468, 1.295, 0.391, 0.292, 0.722]` | `1e-10` | noise lower |
| F8 | 0.99029 | `[1.237, 2.000, 1.010, 2.000, 2.000, 2.000, 1.283, 2.000]` | `1e-10` | L2/L4/L5/L6/L8 upper; noise lower |

Every final fit reaches at least one bound. Upper-bound length scales imply that
the fitted surface is very smooth along those coordinates relative to the
configured domain; they do not prove irrelevance. Noise at the lower bound means
the model estimates negligible independent noise under its assumptions, not that
the objective is known to be noiseless. F2's upper-bound noise estimate and F8's
five upper-bound length scales are particularly important modelling diagnostics.
Wider-bound sensitivity is therefore reported separately rather than used to
rewrite the submitted Week 12 experiment.

## Recommendation robustness

The Week 12 sensitivity appendix evaluates UCB at kappa `0.1`, `0.5`, `1.0`, and
`2.0`, Expected Improvement, standard/wider GP bounds, and Sobol candidates for
F6–F8. F4 and F5 are locally stable across all appendix settings. F1–F3 and F8
are model-sensitive. F6 moves through three candidates as exploration weight
increases. F7's original like-for-like comparison is academically useful:
low-kappa UCB chooses higher predicted mean and lower uncertainty, while
high-kappa UCB accepts a lower mean for substantially greater uncertainty.

Robustness is not realised performance. No Week 12 returns are available, so
the sensitivity study can identify stability and dependence but cannot select a
winning acquisition rule retrospectively.

## Limitations and judgement

- The 88 folds are chronological and leakage-free but arise from adaptive,
  non-random queries; they are not an independent test distribution.
- Eleven folds per function give coarse coverage estimates.
- Hyperparameter fitting sometimes produces convergence warnings and boundary
  estimates, indicating weak identification or restrictive bounds.
- RMSE is meaningful only within a function; calibration coverage and
  standardised residuals are more comparable across scales.
- Absolute regret is unavailable because the true functions and optima are
  unknown.

Overall, the evaluation is ready to share with these caveats. It demonstrates
predictive value for most functions, identifies material calibration failures,
and keeps recommendation sensitivity distinct from returned optimisation gains.
