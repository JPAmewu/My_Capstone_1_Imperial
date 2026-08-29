"""Checks for the generated reader-first final report."""

import unittest
from pathlib import Path

from Code.build_final_report import build_tables


class FinalReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[2]
        cls.scoreboard, cls.timeline, cls.strategy = build_tables(cls.root)

    def test_scoreboard_invariants(self):
        self.assertEqual(len(self.scoreboard), 8)
        self.assertEqual(int(self.scoreboard["incumbent_changes"].sum()), 12)
        self.assertEqual(
            self.scoreboard.loc[self.scoreboard["week_13_improved"], "function"].tolist(),
            ["F5", "F6"],
        )
        self.assertTrue(self.scoreboard["rolling_rmse_skill"].gt(0).all())

    def test_timeline_contains_only_starts_and_improvements(self):
        self.assertEqual(len(self.timeline), 20)
        self.assertEqual(int(self.timeline["week"].eq(0).sum()), 8)

    def test_strategy_is_complete(self):
        self.assertEqual(set(self.strategy["function"]), {f"F{i}" for i in range(1, 9)})
        self.assertEqual(set(self.strategy["acquisition"]), {"UCB", "EI", "PI"})


if __name__ == "__main__":
    unittest.main()
