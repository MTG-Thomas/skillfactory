# Incident: Nightly Backup Success With 0 Rows Restored — 2026-08-21

## Summary
Nightly backup job reported success but produced an empty dump. pg_dump targeted an empty staging schema after connection-string rotation, and exit 0 masked the empty result. Found during restore drill on 2026-08-21 at 10:00 EDT. Service restored by fixing the connection string; row-count gate added but pending verification.

## Impact
- Affected workflow: nightly backup and restore readiness.
- Restores from affected backups would return 0 rows.
- No production outage reported; impact was latent backup integrity failure.

## Timeline
- Detection: 2026-08-21 10:00 EDT — restore drill restored 0 rows despite job reporting success.
- Diagnosis: 2026-08-21 — identified pg_dump targeted empty staging schema after connection-string rotation.
- Mitigation: date/time unknown — connection string fixed; row-count gate added.
- Verification: pending — row-count gate not yet verified.

## Root Cause
Connection-string rotation pointed pg_dump at an empty staging schema instead of production. pg_dump exited 0 on the empty source, so the job framework treated an empty dump as success.

## Detection Gap
No row-count assertion in the backup job. No alert on 0-row or empty dump. Existing job success signal was exit code only. Detection relied solely on manual restore drill.

## Corrective Actions
- Completed: fixed connection string to target correct schema.
- Completed: added row-count gate to backup job.
- Pending verification: confirm row-count gate fails closed on empty dump.
- Pending: alert on 0-row dump.
- Pending: defined restore drill schedule.

## Lessons
- Exit 0 is not proof of useful output; assert on row count or dump size for backups.
- Connection-string rotations need post-change backup validation.
- Restore drills are a control, not a supplement; schedule them explicitly.
