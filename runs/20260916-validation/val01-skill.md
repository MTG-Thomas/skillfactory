# Incident: Docs deploy preview 404 on /guides/* routes — 2026-08-28

## Summary
All `/guides/*` routes returned 404 on the docs site deploy preview from 11:05 to 12:30 EDT on 2026-08-28. Service restored by fixing preview rewrite rules to match the new `base-path` in `vite.config` and redeploying at 12:30 EDT.

## Impact
- Environment: docs site deploy preview only.
- All `/guides/*` pages unreachable (404).
- Reviewer workflow blocked for guide changes; no evidence of production impact.

## Timeline
- 2026-08-28 11:05 EDT: Detection — reviewer click-through finds `/guides/*` 404 on deploy preview.
- 2026-08-28 11:05–12:30 EDT: Diagnosis — traced to `base-path` change in `vite.config` without corresponding preview rewrite rule update.
- 2026-08-28 12:30 EDT: Mitigation — rewrite rules fixed and preview redeployed.
- 2026-08-28 12:30 EDT: Verification — `/guides/*` routes loading on preview.

## Root Cause
`vite.config` base-path change altered the served asset/route prefix, while preview hosting rewrite rules still matched the old prefix. Requests to `/guides/*` fell through rewrites and returned 404. The broken workflow was the preview; the causal mechanism was the uncoupled config change.

## Detection Gap
No automated preview link-check in CI. No health check asserted `/guides/*` routes on preview deploys. Detection depended on manual reviewer click-through.

## Corrective Actions
- Completed: Fixed preview rewrite rules to align with new base-path; redeployed preview (2026-08-28 12:30 EDT, verified).
- Pending: Add preview link-check CI job covering `/guides/*` routes.
- Deferred: None.

## Lessons
- Couple base-path and hosting rewrite changes as one atomic change with a preview route check.
- Preview deploys need an automated smoke signal for key route prefixes, not manual click-through alone.
