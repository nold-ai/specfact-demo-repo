## Why

The demo currently proves real CLI smoke and backlog sync, but does not show how
to start from legacy code without contract decorators. A sidecar validation path
is a high-impact onboarding scenario for brownfield users.

## What Changes

- Add a small buggy legacy Python example under `examples/buggy-sidecar/`.
- Add sidecar demo targets to run real import + sidecar validation.
- Add documentation links to deeper SpecFact CLI use cases and integration docs.
- Add sample sidecar logs to `results/` and reference them in README.

## Capabilities

### New Capabilities

- `legacy-sidecar-demo`: Demonstrate sidecar validation on undecorated legacy code.

### Modified Capabilities

- `demo-onboarding-evidence-pack`: Extend onboarding with deeper documentation links
  and sidecar walkthrough/output references.

## Impact

- Affected files: `README.md`, `Makefile`, `results/README.md`, evidence manifest.
- New example source tree under `examples/buggy-sidecar/`.
