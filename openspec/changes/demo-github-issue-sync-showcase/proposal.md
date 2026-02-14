## Why

Demo users need a practical "spec to backlog" loop that uses real GitHub issues in this
repository. The current demo shows policy enforcement but does not show OpenSpec change
artifacts being synced into a tracked backlog item.

## What Changes

- Add a repeatable demo flow to create a GitHub issue from an OpenSpec change.
- Add source-tracking metadata that links the issue back to OpenSpec artifacts.
- Add validation commands that check both OpenSpec artifact integrity and GitHub sync
  integrity.
- Document the end-to-end dogfooding path in the README.

## Capabilities

### New Capabilities

- `github-backlog-sync-demo`: Create and validate a GitHub issue sync flow driven by
  OpenSpec change artifacts.

### Modified Capabilities

- None.

## Impact

- New scripts for issue creation and sync validation.
- New Makefile targets for quick-start demo execution.
- README demo instructions updated with OpenSpec + GitHub backlog sync walkthrough.

## Source Tracking

- Target repository: `nold-ai/specfact-demo-repo`
- Source change id: `demo-github-issue-sync-showcase`
- Source proposal: `openspec/changes/demo-github-issue-sync-showcase/proposal.md`
- GitHub issue: `https://github.com/nold-ai/specfact-demo-repo/issues/2`
