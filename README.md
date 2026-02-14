# SpecFact Demo Repo

> [!IMPORTANT]
> This repo now uses the **real `specfact-cli`** for demo commands.
> Local demo wrapper binaries were removed.

This repository is a reproducible "aha moment" for SpecFact:

- real CLI import from existing code
- real CLI enforcement mode configuration
- real CLI GitHub backlog sync via bridge adapter

You can run the core smoke flow in under 1 minute.

See `CONTRIBUTING.md` for contributor workflows and issue labels.
See `docs/real-cli-vs-demo.md` for a quick mapping between this demo and the real CLI.

## Quickstart (Real CLI)

```bash
make real-smoke
```

This runs:

- `specfact-cli --version`
- `specfact-cli import from-code demo-repo --repo . --shadow-only --force`
- `specfact-cli enforce stage --preset minimal`

## Commands

### Real CLI helpers

```bash
make real-version
make real-import
make real-enforce
make real-repro
make real-smoke
```

### Backlog sync (real CLI)

```bash
make real-backlog-sync REPO_OWNER=nold-ai REPO_NAME=specfact-demo-repo BACKLOG_IDS=2
```

This uses `specfact-cli sync bridge` with the GitHub adapter in bidirectional mode.
It imports the selected backlog item(s) and syncs via the bundle.

Prerequisite: authenticated GitHub access (`gh auth login` or `specfact-cli auth github`).

## Visual demo

Add a short terminal GIF at:

- `docs/assets/demo-output.gif`

Generation instructions:

- `docs/assets/README.md`

## Ways you can contribute

- Improve real CLI demo scenarios and command ergonomics
- Improve backlog sync examples for GitHub/ADO adapters
- Add contributor-safe fixtures that demonstrate sync conflict handling
- Improve CI reliability and speed for demo verification

Recommended issue labels:

- `good first issue`
- `help wanted`
- `demo-scenario`
- `docs`

## Repo layout

```text
openspec/                    # OpenSpec change artifacts for dogfooding examples
docs/                        # governance, roadmap, and demo docs
tests/                       # local tests for demo harness modules
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
make clean
```
