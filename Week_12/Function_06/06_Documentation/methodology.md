# Week 12 Function 06 methodology

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

Starter arrays remain in `Week_01/Function_06/03_Data`. Exact recorded query/return pairs are transcribed in the shared evidence registry from the corrected canonical notebooks. The local `03_Data/provenance.json` records references instead of duplicating source arrays.

## Validation and analysis

The workflow requires finite aligned arrays, 5 input dimensions, and coordinates in the unit hypercube. It identifies the incumbent maximum, reports the latest verified observation, and creates a response trace plus coordinate heatmap.

## Evidence boundary

At this review point, the corrupted Week 11 arrays remain quarantined and no verified Week 11 or Week 12 return is present. No value is imputed. Results are descriptive within Function 06; they do not imply causality, global optimality, or cross-function ranking.

## Reproduction

```bash
MPLBACKEND=Agg .venv/bin/python Week_12/Function_06/02_Code/analyse_week_12_function_06.py --write-artifacts
```
