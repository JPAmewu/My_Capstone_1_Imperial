# Week 01 Function 05

## Objective

Function 5 is a four-dimensional black-box maximisation problem. In line with
the Week 1 main notebook, this checkpoint is a model-free Manual Reasoning
baseline over 20 starter observations; it does not claim a GP-UCB proposal.

## Week 1 strategy

Manual Reasoning

## Week 1 result

The starter-sample incumbent is query 16 at
`[0.22418902330288348, 0.8464804904862864, 0.8794841797090803, 0.8785156842249731]`,
with output `1088.8596181962705`.

## Later-round plan

Introduce a reproducible surrogate and acquisition function only in a later
checkpoint, and append proposals only after authoritative returns exist.
