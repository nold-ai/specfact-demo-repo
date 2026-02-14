PYTHON ?= python3
FIXTURES ?= fixtures
ARTIFACTS ?= artifacts/latest
OFFICIAL_PLUGIN ?= plugins/official/backlog_labeler/plugin.py

.PHONY: repro enforce test plugin-init plugin-test clean

repro: clean
	./specfact enforce --fixtures "$(FIXTURES)" --artifacts "$(ARTIFACTS)" --use-plugin "$(OFFICIAL_PLUGIN)"

enforce:
	./specfact enforce --fixtures "$(FIXTURES)" --artifacts "$(ARTIFACTS)" --use-plugin "$(OFFICIAL_PLUGIN)" --fail-on-block

test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"

plugin-init:
	./specfact plugin init sample-plugin

plugin-test:
	./specfact plugin test "$(OFFICIAL_PLUGIN)" --fixture "$(FIXTURES)"

clean:
	rm -rf "$(ARTIFACTS)"
