# Case 04 — Bad deploy (env var rename, prod 500s)

## Input (evidence)
- Prod /checkout 500s 12% of requests, 2026-09-02 16:20-16:41 EDT after release v2.14.
- Error: `KeyError: PAYMENTS_API_URL` — renamed to PAYMENTS_BASE_URL in code, Helm values still set old key.
- Cause chain: rename in PR #4770 without values update; preview env uses different values file so it stayed green.
- Detection: error-rate alert 16:24 EDT (4 min). Rollback to v2.13 completed 16:41 EDT.
- Pending: values/key contract check in CI, canary error-rate gate. Completed: rollback, values fix PR #4772.

## Task
Same shape contract. Root cause is the contract gap between code and values,
not "deploy failed". Verify before claiming actions complete.
