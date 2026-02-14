## 1. OpenSpec Artifacts

- [x] 1.1 Create proposal for sidecar legacy demo addition.
- [x] 1.2 Create design for sidecar scenario and command flow.
- [x] 1.3 Add spec deltas for legacy sidecar demo and README linkage updates.

## 2. Implementation

- [x] 2.1 Add `examples/buggy-sidecar/` legacy code sample without decorators.
- [x] 2.2 Add Make targets for sidecar import/repro/demo using real `specfact-cli`.
- [x] 2.3 Update README with sidecar walkthrough and official documentation links.
- [x] 2.4 Update evidence manifest/results references to include sidecar logs.

## 3. Validation

- [x] 3.1 Run sidecar demo commands and capture `results/sidecar-*.log`.
- [x] 3.2 Run `make real-smoke` and `make test`.
- [x] 3.3 Run `openspec validate add-sidecar-legacy-demo --strict`.
