# VAL 02 (HELD OUT — never optimize against this)

## Input (evidence)
- Nightly backup job reported success but restored 0 rows, found 2026-08-21 during restore drill 10:00 EDT.
- Cause chain: pg_dump targeted empty staging schema after connection-string rotation; exit 0 masked empty dump.
- Detection: drill only. No row-count assertion in job.
- Mitigation: fixed connection string, added row-count gate (pending verification).
- Pending: alert on 0-row dump, drill schedule.

## Task
Same shape contract. Used ONLY for final verdict.
