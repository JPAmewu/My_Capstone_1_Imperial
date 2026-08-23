# Consolidated academic reflections: Weeks 1–13

This document consolidates the function-level reflections by week. Each table
uses cumulative evidence available at that checkpoint and compares results only
within the same black-box function. A proposal is never counted as an observed
result until its authoritative objective value is recorded.
The learning sequence is: manual/random baselines, Gaussian Process surrogates,
acquisition functions, exploration/exploitation control, data-lineage failure
and recovery, an immutable ledger, a low-kappa sensitivity experiment, and an
explicitly adaptive function-specific acquisition policy.

**Evolving nature of my Optimisation since my first few rounds of queries**

The early strategies were largely exploratory: I selected different points to understand the general shape of each black-box function. This occasionally produced great improvements. For example, Function 8 increased from 9.5985 to 9.8157 in week 1 and to 9.9399 in week 2, while in week 3 I improved Function 4 to 1.9811 and Function 7 to 2.1499. However, the process was not yet consistently model-driven. As I progressed toward week 12, my approach became well organised. I compiled and validated every input-output pair; then I fitted a separate anisotropic Matérn Gaussian Process for each function, excluded duplicate candidates, and used acquisition optimization. This new strategy produced the best output values so far for Functions 3, 4, 5, 6 and 7. Function 5 moved to about 3546.63, Function 4 moved from its negative output best to 0.36998, while Functions 3, 6, and 7 also produced the best output so far. Function 2 and Function 8 came close to their earlier output best. Interestingly, Function 1 showed no improvement. Since five best output values were recorded from week 1 to week 11, the BBO produced ten incumbent improvements over 96 weekly returns (10.6%), compared with five improvements over 88 weekly returns (5.68%). For Week 13, I  also compared UCB, Expected Improvement (EI), and Probability of Improvement (PI), rather than automatically applying one rule to every function. For example, UCB for Functions 1, 4, 7, and 8. EI for Functions 2,5, and 6. Then PI for Function 3.



## Week 1

### Strategy and evidence position

The week used baseline manual, random, grid, and Bayesian strategies. The latest verified observations produced new
within-function incumbents for: **F8**. Initial methods established coverage, but sparse samples made manual and random choices difficult to justify.

| Function | Verified observations | Latest return | Incumbent | New best? |
| --- | ---: | ---: | ---: | :---: |
| F1 | 11 | `-1.560647e-117` | `7.710875e-16` | No |
| F2 | 11 | `-0.03182956` | `0.6112052` | No |
| F3 | 16 | `-0.04090762` | `-0.03483531` | No |
| F4 | 31 | `-8.727516` | `-4.025542` | No |
| F5 | 21 | `1088.854` | `1088.86` | No |
| F6 | 21 | `-1.152035` | `-0.7142649` | No |
| F7 | 31 | `1.051015` | `1.364968` | No |
| F8 | 41 | `9.815709` | `9.815709` | Yes |

### Reflection and next step

The main lesson is to judge each strategy through verified within-function
improvement, not raw cross-function values or model predictions alone. The next
step was to replace uninformed search with a reproducible surrogate and acquisition function. Evidence gaps remain explicit, and proposals are
kept separate from observations until authoritative returns arrive.

## Week 2

### Strategy and evidence position

The week used GP-UCB for F1–F4 and F6–F8, with manual local search for F5. The latest verified observations produced new
within-function incumbents for: **F8**. Introducing a surrogate made uncertainty explicit and exposed the need for reproducible, function-specific random streams.

| Function | Verified observations | Latest return | Incumbent | New best? |
| --- | ---: | ---: | ---: | :---: |
| F1 | 12 | `1.674933e-36` | `7.710875e-16` | No |
| F2 | 12 | `0.02266663` | `0.6112052` | No |
| F3 | 17 | `-0.08987475` | `-0.03483531` | No |
| F4 | 32 | `-31.73536` | `-4.025542` | No |
| F5 | 22 | `1035.634` | `1088.86` | No |
| F6 | 22 | `-0.8782406` | `-0.7142649` | No |
| F7 | 32 | `0.3087652` | `1.364968` | No |
| F8 | 42 | `9.939904` | `9.939904` | Yes |

### Reflection and next step

