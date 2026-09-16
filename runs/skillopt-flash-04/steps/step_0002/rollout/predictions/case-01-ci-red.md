# Incident RCA: CI red after requests dependency bump

**Date:** 2026-09-10  
**Repo:** example-api  
**Status:** Resolved

## Summary
CI job #4812 failed on branch `renovate/requests-2.32` after PR #4819 bumped `requests` to 2.32. `tests/unit/test_auth.py` failed with an `ImportError` because `requests` 2.32 removed the Python 2 compatibility shim that had kept `collections.Mapping` importable on Python 3.11. Service was restored by reverting to `requests` 2.31 in PR #4820; CI was green at 15:47 EDT.

## Impact
- CI signal was unavailable for the dependency-bump branch; PR #4819 could not merge.
- No production runtime impact.

## Timeline
- 14:02 EDT — CI job #4812 failed on `renovate/requests-2.32`.
- Between 14:02 and 15:47 EDT — Root cause identified as the `requests` 2.32 compatibility-layer removal; PR #4820 was opened to revert to `requests` 2.31.
- 15:47 EDT — PR #4820 merged; CI green.

## Root Cause
The application pins Python 3.11 but did not pin `requests`. The lockfile was regenerated when `requests` 2.32 was introduced, and the unit test still referenced `collections.Mapping`, an import that existed only through `requests` 2.31's Python 2 compatibility layer. When that layer was removed, the test failed.

## Detection Gap
- Only CI caught the failure; there was no local pre-push hook or pre-merge unit-test gate for dependency/lockfile changes.
- The dependency bump was not validated by a focused unit test run before CI.

## Corrective Actions
- **Completed:** Reverted `requests` to 2.31 in PR #4820; CI green.
- **Pending:** Add a dependency pin/upper-bound policy for `requests` so future breaking releases do not enter the lockfile silently.
- **Pending:** Add a pre-merge unit-test gate for dependency and lockfile changes in CI, and document the requirement in `docs/ci.md`.
- **Intentionally deferred:** None.

## Lessons
- A lockfile regeneration is not safe until the same unit test suite that runs in CI passes locally.
- Removing a legacy compatibility layer can break tests even when the application Python version stays fixed.
- Dependency bumps need the same test validation as application code.