# Real CLI vs Demo Repo

This repository is a small demo harness that runs the real `specfact-cli`.

## What this repo is

- A reproducible showcase for import, enforcement, sidecar validation, and backlog sync.
- A safe place to iterate on demo scenarios, docs, and onboarding scripts.
- A real-CLI-first workflow using `specfact-cli` commands.

## What this repo is not

- Not the production `specfact-cli` codebase.
- Not the source of truth for complete CLI behavior.
- Not a replacement for official docs and releases.

## Command expectations

- Smoke lane:
  - `make real-smoke`
- Sidecar lane:
  - `make sidecar-demo`
- Backlog sync lane:
  - `make real-backlog-sync REPO_OWNER=<owner> REPO_NAME=<repo> BACKLOG_IDS=<id-list>`

Internal `specfact_demo/` Python modules are retained as local test fixtures only and are not the supported user path.
