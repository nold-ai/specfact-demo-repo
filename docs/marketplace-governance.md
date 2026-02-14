# Marketplace Governance

This demo documents a future marketplace extension policy aligned with
Spec-First and No-Escape invariants.

## Tier 1: Official

- Maintained by NOLD AI
- Enforcement-critical and release-blocking
- Required to ship attestation hash and invariants metadata

## Tier 2: Verified

- Community maintained
- Must pass reproducibility checks
- Must pass extension validation checks
- Must declare scope, invariants_touched, and side_effects

## Tier 3: Experimental

- Community maintained
- Not verified for production workflows
- Runs with explicit warning labels

## Hard requirements

All marketplace plugins must:

1. Declare `api_version`
2. Use lifecycle hooks only
3. Avoid direct gate bypass behavior
4. Stay within allowed policy scope

## Compatibility rule

- Current supported plugin API: `1.0`
- Breaking lifecycle changes require API version bump