The main lesson is to judge each strategy through verified within-function
improvement, not raw cross-function values or model predictions alone. The next
step was to compare returned performance with the incumbent before refining the acquisition rule. Evidence gaps remain explicit, and proposals are
kept separate from observations until authoritative returns arrive.

## Week 3

### Strategy and evidence position

The week used reproducible GP-UCB for F1–F4 and F6–F8, with local exploration for F5. The latest verified observations produced new
within-function incumbents for: **F4, F7**. Repeated UCB use showed that a plausible model recommendation still needs a returned value before it counts as progress.

| Function | Verified observations | Latest return | Incumbent | New best? |
| --- | ---: | ---: | ---: | :---: |
| F1 | 13 | `-1.075594e-32` | `7.710875e-16` | No |
| F2 | 13 | `0.0486837` | `0.6112052` | No |
| F3 | 18 | `-0.1832388` | `-0.03483531` | No |
| F4 | 33 | `-1.981075` | `-1.981075` | Yes |
| F5 | 23 | `1035.665` | `1088.86` | No |
| F6 | 23 | `-1.339542` | `-0.7142649` | No |
| F7 | 33 | `2.149905` | `2.149905` | Yes |
| F8 | 43 | `8.963604` | `9.939904` | No |

### Reflection and next step

The main lesson is to judge each strategy through verified within-function
improvement, not raw cross-function values or model predictions alone. The next
step was to retain uncertainty diagnostics and verify every appended query/return pair. Evidence gaps remain explicit, and proposals are
kept separate from observations until authoritative returns arrive.

## Week 4

### Strategy and evidence position

The week used GP-UCB for modelled functions and bounded local exploration for F5. The latest verified observations produced new
within-function incumbents for: **none**. Repairing the evidence chain mattered as much as fitting the model; unverified rows could otherwise move the apparent incumbent.

| Function | Verified observations | Latest return | Incumbent | New best? |
| --- | ---: | ---: | ---: | :---: |
| F1 | 14 | `-2.466641e-107` | `7.710875e-16` | No |
| F2 | 14 | `0.03877494` | `0.6112052` | No |
| F3 | 19 | `-0.0825135` | `-0.03483531` | No |
| F4 | 34 | `-9.312812` | `-1.981075` | No |
| F5 | 24 | `163.1225` | `1088.86` | No |
| F6 | 24 | `-2.437508` | `-0.7142649` | No |
| F7 | 34 | `1.208733` | `2.149905` | No |
| F8 | 44 | `9.254064` | `9.939904` | No |

### Reflection and next step

The main lesson is to judge each strategy through verified within-function
improvement, not raw cross-function values or model predictions alone. The next
step was to use only reconciled evidence and compare UCB with an improvement-based acquisition. Evidence gaps remain explicit, and proposals are
kept separate from observations until authoritative returns arrive.

## Week 5

### Strategy and evidence position

The week used GP-UCB for F1–F4 and F6–F8, with Expected Improvement for F5. The latest verified observations produced new
within-function incumbents for: **none**. Comparing UCB with Expected Improvement clarified that acquisition rules express different attitudes to improvement and uncertainty.

| Function | Verified observations | Latest return | Incumbent | New best? |
| --- | ---: | ---: | ---: | :---: |
| F1 | 15 | `7.65121e-239` | `7.710875e-16` | No |
| F2 | 15 | `0.2207807` | `0.6112052` | No |
| F3 | 20 | `-0.0573971` | `-0.03483531` | No |
| F4 | 35 | `-17.92631` | `-1.981075` | No |
| F5 | 25 | `0.9401161` | `1088.86` | No |
| F6 | 25 | `-2.529369` | `-0.7142649` | No |
| F7 | 35 | `0.1907826` | `2.149905` | No |
| F8 | 45 | `9.138609` | `9.939904` | No |

### Reflection and next step

The main lesson is to judge each strategy through verified within-function
improvement, not raw cross-function values or model predictions alone. The next
step was to test a global/local candidate mixture rather than relying on one search geometry. Evidence gaps remain explicit, and proposals are
kept separate from observations until authoritative returns arrive.

## Week 6

### Strategy and evidence position

