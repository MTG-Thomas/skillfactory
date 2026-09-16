# Case 01 — CI red after dependency bump

## Input (evidence)
- Repo: example-api, branch renovate/requests-2.32, CI job #4812 failed 2026-09-10 14:02 EDT.
- Error: `ImportError: cannot import name 'Mapping' from 'collections'` in tests/unit/test_auth.py.
- Cause chain: requests 2.32 dropped py2 shim; app pinned Python 3.11, unpinned requests; lockfile regenerated without running unit tests locally.
- Detection: CI only. No local pre-push hook. Dependabot PR merged without focused test run.
- Mitigation: reverted to requests 2.31 in PR #4820, CI green 2026-09-10 15:47 EDT. Pending: pin policy + pre-merge unit gate.
- Related: PR #4819 (bump), PR #4820 (revert), runbook docs/ci.md.

## Task
Write a lightweight incident RCA note following the standard shape
(Summary, Impact, Timeline, Root Cause, Detection Gap, Corrective Actions, Lessons).
Keep it concise, blameless, with absolute timestamps and owned corrective actions.
Do NOT paste raw logs; summarize the causal mechanism.
