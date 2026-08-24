# Evaluation: optimisation, surrogate calibration, and robustness

## Evaluation questions

The capstone has three related but non-interchangeable evaluation targets.

| Evaluation target | Question | Evidence | What it cannot establish |
| --- | --- | --- | --- |
| Optimisation performance | Did a returned query improve the within-function incumbent? | Immutable returned-pair ledger and best-so-far trajectory | Predictive accuracy, calibrated uncertainty, or global optimality |
| Surrogate accuracy and calibration | Does a GP trained on the historical prefix predict the next return, and do predictive intervals cover at nominal rates? | 96 one-step-ahead rolling folds | Independent-distribution generalisation or recommendation quality |
| Recommendation policy | Why was each Week 13 acquisition selected before outcomes? | Pre-outcome function-specific UCB/EI/PI record | A statistically controlled acquisition comparison |

Keeping these targets separate prevents a high predicted value from being called
an optimisation success and prevents a stable recommendation from being called
an accurate model.

## Optimisation performance

Across the 96 recovered weekly returned pairs, ten established a new
within-function incumbent. Week 12 contributed five: F3 (`+0.012206`), F4
(`+2.351050`), F5 (`+2081.120`), F6 (`+0.176443`), and F7 (`+0.116896`).
The resulting raw improvement rate is `10/96 = 10.4%`.
This descriptive rate is conditional on different functions, strategies, and
adaptive histories; it is not a controlled comparison of acquisition methods.

Best observed values after Week 12 are approximately `7.710875e-16`,
`0.6112052`, `-0.02262932`, `0.3699753`, `3546.632`, `-0.5378218`, `2.266802`,
and `9.939904` for F1–F8. They are incumbents, not proven global optima.

## Rolling historical GP validation

For each function, the starter data train the first GP. Each historical returned
query is then predicted using only observations available before that return;
the true value is held out, scored, appended, and the process repeats. This
creates twelve chronological folds per function and 96 folds in total without
look-ahead leakage. Every fold refits a Matérn-5/2 GP with target normalisation,
the canonical kernel bounds, one optimiser restart, and a deterministic seed.

| Function | RMSE | Mean-baseline RMSE | RMSE skill | Mean NLPD | 50% coverage | 80% coverage | 95% coverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| F1 | 0.000176 | 0.000252 | 0.302 | -6.502 | 1.000 | 1.000 | 1.000 |
| F2 | 0.143416 | 0.187096 | 0.233 | -0.652 | 0.500 | 0.833 | 1.000 |
| F3 | 0.032853 | 0.049847 | 0.341 | 6.977 | 0.417 | 0.750 | 0.917 |
| F4 | 2.406150 | 9.648559 | 0.751 | 2.247 | 0.333 | 0.750 | 0.833 |
| F5 | 615.634318 | 1133.470118 | 0.457 | 13.574 | 0.417 | 0.667 | 0.667 |
| F6 | 0.240410 | 0.562546 | 0.573 | -0.289 | 0.500 | 0.583 | 0.750 |
| F7 | 0.439857 | 1.013354 | 0.566 | 2.062 | 0.250 | 0.500 | 0.667 |
| F8 | 0.132685 | 1.391781 | 0.905 | -0.467 | 0.833 | 1.000 | 1.000 |

All eight functions have positive RMSE skill relative to predicting the historical
training mean. Raw RMSE is reported within each function only because objective
scales differ. With twelve folds, one miss moves coverage by 8.3 percentage points.
F5–F7 materially under-cover at 95%. F1, F2, and F8 over-cover, indicating
conservative intervals. These are calibration diagnostics, not claims that one
function is easier or more important.

Mean negative log predictive density (NLPD) evaluates the full predictive
distribution: lower values reward concentrated probability around realised
returns, while large positive values penalise overconfident misses. NLPD is
scale-sensitive and is interpreted within each function, alongside RMSE and
coverage rather than as a cross-function ranking.

