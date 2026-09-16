# Incident: CI failure on renovate/requests-2.32

## Summary
CI failed on `renovate/requests-2.32` after the requests 2.32 bump; reverted to 2.31 in PR #4820, green 2026-09-10 15:47 EDT.

## Impact
example-api branch CI only; no prod impact. Merges blocked during red window.

## Timeline
- 2026-09-10 14:02 EDT — CI job #4812 failed in tests/unit/test_auth.py with `ImportError: cannot import name 'Mapping' from 'collections'`.
- 2026-09-10 15:47 EDT — Revert PR #4820 merged, CI green.

## Root Cause
requests 2.32 removed a Python 2 compatibility shim, exposing a `collections.Mapping` import incompatible with the pinned Python 3.11 runtime. requests was unpinned, and the lockfile was regenerated without a local unit run.

## Detection Gap
No pre-push hook and no required unit run on dependency PRs. CI was the only signal.

## Corrective Actions
- Completed: revert to requests 2.31 in PR #4820, verified green.
- Pending: add pin policy for direct deps in docs/ci.md.
- Pending: require unit gate on dependency PRs before merge.
- Deferred: none.

Related: PR #4819 (bump), PR #4820 (revert), runbook docs/ci.md.

## Lessons
Pin direct deps, run affected unit tests before merging bumps, and keep the merge gate automatic.
