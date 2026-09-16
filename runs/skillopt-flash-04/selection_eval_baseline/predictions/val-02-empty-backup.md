# Lightweight Incident RCA: Empty Nightly Backup Dump

## Summary
The nightly backup job reported success but produced an empty pg_dump archive. The invalid backup was discovered during a restore drill on 2026-08-21 when the restore returned 0 rows. Service was restored by correcting the backup connection string and adding a row-count gate.

## Impact
- Restore drill failed because the backup archive contained no data.
- Nightly backup artifact was unusable for DR/restore purposes.
- No production user-facing outage was reported.

## Timeline
- 2026-08-21 10:00 EDT — Restore drill detected that the nightly backup restored 0 rows.
- 2026-08-21, during drill session — Diagnosed: pg_dump targeted an empty staging schema after connection-string rotation; exit code 0 masked the empty dump.
- 2026-08-21, during drill session — Mitigated: corrected connection string and added a row-count gate. Row-count gate verification is pending.

## Root Cause
A connection-string rotation caused the nightly backup job’s pg_dump command to connect to an empty staging schema. pg_dump exited with status 0 because the connection succeeded and the dump was valid; it simply contained no rows. The backup job treated exit 0 as success and did not validate that data was actually dumped.

## Detection Gap
- The backup job had no row-count assertion after pg_dump completed.
- No alert existed for 0-row dumps.
- The only detection path was a manual restore drill.

## Corrective Actions
Completed:
- Fixed the backup connection string to point at the correct schema/database.
- Added a row-count gate to the backup job (verification pending).

Pending:
- Alert on 0-row dump.
- Schedule recurring restore drills to validate backup usability.

## Lessons
- Exit code 0 from pg_dump does not prove data was dumped; assert row counts on backup artifacts.
- Restore drills are required to verify that backups are actually restorable.
- Connection-string rotations must include validation that the backup job still targets the expected schema and returns expected row counts.