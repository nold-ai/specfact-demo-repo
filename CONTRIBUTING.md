# Contributing to SpecFact Demo Repo

Thanks for contributing. This repo is intentionally small and reproducible, so changes should
keep demo flows deterministic and fast.

Important: this repo is a demo harness, not the production `specfact-cli` codebase.

## Quick Start

```bash
make real-smoke
make test
```

## Ways You Can Contribute

- Improve demo scenarios:
  add new fixture variants that show realistic policy failures or recoveries.
- Improve developer UX:
  simplify output readability and command ergonomics in `Makefile` and `README.md`.
- Expand plugin examples:
  add safe lifecycle plugins under `plugins/official/`.
- Improve OpenSpec dogfooding:
  refine backlog sync flow using `specfact-cli sync bridge`.
- Improve CI reliability:
  make real-CLI verification faster and clearer in GitHub Actions.

## Good First Issue Labels

Use these labels when opening or triaging issues:

- `good first issue`: Small, bounded, newcomer-friendly tasks.
- `help wanted`: Valuable tasks that need contributor help.
- `demo-scenario`: New or improved showcase scenario work.
- `docs`: Documentation clarity and onboarding improvements.

## Contribution Expectations

- Keep changes scoped and avoid unrelated refactors.
- Preserve or improve reproducibility of `make real-smoke`.
- Add/update tests when behavior changes.
- Update README when user-facing commands or outputs change.

## Pull Request Checklist

- Run:
  `make real-smoke`
- Run:
  `make test`
- If OpenSpec artifacts changed, run:
  `openspec validate <change-id> --strict`
- Summarize behavior changes and validation output in PR description.
