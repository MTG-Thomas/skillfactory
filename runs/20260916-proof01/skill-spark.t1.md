# Incident: CI failure on renovate requests-2.32 - collections.Mapping ImportError

## Summary
CI failed on `renovate/requests-2.32` branch with `ImportError: Mapping from collections`. Restored service by reverting to `requests 2.31` in PR #4820.

## Impact
- Environment: CI on renovate branch.
- Users: No production impact. Dependency upgrade workflow blocked.
- Checks: Import-time failure blocked renovate branch verification.

## Timeline
- Detection: CI failure observed on `renovate/requests-2.32` branch with `ImportError: Mapping from collections` (exact detection time unknown).
- Diagnosis: Failure attributed to `requests 2.32` incompatibility with `collections.Mapping` import path.
- Mitigation: Reverted to `requests 2.31` in PR #4820.
- Verification: CI green on 2026-09-10 15:47 EDT.

## Root Cause
Upgrade to `requests 2.32` exposed use of deprecated `collections.Mapping` import instead of `collections.abc.Mapping`, which is unsupported on the current Python runtime. The dependency bump was incompatible with the runtime import contract, causing failure at import time.

## Detection Gap
CI correctly caught the broken import on the renovate branch. Gap was prevention-side: no compatibility constraint or pre-merge signal prevented proposing `requests 2.32` against a runtime where `collections.Mapping` is removed.

## Corrective Actions
- Completed:
  - Reverted to `requests 2.31` in PR #4820.
  - Verified CI green on 2026-09-10 15:47 EDT.
- Pending:
  - Identify exact import site expecting `collections.Mapping` and confirm `collections.abc.Mapping` fix path.
  - Re-attempt `requests 2.32` upgrade after compatibility fix, with CI import check.
- Deferred:
  - `requests 2.32` adoption deferred until import compatibility is resolved. No further action on 2.32 until then.

## Lessons
- Treat Renovate minor bumps as potentially breaking when they touch import-time behavior.
- Prefer `collections.abc` imports; `collections` aliases are removed on modern Python.
- Keep dependency reverts tied to a verification timestamp before closing the incident.

Related: PR #4820, renovate branch `requests-2.32`.
