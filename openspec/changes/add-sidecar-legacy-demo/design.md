## Context

SpecFact’s strongest onboarding path is brownfield modernization. The demo should
prove that users can validate existing code without first adopting decorators or
rewriting modules.

## Goals / Non-Goals

**Goals:**

- Add a deterministic sidecar demo path that works with real `specfact-cli`.
- Keep scenario small and self-contained for fast local runs.
- Connect README to deeper official docs for broader workflows.

**Non-Goals:**

- Replacing current smoke or backlog sync flows.
- Adding full framework-specific app stacks in this change.
- Introducing plugin or marketplace runtime demos.

## Decisions

- Use a tiny pure-Python buggy example (`calculator.py`) with no decorators.
  - Alternative: full Flask/Django app.
  - Rejected due to heavier setup and slower onboarding.
- Add dedicated Make targets (`sidecar-import`, `sidecar-repro`, `sidecar-demo`).
  - Alternative: embed commands only in README.
  - Rejected to keep reproducibility one-command friendly.
- Capture sidecar logs under `results/` and include in evidence manifest.
  - Alternative: require users to run manually every time.
  - Rejected because expected outputs improve trust.

## Risks / Trade-offs

- [Risk] Sidecar behavior may evolve across CLI versions.
  -> Mitigation: keep logs illustrative and regenerate on version bump.
- [Risk] Validation output may be environment-sensitive.
  -> Mitigation: keep example deterministic and avoid external dependencies.
