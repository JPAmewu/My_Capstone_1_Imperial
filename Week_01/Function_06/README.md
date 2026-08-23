# Week 01 Function 06

## Objective

Function 6 is a five-dimensional black-box maximisation problem. In line with
the Week 1 main notebook, this checkpoint is a model-free Manual Reasoning
baseline over 20 starter observations; it does not claim a GP-UCB proposal.

## Week 1 strategy

Manual Reasoning

## Week 1 result

The starter-sample incumbent is query 1 at
`[0.7281861047460138, 0.1546925696237983, 0.7325516687239811, 0.6939965090690888, 0.056401310518258585]`,
with output `-0.7142649478202404`.

## Later-round plan

Introduce a reproducible surrogate and acquisition function only in a later
checkpoint, and append proposals only after authoritative returns exist.
