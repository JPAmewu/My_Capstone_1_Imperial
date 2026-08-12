# Week 01 Reflection

## Objectives

I intended to validate Function 04's supplied observations and use Grid Search to select a defensible maximisation query.

## Work completed

I preserved and validated the starter arrays, produced descriptive evidence and diagnostics, documented the method, and recorded the submitted query and returned value in a reproducible workflow.

## Key learning

Objective values must be interpreted within one black-box function. Improvement means exceeding that function's incumbent, not comparing raw magnitudes across different functions.

## Challenges

The response surface is unknown and the starter set is sparse in 4 dimensions, so interactions and the global maximum cannot be established reliably.

## Decisions and reasoning

I used Grid Search, treated the largest supplied response as the incumbent, kept source data immutable, and separated computation from notebook presentation.

## Results and interpretation

The submitted query was `[0.555555,0.444444,0.222222,0.111111]` and returned `-8.727516493155957`. The generated summary reports its exact difference from the starter incumbent and whether it improved it; the claim is limited to Function 04.

## Limitations and ethical considerations

A small observational sample does not support causal claims. Hidden measurement error or bias could be amplified by optimisation, so provenance, uncertainty, and unsuccessful queries remain visible.

## Improvements and next steps

I would collect additional well-spaced evidence, validate a probabilistic surrogate, inspect uncertainty, and apply a documented acquisition rule with boundary and duplicate checks.

