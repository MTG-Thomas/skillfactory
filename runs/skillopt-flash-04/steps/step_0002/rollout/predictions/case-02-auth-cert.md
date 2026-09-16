# Incident: Staging auth outage (expired cert)

## Summary
Staging login returned HTTP 401 for all users from 2026-09-08 09:12 EDT to 09:58 EDT because the staging IdP certificate had expired. Service was restored by reissuing the certificate at 09:51 EDT and verified at 09:58 EDT.

## Impact
- Environment: staging
- All login attempts to staging failed during the window.
- Error observed: `x509: certificate has expired` on idp-staging internal endpoint.
- No production impact; staging uses a distinct certificate from prod.

## Timeline
- 2026-09-08 09:12 EDT: Staging login begins returning 401s.
- 2026-09-08 ~09:45 EDT: User report received; on-call investigation begins.
- 2026-09-08 09:51 EDT: Expired staging IdP certificate reissued.
- 2026-09-08 09:58 EDT: Login verified working.

## Root Cause
The staging IdP certificate had expired. It was manually rotated approximately 90 days prior, and no automated expiry alert existed. Staging uses its own certificate distinct from production, so any prod certificate monitoring did not cover it.

## Detection Gap
Two missing signals delayed detection:
- No certificate expiry alert for the staging IdP certificate.
- Existing health check only tested `/alive`, which skipped the IdP dependency; it did not validate that login/auth was ready.

## Corrective Actions
- Completed: Reissued staging IdP certificate and verified login at 2026-09-08 09:58 EDT. Tracked in OPS-214.
- Pending: Add certificate expiry alert covering the staging IdP certificate.
- Pending: Add/update readiness check (`/ready`) that validates the IdP handshake and use it for staging health monitoring.
- Pending: Update `docs/auth.md` with certificate rotation and verification steps.

## Lessons
- A healthy `/alive` endpoint is not proof that authentication works; readiness checks must cover critical dependencies.
- Distinct environments need distinct certificate monitoring; coverage for one cert does not imply coverage for another.
- Manual certificate rotations need an expiry alert before expiration, not after.