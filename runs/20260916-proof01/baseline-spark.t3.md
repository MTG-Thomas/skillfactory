# Incident: CI failure on requests 2.32 upgrade

**Summary:** CI failed on renovate/requests-2.32 branch with `ImportError: Mapping from collections`. Reverted to requests 2.31 in PR 4820. CI green on 2026-09-10 15:47 EDT.

**Impact:** Dependency upgrade branch blocked. No production impact. CI checks failed until revert merged.

**Timeline:**
- Detection: CI failure reported on renovate/requests-2.32 branch.
- Mitigation: Reverted to requests 2.31 in PR 4820.
- Verification: CI green on 2026-09-10 15:47 EDT.

**Root Cause:** requests 2.32 uses `collections.Mapping`, removed in Python 3.10 and later. Compatible import is `collections.abc.Mapping`. The upgraded dependency was incompatible with the runtime Python version.

**Detection Gap:** Renovate upgrade CI was the detection signal. No earlier pin compatibility check blocked the incompatible minor upgrade before CI ran.

**Corrective Actions:**
- Completed: Pinned requests to 2.31 in PR 4820 and verified green CI.
- Pending: Re-evaluate requests upgrade after upstream fixes `collections.Mapping` usage or runtime compatibility is confirmed.
- Deferred: None.

**Lessons:** Pin back to last known good on incompatible dependency upgrades. Verify major and minor dependency upgrades against runtime Python version.
