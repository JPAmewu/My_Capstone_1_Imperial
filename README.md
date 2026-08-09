# Bayesian Optimisation for Black-Box Functions

An Imperial College London Machine Learning and Artificial Intelligence
capstone project exploring sequential black-box optimisation with Gaussian
Process (GP) surrogate models and acquisition functions.

## Project documentation

- [Dataset datasheet](DATASET_DATASHEET.md)
- [Model card](MODEL_CARD.md)

The repository records a week-by-week experimental workflow across eight
unknown objective functions. Each round incorporates the previous query
results, analyses the accumulated observations, fits surrogate models, and
proposes the next points to evaluate.

> **Project status:** exploratory coursework in progress. Weeks 1–11 contain
> the substantive notebook progression. The notebooks currently stored under
> Weeks 12–13 repeat the Week 10 workflow and should be treated as placeholders
> until their data lineage and analysis are updated for the relevant week.

## Project goals

- Optimise expensive black-box functions with as few evaluations as possible.
- Use Gaussian Processes to represent predictions and uncertainty.
- Compare manual, exploratory, exploitative, and acquisition-led strategies.
- Study how performance changes as observations accumulate.
- Keep a reproducible record of queries, returned outputs, analysis, and
  reflections.

## Repository structure

```text
.
├── Week_01/ ... Week_13/   Weekly notebooks, queries, and function folders
│   ├── 01_Queries/         Submitted query records or notes
│   ├── 02_Notebook/        Main weekly Jupyter notebook
│   └── Function_01/ ...    Per-function placeholders for data and artefacts
├── Code/                   Reserved for reusable source code
├── Documentation/          Reserved for project documentation
├── Notebooks/              Reserved for consolidated notebooks
├── Reflections/            Weekly learning reflections
├── Resources/              Reserved for references and supporting material
└── README.md                Project overview and notebook index
```

Most per-function folders currently contain README placeholders. The numerical
starter data committed to the repository is under `Week_01`; later notebooks
primarily expect datasets to be uploaded to Google Colab or mounted from Google
Drive.

## Notebook guide

| Week | Notebook focus | Execution state |
| --- | --- | --- |
| 1 | Loads the eight starter datasets, inspects shapes and outputs, establishes simple query heuristics, and plots observations. | Mostly executed |
| 2 | Appends the first returned results and introduces GP regression with an RBF-based kernel, random candidates, and an exploration parameter. | Mostly executed |
| 3 | Reconstructs uploaded data, repairs dimensions, compares manual reasoning with GP-based query selection, and packages the next submission. | Outputs cleared |
| 4 | Continues the GP workflow and examines manual choices, exploration versus exploitation, and sensitivity to dimensionality. | Outputs cleared |
| 5 | Builds the accumulated dataset, parses text results, introduces Matérn kernels and Expected Improvement, and writes query points. | Executed |
| 6 | Adds data-quality checks, scaling, EI and UCB acquisition functions, and a mixture of global and local candidate generation. | Outputs cleared |
| 7 | Emphasises exploitation around the strongest region, cleans malformed arrays, performs EDA, and rebuilds per-function summaries. | Executed |
| 8 | Runs detailed, repeated EDA and separate GP/UCB modelling for all eight functions, including trends, correlations, and candidate searches. | Executed |
| 9 | Parses and appends Week 8 results, checks and repairs dataset length mismatches, performs EDA, and generates later queries. | Mostly executed |
| 10 | Builds the Week 10 dataset from Week 9, performs reusable EDA, fits anisotropic Matérn GP models, and selects Week 11 queries with UCB. | Executed |
| 11 | Appends the confirmed Week 10 observations, creates and analyses the Week 11 dataset, fits GP models, and generates Week 12 query points. | Executed |
| 12 | Repeats the corrected Week 10 workflow; still references Week 9/10 data and emits Week 11 queries. | Placeholder |
| 13 | Repeats the corrected Week 10 workflow; still references Week 9/10 data and emits Week 11 queries. | Placeholder |

## Method

The notebooks evolve, but the common optimisation loop is:

1. Load the accumulated input arrays `X` and objective values `y`.
2. Validate dimensions and inspect the observations.
3. Scale the target where appropriate.
4. Fit a Gaussian Process surrogate.
5. Generate candidate points inside the assumed unit hypercube `[0, 1]^d`.
6. score candidates with an acquisition function such as Expected Improvement
   (EI) or Upper Confidence Bound (UCB).
7. Submit the best candidate, receive its black-box output, and append it to the
   next dataset.

The later notebooks use scikit-learn's `GaussianProcessRegressor`, typically
with RBF or Matérn covariance kernels plus a constant and/or white-noise term.

## Running the notebooks

The notebooks were authored for Google Colab and several contain `/content/...`
paths, Drive mounts, and Colab-specific imports. To reproduce a notebook:

1. Open it in Google Colab.
2. Upload the dataset expected by that week, preserving its filename.
3. Run cells from top to bottom.
4. Review any cell that deletes, truncates, or overwrites data before executing
   it.

Core dependencies used across the notebooks are:

```text
numpy
pandas
matplotlib
seaborn
scipy
scikit-learn
jupyter
```

There are currently no standalone Python modules or automated tests in the
repository. Extracting shared loading, validation, plotting, GP fitting, and
acquisition logic into a tested package would make future experiments easier to
reproduce and maintain.

## Known limitations

- The corrected notebooks now stop on input/output mismatches instead of
  truncating or overwriting source data. Resolving any mismatch still requires
  the original query history, which is not committed here.
- Random candidate search becomes inefficient in higher dimensions, even with
  previously evaluated points excluded at submission precision.
- Weeks 11–13 need distinct notebooks and corrected data lineage.
- Repeated imports and function-specific notebook cells should be consolidated
  into reusable, tested functions.

## Recommended next steps

1. Preserve raw weekly data as immutable inputs and write derived data elsewhere.
2. Add exact shape, bounds, duplicate, and finite-value checks before GP fitting.
3. Extract the repeated workflow into a small Python package with unit tests.
4. Optimise acquisition functions with multi-start numerical optimisation or a
   space-filling candidate design instead of only uniform random sampling.
5. Evaluate GP calibration and acquisition choices with repeatable metrics.
6. Replace the Week 11–13 placeholder notebooks with their actual weekly work.

## Author

JP Amewu<br>
Machine Learning & Artificial Intelligence Programme<br>
Imperial College London, 2026
