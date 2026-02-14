"""Enforcement pipeline used by the demo repository."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .plugin_tools import load_plugins, run_lifecycle


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(8192)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _validate_contract(contract: dict[str, Any], required_api_version: str) -> list[str]:
    errors: list[str] = []
    required_fields = {"name", "version", "api_version", "endpoints"}
    missing = sorted(required_fields - set(contract))
    if missing:
        errors.append(f"Missing fields: {', '.join(missing)}")

    if contract.get("api_version") != required_api_version:
        errors.append(
            "Unsupported api_version "
            f"{contract.get('api_version')!r}; expected {required_api_version!r}"
        )

    endpoints = contract.get("endpoints", [])
    if not isinstance(endpoints, list) or not endpoints:
        errors.append("Contract must define at least one endpoint.")
        return errors

    endpoint_required = ("method", "path", "request_schema", "response_schema")
    for index, endpoint in enumerate(endpoints):
        if not isinstance(endpoint, dict):
            errors.append(f"Endpoint {index} is not an object.")
            continue
        for field in endpoint_required:
            if not endpoint.get(field):
                errors.append(f"Endpoint {index} missing field {field}.")

    return errors


def _sync_backlog(
    backlog_data: dict[str, Any],
    violations: list[dict[str, Any]],
) -> dict[str, Any]:
    blocking_by_story: dict[str, list[str]] = {}
    for violation in violations:
        if violation["severity"] != "blocking":
            continue
        blocking_by_story.setdefault(violation["story_id"], []).append(violation["code"])

    updated_items = []
    for item in backlog_data.get("items", []):
        story_id = item.get("story_id")
        codes = blocking_by_story.get(story_id)
        if not codes:
            continue
        updated = dict(item)
        updated["status"] = "blocked"
        updated["block_reasons"] = sorted(set(codes))
        updated_items.append(updated)

    return {
        "total_updated": len(updated_items),
        "items_blocked": len(updated_items),
        "updated_items": updated_items,
        "unmodified_items": len(backlog_data.get("items", [])) - len(updated_items),
    }


def run_enforcement(
    fixtures_dir: Path | str,
    artifacts_dir: Path | str,
    plugin_paths: Iterable[Path | str] | None = None,
) -> dict[str, Any]:
    fixtures_path = Path(fixtures_dir)
    artifacts_path = Path(artifacts_dir)
    plugin_paths = list(plugin_paths or [])

    plugins = load_plugins(plugin_paths)
    context: dict[str, Any] = {
        "fixtures_dir": str(fixtures_path),
        "violations": [],
        "sync_result": {},
    }

    run_lifecycle(plugins, "pre_read", context)

    stories_data = _read_json(fixtures_path / "specs" / "stories.json")
    backlog_data = _read_json(fixtures_path / "backlog" / "backlog.json")
    policy_data = _read_json(fixtures_path / "policies" / "enforcement_policy.json")
    stories = stories_data.get("stories", [])
    context.update(
        {
            "policy": policy_data,
            "stories": stories,
            "backlog": backlog_data,
        }
    )
    run_lifecycle(plugins, "post_read", context)
    run_lifecycle(plugins, "pre_validate", context)

    required_api_version = policy_data.get("required_contract_api_version", "1.0")
    violations: list[dict[str, Any]] = []
    valid_contracts = 0
    verified_evidence = 0

    for idx, story in enumerate(stories, start=1):
        story_id = story["id"]

        if not story.get("definition_of_ready"):
            violations.append(
                {
                    "id": f"V{idx:03d}A",
                    "story_id": story_id,
                    "code": "DOR_MISSING",
                    "severity": "blocking",
                    "control": "definition_of_ready",
                    "message": "Story is missing Definition of Ready.",
                }
            )

        contract_rel = story.get("contract")
        if not contract_rel:
            violations.append(
                {
                    "id": f"V{idx:03d}B",
                    "story_id": story_id,
                    "code": "CONTRACT_MISSING",
                    "severity": "blocking",
                    "control": "contract_validity",
                    "message": "Story does not define contract path.",
                }
            )
        else:
            contract_path = fixtures_path / contract_rel
            if not contract_path.exists():
                violations.append(
                    {
                        "id": f"V{idx:03d}B",
                        "story_id": story_id,
                        "code": "CONTRACT_MISSING",
                        "severity": "blocking",
                        "control": "contract_validity",
                        "message": f"Contract path does not exist: {contract_rel}",
                    }
                )
            else:
                contract_payload = _read_json(contract_path)
                contract_errors = _validate_contract(contract_payload, required_api_version)
                if contract_errors:
                    violations.append(
                        {
                            "id": f"V{idx:03d}B",
                            "story_id": story_id,
                            "code": "CONTRACT_INVALID",
                            "severity": "blocking",
                            "control": "contract_validity",
                            "message": "Contract failed validation.",
                            "details": contract_errors,
                        }
                    )
                else:
                    valid_contracts += 1

        evidence_path = fixtures_path / "evidence" / f"{story_id}.json"
        if not evidence_path.exists():
            violations.append(
                {
                    "id": f"V{idx:03d}C",
                    "story_id": story_id,
                    "code": "EVIDENCE_MISSING",
                    "severity": "blocking",
                    "control": "evidence_pack",
                    "message": "Evidence file is missing for story.",
                }
            )
        else:
            evidence_payload = _read_json(evidence_path)
            if evidence_payload.get("verified") is True:
                verified_evidence += 1
            else:
                violations.append(
                    {
                        "id": f"V{idx:03d}C",
                        "story_id": story_id,
                        "code": "EVIDENCE_UNVERIFIED",
                        "severity": "blocking",
                        "control": "evidence_pack",
                        "message": "Evidence exists but is not verified.",
                    }
                )

    context["violations"] = violations
    run_lifecycle(plugins, "post_validate", context)
    run_lifecycle(plugins, "pre_sync", context)

    sync_result = _sync_backlog(backlog_data, violations)
    context["sync_result"] = sync_result
    run_lifecycle(plugins, "post_sync", context)

    total_stories = len(stories)
    total_controls = total_stories * 3
    blocking_violations = len([item for item in violations if item["severity"] == "blocking"])
    ratio_pct = round((blocking_violations / total_controls) * 100, 2) if total_controls else 0.0
    contract_coverage_pct = round((valid_contracts / total_stories) * 100, 2) if total_stories else 0.0
    evidence_coverage_pct = (
        round((verified_evidence / total_stories) * 100, 2) if total_stories else 0.0
    )
    baseline_coverage = float(policy_data.get("baseline_evidence_coverage", 0.0))
    coverage_delta_pct = round(evidence_coverage_pct - baseline_coverage, 2)
    gate_decision = "BLOCK" if blocking_violations else "PASS"

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    run_id = datetime.now(timezone.utc).strftime("run-%Y%m%dT%H%M%SZ")
    report = {
        "run_id": run_id,
        "generated_at_utc": timestamp,
        "gate_decision": gate_decision,
        "counts": {
            "stories": total_stories,
            "controls": total_controls,
            "blocking_violations": blocking_violations,
        },
        "metrics": {
            "violation_blocking_ratio_pct": ratio_pct,
            "contract_coverage_pct": contract_coverage_pct,
            "evidence_coverage_pct": evidence_coverage_pct,
            "coverage_delta_pct": coverage_delta_pct,
        },
        "plugins": [
            {
                "name": plugin.name,
                "version": plugin.version,
                "api_version": plugin.api_version,
            }
            for plugin in plugins
        ],
        "violations": violations,
    }

    backlog_sync = {
        "run_id": run_id,
        "total_updated": sync_result["total_updated"],
        "items_blocked": sync_result["items_blocked"],
        "updated_items": sync_result["updated_items"],
    }

    artifacts_path.mkdir(parents=True, exist_ok=True)
    report_path = artifacts_path / "enforce_report.json"
    backlog_path = artifacts_path / "backlog_sync.json"
    _write_json(report_path, report)
    _write_json(backlog_path, backlog_sync)

    manifest = {
        "run_id": run_id,
        "generated_at_utc": timestamp,
        "invariants": ["spec_first", "no_escape", "evidence_gate"],
        "artifacts": [
            {"path": str(report_path), "sha256": _sha256(report_path)},
            {"path": str(backlog_path), "sha256": _sha256(backlog_path)},
        ],
        "plugins": report["plugins"],
    }
    manifest_path = artifacts_path / "evidence_manifest.json"
    _write_json(manifest_path, manifest)

    summary_lines = [
        f"Gate decision: {gate_decision}",
        f"Violation blocking ratio: {ratio_pct:.2f}% ({blocking_violations}/{total_controls})",
        f"Coverage delta: {coverage_delta_pct:+.2f}%",
        "Backlog sync result: "
        f"{sync_result['total_updated']} items updated ({sync_result['items_blocked']} blocked)",
        f"Evidence manifest: {manifest_path}",
    ]
    summary = "\n".join(summary_lines) + "\n"
    summary_path = artifacts_path / "summary.txt"
    summary_path.write_text(summary, encoding="utf-8")
    print(summary, end="")

    return {
        "report": report,
        "backlog_sync": backlog_sync,
        "manifest": manifest,
        "summary_path": str(summary_path),
    }
