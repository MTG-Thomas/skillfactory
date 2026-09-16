# Incident: Nightly backup reported success but restored 0 rows - 2026-08-21

**Summary:** Nightly backup job reported success but produced an empty dump. Issue found during restore drill on 2026-08-21 at 10:00 EDT when restore yielded 0 rows.

**Impact:** Backups were effectively missing. No production outage. Restore capability was compromised until fix.

**Timeline:**
- 2026-08-21 10:00 EDT: Restore drill detected 0-row restore.
- Post detection: Diagnosed pg_dump targeting wrong schema.
- Mitigation: Fixed connection string and added row-count gate. Verification pending.

**Root Cause:** Connection-string rotation pointed pg_dump at an empty staging schema. pg_dump exited 0 on empty dump, so the job reported success.

**Detection Gap:** No row-count assertion in job. No alert on 0-row dump. Only manual restore drill caught it.

**Corrective Actions:**
- Completed: Fixed connection string.
- Pending verification: Row-count gate in backup job.
- Pending: Alert on 0-row dump. Defined drill schedule.

**Lessons:** Backup success must require restore validation. Exit 0 is not proof of a usable backup.
