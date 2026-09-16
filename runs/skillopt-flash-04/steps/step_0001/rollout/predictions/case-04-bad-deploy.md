# Incident: Production /checkout 500s after v2.14 env var rename (2026-09-02)

## Summary
Release v2.14 introduced a code/values contract mismatch: the payment client code was renamed to use `PAYMENTS_BASE_URL`, but the production Helm values still set the old `PAYMENTS_API_URL` key. This caused `KeyError` during checkout handling and HTTP 500s on roughly 12% of `/checkout` requests. Service was restored by rolling back to v2.13.

## Impact
- Environment: production
- Workflow: `/checkout`
- 12% of `/checkout` requests returned HTTP 500 between 16:20 and 16:41 EDT on 2026-09-02.
- No data loss; checkout was degraded for affected requests.

## Timeline
All times EDT (UTC-4).

- 16:20: v2.14 began serving production traffic; `/checkout` 500s started.
- 16:24: error-rate alert fired, 4 minutes after first impact.
- 16:25–16:40: investigation traced the failures to a missing/mismatched payment URL env key; PR #4770 was identified as the code rename that changed the config contract.
- 16:41: rollback to v2.13 completed; `/checkout` error rate returned to baseline.

## Root Cause
PR #4770 renamed the payment URL configuration key in code from `PAYMENTS_API_URL` to `PAYMENTS_BASE_URL`, but the production Helm values were not updated to provide the new key. The app therefore raised `KeyError` when the payment client tried to read its required configuration. This is a code-to-values contract gap, not a deploy mechanism failure.

## Detection Gap
- The error-rate alert fired 4 minutes after impact, but it detected symptoms, not the missing configuration key.
- No CI check validated that the target Helm values contain every key the code reads.
- Preview/staging stayed green because it used a different values file that already contained the new key; this gave false confidence in production config compatibility.

## Corrective Actions
Completed:
- Rolled back production to v2.13 at 16:41 EDT on 2026-09-02, restoring `/checkout` success rate.
- Submitted PR #4772 to update Helm values to provide `PAYMENTS_BASE_URL` and remove the obsolete `PAYMENTS_API_URL` key.

Pending:
- Add a values/key contract check in CI that verifies the target Helm values satisfy the config keys expected by the deployed code.
- Add a canary error-rate gate to the deploy pipeline so a rollout is automatically halted if `/checkout` error rate exceeds a defined threshold.

Deferred:
- None.

## Lessons
- Renaming an environment variable/config key is a cross-artifact contract change; update code and production values together or block the deploy with a failing check.
- Green preview/staging environments are not proof of production config compatibility if they use different values files.
- Rollout pipelines need an explicit canary error-rate gate; symptom alerting alone is too late to prevent impact.

## References
- PR #4770: env var rename in code (root cause)
- PR #4772: production Helm values fix
- Release v2.14; rollback to v2.13
