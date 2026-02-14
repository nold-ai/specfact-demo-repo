## Context

The repository is transitioning from simulator-heavy messaging to real `specfact-cli`
execution. Current docs and CI still contain gaps that make trust and reproducibility
harder for new users.

## Goals / Non-Goals

**Goals:**

- Make README self-sufficient for first-time setup and execution.
- Make demo outcomes concrete with expected output and visual/log artifacts.
- Add a minimal evidence pack aligned with reproducibility expectations.
- Keep commands CLI-first and remove stale plugin simulation references.

**Non-Goals:**

- Expanding into multi-language sample applications in this change.
- Reintroducing plugin marketplace implementation demos.
- Changing core product behavior of `specfact-cli`.

## Decisions

- Add explicit installation + auth prerequisites in README.
  - Alternative: keep prerequisites in external docs only.
  - Rejected due to onboarding friction in demo repos.
- Add evidence structure as committed scaffolding plus generated logs.
  - Alternative: generate on-demand only.
  - Rejected because contributors need stable expected outputs and file map.
- Align CI artifact upload to `.specfact/**` and demo logs from real commands.
  - Alternative: keep legacy `artifacts/latest` paths.
  - Rejected because those paths come from removed simulator flow.

## Risks / Trade-offs

- [Risk] Sample outputs become stale after CLI releases.
  -> Mitigation: document that outputs are illustrative and refresh during release bumps.
- [Risk] Real backlog sync may fail in CI due to auth/network.
  -> Mitigation: keep CI smoke focused on local import/enforce/test; backlog sync remains manual.
- [Risk] Evidence artifacts may be mistaken as production guarantees.
  -> Mitigation: include explicit scope/limitations in `threats.md`.
