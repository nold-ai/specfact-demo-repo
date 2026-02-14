"""CLI entrypoint for the SpecFact demo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .enforce import run_enforcement
from .plugin_tools import init_plugin_scaffold, run_plugin_harness


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="specfact",
        description="SpecFact demo CLI for enforcement and plugin workflows.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    enforce = subparsers.add_parser(
        "enforce",
        help="Run read/validate/sync/evidence pipeline.",
    )
    enforce.add_argument("--fixtures", default="fixtures", help="Fixture repository path.")
    enforce.add_argument(
        "--artifacts",
        default="artifacts/latest",
        help="Output directory for generated artifacts.",
    )
    enforce.add_argument(
        "--use-plugin",
        action="append",
        default=[],
        help="Plugin file path to load (repeat flag for multiple plugins).",
    )
    enforce.add_argument(
        "--fail-on-block",
        action="store_true",
        help="Exit non-zero when enforcement gate decision is BLOCK.",
    )

    plugin = subparsers.add_parser("plugin", help="Plugin authoring commands.")
    plugin_subparsers = plugin.add_subparsers(dest="plugin_command", required=True)

    plugin_init = plugin_subparsers.add_parser("init", help="Create plugin scaffold.")
    plugin_init.add_argument("name", help="Name for the new plugin.")
    plugin_init.add_argument(
        "--target-dir",
        default="plugins",
        help="Parent directory where plugin folder will be created.",
    )

    plugin_test = plugin_subparsers.add_parser("test", help="Run plugin harness checks.")
    plugin_test.add_argument("plugin_path", help="Path to plugin.py")
    plugin_test.add_argument(
        "--fixture",
        default="fixtures",
        help="Fixture folder containing policy files.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "enforce":
        result = run_enforcement(
            fixtures_dir=Path(args.fixtures),
            artifacts_dir=Path(args.artifacts),
            plugin_paths=[Path(path) for path in args.use_plugin],
        )
        gate = result["report"]["gate_decision"]
        if args.fail_on_block and gate == "BLOCK":
            return 2
        return 0

    if args.command == "plugin" and args.plugin_command == "init":
        created = init_plugin_scaffold(args.name, args.target_dir)
        print(json.dumps(created, indent=2))
        return 0

    if args.command == "plugin" and args.plugin_command == "test":
        report = run_plugin_harness(args.plugin_path, args.fixture)
        print(json.dumps(report, indent=2))
        return 0 if report["passed"] else 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
