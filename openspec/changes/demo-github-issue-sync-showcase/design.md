## Context

This repository now contains OpenSpec scaffolding and a demo enforcement pipeline. We need
an additional demo that shows how an OpenSpec change is turned into a real GitHub backlog
issue with traceable source metadata and a deterministic validation step.

## Goals / Non-Goals

**Goals:**

- Provide one command to create a GitHub issue from a change id.
- Persist local source-tracking metadata under the change directory.
- Validate both OpenSpec change artifacts and synced issue metadata.
- Keep implementation small and runnable in a typical developer environment with `gh`.

**Non-Goals:**

- Building a general integration service for every backlog provider.
- Automatic bidirectional syncing of issue state back into tasks/specs.
- Replacing the existing enforcement demo flow.

## Decisions

- Use small Python CLI scripts in `scripts/` instead of shell-only logic to keep parsing,
  JSON handling, and metadata updates reliable.
  - Alternative considered: Makefile-only `gh` commands.
  - Rejected because source tracking updates and validation checks become brittle.
- Use `gh` CLI as the integration surface for GitHub issue operations.
  - Alternative considered: GitHub API calls directly via Python HTTP client.
  - Rejected to avoid adding a new dependency and auth flow.
- Persist sync artifacts at
  `openspec/changes/<change-id>/source_tracking.json` and keep a human-readable source
  section in `proposal.md`.
  - Alternative considered: artifacts-only storage.
  - Rejected because proposal should stay self-describing for reviewers.

## Risks / Trade-offs

- [Risk] `gh` is unauthenticated or missing on contributor machine.
  -> Mitigation: fail fast with actionable error text.
- [Risk] Network/API transient failures.
  -> Mitigation: keep idempotent behavior and print exact retry command.
- [Risk] Manual edits remove source markers from issue body.
  -> Mitigation: validation command checks body markers and fails clearly.

## Migration Plan

1. Add scripts and Make targets.
2. Run OpenSpec strict validation for this change.
3. Execute issue-sync command against `nold-ai/specfact-demo-repo`.
4. Run sync validation command.
5. Update docs with usage and expected output.

Rollback: remove new script/Makefile/docs files and delete the created demo issue if needed.

## Open Questions

- Should the issue sync command auto-add labels/milestone beyond a default demo label?
- Should we create a follow-up capability for syncing issue status back into tasks?
