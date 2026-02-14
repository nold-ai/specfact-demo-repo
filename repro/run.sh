#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESULTS_DIR="$ROOT_DIR/results"
mkdir -p "$RESULTS_DIR"

echo "Running real smoke..."
make -C "$ROOT_DIR" real-smoke | tee "$RESULTS_DIR/real-smoke.log"

echo "Running unit tests..."
make -C "$ROOT_DIR" test | tee "$RESULTS_DIR/test.log"

echo "Validating current OpenSpec change set..."
openspec validate --changes --strict | tee "$RESULTS_DIR/openspec-validate.log"

echo "Repro run complete. Logs written to $RESULTS_DIR"
