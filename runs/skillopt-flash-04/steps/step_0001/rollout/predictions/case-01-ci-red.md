# Incident RCA: example-api CI red after requests 2.32 dependency bump

Date: 2026-09-10  
Status: Resolved

## Summary
example-api CI went red after the dependency update PR #4819 to `requests` 2.32. Unit tests failed with `ImportError: cannot import name 'Mapping' from 'collections'` in `tests/unit/test_auth.py`. Service was restored by reverting to `requests` 2.31 in PR #4820.

## Impact
- Environment: example-api CI/trunk checks.
- Workflows affected: Unit test job blocked; no production deployment or user-facing impact observed.

## Timeline
- 2026-09-10 14:02 EDT — CI job #4812 failed after the `requests` 2.32 dependency change.
- 2026-09-10 15:47 EDT — PR #4820 (revert to `requests` 2.31) merged; CI green.

Related: PR #4819 (dependency bump), PR #4820 (revert), docs/ci.md.

## Root Cause
`requests` was an unpinned direct dependency. A regenerated lockfile pulled `requests` 2.32, which removed a Python 2 compatibility shim that had previously made the legacy `from collections import Mapping` import path in `tests/unit/test_auth.py` resolve. On Python 3.11 with `requests` 2.32, that import no longer worked, causing the unit tests to fail.

## Detection Gap
- The dependency update was merged without a focused unit-test run.
- No local pre-push hook or pre-merge required test gate prevented the broken state from reaching trunk CI.
- CI caught the failure after the dependency change was already in place.

## Corrective Actions

### Completed
- Reverted `requests` to 2.31 in PR #4820; CI green 2026-09-10 15:47 EDT.

### Pending
- Pin `requests` to a known-good version or compatible range in the project dependency file, and regenerate the lockfile with tests run.
- Add a required pre-merge unit-test gate for dependency update PRs.
- Document the dependency pin policy in docs/ci.md.

### Deferred
- Replace the legacy `collections.Mapping` import in `tests/unit/test_auth.py` with `collections.abc.Mapping`, so future `requests` versions do not depend on removed compatibility shims.

## Lessons
- Dependency updates are code changes: run focused tests before merge or require the test job to pass.
- Unpinned direct dependencies can introduce breaking changes after lockfile regeneration; pin direct dependencies explicitly.
- If code relies on deprecated compatibility aliases, fix the import at the source instead of relying on a dependency-provided shim.