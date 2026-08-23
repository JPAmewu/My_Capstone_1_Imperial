# Function 5 Reflection
## Week 1

### Technique Used
Manual Reasoning

### Starter-baseline incumbent
`1088.8596181962705` at query 16.

### Observations
The 20 starter rows contain one value far above most other Function 5 outputs.
That makes the query 16 neighbourhood worth later investigation, but it does
not establish a global optimum or support comparisons with other functions.

### Lessons Learned
Manual Reasoning can identify a promising region, but this observational
baseline cannot isolate the effect of the strategy from the sampled points.

### Week 2 Strategy
Consider a reproducible surrogate and acquisition function in a later round,
while retaining exploration and recording a proposal only after its return is known.
