## Incident: CI failure on renovate requests-2.32

**Summary:** CI failed on renovate branch for `requests-2.32` with `ImportError: Mapping from collections`. Service restored by reverting to `requests 2.31` in PR #4820.

**Impact:** CI checks on renovate branch blocked. No production impact reported.

**Timeline:**
- 2026-09-10 15:47 EDT: PR #4820 verification green after revert to `requests 2.31`.

**Root Cause:** `requests 2.32` incompatible with runtime expecting `collections.Mapping` (moved to `collections.abc.Mapping` in Python 3.10+). Dependency upgrade exposed deprecated import path.

**Detection Gap:** No pre-merge compatibility check for `requests` major/minor upgrade against supported Python version. CI only caught failure after renovate branch creation, with no alert naming the deprecated `collections.Mapping` signal.

**Corrective Actions:**
- Completed: Reverted to `requests 2.31` in PR #4820, verified green 2026-09-10 15:47 EDT.
- Pending: Pin or constrain `requests` version pending upstream fix or code migration to `collections.abc.Mapping`.
- Deferred: None.

**Lessons:**
- Treat first broken CI branch as symptom; verify dependency and interpreter compatibility.
- Name missing signals explicitly: monitor for deprecated `collections` imports on dependency bumps.
