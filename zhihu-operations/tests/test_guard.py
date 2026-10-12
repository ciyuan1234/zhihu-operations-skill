#!/usr/bin/env python3
"""Unit tests for Zhihu guard cadence logic."""

import unittest
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from guard import check_cadence, record_answer, CST


class TestZhihuGuard(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.state_file = Path(self.tmp_dir.name) / "test_zhihu_state.json"

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_midnight_blackout_blocked(self):
        # 04:15 AM CST (midnight blackout)
        dt = datetime(2026, 10, 12, 4, 15, tzinfo=CST)
        res = check_cadence(self.state_file, target_time=dt)
        self.assertFalse(res["allowed"])
        self.assertTrue(any("夜间禁发" in r for r in res["reasons"]))

    def test_golden_window_allowed_when_empty(self):
        # 21:00 PM CST (Golden window: 晚间深度阅读主力波峰)
        dt = datetime(2026, 10, 12, 21, 0, tzinfo=CST)
        res = check_cadence(self.state_file, target_time=dt)
        self.assertTrue(res["allowed"])
        self.assertEqual(res["golden_window"], "晚间深度阅读主力波峰")

    def test_minimum_gap_enforced(self):
        # Record post at 12:00 PM CST
        t1 = datetime(2026, 10, 12, 12, 0, tzinfo=CST)
        record_answer(self.state_file, timestamp=t1.isoformat())

        # Check at 15:00 PM (3h later, under 6h minimum gap)
        t2 = datetime(2026, 10, 12, 15, 0, tzinfo=CST)
        res = check_cadence(self.state_file, target_time=t2)
        self.assertFalse(res["allowed"])
        self.assertTrue(any("距上条发布不足" in r for r in res["reasons"]))

        # Check at 18:30 PM (6.5h later, exceeds 6h gap)
        t3 = datetime(2026, 10, 12, 18, 30, tzinfo=CST)
        res3 = check_cadence(self.state_file, target_time=t3)
        self.assertTrue(res3["allowed"])


if __name__ == "__main__":
    unittest.main()
