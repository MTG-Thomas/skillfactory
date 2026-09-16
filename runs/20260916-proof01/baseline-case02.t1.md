Incident: Staging login 100% 401s

Date: 2026-09-08 09:12 to 09:58 EDT
Severity: Staging-only outage
Impact: All staging logins failed with 401.

Cause: x509 certificate expired on idp-staging. Cert was rotated manually 90 days ago with no expiry alert. Health check hits /alive which skips IdP, so expiry was undetected.

Timeline:
09:12 - Staging login failures begin
09:51 - Cert reissued
09:58 - Login verified recovered

Resolution: Reissued cert, verified login.

Follow-up:
- Add expiry alert for idp-staging cert
- Fix health check to cover IdP auth path

Related: OPS-214
