import tempfile
import unittest
from pathlib import Path

from specfact_demo.enforce import run_enforcement


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
FIXTURES_PASS = ROOT / "fixtures_pass"
PLUGIN = ROOT / "plugins" / "official" / "backlog_labeler" / "plugin.py"


class EnforcePipelineTests(unittest.TestCase):
    def test_enforcement_reports_expected_blocking_results(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            artifacts = Path(temp_dir)
            result = run_enforcement(FIXTURES, artifacts, [PLUGIN])

        report = result["report"]
        self.assertEqual(report["gate_decision"], "BLOCK")
        self.assertEqual(report["counts"]["blocking_violations"], 3)
        self.assertAlmostEqual(
            report["metrics"]["violation_blocking_ratio_pct"],
            33.33,
            places=2,
        )
        self.assertAlmostEqual(
            report["metrics"]["coverage_delta_pct"],
            -18.33,
            places=2,
        )

    def test_backlog_sync_is_updated_for_blocked_items(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            artifacts = Path(temp_dir)
            result = run_enforcement(FIXTURES, artifacts, [PLUGIN])

            backlog_sync = result["backlog_sync"]
            self.assertEqual(backlog_sync["total_updated"], 2)
            labels = [
                label
                for item in backlog_sync["updated_items"]
                for label in item.get("labels", [])
            ]
            self.assertIn("specfact:blocker", labels)

            manifest_path = artifacts / "evidence_manifest.json"
            self.assertTrue(manifest_path.exists())

    def test_fixed_fixture_reports_pass(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            artifacts = Path(temp_dir)
            result = run_enforcement(FIXTURES_PASS, artifacts, [PLUGIN])

        report = result["report"]
        self.assertEqual(report["gate_decision"], "PASS")
        self.assertEqual(report["counts"]["blocking_violations"], 0)
        self.assertAlmostEqual(
            report["metrics"]["violation_blocking_ratio_pct"],
            0.0,
            places=2,
        )
        self.assertAlmostEqual(
            report["metrics"]["coverage_delta_pct"],
            15.0,
            places=2,
        )


if __name__ == "__main__":
    unittest.main()
