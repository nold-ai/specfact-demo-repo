# SpecFact Demo Repo

A one-repo proof of the core SpecFact promise:

> point the real `specfact-cli` at existing code, generate machine-readable specs,
> and run enforceable checks that can block regressions.

This demo is intentionally small and reproducible.

See `docs/real-cli-vs-demo.md` for scope boundaries and official docs for deeper workflows:

- https://docs.specfact.io/use-cases/
- https://docs.specfact.io/getting-started/installation/
- https://docs.specfact.io/guides/

## 90-Second Proof

Run the real CLI smoke path:

```bash
make real-smoke
```

Equivalent direct commands:

```bash
specfact-cli --version
specfact-cli import from-code demo-repo --repo . --shadow-only --force
specfact-cli enforce stage --preset minimal
```

Expected indicators:

- `SpecFact CLI version ...`
- `Import complete!`
- `Enforcement mode set to minimal`

Sample output logs:

- `results/real-smoke.log`
- `results/test.log`

## What Success Looks Like

After a successful run, you should have:

- a generated bundle under `.specfact/projects/demo-repo/`
- enforcement preset configured via `enforce stage`
- reproducible logs you can inspect or attach to a PR

## Read Output Fast

Use this quick interpretation guide for new users:

- `Import complete!` means the codebase was parsed and bundled successfully.
- `Enforcement mode set ...` means gate policy is configured for this bundle.
- `BLOCK` in an enforcement/repro summary means at least one contract/policy violation failed the gate.
- `ALLOW` means configured checks passed for the evaluated scope.

## Demo Lanes

### 1) Brownfield smoke lane

```bash
make real-smoke
```

This is the fastest onboarding path and should complete in about one minute on a typical laptop.

### 2) Legacy sidecar validation lane

```bash
make sidecar-demo
```

This imports and validates the deliberately buggy sample in `examples/buggy-sidecar/`.

Expected logs:

- `results/sidecar-import.log`
- `results/sidecar-repro.log`

### 3) Backlog sync lane (GitHub adapter)

```bash
make real-backlog-sync REPO_OWNER=nold-ai REPO_NAME=specfact-demo-repo BACKLOG_IDS=2
```

This uses `specfact-cli sync bridge` in bidirectional mode and writes tracking artifacts under:

- `openspec/changes/`
- `.specfact/projects/<bundle>/change_tracking/`

Prerequisite: authenticated GitHub access (`gh auth login` or `specfact-cli auth github`).

## Install and Prerequisites

Install the real CLI:

```bash
pip install specfact-cli
specfact-cli --version
```

For backlog sync demos, ensure:

- GitHub authentication is active
- you can read/write issues in the target repository

## Core Commands

```bash
make real-version
make real-import
make real-enforce
make real-repro
make real-backlog-sync REPO_OWNER=<owner> REPO_NAME=<repo> BACKLOG_IDS=<id-list>
make sidecar-demo
make real-smoke
make test
```

## Visual Demo

Rendered terminal snapshot:

- `docs/assets/demo-output.svg`

Capture instructions:

- `docs/assets/README.md`

## Ways You Can Contribute

- Improve demo scenarios and command ergonomics
- Improve backlog sync examples for real-world repos
- Add contributor-safe fixtures that demonstrate sync conflict handling
- Improve CI reliability and run time for demo verification

Recommended labels:

- `good first issue`
- `help wanted`
- `demo-scenario`
- `docs`

## Repo Layout

```text
examples/                    # runnable demo examples
openspec/                    # OpenSpec change artifacts for dogfooding examples
repro/                       # reproducibility runners
evidence/                    # evidence manifest and threat model
results/                     # sample run outputs
docs/                        # supporting demo docs
tests/                       # local tests for demo harness modules
```
