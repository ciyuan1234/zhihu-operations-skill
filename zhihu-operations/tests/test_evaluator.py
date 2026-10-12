#!/usr/bin/env python3
"""Unit tests for Zhihu question potential evaluator."""

import unittest
import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from question_evaluator import evaluate_question


class TestZhihuQuestionEvaluator(unittest.TestCase):
    def test_high_potential_question_gets_high_score(self):
        # 1500 followers with only 12 answers -> high demand, low competition
        res = evaluate_question(followers=1500, answers=12, views=45000, title="测试高潜力问题")
        self.assertGreaterEqual(res["score"], 70.0)
        self.assertIn("S", res["tier"])
        self.assertGreaterEqual(res["follower_to_answer_ratio"], 100.0)

    def test_saturated_question_gets_lower_score(self):
        # 200 followers with 180 answers -> low demand, saturated competition
        res = evaluate_question(followers=200, answers=180, views=15000, title="测试低潜力过饱和问题")
        self.assertLess(res["score"], 50.0)
        self.assertIn("C", res["tier"])


if __name__ == "__main__":
    unittest.main()
