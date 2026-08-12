# Academic reflections

This single document consolidates the available learning reflection and links
to the detailed weekly evidence. Technical analysis, data, plots, and query
provenance remain in the canonical weekly notebooks.

## Week 1 reflection

### Context

The first round established a baseline for maximising eight unrelated
black-box functions with one submitted query per function. Random search, grid
search, manual reasoning, and Bayesian optimisation were explored as candidate
strategies.

Because each function has a different objective scale, raw values must be
evaluated within each function rather than ranked or averaged across functions.

### Recorded outcomes

| Function | Initial strategy | Returned value |
| --- | --- | ---: |
| F1 | Random search | `-1.560646704467778e-117` |
| F2 | Random search | `-0.03182956281754251` |
| F3 | Grid search | `-0.04090761844901528` |
| F4 | Grid search | `-8.727516493155957` |
| F5 | Manual reasoning | `1088.8535114737463` |
| F6 | Manual reasoning | `-1.1520351120911565` |
| F7 | Bayesian optimisation | `1.0510148516295004` |
| F8 | Bayesian optimisation | `9.8157087929671` |

### Learning

- Function-specific history is the appropriate basis for judging improvement.
- Strong single observations do not establish that one method is globally
  superior, particularly across objectives with incompatible scales.
- Later rounds should retain exploration while using surrogate uncertainty to
  guide expensive evaluations.
- Query provenance, dimensional validation, and reproducible candidate
  generation are essential for reliable comparisons.

See the [corrected Week 1 notebook](../Week_01/02_Notebook/Week_1_Capstone.ipynb)
for the complete evidence and plots.

## Reflection record for Weeks 2–8

Separate academic reflections were not recorded for Weeks 2–8. The validated
analysis and decisions are preserved in the corresponding notebooks:

| Week | Supporting analysis |
| --- | --- |
| 2 | [Week 2 notebook](../Week_02/02_Notebook/Week_2_Capstone.ipynb) |
| 3 | [Week 3 notebook](../Week_03/02_Notebook/Week_3_Capstone.ipynb) |
| 4 | [Week 4 notebook](../Week_04/02_Notebook/Week_4_Capstone.ipynb) |
| 5 | [Week 5 notebook](../Week_05/02_Notebook/Week_5_Capstone.ipynb) |
| 6 | [Week 6 notebook](../Week_06/02_Notebook/Week_6_Capstone.ipynb) |
| 7 | [Week 7 notebook](../Week_07/02_Notebook/Week_7_Capstone.ipynb) |
| 8 | [Week 8 notebook](../Week_08/02_Notebook/Week_8_Capstone.ipynb) |

No personal reflection is inferred from notebook outputs. Missing reflections
are identified explicitly instead of being filled with invented commentary.
