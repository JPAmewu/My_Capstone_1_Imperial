# Function 7 Reflection
## Week 1

### Technique Used
Bayesian Optimisation

### Starter-baseline incumbent
`1.3649683044991994` at query 7.

### Observations
The 30 starter rows identify query 7 as the within-function incumbent. This is
a promising observed region, but output magnitudes are not comparable across
functions and the starter sample does not establish a global optimum.

### Lessons Learned
The Bayesian Optimisation label is insufficient for reproducibility without
the fitted model, preprocessing choices, acquisition rule, and candidate search.

### Week 2 Strategy
For a later round, preserve the surrogate and acquisition configuration,
balance local exploitation with exploration, and wait for the returned value
before treating a proposal as evidence.
