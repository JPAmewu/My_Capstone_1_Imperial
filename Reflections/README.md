# Consolidated academic reflections: Weeks 1–12

This document consolidates the function-level reflections by week. Each table
uses cumulative evidence available at that checkpoint and compares results only
within the same black-box function. A proposal is never counted as an observed
result until its authoritative objective value is recorded.

The learning sequence is: manual/random baselines, Gaussian Process surrogates,
acquisition functions, exploration/exploitation control, data-lineage failure
and recovery, an immutable ledger, and a low-kappa sensitivity experiment.

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

The week used validated GP-UCB with kappa 0.1 and a separate sensitivity appendix. The latest verified observations produced new
within-function incumbents for: **none**. The immutable ledger separated observations from proposals, while low-kappa sensitivity made the exploration/exploitation choice explicit.

The submitted proposals use `kappa = 0.1`, deliberately favouring predicted mean over uncertainty. The non-submission appendix compares kappa values `0.1`, `0.5`, `1.0`, and `2.0`, Expected Improvement, wider GP bounds, and Sobol candidates for F6–F8. F4 remains stable; F7's original common-candidate comparison clearly separates low-kappa exploitation from high-kappa uncertainty seeking.

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
step was to wait for authoritative returns, then evaluate realised improvement without retrospectively changing the submission. Evidence gaps remain explicit, and proposals are
kept separate from observations until authoritative returns arrive.
