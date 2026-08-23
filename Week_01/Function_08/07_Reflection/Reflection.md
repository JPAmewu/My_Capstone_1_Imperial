# Function 8 Reflection
## Week 1

### Technique Used
Bayesian Optimisation

### Starter-baseline incumbent
`9.598482002566342` at query 15.

### Observations
The 40 starter rows identify query 15 as the within-function incumbent. The
later cumulative ledger return improves it, but that return is not part of the
starter baseline and output scales are not comparable across functions.

### Lessons Learned
The Bayesian Optimisation label is insufficient for reproducibility without
the fitted model, preprocessing choices, acquisition rule, and candidate search.

### Week 2 Strategy
For a later round, preserve the surrogate and acquisition configuration,
balance local exploitation with exploration, and wait for the returned value
before treating a proposal as evidence.
