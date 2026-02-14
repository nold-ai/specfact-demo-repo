# SpecFact Demo Repo

This repository is a reproducible "OpenClaw moment" for SpecFact:

- one command to enforce spec-first invariants
- visible blocking of violations
- automatic backlog sync updates
- deterministic evidence pack artifacts

You can run the full flow in less than 5 minutes.

## Quickstart (3 commands)

```bash
make repro
```

Expected output includes:

- `Violation blocking ratio: ...`
- `Coverage delta: ...`
- `Backlog sync result: ...`
- `Evidence manifest: artifacts/latest/evidence_manifest.json`

## Demo story

The fixture repo intentionally includes three blocking issues:

1. Missing Definition of Ready (DoR)
2. Invalid contract (API version mismatch)
3. Missing evidence pack for one story

The enforcement flow blocks affected work and writes machine-readable artifacts.

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

## Repo layout

```text
specfact_demo/               # demo CLI + enforcement engine + plugin SDK
fixtures/                    # deterministic broken sample repo
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
