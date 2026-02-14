# Real CLI vs Demo Repo

This repository is intentionally a local demo harness.

## What this repo is

- A reproducible showcase for enforcement, artifact generation, and backlog-sync behavior.
- A safe place for contributors to add scenarios, scripts, and docs.
- A real-CLI-first workflow using `specfact-cli`.

## What this repo is not

- Not the production `specfact-cli` distribution.
- Not a source-of-truth implementation of all real SpecFact commands.
- Not a replacement for official docs/releases.

## Command expectations

- Real CLI smoke path in this repo:
  - `make real-smoke`
  - `specfact-cli import from-code demo-repo --repo . --shadow-only --force`
  - `specfact-cli enforce stage --preset minimal`
- Real CLI backlog sync path in this repo:
  - `make real-backlog-sync REPO_OWNER=<owner> REPO_NAME=<repo> BACKLOG_IDS=<id-list>`
- Internal `specfact_demo/` Python modules remain for test fixtures only; they are not
  the public CLI path.
