# Good example (passes grader): case-01-ci-red
## Summary
CI failed on `renovate/requests-2.32` after an unpinned `requests` bump; reverted to 2.31 in PR #4820, green 2026-09-10 15:47 EDT.
## Impact
`example-api` branch CI only; no prod impact. Blocked merges ~2h.
## Timeline
- 2026-09-10 14:02 EDT — CI job #4812 failed (`ImportError: Mapping`).
- 2026-09-10 15:47 EDT — revert PR #4820 merged, CI green.
## Root Cause
Unpinned dependency accepted a breaking major shim removal without a local unit run; lockfile regenerated blind.
## Detection Gap
No pre-push hook and no required focused test run on Dependabot PRs — CI was the only signal.
## Corrective Actions
- Completed: revert PR #4820, verified green.
- Pending: pin policy + required unit gate on dependency PRs (docs/ci.md).
- Deferred: none.
## Lessons
Pin direct deps; run affected unit tests before merging dependency bumps; make the gate automatic.
