# Incident: Staging login 100% 401s - expired IdP certificate (2026-09-08)

**Summary:** All staging logins returned 401 from 2026-09-08 09:12 to 09:58 EDT. Expired x509 certificate on idp-staging. Service restored by reissuing certificate.

**Impact:** Staging environment only. All login workflows via idp-staging failed with 401. No production impact reported.

**Timeline (EDT):**
- 2026-09-08 09:12 - Detected: 100% 401s on staging login
- 2026-09-08 09:12-09:51 - Diagnosed: x509 certificate on idp-staging expired; prior manual rotation ~90 days ago
- 2026-09-08 09:51 - Mitigated: certificate reissued
- 2026-09-08 09:58 - Verified: staging login succeeding

**Root Cause:** x509 certificate on idp-staging expired. Manual rotation 90 days ago left no automated renewal, so expiry broke token issuance and caused 401s.

**Detection Gap:** Health check hits `/alive` which skips IdP validation, so IdP cert expiry produced no alert. No expiry alert configured for idp-staging certificate.

**Corrective Actions:**
- Completed: Reissued idp-staging certificate on 2026-09-08 09:51; verified login 09:58 EDT
- Pending: Add certificate-expiry monitor/alert for idp-staging with threshold before expiry
- Pending: Extend staging health check or add synthetic login check covering IdP
- Deferred: None
- Related: OPS-214

**Lessons:**
- Manual certificate rotations require paired expiry alerts.
- Health checks that bypass dependencies cannot verify user login paths.
