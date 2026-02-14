## ADDED Requirements

### Requirement: Legacy Sidecar Demo Exists

The demo repository SHALL include a runnable legacy-code example that does not
use contract decorators.

#### Scenario: Example source remains undecorated

- **WHEN** a contributor inspects the sidecar demo source
- **THEN** no contract decorators are required in the example code
- **AND** code intentionally reflects brownfield quality issues.

### Requirement: Sidecar Demo Is Runnable Through Makefile

The repository SHALL provide Make targets that run import and sidecar validation
for the legacy example with real `specfact-cli`.

#### Scenario: One-command sidecar walkthrough

- **WHEN** a user runs the sidecar demo target
- **THEN** import runs for the legacy example bundle
- **AND** sidecar validation runs with `--sidecar` and `--sidecar-bundle`.

## MODIFIED Requirements

### Requirement: Demo README Includes Real CLI Prerequisites

The demo repository SHALL document installation, authentication, and expected real-CLI
smoke command behavior for first-time users.

#### Scenario: README links to deeper official workflows

- **WHEN** a user reads onboarding docs
- **THEN** README provides links to official use-cases and integration guides
- **AND** sidecar demo output references are discoverable.