The week used hybrid global/local candidates, UCB for F1–F4/F6–F7, and EI for F5/F8. The latest verified observations produced new
within-function incumbents for: **none**. Hybrid candidates linked global coverage with local refinement and reduced dependence on a single uniform random search.

| Function | Verified observations | Latest return | Incumbent | New best? |
| --- | ---: | ---: | ---: | :---: |
| F1 | 16 | `6.131855e-211` | `7.710875e-16` | No |
| F2 | 16 | `0.1605315` | `0.6112052` | No |
| F3 | 21 | `-0.1170052` | `-0.03483531` | No |
| F4 | 36 | `-20.87936` | `-1.981075` | No |
| F5 | 26 | `281.9116` | `1088.86` | No |
| F6 | 26 | `-1.31254` | `-0.7142649` | No |
| F7 | 36 | `1.611967` | `2.149905` | No |
| F8 | 46 | `8.557034` | `9.939904` | No |

### Reflection and next step

The main lesson is to judge each strategy through verified within-function
improvement, not raw cross-function values or model predictions alone. The next
step was to evaluate whether deliberate exploitation improves on the verified incumbent. Evidence gaps remain explicit, and proposals are
kept separate from observations until authoritative returns arrive.

## Week 7

### Strategy and evidence position

The week used an exploitation-focused round with local search around verified incumbents. The latest verified observations produced new
within-function incumbents for: **none**. Stronger exploitation did not reliably improve incumbents, demonstrating the risk of repeatedly searching one attractive basin.

| Function | Verified observations | Latest return | Incumbent | New best? |
| --- | ---: | ---: | ---: | :---: |
| F1 | 17 | `-6.738616e-151` | `7.710875e-16` | No |
| F2 | 17 | `0.04871438` | `0.6112052` | No |
| F3 | 22 | `-0.04718314` | `-0.03483531` | No |
| F4 | 37 | `-20.19585` | `-1.981075` | No |
| F5 | 27 | `163.1225` | `1088.86` | No |
| F6 | 27 | `-1.287089` | `-0.7142649` | No |
| F7 | 37 | `0.8994987` | `2.149905` | No |
| F8 | 47 | `8.563639` | `9.939904` | No |

### Reflection and next step

The main lesson is to judge each strategy through verified within-function
improvement, not raw cross-function values or model predictions alone. The next
step was to restore broader exploration where local concentration has not produced improvement. Evidence gaps remain explicit, and proposals are
kept separate from observations until authoritative returns arrive.

## Week 8

### Strategy and evidence position

The week used a consistent reusable GP-UCB workflow across all eight functions. The latest verified observations produced new
within-function incumbents for: **F5**. A shared pipeline reduced cell-order leakage and made cross-function implementation consistent without comparing incompatible objective scales.

| Function | Verified observations | Latest return | Incumbent | New best? |
| --- | ---: | ---: | ---: | :---: |
| F1 | 18 | `-1.7724e-96` | `7.710875e-16` | No |
| F2 | 18 | `0.07276416` | `0.6112052` | No |
| F3 | 23 | `-0.07741316` | `-0.03483531` | No |
| F4 | 38 | `-28.73632` | `-1.981075` | No |
| F5 | 28 | `1465.512` | `1465.512` | Yes |
| F6 | 28 | `-1.479452` | `-0.7142649` | No |
| F7 | 38 | `0.8461801` | `2.149905` | No |
| F8 | 48 | `9.020091` | `9.939904` | No |

### Reflection and next step

The main lesson is to judge each strategy through verified within-function
improvement, not raw cross-function values or model predictions alone. The next
step was to use Expected Improvement on reconciled evidence and preserve per-function diagnostics. Evidence gaps remain explicit, and proposals are
kept separate from observations until authoritative returns arrive.

## Week 9

### Strategy and evidence position

The week used 80% local / 20% global Expected Improvement after evidence recovery. The latest verified observations produced new
within-function incumbents for: **none**. Recovered rounds demonstrated that data lineage can change the modelling state; evidence must be reconciled before optimisation.

