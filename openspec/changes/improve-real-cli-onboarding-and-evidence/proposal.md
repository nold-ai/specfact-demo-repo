## Why

The demo now uses the real `specfact-cli`, but onboarding and verification context
is still incomplete for first-time users. Missing install prerequisites, unclear
backlog sync outcomes, and absent evidence-pack artifacts reduce trust and
contribution readiness.

## What Changes

- Expand README with a clearer product context and explicit install/prerequisite steps.
- Add expected output references and a committed visual demo artifact.
- Clarify real backlog sync behavior and post-sync file effects.
- Add reproducibility/evidence-pack structure (`repro/`, `evidence/`, `results/`, `threats`).
- Align CI artifact upload paths with real-CLI workflow outputs.
- Remove stale plugin-centric wording from contributor-facing docs.

## Capabilities

### New Capabilities

- `demo-onboarding-evidence-pack`: A reproducible onboarding and evidence baseline for
  the real-CLI demo repository.

### Modified Capabilities

- None.

## Impact

- Affected docs: `README.md`, `CONTRIBUTING.md`, `docs/*`.
- Affected CI: `.github/workflows/demo-ci.yml`.
- New reproducibility artifacts: `repro/*`, `evidence/*`, `results/*`.
