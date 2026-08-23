# Function 3 Reflection
## Week 1

### Technique Used
Grid Search

### Starter-baseline incumbent
`-0.034835313350078584` at query 4.

### Observations
The 15 starter rows provide a reproducible baseline but are too sparse to
establish the surface shape or a global optimum.

### Lessons Learned
Grid Search provides structured coverage, but a limited grid can miss narrow
high-value regions in a nonlinear three-dimensional space.

### Week 2 Strategy
Consider a reproducible surrogate and acquisition function in a later round,
without treating its proposal as evidence before a return is recorded.
