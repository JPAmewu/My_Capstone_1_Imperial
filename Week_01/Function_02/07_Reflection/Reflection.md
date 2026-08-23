# Function 2 Reflection

## Week 1

### Technique Used
Random Search

### Starter-baseline incumbent
`0.6112052157614438` at query 10.

### Observations.
The ten starter rows provide a useful baseline but are too sparse to establish
the surface shape or a global optimum.

### Lessons Learned
Random search gives coverage but does not use observed structure efficiently.

### Week 2 Strategy
Consider a reproducible surrogate and acquisition function in a later round,
without treating its proposal as evidence before a return is recorded.
