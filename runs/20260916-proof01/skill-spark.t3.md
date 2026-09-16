# Incident: CI failure on renovate/requests-2.32 - `ImportError: Mapping from collections`

## Summary
CI failed on renovate branch `renovate/requests-2.32`. Import failed with `ImportError: Mapping from collections`. Service restored by reverting to `requests 2.31` in PR #4820.

## Impact
- Affected: CI checks on renovate branch for requests 2.32.
- Users/workflows: Dependency update workflow blocked. No production impact reported.
- Checks: Import-time failure, blocking merge of 2.32 bump.

## Timeline
- 2026-09-10 15:47 EDT: PR #4820 verified green after revert to requests 2.31.
- Prior: CI failure observed on `renovate/requests-2.32` with `ImportError: Mapping from collections`.

## Root Cause
Incompatibility surfaced by requests 2.32 upgrade path: code under test imports `Mapping` from `collections` instead of `collections.abc`. Removed in Python 3.10+. Bump exposed latent import rather than requests regression itself.

## Detection Gap
- No pre-merge compatibility check for deprecated `collections` aliases.
- CI only caught failure after renovate branch creation. No local lint rule or import check to flag `from collections import Mapping`.

## Corrective Actions
- Completed:
  - Reverted to requests 2.31 in PR #4820. Verified green 2026-09-10 15:47 EDT.
- Pending:
  - Replace `from collections import Mapping` with `from collections.abc import Mapping` and re-attempt 2.32 bump.
  - Add import lint for deprecated `collections` aliases.
- Deferred:
  - None.

## Lessons
- Treat major/minor dependency bumps as compatibility probes, not safe merges.
- Pin recovery to a verified artifact: revert PR with green check, not chat-only fix.
- Name missing signals explicitly: missing lint for `collections.abc` migration allowed repeat risk.
