# Week 01 Function 04

## Objective

Function 4 is a four-dimensional black-box maximisation problem. In line with
the Week 1 main notebook, this checkpoint is a model-free Grid Search baseline
over 30 starter observations; it does not claim a GP-UCB proposal.

## Week 1 strategy

Grid Search

## Week 1 result

The starter-sample incumbent is query 28 at
`[0.5777656143780968, 0.4287717415443063, 0.4258258674882194, 0.24900741466191134]`,
with output `-4.025542281908162`.

## Later-round plan

Introduce a reproducible surrogate and acquisition function only in a later
checkpoint, and append proposals only after authoritative returns exist.
