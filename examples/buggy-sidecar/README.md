# Buggy Sidecar Demo

This example intentionally avoids contract decorators and represents legacy code.
Use it to demonstrate sidecar validation on existing code.

Run from repo root:

```bash
make sidecar-demo
```

Direct commands:

```bash
specfact-cli import from-code buggy-sidecar --repo examples/buggy-sidecar --shadow-only --force
specfact-cli repro --repo examples/buggy-sidecar --sidecar --sidecar-bundle buggy-sidecar
```
