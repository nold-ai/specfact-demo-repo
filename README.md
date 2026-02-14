# SpecFact Demo Repo

This repository is a reproducible "aha moment" for SpecFact:

- one command to enforce spec-first invariants
- visible blocking of violations
- automatic backlog sync updates
- deterministic evidence pack artifacts

You can run the full flow in less than 5 minutes.

See `CONTRIBUTING.md` for contributor workflows and issue labels.

## Quickstart (3 commands)

```bash
make repro
make explain
make repro-pass
```

Expected output includes:

- `Violation blocking ratio: ...`
- `Coverage delta: ...`
- `Backlog sync result: ...`
- `Evidence manifest: artifacts/latest/evidence_manifest.json`
- `Gate decision: PASS` for the fixed fixture run

## Demo story

The fixture repo intentionally includes three blocking issues:

1. Missing Definition of Ready (DoR)
2. Invalid contract (API version mismatch)
3. Missing evidence pack for one story

The enforcement flow blocks affected work and writes machine-readable artifacts.

Then a second fixture set (`fixtures_pass/`) resolves those same issues so you can
show a clean PASS path in the same session.

## 60-second demo talk track

1. "I run `make repro`; SpecFact reads stories/contracts/evidence and blocks unsafe work."
2. "I run `make explain`; it maps each blocking code to the affected story."
3. "I run `make repro-pass`; same rules, fixed fixtures, and the gate passes."
4. "Everything is in machine-readable artifacts, so this can drive CI and backlog sync."

## Commands

### Composite enforcement pipeline

```bash
./specfact enforce --fixtures fixtures --artifacts artifacts/latest
```

Phases:

1. `pre_read`
2. `post_read`
3. `pre_validate`
4. `post_validate`
5. `pre_sync`
6. `post_sync`

### Plugin scaffold generator

```bash
./specfact plugin init my-plugin
```

Generates:

- `manifest.yaml`
- `plugin.py`
- `test_fixture/`
- CI workflow skeleton
- README skeleton

### Plugin test harness

```bash
./specfact plugin test plugins/official/backlog_labeler/plugin.py --fixture fixtures
```

Checks:

- stable API contract (`api_version == 1.0`)
- lifecycle execution safety
- allowed scope constraints from policy
- no explicit enforcement bypass flags

### Demo helpers

```bash
make repro       # run intentionally broken fixtures, expect BLOCK
make explain     # print blocking violations from artifacts/latest/enforce_report.json
make repro-pass  # run fixed fixtures, expect PASS
make diff-report # compare BLOCK vs PASS metrics side-by-side
make demo        # orchestrates repro -> explain -> repro-pass
```

### OpenSpec + GitHub dogfooding demo

```bash
make opsx-dogfood CHANGE=demo-github-issue-sync-showcase
```

This flow does three things:

1. Runs strict OpenSpec validation for the change.
2. Creates a real GitHub issue in `nold-ai/specfact-demo-repo` from the change proposal.
3. Validates issue linkage markers and local source tracking metadata.

Related commands:

```bash
make sync-issue CHANGE=demo-github-issue-sync-showcase
make validate-sync CHANGE=demo-github-issue-sync-showcase
```

Source tracking is written to:

- `openspec/changes/demo-github-issue-sync-showcase/source_tracking.json`
- `openspec/changes/demo-github-issue-sync-showcase/proposal.md` (`## Source Tracking`)

## Visual demo

Add a short terminal GIF at:

- `docs/assets/demo-output.gif`

Generation instructions:

- `docs/assets/README.md`

## Ways you can contribute

- Improve demo scenarios (additional realistic BLOCK and PASS cases)
- Improve output readability (`make explain`, `make diff-report`)
- Add plugin showcase scenarios under `plugins/official/`
- Improve OpenSpec issue-sync validation and source tracking
- Improve CI reliability and speed for demo verification

Recommended issue labels:

- `good first issue`
- `help wanted`
- `demo-scenario`
- `docs`

## Repo layout

```text
specfact_demo/               # demo CLI + enforcement engine + plugin SDK
fixtures/                    # deterministic broken sample repo
fixtures_pass/               # deterministic fixed sample repo
plugins/official/            # official example plugins
docs/                        # governance, roadmap, wanted plugins
tests/                       # unit tests for enforce + plugin harness
```

## Marketplace governance model

See `docs/marketplace-governance.md` for:

- Tier 1: Official
- Tier 2: Verified
- Tier 3: Experimental

See `docs/wanted-plugins.md` for immediate extension gaps.

## Development helpers

```bash
make test
make enforce
make plugin-test
```
