# Lightweight Incident RCA — 2026-09-02 /checkout 500s after v2.14 deploy

## Summary
Prod `/checkout` returned HTTP 500s on 12% of requests after release v2.14 deployed. Code in PR #4770 renamed `PAYMENTS_API_URL` to `PAYMENTS_BASE_URL`, but Helm values still supplied the old key. This caused `KeyError: PAYMENTS_API_URL` at runtime. Service was restored by rolling back to v2.13; a follow-up values fix was merged in PR #4772.

## Impact
- **Environment:** Production
- **Users/workflows:** Checkout requests; 12% of requests failed between 16:20 and 16:41 EDT
- **Duration:** ~21 minutes

## Timeline
- **16:20 EDT** — Release v2.14 deployed to production.
- **16:20 EDT** — `/checkout` begins returning 500s with `KeyError: PAYMENTS_API_URL`.
- **16:24 EDT** — Error-rate alert fires; on-call begins investigation.
- **16:41 EDT** — Rollback to v2.13 completed; error rate returns to baseline.
- **Post-incident** — Values fix merged via PR #4772.

## Root Cause
The incident was caused by a contract gap between application code and Helm values. PR #4770 renamed the environment variable in code without updating the production values file. The preview environment stayed green because it uses a different values file that already supplied the new key, so the missing production key was not caught before deploy.

## Detection Gap
Existing CI/preview checks did not verify that every environment variable referenced by code exists in the production Helm values. The production error-rate alert worked as intended and fired 4 minutes after the bad deploy, but there was no pre-deploy check for code/values key parity.

## Corrective Actions
- **Completed:** Rolled back production to v2.13, restoring service.
- **Completed:** Updated production Helm values to use `PAYMENTS_BASE_URL` (PR #4772).
- **Pending:** Add CI check enforcing that code-referenced config keys exist in Helm values.
- **Pending:** Add canary error-rate gate to block deploys that cause elevated checkout errors before full rollout.

## Lessons
- Renaming a configuration contract requires updating both sides of the contract: code and deployment values.
- A green preview environment is not proof that production configuration is correct.
- Deploys should be halted by early error-rate signals before they reach wide rollout.