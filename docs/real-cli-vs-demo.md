# Real CLI vs Demo Repo

This repository is intentionally a local demo harness.

## What this repo is

- A reproducible showcase for enforcement, artifact generation, and backlog-sync behavior.
- A safe place for contributors to add scenarios, scripts, and docs.
- A local CLI wrapper (`./specfact`) around `specfact_demo/` Python modules.

## What this repo is not

- Not the production `specfact-cli` distribution.
- Not a source-of-truth implementation of all real SpecFact commands.
- Not a replacement for official docs/releases.

## Command expectations

- Real CLI smoke path in this repo:
  - `make real-smoke`
  - `specfact-cli import from-code demo-repo --repo . --shadow-only --force`
  - `specfact-cli enforce stage --preset minimal`
- Local simulator commands and fixtures:
  - `make demo`
  - `./specfact enforce ...`
  - `make opsx-dogfood ...`
- Simulator commands are designed for deterministic output, not production rollout.
