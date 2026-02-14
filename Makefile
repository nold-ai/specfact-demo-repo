PYTHON ?= python3
FIXTURES ?= fixtures
FIXTURES_PASS ?= fixtures_pass
ARTIFACTS ?= artifacts/latest
ARTIFACTS_PASS ?= artifacts/pass
OFFICIAL_PLUGIN ?= plugins/official/backlog_labeler/plugin.py
CHANGE ?= demo-github-issue-sync-showcase
GITHUB_REPO ?= nold-ai/specfact-demo-repo

.PHONY: repro repro-pass explain diff-report demo sync-issue validate-sync opsx-dogfood enforce test plugin-init plugin-test clean clean-latest clean-pass

repro: clean-latest
	./specfact enforce --fixtures "$(FIXTURES)" --artifacts "$(ARTIFACTS)" --use-plugin "$(OFFICIAL_PLUGIN)"

repro-pass: clean-pass
	./specfact enforce --fixtures "$(FIXTURES_PASS)" --artifacts "$(ARTIFACTS_PASS)" --use-plugin "$(OFFICIAL_PLUGIN)"

explain:
	@$(PYTHON) -c 'import json; from pathlib import Path; p = Path("$(ARTIFACTS)/enforce_report.json"); r = json.loads(p.read_text(encoding="utf-8")); print("Gate decision: {}".format(r["gate_decision"])); print("Blocking violations:"); v = [x for x in r.get("violations", []) if x.get("severity") == "blocking"]; print("  - none") if not v else None; [print("  - {}: {} ({})".format(x["story_id"], x["code"], x["control"])) for x in v]'

diff-report:
	@$(PYTHON) -c 'import json; from pathlib import Path; b = json.loads(Path("$(ARTIFACTS)/enforce_report.json").read_text(encoding="utf-8")); p = json.loads(Path("$(ARTIFACTS_PASS)/enforce_report.json").read_text(encoding="utf-8")); bm = b["metrics"]; pm = p["metrics"]; print("BLOCK run: {} | PASS run: {}".format(b["gate_decision"], p["gate_decision"])); print("Metric deltas (pass - block):"); print("  - violation_blocking_ratio_pct: {:+.2f} ({:.2f} -> {:.2f})".format(pm["violation_blocking_ratio_pct"] - bm["violation_blocking_ratio_pct"], bm["violation_blocking_ratio_pct"], pm["violation_blocking_ratio_pct"])); print("  - contract_coverage_pct: {:+.2f} ({:.2f} -> {:.2f})".format(pm["contract_coverage_pct"] - bm["contract_coverage_pct"], bm["contract_coverage_pct"], pm["contract_coverage_pct"])); print("  - evidence_coverage_pct: {:+.2f} ({:.2f} -> {:.2f})".format(pm["evidence_coverage_pct"] - bm["evidence_coverage_pct"], bm["evidence_coverage_pct"], pm["evidence_coverage_pct"])); print("  - coverage_delta_pct: {:+.2f} ({:+.2f} -> {:+.2f})".format(pm["coverage_delta_pct"] - bm["coverage_delta_pct"], bm["coverage_delta_pct"], pm["coverage_delta_pct"]))'

demo: repro
	@echo ""
	@echo "=== Why did it block? ==="
	@$(MAKE) --no-print-directory explain
	@echo ""
	@echo "=== Run fixed fixtures (PASS path) ==="
	@$(MAKE) --no-print-directory repro-pass
	@echo ""
	@echo "=== BLOCK vs PASS metric diff ==="
	@$(MAKE) --no-print-directory diff-report

sync-issue:
	$(PYTHON) scripts/sync_change_to_github_issue.py --change "$(CHANGE)" --repo "$(GITHUB_REPO)"

validate-sync:
	$(PYTHON) scripts/validate_change_sync.py --change "$(CHANGE)" --repo "$(GITHUB_REPO)"

opsx-dogfood:
	openspec validate "$(CHANGE)" --strict
	$(MAKE) --no-print-directory sync-issue
	$(MAKE) --no-print-directory validate-sync

enforce:
	./specfact enforce --fixtures "$(FIXTURES)" --artifacts "$(ARTIFACTS)" --use-plugin "$(OFFICIAL_PLUGIN)" --fail-on-block

test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"

plugin-init:
	./specfact plugin init sample-plugin

plugin-test:
	./specfact plugin test "$(OFFICIAL_PLUGIN)" --fixture "$(FIXTURES)"

clean:
	$(MAKE) --no-print-directory clean-latest
	$(MAKE) --no-print-directory clean-pass

clean-latest:
	rm -rf "$(ARTIFACTS)"

clean-pass:
	rm -rf "$(ARTIFACTS_PASS)"
