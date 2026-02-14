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

- Commands in this repo are demo commands and fixtures:
  - `make demo`
  - `./specfact enforce ...`
  - `make opsx-dogfood ...`
- They are designed for deterministic demo output, not production rollout.
