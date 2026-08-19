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

## Week 12 final reflection

### How have patterns in your past queries influenced your latest choices?

My strategy developed from early manual, random, and grid-based searches into
Gaussian Process surrogates, then Expected Improvement and UCB. Past returns
showed that a visually plausible point or a strong previous value does not
guarantee improvement. I therefore used every verified observation, validated
the post-Week-11 counts, rejected duplicates, and selected `kappa = 0.1` to make
the Week 12 proposal deliberately exploitation-led. This favours high predicted
means while retaining a small uncertainty allowance. The choice is a testable
decision, not a claim that exploitation is always superior.

### Have you identified any clusters or recurring promising regions?

There are function-specific recurring regions, but they vary in credibility.
F2 repeatedly favours a first coordinate near 0.69–0.70; F4's recommendation is
unchanged across acquisition settings and GP bounds; F5 repeatedly favours a
high-output boundary region. F6–F8 are harder to interpret because 31–51 samples
remain sparse in five to eight dimensions. Two-dimensional projections may look
clustered while points remain far apart elsewhere. I therefore describe these
as surrogate-supported regions, not discovered optima.

### Which strategies or parameter choices have proven less effective, and how are you adjusting?

Manual selection and uniform random candidate search became less defensible as
dimension increased. A fixed acquisition setting also hides how strongly a
recommendation depends on uncertainty weighting. The sensitivity appendix keeps
the submitted experiment unchanged but compares UCB at kappa values `0.1`,
`0.5`, `1.0`, and `2.0`, Expected Improvement, and wider GP bounds. It also
replaces 20,000 uniform candidates with 32,768 Sobol points for F6–F8. F4 is
unchanged between `kappa = 0.1` and `kappa = 2.0`; F7 contrasts sharply in the
original common-candidate run: low
kappa chooses higher mean and lower uncertainty, while high kappa accepts lower
mean for greater uncertainty.

### In what ways do your refinements parallel clustering algorithms?

Clustering separates repeatable structure from noise by testing whether groups
persist under different assumptions. My refinements do something similar:
verified query-return pairs define the evidence; the GP smooths local patterns;
the acquisition function decides whether to remain near a promising region or
probe an uncertain one; and sensitivity checks test whether a recommendation
persists when modelling choices change. Stable F4/F5 recommendations resemble
robust clusters. The shifting F1–F3 and F8 recommendations resemble assignments
that are sensitive to scale, distance, or model specification.

### If your query results were plotted, what trends or groupings might appear?

Plots would show adaptive concentration around some incumbents, boundary-seeking
behaviour, and isolated exploratory jumps at larger kappa. They would also expose
the data-lineage interruption: the recovered Week 11 return belongs in the
immutable ledger, whereas Week 12 proposals must remain visually and logically
separate until returns arrive. My next iteration would overlay returned values,
predicted mean, uncertainty, and acquisition setting, then judge strategies by
realised within-function improvement. The main learning is methodological:
manual exploration evolved into probabilistic optimisation, a lineage failure
forced recovery and immutable provenance, and the low-kappa experiment is now
evaluated through sensitivity rather than rewritten after the fact.
