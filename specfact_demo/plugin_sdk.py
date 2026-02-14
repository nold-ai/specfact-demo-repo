"""Stable plugin surface for the SpecFact demo."""

from __future__ import annotations

from typing import Any

SUPPORTED_PLUGIN_API_VERSION = "1.0"
LIFECYCLE_PHASES = (
    "pre_read",
    "post_read",
    "pre_validate",
    "post_validate",
    "pre_sync",
    "post_sync",
)


class Plugin:
    """Base class for plugins.

    Plugins should override lifecycle methods they need.
    """

    name = "unnamed-plugin"
    version = "0.0.0"
    api_version = SUPPORTED_PLUGIN_API_VERSION
    scope = ["read-only"]
    invariants_touched = []
    side_effects = []
    attestation_hash = None

    def pre_read(self, context: dict[str, Any]) -> None:
        """Run before fixture data is read."""

    def post_read(self, context: dict[str, Any]) -> None:
        """Run after fixture data is read."""

    def pre_validate(self, context: dict[str, Any]) -> None:
        """Run before validation starts."""

    def post_validate(self, context: dict[str, Any]) -> None:
        """Run after validation completes."""

    def pre_sync(self, context: dict[str, Any]) -> None:
        """Run before backlog sync starts."""

    def post_sync(self, context: dict[str, Any]) -> None:
        """Run after backlog sync completes."""
