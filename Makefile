PYTHON ?= python3
REAL_BUNDLE ?= demo-repo
REPO_OWNER ?= nold-ai
REPO_NAME ?= specfact-demo-repo
BACKLOG_IDS ?= 2
SIDECAR_BUNDLE ?= buggy-sidecar
SIDECAR_REPO ?= examples/buggy-sidecar

.PHONY: real-version real-import real-enforce real-repro real-backlog-sync sidecar-import sidecar-repro sidecar-demo real-smoke test clean

real-version:
	specfact-cli --version

real-import:
	specfact-cli import from-code "$(REAL_BUNDLE)" --repo . --shadow-only --force

real-enforce:
	specfact-cli enforce stage --preset minimal

real-repro:
	specfact-cli repro --repo .

real-backlog-sync:
	specfact-cli sync bridge --adapter github --mode bidirectional --repo . --bundle "$(REAL_BUNDLE)" --repo-owner "$(REPO_OWNER)" --repo-name "$(REPO_NAME)" --backlog-ids "$(BACKLOG_IDS)" --use-gh-cli

sidecar-import:
	specfact-cli import from-code "$(SIDECAR_BUNDLE)" --repo "$(SIDECAR_REPO)" --shadow-only --force

sidecar-repro:
	specfact-cli repro --repo "$(SIDECAR_REPO)" --sidecar --sidecar-bundle "$(SIDECAR_BUNDLE)"

sidecar-demo:
	$(MAKE) --no-print-directory sidecar-import
	$(MAKE) --no-print-directory sidecar-repro

real-smoke:
	$(MAKE) --no-print-directory real-version
	$(MAKE) --no-print-directory real-import
	$(MAKE) --no-print-directory real-enforce

test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"

clean:
	rm -rf artifacts/latest artifacts/pass