| Function | Verified observations | Latest return | Incumbent | New best? |
| --- | ---: | ---: | ---: | :---: |
| F1 | 19 | `-3.089424e-96` | `7.710875e-16` | No |
| F2 | 19 | `0.04940641` | `0.6112052` | No |
| F3 | 24 | `-0.08189345` | `-0.03483531` | No |
| F4 | 39 | `-23.4228` | `-1.981075` | No |
| F5 | 29 | `430.8031` | `1465.512` | No |
| F6 | 29 | `-1.171713` | `-0.7142649` | No |
| F7 | 39 | `1.009894` | `2.149905` | No |
| F8 | 49 | `9.699892` | `9.939904` | No |

### Reflection and next step

The main lesson is to judge each strategy through verified within-function
improvement, not raw cross-function values or model predictions alone. The next
step was to return to GP-UCB with transparent normalisation and duplicate checks. Evidence gaps remain explicit, and proposals are
kept separate from observations until authoritative returns arrive.

## Week 10

### Strategy and evidence position

The week used normalised Gaussian Processes with reproducible GP-UCB. The latest verified observations produced new
within-function incumbents for: **none**. One transparent target-normalisation path made GP diagnostics easier to interpret and reproduce.

| Function | Verified observations | Latest return | Incumbent | New best? |
| --- | ---: | ---: | ---: | :---: |
| F1 | 20 | `-4.592141e-89` | `7.710875e-16` | No |
| F2 | 20 | `0.02678837` | `0.6112052` | No |
| F3 | 25 | `-0.0463388` | `-0.03483531` | No |
| F4 | 40 | `-15.12573` | `-1.981075` | No |
| F5 | 30 | `1424.637` | `1465.512` | No |
| F6 | 30 | `-1.449089` | `-0.7142649` | No |
| F7 | 40 | `0.8456374` | `2.149905` | No |
| F8 | 50 | `9.373668` | `9.939904` | No |

### Reflection and next step

The main lesson is to judge each strategy through verified within-function
improvement, not raw cross-function values or model predictions alone. The next
step was to quarantine unverified arrays and reconstruct the modelling state from canonical evidence. Evidence gaps remain explicit, and proposals are
kept separate from observations until authoritative returns arrive.

## Week 11

### Strategy and evidence position

The week used corruption-aware GP-UCB using only canonical-ledger evidence. The latest verified observations produced new
within-function incumbents for: **none**. Quarantining suspicious arrays prevented corrupted or unprovenanced rows from becoming model evidence.

| Function | Verified observations | Latest return | Incumbent | New best? |
| --- | ---: | ---: | ---: | :---: |
| F1 | 21 | `8.15922e-130` | `7.710875e-16` | No |
| F2 | 21 | `0.06529973` | `0.6112052` | No |
| F3 | 26 | `-0.03844613` | `-0.03483531` | No |
| F4 | 41 | `-14.99267` | `-1.981075` | No |
| F5 | 31 | `210.0383` | `1465.512` | No |
| F6 | 31 | `-1.154424` | `-0.7142649` | No |
| F7 | 41 | `1.478174` | `2.149905` | No |
| F8 | 51 | `9.276069` | `9.939904` | No |

### Reflection and next step

The main lesson is to judge each strategy through verified within-function
improvement, not raw cross-function values or model predictions alone. The next
step was to generate Week 12 proposals only after ledger checksum and count validation. Evidence gaps remain explicit, and proposals are
kept separate from observations until authoritative returns arrive.

## Week 12

### Strategy and evidence position

The week used validated GP-UCB with kappa 0.1 and a separate sensitivity appendix. Once the authoritative Week 12 returns were reconciled, the latest observations produced new within-function incumbents for: **F3, F4, F5, F6 and F7**. This was the strongest single round of incumbent improvement in the verified sequence. The immutable ledger separated observations from proposals, while low-kappa sensitivity made the exploration/exploitation choice explicit.

The submitted proposals use `kappa = 0.1`, deliberately favouring predicted mean over uncertainty. The non-submission appendix compares kappa values `0.1`, `0.5`, `1.0`, and `2.0`, Expected Improvement, wider GP bounds, and Sobol candidates for F6–F8. F4 remains stable; F7's original common-candidate comparison clearly separates low-kappa exploitation from high-kappa uncertainty seeking.

