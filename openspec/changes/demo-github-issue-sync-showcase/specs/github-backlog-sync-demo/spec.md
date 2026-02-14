## ADDED Requirements

### Requirement: OpenSpec Change Can Sync To GitHub Issue

The system SHALL generate and create a GitHub issue from an OpenSpec change using proposal
content as source context.

#### Scenario: Create issue from change artifacts

- **WHEN** a user runs the sync command with a valid change id and repo
- **THEN** the command creates a GitHub issue in the target repository
- **AND** the issue body includes the change id and source proposal path.

### Requirement: Source Tracking Metadata Is Persisted

The system SHALL persist source-tracking metadata for each synced change.

#### Scenario: Write source tracking file after sync

- **WHEN** issue creation succeeds
- **THEN** the command writes `openspec/changes/<change-id>/source_tracking.json`
- **AND** the file records issue url, issue number, repo, change id, and timestamp.

### Requirement: Sync Validation Detects Drift

The system SHALL validate that OpenSpec artifacts and GitHub issue metadata remain aligned.

#### Scenario: Validation checks both spec and issue linkage

- **WHEN** a user runs the validation command for a change id
- **THEN** the command runs `openspec validate <change-id> --strict`
- **AND** verifies issue body markers and local source tracking metadata
- **AND** exits non-zero when any linkage check fails.
