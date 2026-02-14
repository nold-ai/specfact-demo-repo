"""Plugin loading, lifecycle execution, and harness checks."""

from __future__ import annotations

import importlib.util
import inspect
import json
import re
from pathlib import Path
from typing import Any, Iterable

from .plugin_sdk import LIFECYCLE_PHASES, Plugin, SUPPORTED_PLUGIN_API_VERSION


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_plugin_from_path(plugin_path: Path | str) -> Plugin:
    path = Path(plugin_path)
    if not path.exists():
        raise FileNotFoundError(f"Plugin path not found: {path}")

    module_name = f"specfact_plugin_{abs(hash(path.resolve()))}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to import plugin from path: {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    candidates = []
    for value in vars(module).values():
        if inspect.isclass(value) and issubclass(value, Plugin) and value is not Plugin:
            candidates.append(value)

    if not candidates:
        raise ValueError(f"No Plugin subclass found in {path}")

    if len(candidates) > 1:
        candidates.sort(key=lambda cls: cls.__name__)

    return candidates[0]()


def load_plugins(plugin_paths: Iterable[Path | str]) -> list[Plugin]:
    return [load_plugin_from_path(path) for path in plugin_paths]


def run_lifecycle(plugins: Iterable[Plugin], phase: str, context: dict[str, Any]) -> None:
    for plugin in plugins:
        hook = getattr(plugin, phase, None)
        if callable(hook):
            hook(context)


def validate_plugin_metadata(plugin: Plugin, allowed_scopes: list[str]) -> list[str]:
    errors: list[str] = []

    if not plugin.name:
        errors.append("Plugin must set name.")
    if not plugin.version:
        errors.append("Plugin must set version.")
    if plugin.api_version != SUPPORTED_PLUGIN_API_VERSION:
        errors.append(
            "Plugin api_version mismatch. "
            f"Expected {SUPPORTED_PLUGIN_API_VERSION}, got {plugin.api_version}."
        )
    if not isinstance(plugin.scope, list) or not plugin.scope:
        errors.append("Plugin scope must be a non-empty list.")
    if not isinstance(plugin.invariants_touched, list):
        errors.append("Plugin invariants_touched must be a list.")
    if not isinstance(plugin.side_effects, list):
        errors.append("Plugin side_effects must be a list.")

    if isinstance(plugin.scope, list):
        invalid_scopes = sorted(set(plugin.scope) - set(allowed_scopes))
        if invalid_scopes:
            errors.append(
                "Plugin scope contains unsupported entries: "
                + ", ".join(invalid_scopes)
            )

    return errors


def run_plugin_harness(plugin_path: Path | str, fixture_dir: Path | str) -> dict[str, Any]:
    fixture_path = Path(fixture_dir)
    policy_path = fixture_path / "policies" / "enforcement_policy.json"
    policy = _read_json(policy_path)
    allowed_scopes = policy.get("allowed_plugin_scopes", ["read-only"])

    plugin = load_plugin_from_path(plugin_path)
    errors = validate_plugin_metadata(plugin, allowed_scopes)

    context: dict[str, Any] = {
        "fixture_dir": str(fixture_path),
        "policy": policy,
        "stories": [],
        "violations": [],
        "sync_result": {"updated_items": []},
        "lifecycle_log": [],
    }

    if not errors:
        for phase in LIFECYCLE_PHASES:
            context["lifecycle_log"].append(phase)
            hook = getattr(plugin, phase, None)
            if not callable(hook):
                continue
            try:
                hook(context)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{phase} hook failed: {exc}")

    if context.get("bypass_enforcement") is True:
        errors.append("Plugin attempted to set bypass_enforcement=True.")

    return {
        "plugin_name": plugin.name,
        "plugin_version": plugin.version,
        "plugin_api_version": plugin.api_version,
        "checked_lifecycle_phases": list(LIFECYCLE_PHASES),
        "passed": not errors,
        "errors": errors,
    }


def init_plugin_scaffold(
    plugin_name: str,
    target_dir: Path | str = "plugins",
) -> dict[str, Any]:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", plugin_name).strip("-").lower()
    if not slug:
        raise ValueError("Plugin name must contain at least one valid character.")

    base_dir = Path(target_dir) / slug
    if base_dir.exists():
        raise FileExistsError(f"Plugin directory already exists: {base_dir}")

    fixture_dir = base_dir / "test_fixture"
    workflow_dir = base_dir / ".github" / "workflows"
    fixture_dir.mkdir(parents=True, exist_ok=False)
    workflow_dir.mkdir(parents=True, exist_ok=False)

    manifest = (
        f"name: {slug}\n"
        "version: 0.1.0\n"
        f"api_version: {SUPPORTED_PLUGIN_API_VERSION}\n"
        "scope:\n"
        "  - read-only\n"
        "invariants_touched:\n"
        "  - evidence_gate\n"
        "side_effects:\n"
        "  - none\n"
        "attestation_hash: null\n"
    )
    plugin_py = (
        "from specfact_demo.plugin_sdk import Plugin\n\n\n"
        f"class {slug.replace('-', '_').title().replace('_', '')}(Plugin):\n"
        f'    name = "{slug}"\n'
        '    version = "0.1.0"\n'
        f'    api_version = "{SUPPORTED_PLUGIN_API_VERSION}"\n'
        '    scope = ["read-only"]\n'
        '    invariants_touched = ["evidence_gate"]\n'
        '    side_effects = ["none"]\n'
        "    attestation_hash = None\n\n"
        "    def post_validate(self, context):\n"
        "        context.setdefault('notes', []).append(\n"
        "            'sample plugin observed validation stage'\n"
        "        )\n"
    )
    readme = (
        f"# {slug}\n\n"
        "Generated SpecFact plugin scaffold.\n\n"
        "## Local checks\n\n"
        "```bash\n"
        f"./specfact plugin test plugins/{slug}/plugin.py --fixture fixtures\n"
        "```\n"
    )
    ci_workflow = (
        "name: plugin-check\n\n"
        "on:\n"
        "  pull_request:\n"
        "  push:\n\n"
        "jobs:\n"
        "  plugin-test:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - uses: actions/checkout@v4\n"
        "      - uses: actions/setup-python@v5\n"
        "        with:\n"
        "          python-version: '3.x'\n"
        "      - run: ./specfact plugin test plugin.py --fixture test_fixture\n"
        "        working-directory: plugins/"
        f"{slug}\n"
    )

    files_to_write = {
        base_dir / "manifest.yaml": manifest,
        base_dir / "plugin.py": plugin_py,
        base_dir / "README.md": readme,
        fixture_dir / "README.md": "Place deterministic fixtures for plugin tests.\n",
        workflow_dir / "plugin-ci.yml": ci_workflow,
    }

    for path, content in files_to_write.items():
        path.write_text(content, encoding="utf-8")

    return {
        "plugin": slug,
        "created": [str(path) for path in sorted(files_to_write)],
    }
