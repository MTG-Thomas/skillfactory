# Incident: CI failure on renovate requests-2.32

**Summary:** CI failed on renovate branch for `requests-2.32` with `ImportError: cannot import name 'Mapping' from 'collections'`. Mitigated by reverting to `requests 2.31` in PR #4820.

**Impact:** CI checks blocked on renovate branch; no production impact.

**Timeline:**
- Detected: CI failure on renovate `requests-2.32` branch
- Mitigated: Reverted to `requests 2.31` in PR #4820
- Verified green: 2026-09-10 15:47 EDT

**Root Cause:** `requests 2.32` dependency chain uses deprecated `collections.Mapping` alias, removed in Python 3.10+, should be `collections.abc.Mapping`.

**Detection Gap:** Renovate upgrade not validated against runtime Python version before CI; no pin compatibility check for `collections.abc` migration.

**Corrective Actions:**
- Completed: Pin/revert to `requests 2.31` via PR #4820, CI green.
- Pending: Evaluate `requests >=2.32` compatibility or patch `Mapping` import; add Python-version compatibility check to renovate flow.
- Deferred: None.

**Lessons:** Pin major dependency upgrades behind version-aware CI; treat `collections` -> `collections.abc` deprecations as breaking on modern Python.
