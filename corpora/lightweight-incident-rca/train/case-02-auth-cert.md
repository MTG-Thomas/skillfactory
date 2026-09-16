# Case 02 — Staging auth outage (expired cert)

## Input (evidence)
- Staging login 100% 401s from 2026-09-08 09:12 EDT to 09:58 EDT.
- Error: `x509: certificate has expired` on idp-staging internal endpoint.
- Cause chain: cert rotated manually 90 days ago, no expiry alert; staging uses distinct cert from prod.
- Detection: user report, not monitoring. Health check hits /alive which skips IdP.
- Mitigation: reissued cert 09:51 EDT, verified login 09:58 EDT. Pending: expiry alert + /ready check covering IdP.
- Related: ops ticket OPS-214, runbook docs/auth.md.

## Task
Same shape contract as case 01. Name the detection gap separately from the root cause
(missing expiry signal + shallow health check). No secrets.
