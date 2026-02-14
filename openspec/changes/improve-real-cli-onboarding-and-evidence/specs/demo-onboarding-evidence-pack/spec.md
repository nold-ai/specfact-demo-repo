## ADDED Requirements

### Requirement: Demo README Includes Real CLI Prerequisites

The demo repository SHALL document installation, authentication, and expected real-CLI
smoke command behavior for first-time users.

#### Scenario: New user follows onboarding without external assumptions

- **WHEN** a user opens the README for the first time
- **THEN** install and verification commands are explicitly listed
- **AND** required auth steps for backlog sync are explicitly listed.

### Requirement: Demo Provides Reproducible Evidence Pack Structure

The repository SHALL include a reproducibility structure with commands, manifest metadata,
results, and documented limitations.

#### Scenario: Contributor can run and inspect evidence artifacts

- **WHEN** a contributor runs the repro script
- **THEN** logs are written under `results/`
- **AND** `evidence/manifest.yaml` declares demonstrated invariants
- **AND** `evidence/threats.md` documents known limitations.

### Requirement: CI Artifacts Match Real CLI Workflow

The repository SHALL upload artifacts that are produced by the real-CLI demo flow.

#### Scenario: CI run publishes relevant outputs

- **WHEN** `make real-smoke` and tests run in CI
- **THEN** uploaded artifacts include run logs and `.specfact` outputs
- **AND** obsolete simulator artifact paths are not referenced.