![Rolling GP coverage and uncertainty diagnostics](../Figures/gp_rolling_validation_diagnostics.png)

## Fitted GP hyperparameters

Final models use the canonical post-Week-12 counts and three optimiser restarts.
The length-scale vector is anisotropic and follows input-coordinate order.

| Function | Constant | Length scales | Noise | Parameters at bounds |
| --- | ---: | --- | ---: | --- |
| F1 | 1.41109 | `[2.000, 0.0455]` | `1.58e-8` | L1 upper |
| F2 | 0.76778 | `[0.0461, 2.000]` | `1e-2` | L2 upper; noise upper |
| F3 | 1.91209 | `[2.000, 1.796, 0.0789]` | `0.00218` | L1 upper |
| F4 | 14.2282 | `[1.765, 1.752, 1.775, 1.802]` | `0.00179` | none |
| F5 | 2.85782 | `[2.000, 0.258, 0.720, 2.000]` | `1e-10` | L1/L4 upper; noise lower |
| F6 | 4.32511 | `[1.171, 0.837, 1.125, 1.874, 2.000]` | `0.00113` | L5 upper |
| F7 | 0.72181 | `[0.647, 0.449, 1.863, 0.403, 0.291, 0.753]` | `1.08e-10` | none |
| F8 | 0.95206 | `[1.243, 2.000, 1.016, 2.000, 2.000, 2.000, 1.299, 2.000]` | `1e-10` | L2/L4/L5/L6/L8 upper; noise lower |

Six final fits reach at least one configured bound; F4 and F7 do not. Upper-bound length scales imply that
the fitted surface is very smooth along those coordinates relative to the
configured domain; they do not prove irrelevance. Noise at the lower bound means
the model estimates negligible independent noise under its assumptions, not that
the objective is known to be noiseless. F2's upper-bound noise estimate and F8's
five upper-bound length scales are particularly important modelling diagnostics.
Wider-bound sensitivity is therefore reported separately rather than used to
rewrite the submitted Week 12 experiment.

## Week 13 acquisition justification

Before any Week 13 outcomes, UCB was selected for F1/F4/F7/F8 to retain
uncertainty-led exploration, EI for F2/F5/F6 to balance improvement around
promising Week 12 regions, and PI for F3 for controlled exploitation after its
new incumbent. The policy is adaptive and heuristic. It is not randomised and
does not provide a statistically controlled comparison among acquisition rules.
The diagnostics in the Week 13 strategy and acquisition-comparison files are
evaluated at the exact six-decimal coordinates submitted to the portal.

## Week 13 boundary-generation sensitivity

The frozen proposals remain unchanged. A diagnostic rerun replaced clipped
Gaussian local perturbations with reflected perturbations while holding the GP,
seeds, Sobol candidates, counts, scales, evidence, and acquisition rules fixed.
F2, F5, and F6 no longer selected an exact boundary coordinate under reflection.
F5 remained very close to its three upper boundaries (`0.999459`, `0.996407`,
`0.988539`) and only `0.0204` Euclidean distance from the frozen query, so its
boundary-region recommendation is substantively robust even though the exact
boundary values are partly induced by clipping. F2 and F6 moved materially.
Full results are in [`week_13_boundary_generation_sensitivity.csv`](../Week_13/04_Results/week_13_boundary_generation_sensitivity.csv).

## Limitations and judgement

- The 96 folds are chronological and leakage-free but arise from adaptive,
  non-random queries; they are not an independent test distribution.
- Twelve folds per function give coarse coverage estimates.
- Hyperparameter fitting sometimes produces convergence warnings and boundary
  estimates, indicating weak identification or restrictive bounds.
- RMSE is meaningful only within a function; calibration coverage and
  standardised residuals are more comparable across scales.
- Absolute regret is unavailable because the true functions and optima are
  unknown.

Overall, the evaluation is ready to share with these caveats. It demonstrates
predictive value for most functions, identifies material calibration failures,
and keeps recommendation sensitivity distinct from returned optimisation gains.
