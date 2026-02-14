#!/usr/bin/env python3
"""Create a GitHub issue from an OpenSpec change and persist source tracking."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def _extract_section(markdown: str, heading: str) -> str:
    pattern = rf"(?ms)^## {re.escape(heading)}\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, markdown)
    return match.group(1).strip() if match else ""


def _run_command(args: list[str]) -> str:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result.stdout.strip()


def _build_issue_body(change_id: str, proposal_path: Path, tasks_path: Path) -> str:
    proposal = proposal_path.read_text(encoding="utf-8")
    why = _extract_section(proposal, "Why")
    what_changes = _extract_section(proposal, "What Changes")
    synced_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return "\n".join(
        [
            "## OpenSpec Change Backlog Sync Demo",
            "",
            "### Why",
            why or "N/A",
            "",
            "### What Changes",
            what_changes or "N/A",
            "",
            "### OpenSpec Source Tracking",
            f"- Change ID: {change_id}",
            f"- Proposal: `{proposal_path.as_posix()}`",
            f"- Tasks: `{tasks_path.as_posix()}`",
            f"- Synced At UTC: {synced_at}",
        ]
    ).strip() + "\n"


def _extract_issue_number(issue_url: str) -> int:
    match = re.search(r"/issues/(\d+)$", issue_url.strip())
    if not match:
        raise ValueError(f"Unable to parse issue number from URL: {issue_url}")
    return int(match.group(1))


def _update_proposal_tracking(proposal_path: Path, issue_url: str) -> None:
    content = proposal_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    updated = False
    for idx, line in enumerate(lines):
        if line.startswith("- GitHub issue:"):
            lines[idx] = f"- GitHub issue: `{issue_url}`"
            updated = True
            break
    if not updated:
        if not content.endswith("\n"):
            content += "\n"
        content += f"\n## Source Tracking\n\n- GitHub issue: `{issue_url}`\n"
        proposal_path.write_text(content, encoding="utf-8")
        return
    proposal_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--change", required=True, help="OpenSpec change id.")
    parser.add_argument(
        "--repo",
        default="nold-ai/specfact-demo-repo",
        help="GitHub repo in owner/name format.",
    )
    parser.add_argument(
        "--label",
        default="enhancement",
        help="GitHub issue label to apply.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate issue body and tracking payload without creating an issue.",
    )
    args = parser.parse_args()

    change_dir = Path("openspec/changes") / args.change
    proposal_path = change_dir / "proposal.md"
    tasks_path = change_dir / "tasks.md"
    tracking_path = change_dir / "source_tracking.json"
    if not proposal_path.exists() or not tasks_path.exists():
        raise FileNotFoundError(
            f"Missing proposal/tasks for change '{args.change}' in {change_dir.as_posix()}"
        )

    issue_title = f"[Demo] OpenSpec backlog sync: {args.change}"
    issue_body = _build_issue_body(args.change, proposal_path, tasks_path)

    if args.dry_run:
        print(issue_body)
        return 0

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as temp_file:
        temp_file.write(issue_body)
        temp_body_path = temp_file.name

    output = _run_command(
        [
            "gh",
            "issue",
            "create",
            "--repo",
            args.repo,
            "--title",
            issue_title,
            "--body-file",
            temp_body_path,
            "--label",
            args.label,
        ]
    )
    issue_url = output.strip().splitlines()[-1].strip()
    issue_number = _extract_issue_number(issue_url)

    tracking_payload = {
        "change_id": args.change,
        "repo": args.repo,
        "issue_number": issue_number,
        "issue_url": issue_url,
        "proposal_path": proposal_path.as_posix(),
        "tasks_path": tasks_path.as_posix(),
        "synced_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    tracking_path.write_text(json.dumps(tracking_payload, indent=2) + "\n", encoding="utf-8")
    _update_proposal_tracking(proposal_path, issue_url)

    print(f"Created issue: {issue_url}")
    print(f"Source tracking: {tracking_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
