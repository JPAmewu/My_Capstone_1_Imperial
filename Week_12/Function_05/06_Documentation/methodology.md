# Week 12 Function 05 methodology

## Purpose

Provide a notebook-independent audit of the cumulative evidence recoverable at the Week 12 review point.

## Corrections applied

- Removed notebook-cell-order and environment-specific path dependencies.
- Replaced implicit display calls with explicit tables and Matplotlib figures.
- Consolidated fragmented plots into one response trace and coordinate heatmap.
- Replaced cross-function or correlation-based performance claims with within-function evidence comparisons.
- Added finite-value, shape, unit-domain, provenance, and evidence-gap checks.
- Kept missing returns missing instead of imputing or presenting proposals as observations.

## Provenance

Starter arrays remain in `Week_01/Function_05/03_Data`. Exact recorded query/return pairs are transcribed in the shared evidence registry from the corrected canonical notebooks. The local `03_Data/provenance.json` records references instead of duplicating source arrays.

## Validation and analysis

The workflow requires finite aligned arrays, 4 input dimensions, and coordinates in the unit hypercube. It identifies the incumbent maximum, reports the latest verified observation, and creates a response trace plus coordinate heatmap.

## Evidence boundary

The submitted Week 12 proposal uses GP-UCB with `kappa = 0.1`, an explicit
exploitation-led decision because the uncertainty bonus is small relative to the
predictive mean. The archived `kappa = 2.0` proposal gives uncertainty twenty
times as much weight. A separate, non-submission appendix compares intermediate
kappa values, Expected Improvement, and wider GP bounds; it does not alter the
canonical proposal or returned-pair ledger.

At this review point, no verified Week 12 return is present; confirmed cumulative evidence is available through Week 11. The original Week 11 arrays remain quarantined and are not used. No value is imputed. Results are descriptive within Function 05; they do not imply causality, global optimality, or cross-function ranking.

## Reproduction

```bash
MPLBACKEND=Agg .venv/bin/python Week_12/Function_05/02_Code/analyse_week_12_function_05.py --write-artifacts
```
