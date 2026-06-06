# Week 1 Reflection

## Overview

The objective was to maximise eight unknown black-box functions using one query per function.

Different optimisation techniques were explored to understand how each strategy performs under limited information.

## Techniques Used

| Function | Technique |

|----------|-----------|

| Function 1 | Random Search |

| Function 2 | Random Search |

| Function 3 | Grid Search |

| Function 4 | Grid Search |

| Function 5 | Manual Reasoning |

| Function 6 | Manual Reasoning |

| Function 7 | Bayesian Optimisation |

| Function 8 | Bayesian Optimisation |

## Results

| Function | Output |

|----------|----------|

| Function 1 | -1.560646704467778e-117 |

| Function 2 | -0.03182956281754251 |

| Function 3 | -0.04090761844901528 |

| Function 4 | -8.727516493155957 |

| Function 5 | 1088.8535114737463 |

| Function 6 | -1.1520351120911565 |

| Function 7 | 1.0510148516295004 |

| Function 8 | 9.8157087929671 |

## Ranking of Functions
Rank          Function       Output        Technique
1             F5             1088.8535     Manual Reasoning
2             F8             9.8157        Bayesian Optimisation
3             F7             1.0510        Bayesian Optimisation
4             F2             -0.0318       Random Search
5             F3             -0.0409       Grid Search
6             F6             -1.1520       Manaul Reasoning
7             F4             -8.7275       Grid Search
8             F1             -1.566e-117   Random Search

## Ranking of Optimisation Techniques
Rank          Techniques      Functions    Average
1             Manual          F5,F6        543.8507
2             Bayesian        F7,F8        5.4334
3             Random Search   F1,F4        -0.0159
4             Grid            F3,F4        -4.3842

## Key Observations

- Manual Reasoning performed exceptionally well for Function 5.

- Bayesian Optimisation performed strongly for Functions 7 and 8.

- Random Search produced mixed results.

- Grid Search was less successful on Functions 3 and 4.

## Week 2 Strategy

- Continue exploiting Functions 5, 7 and 8.

- Refine search regions around promising points.

- Explore alternative regions for Functions 1, 3, 4 and 6.

- Use Week 1 results to guide Week 2 query selection.
