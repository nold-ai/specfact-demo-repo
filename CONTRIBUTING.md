# Contributing to SpecFact Demo Repo

This repository is a demo harness for the real `specfact-cli`.
Keep changes small, reproducible, and focused on onboarding value.

## Quick Start

```bash
make real-smoke
make test
```

## Ways You Can Contribute

- Improve demo scenarios with realistic, small fixtures.
- Improve developer UX in `README.md`, `Makefile`, and demo logs.
- Improve OpenSpec dogfooding flows, including backlog sync examples.
- Improve CI clarity/speed for the real CLI smoke path.

## Good First Issue Labels

Use these labels when opening or triaging issues:

- `good first issue`: small newcomer-friendly tasks.
- `help wanted`: valuable tasks needing contributor help.
- `demo-scenario`: new or improved showcase scenarios.
- `docs`: onboarding and clarity improvements.

## Contribution Expectations

- Keep changes scoped and avoid unrelated refactors.
- Preserve or improve reproducibility of `make real-smoke`.
- Add or update tests when behavior changes.
- Update docs when user-facing commands or outputs change.
- If demo behavior changes, refresh relevant files in `results/` and `evidence/`.

## Pull Request Checklist

- Run `make real-smoke`
- Run `make test`
- If OpenSpec artifacts changed, run `openspec validate <change-id> --strict`
- Summarize behavior and validation output in the PR description
