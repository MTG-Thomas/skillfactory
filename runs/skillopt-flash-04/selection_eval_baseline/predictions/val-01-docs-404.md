# Lightweight Incident RCA

## Summary
All `/guides/*` routes on the docs site deploy preview returned 404 on 2026-08-28. A base-path change in `vite.config` was made without updating the preview rewrite rules. Service was restored by fixing the rewrite rules and redeploying the preview.

## Impact
- Affected: deploy preview for the docs site; reviewer click-throughs.
- Routes: `/guides/*` returned 404.
- Production docs were not affected.

## Timeline (EDT)
- **2026-08-28 11:05** — Reviewer reported 404s on `/guides/*` in the deploy preview.
- **2026-08-28 11:20** — Investigation identified that the base path in `vite.config` had changed and the preview rewrite rules still used the old path prefix.
- **2026-08-28 12:25** — Rewrite rules were updated to match the new base path.
- **2026-08-28 12:30** — Preview redeployed; `/guides/*` routes verified as working.

## Root Cause
The base-path in `vite.config` was changed, but the deploy preview rewrite rules were not updated to match. The preview server therefore served 404s for all URLs under the new base path.

## Detection Gap
No link-check or route smoke test existed in CI. The failure was caught only by a manual reviewer click-through.

## Corrective Actions
**Completed**
- Updated preview rewrite rules to match the changed base path.
- Redeployed the docs preview and verified `/guides/*` routes return successful responses.

**Pending**
- Add a preview link-check job to CI that verifies all `/guides/*` routes return 200 before the preview is marked ready.

**Intentionally deferred**
- None.

## Lessons
- When changing the base path, update all path-dependent preview and proxy rules in the same change.
- A preview without an automated route/link check cannot be trusted to verify docs changes.