#!/usr/bin/env python3
"""Validate OpenSpec change and GitHub issue source-link integrity."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def _run(args: list[str]) -> str:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--change", required=True, help="OpenSpec change id.")
    parser.add_argument(
        "--repo",
        default="nold-ai/specfact-demo-repo",
        help="GitHub repo in owner/name format.",
    )
    args = parser.parse_args()

    change_dir = Path("openspec/changes") / args.change
    proposal_path = change_dir / "proposal.md"
    tracking_path = change_dir / "source_tracking.json"
    if not proposal_path.exists() or not tracking_path.exists():
        raise FileNotFoundError(
            f"Missing proposal/source tracking for change '{args.change}' in {change_dir.as_posix()}"
        )

    _run(["openspec", "validate", args.change, "--strict"])
    tracking = json.loads(tracking_path.read_text(encoding="utf-8"))
    issue_number = tracking["issue_number"]
    if tracking["repo"] != args.repo:
        raise RuntimeError(
            f"Repo mismatch in source_tracking.json: expected {args.repo}, found {tracking['repo']}"
        )

    raw = _run(
        [
            "gh",
            "issue",
            "view",
            str(issue_number),
            "--repo",
            args.repo,
            "--json",
            "number,url,state,body",
        ]
    )
    issue = json.loads(raw)
    expected_markers = [
        f"Change ID: {args.change}",
        f"Proposal: `{proposal_path.as_posix()}`",
    ]
    body = issue.get("body", "")
    missing = [marker for marker in expected_markers if marker not in body]
    if missing:
        raise RuntimeError(f"Issue is missing source tracking markers: {missing}")

    print(f"OpenSpec strict validation: PASS ({args.change})")
    print(f"Issue linkage validation: PASS ({issue['url']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