| Function | Verified observations | Latest return | Incumbent | New best? |
| --- | ---: | ---: | ---: | :---: |
| F1 | 22 | `-1.623962e-106` | `7.710875e-16` | No |
| F2 | 22 | `0.6073819` | `0.6112052` | No |
| F3 | 27 | `-0.02262932` | `-0.02262932` | Yes |
| F4 | 42 | `0.3699753` | `0.3699753` | Yes |
| F5 | 32 | `3546.632` | `3546.632` | Yes |
| F6 | 32 | `-0.5378218` | `-0.5378218` | Yes |
| F7 | 42 | `2.266802` | `2.266802` | Yes |
| F8 | 52 | `9.926835` | `9.939904` | No |

### Reflection and next step

The main lesson is that exploitation can be productive when it is grounded in a
reconciled modelling state, but the five improvements do not establish that low
kappa is generally superior. There was no randomised acquisition assignment or
counterfactual evaluation. The correct next step was therefore to use the new
incumbents as evidence, reconsider the acquisition rule function by function,
and record those choices before observing Week 13 outcomes.

## Week 13

### Strategy and evidence position

The canonical Week 13 notebook begins from **96 verified returned pairs across
Weeks 1–12** and proposes one new point for each function. Week 13 outcomes have
not been observed. The proposal set is therefore excluded from incumbent
counts, empirical performance claims, and the immutable return ledger.

Rather than applying one acquisition rule uniformly, the notebook compares UCB,
Expected Improvement (EI), and Probability of Improvement (PI) within each
function's fitted anisotropic Matérn-5/2 Gaussian Process. The policy was fixed
after the Week 12 returns and before any Week 13 outcomes. It is an adaptive
heuristic, not a randomised or statistically controlled comparison of
acquisition functions.

| Function | Verified observations | Week 12 position | Week 13 acquisition | Proposed query | Pre-outcome rationale |
| --- | ---: | --- | --- | --- | --- |
| F1 | 22 | Sparse near-zero signal | UCB | `0.987450-0.502905` | Preserve uncertainty-led exploration where useful signal remains sparse. |
| F2 | 22 | Return close to incumbent | EI | `0.686305-0.999999` | Balance local improvement with uncertainty around a promising region. |
| F3 | 27 | New incumbent | PI | `0.685419-0.626770-0.366737` | Use controlled exploitation after a stable new best. |
| F4 | 42 | Large new incumbent improvement | UCB | `0.332326-0.427941-0.445087-0.470215` | Test uncertainty around the improved region rather than collapse to pure exploitation. |
| F5 | 32 | Much stronger new incumbent | EI | `0.035438-0.999999-0.999999-0.999999` | Seek further improvement near the strengthened incumbent. |
| F6 | 32 | New incumbent | EI | `0.395407-0.091768-0.662260-0.806631-0.000000` | Exploit the improved region while retaining uncertainty protection. |
| F7 | 42 | New incumbent | UCB | `0.186669-0.174973-0.820528-0.287970-0.334213-0.844074` | Combine local focus with moderate exploration. |
| F8 | 52 | Near-best return in eight dimensions | UCB | `0.032909-0.091943-0.072309-0.221801-0.904654-0.989379-0.024400-0.951853` | Retain strong exploration because dimensional sparsity remains substantial. |

All proposals are finite, bounded by `0.999999`, formatted to six decimal
places, and distinct from the 96 evaluated points. Candidate selection uses
45,056 points per function and records the fitted kernel, predictive mean,
predictive standard deviation, acquisition score, and distance from the
incumbent. These diagnostics make the decision reproducible, but they do not
convert model expectations into observed outcomes.

### Reflection and next step

Week 13 marks a shift from using one broadly preferred acquisition rule to
making the exploration–exploitation decision conditional on each function's
evidence. This is methodologically more defensible than treating heterogeneous
response surfaces as interchangeable. It also creates a new responsibility:
because the policy is adaptive, later outcomes cannot be used as if they were an
unbiased head-to-head test of UCB, EI, and PI.

The principal academic lesson is epistemic discipline. A well-calibrated model,
a high acquisition score, and a carefully formatted portal query remain
proposals until the black box returns aligned objective values. The next step is
to freeze the eight decisions, collect the Week 13 returns, append them only
after integrity checks, and evaluate realised within-function improvement
without retrospectively changing the stated rationale.
