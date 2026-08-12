import tempfile
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

from Code.candidate_generation import hybrid_candidates, make_rng, uniform_candidates
from Code.data_loading import load_numpy_pair, load_starter_data
from Code.data_validation import duplicate_mask, validate_observations
from Code.eda import observation_summary, observations_frame, running_best
from Code.gaussian_process import fit_gaussian_process, predict_with_uncertainty
from Code.plotting import plot_function_diagnostics, plot_proposal_overview
from Code.query_selection import expected_improvement, select_query, upper_confidence_bound


class ReusableCodeTests(unittest.TestCase):
    def setUp(self):
        self.X = np.array([[0.0, 0.0], [0.5, 0.5], [1.0, 1.0]])
        self.y = np.array([0.0, 1.0, 0.25])

    def test_validation_and_duplicates(self):
        X, y = validate_observations(self.X, self.y, dimensions=2)
        self.assertEqual(X.shape, (3, 2)); self.assertEqual(y.shape, (3,))
        mask = duplicate_mask([[0.5000004, 0.5], [0.2, 0.3]], X)
        self.assertEqual(mask.tolist(), [True, False])
        with self.assertRaises(ValueError):
            validate_observations(self.X, self.y[:2])

    def test_safe_loading_and_starter_data(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); np.save(root / "X.npy", self.X); np.save(root / "y.npy", self.y)
            X, y = load_numpy_pair(root / "X.npy", root / "y.npy", dimensions=2)
            self.assertEqual((X.shape, y.shape), ((3, 2), (3,)))
        starter_X, starter_y = load_starter_data(1)
        self.assertEqual(starter_X.shape[1], 2); self.assertEqual(len(starter_X), len(starter_y))

    def test_eda(self):
        self.assertEqual(running_best(self.y).tolist(), [0.0, 1.0, 1.0])
        summary = observation_summary(self.X, self.y)
        self.assertEqual(summary["best_query_number"], 2)
        self.assertEqual(list(observations_frame(self.X, self.y).columns), ["x1", "x2", "output", "query", "running_best"])

    def test_candidates_are_reproducible(self):
        first = uniform_candidates(2, 5, rng=make_rng(12))
        second = uniform_candidates(2, 5, rng=make_rng(12))
        np.testing.assert_allclose(first, second)
        points, sources = hybrid_candidates(self.X[1], rng=make_rng(7), global_count=4, local_count=3)
        self.assertEqual(points.shape, (7, 2)); self.assertEqual(sources.tolist().count("local"), 3)

    def test_gp_prediction_and_query_selection(self):
        model = fit_gaussian_process(self.X, self.y, optimizer_restarts=0)
        candidates = np.array([[0.5, 0.5], [0.45, 0.55], [0.2, 0.8]])
        mean, std = predict_with_uncertainty(model, candidates)
        choice = select_query(candidates, self.X, mean, std, method="ucb", kappa=2.0)
        self.assertFalse(np.allclose(choice.query, [0.5, 0.5]))
        self.assertEqual(upper_confidence_bound([1], [0.5], kappa=2).tolist(), [2.0])
        self.assertGreaterEqual(expected_improvement([1], [0.5], best=0.5)[0], 0)

    def test_plotting_returns_figures(self):
        first = plot_function_diagnostics(self.X, self.y)
        second = plot_proposal_overview(["F1", "F2"], [0.1, 0.2], [0.3, 0.4])
        self.assertGreaterEqual(len(first.axes), 4); self.assertEqual(len(second.axes), 2)


if __name__ == "__main__":
    unittest.main()
