import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from Code.acquisition_function import expected_improvement, probability_improvement, upper_confidence_bound
from Code.candidate_generation import hybrid_candidates, make_rng, reflected_local_candidates, uniform_candidates
from Code.data_loading import load_numpy_pair, load_starter_data
from Code.data_validation import duplicate_mask, validate_observations
from Code.eda import observation_summary, observations_frame, running_best
from Code.gaussian_process import fit_gaussian_process, predict_with_uncertainty
from Code.plotting import plot_function_diagnostics, plot_proposal_overview
from Code.query_selection import select_query
from Code.portal_format import format_portal_query, validate_portal_query, validate_query_file
from Code.weekly_evidence import EVIDENCE_GAPS, recorded_pairs
from Code.weekly_function_review import analyse_weekly_function, load_weekly_evidence, plot_weekly_function
from Code.historical_function_review import analyse_historical_function, proposal_for_week


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
        self.assertGreaterEqual(float(points.min()), 0.0)
        self.assertLessEqual(float(points.max()), 0.999999)
        reflected = reflected_local_candidates([0.0, 0.999999], 100, scale=0.2, rng=make_rng(19))
        repeated = reflected_local_candidates([0.0, 0.999999], 100, scale=0.2, rng=make_rng(19))
        np.testing.assert_allclose(reflected, repeated)
        self.assertTrue(np.all((reflected >= 0.0) & (reflected <= 0.999999)))
        self.assertFalse(np.any((reflected == 0.0) | (reflected == 0.999999)))

    def test_strict_portal_format(self):
        text = format_portal_query([0, 0.1234564, 0.999999], dimensions=3)
        self.assertEqual(text, "0.000000-0.123456-0.999999")
        np.testing.assert_allclose(
            validate_portal_query(text, dimensions=3),
            [0.0, 0.123456, 0.999999],
        )
        for invalid in (
            "0-0.500000",
            "0.000000,0.500000",
            "0.000000-1.000000",
            " 0.000000-0.500000",
            "0.000000-0.50000",
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                validate_portal_query(invalid, dimensions=2)
        with self.assertRaises(ValueError):
            format_portal_query([1.0], dimensions=1)

    def test_week12_query_file_is_portal_valid(self):
        count = validate_query_file(
            Path("Week_12/01_Queries/week_12_query_points.txt"),
            {1: 2, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6, 8: 8},
        )
        self.assertEqual(count, 8)

    def test_week13_query_file_is_portal_valid(self):
        count = validate_query_file(
            Path("Week_13/01_Queries/week_13_query_points.txt"),
            {1: 2, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6, 8: 8},
        )
        self.assertEqual(count, 8)
        payload = Path("Week_13/01_Queries/week_13_query_points.txt").read_bytes()
        self.assertEqual(hashlib.sha256(payload).hexdigest(), "55e012ff2df6bd04fa8d78c527c3c5fe32634cdf9da0744ecfcf22cbd4537686")

    def test_week13_diagnostics_and_boundary_sensitivity_are_auditable(self):
        with Path("Week_13/04_Results/week_13_strategy_summary.csv").open(newline="") as handle:
            strategy = list(csv.DictReader(handle))
        self.assertEqual(len(strategy), 8)
        self.assertTrue(all(row["diagnostic_coordinate"] == "rounded_submission_6dp" for row in strategy))
        with Path("Week_13/04_Results/week_13_boundary_generation_sensitivity.csv").open(newline="") as handle:
            sensitivity = list(csv.DictReader(handle))
        self.assertEqual({int(row["function"]) for row in sensitivity}, {2, 5, 6})
        self.assertTrue(all(row["status"] == "diagnostic_only_frozen_query_unchanged" for row in sensitivity))

    def test_gp_prediction_and_query_selection(self):
        model = fit_gaussian_process(self.X, self.y, optimizer_restarts=0)
        candidates = np.array([[0.5, 0.5], [0.45, 0.55], [0.2, 0.8]])
        mean, std = predict_with_uncertainty(model, candidates)
        choice = select_query(candidates, self.X, mean, std, method="ucb", kappa=2.0)
        self.assertFalse(np.allclose(choice.query, [0.5, 0.5]))
        self.assertEqual(upper_confidence_bound([1], [0.5], kappa=2).tolist(), [2.0])
        self.assertGreaterEqual(expected_improvement([1], [0.5], best=0.5)[0], 0)
        self.assertEqual(expected_improvement([1], [0], best=0.5).tolist(), [0.0])
        self.assertGreater(probability_improvement([1], [0.5], best=0.5)[0], 0.5)

    def test_acquisition_validation(self):
        with self.assertRaises(ValueError):
            upper_confidence_bound([1, 2], [0.1])
        with self.assertRaises(ValueError):
            expected_improvement([1], [-0.1], best=0.5)

    def test_plotting_returns_figures(self):
        first = plot_function_diagnostics(self.X, self.y)
        second = plot_proposal_overview(["F1", "F2"], [0.1, 0.2], [0.3, 0.4])
        self.assertGreaterEqual(len(first.axes), 4); self.assertEqual(len(second.axes), 2)

    def test_weekly_evidence_is_reproducible_and_gap_aware(self):
        self.assertEqual(len(recorded_pairs(2, 1)), 1)
        self.assertEqual(len(recorded_pairs(11, 1)), 10)
        self.assertIn("Week 11", EVIDENCE_GAPS[11])
        X, y, starter_count = load_weekly_evidence(11, 2)
        self.assertEqual((X.shape, y.shape), ((21, 2), (21,)))
        self.assertEqual(starter_count, 10)
        X, y, starter_count = load_weekly_evidence(2, 2, evidence_through_week=1)
        self.assertEqual((X.shape, y.shape), ((11, 2), (11,)))
        frame, cutoff_summary = analyse_weekly_function(
            2, 2, evidence_through_week=1
        )
        self.assertEqual(len(frame), 11)
        self.assertEqual(cutoff_summary["recorded_pairs"], 1)
        frame, summary = analyse_weekly_function(13, 8)
        self.assertEqual(summary["recorded_pairs"], 12)
        self.assertEqual(summary["total_verified_observations"], len(frame))
        self.assertIn("archive_integrity", summary)
        figure = plot_weekly_function(frame, summary)
        self.assertGreaterEqual(len(figure.axes), 3)

    def test_historical_reviews_enforce_prior_week_boundary(self):
        for week in range(3, 14):
            for function in range(1, 9):
                frame, summary, proposal, figure = analyse_historical_function(week, function)
                plt.close(figure)
                self.assertEqual(summary["recorded_pairs"], week - 1)
                self.assertEqual(proposal["status"], "proposed_only")
                candidate = np.asarray(proposal["query"], dtype=float)
                self.assertTrue(np.all(candidate <= 0.999999))
                observed = frame[[c for c in frame if c.startswith("x")]].to_numpy(float)
                duplicate = bool(np.any(np.all(np.isclose(observed, candidate, rtol=0, atol=5e-7), axis=1)))
                self.assertEqual(duplicate, proposal["duplicates_observed_evidence"])

    def test_week_13_uses_canonical_function_specific_strategy(self):
        expected = {1: "UCB", 2: "EI", 3: "PI", 4: "UCB", 5: "EI", 6: "EI", 7: "UCB", 8: "UCB"}
        for function, method in expected.items():
            proposal = proposal_for_week(13, function)
            self.assertEqual(proposal["method"], method)
            self.assertIn("adaptive heuristic", proposal["policy_scope"].lower())
            self.assertIn("before any Week 13 outcome", proposal["decision_timing"])
            self.assertFalse(proposal.get("duplicates_observed_evidence", False))


if __name__ == "__main__":
    unittest.main()
