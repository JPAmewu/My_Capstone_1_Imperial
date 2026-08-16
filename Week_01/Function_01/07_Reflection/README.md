# Week 01 Reflection

**Function 01**

## Objectives

Establish a baseline for the unknown two-dimensional function and identify a
promising point using the available starter observations.

## Work completed

I validated the ten input/output pairs, used random search as the Week 1
strategy, identified the best observed point, and reviewed objective and
running-best plots.

## Key learning

Random search is useful for initial coverage when little is known, but it does
not use accumulated evidence or uncertainty to select the next point.

## Challenges

The outputs are extremely close to zero across much of the observed space, so
the small numerical differences are difficult to interpret as a strong region.

## Decisions and reasoning

I treated query 3 as the best observed point because maximisation requires the
largest recorded output. I did not compare its raw value with other functions,
because their objective scales are unrelated.

## Results and interpretation

The best starter point was approximately `[0.731024, 0.733000]`, with output
`7.710875e-16`. The subsequently submitted random-search point returned
`-1.560646704467778e-117`, so it did not improve the starter best.

## Limitations and ethical considerations

Ten observations cannot establish the global optimum or reliable surface
shape. The result is sensitive to sparse sampling and floating-point scale.
Responsible reporting requires preserving provenance and avoiding exaggerated
claims of optimality.

## Improvements and next steps

For the next week, which is the second week, I will continue to use a Gaussian Process with explicit uncertainty and a reproducible acquisition
strategy in Week 2, while retaining duplicate, bounds, and dimensional checks.
