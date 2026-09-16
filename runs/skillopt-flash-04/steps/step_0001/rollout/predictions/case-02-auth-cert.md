# Incident: Staging auth outage — expired IdP certificate

## Summary
Staging authentication returned 100% 401s for 46 minutes on 2026-09-08 because the internal IdP staging certificate had expired. The certificate was reissued at 09:51 EDT; login was verified restored at 09:58 EDT.

## Impact
- Environment: staging
- Staging login was unavailable from 09:12 EDT to 09:58 EDT (46 minutes)
- All staging users and dependent auth workflows were affected

## Timeline
All times EDT.

- 09:12: Staging login begins returning 401s
- 09:51: Expired IdP certificate reissued
- 09:58: Login verified restored

## Root Cause
The staging IdP certificate had expired. It was rotated manually 90 days before the incident; no expiry monitoring existed. Staging uses a distinct certificate from production, so production certificate monitoring would not have detected this.

## Detection Gap
Detection relied on a user report, not monitoring. The existing health check only calls `/alive`, which skips the IdP auth path, so it did not catch the expired certificate.

## Corrective Actions
Completed:
- Reissued the staging IdP certificate and verified login at 09:58 EDT

Pending:
- Add expiration alerting for the staging IdP certificate
- Add a `/ready` health check that exercises the IdP auth path

Related: OPS-214, runbook `docs/auth.md`

## Lessons
- Certificates need expiry alerts for every environment, especially when certificates are environment-specific.
- Liveness checks are not enough; readiness checks must cover external authentication dependencies.