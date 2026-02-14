import tempfile
import textwrap
import unittest
from pathlib import Path

from specfact_demo.plugin_tools import run_plugin_harness


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
PLUGIN = ROOT / "plugins" / "official" / "backlog_labeler" / "plugin.py"


class PluginHarnessTests(unittest.TestCase):
    def test_official_plugin_passes_harness(self):
        report = run_plugin_harness(PLUGIN, FIXTURES)
        self.assertTrue(report["passed"])
        self.assertEqual(report["errors"], [])

    def test_invalid_plugin_api_version_fails_harness(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            bad_plugin = Path(temp_dir) / "bad_plugin.py"
            bad_plugin.write_text(
                textwrap.dedent(
                    """
                    from specfact_demo.plugin_sdk import Plugin


                    class BadPlugin(Plugin):
                        name = "bad-plugin"
                        version = "0.0.1"
                        api_version = "2.0"
                        scope = ["sync-adapter"]
                        invariants_touched = []
                        side_effects = []
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            report = run_plugin_harness(bad_plugin, FIXTURES)

        self.assertFalse(report["passed"])
        self.assertTrue(any("api_version" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
