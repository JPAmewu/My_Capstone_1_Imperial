# Week 01 Function 03

## Objective

Function 3 is a three-dimensional black-box maximisation problem. In line with
the Week 1 main notebook, this checkpoint is a model-free Grid Search baseline
over 15 starter observations; it does not claim a GP-UCB proposal.

## Week 1 strategy

Grid Search

## Week 1 result

The starter-sample incumbent is query 4 at
`[0.49258141463713434, 0.6115931882759961, 0.3401763860035727]`, with output
`-0.034835313350078584`.

## Later-round plan

Introduce a reproducible surrogate and acquisition function only in a later
checkpoint, and append proposals only after authoritative returns exist.
