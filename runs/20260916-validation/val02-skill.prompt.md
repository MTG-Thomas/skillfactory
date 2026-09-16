Follow this skill exactly. Reply with ONLY the incident note text, do not create files.
---
name: lightweight-incident-rca
description: Use when Codex needs to write or update a concise incident note, RCA, postmortem, outage review, lessons-learned document, or operational retrospective after a production, dev, CI, infrastructure, automation, or workflow failure.
---

# Lightweight Incident RCA

Create short, blameless incident records that future operators can find and use.
Prefer durable repo docs over chat-only lessons when the incident changed code,
infra, monitoring, runbooks, or operating assumptions.

## Standard Shape

Use this structure unless the repo already has a stronger local convention:

- `Summary`: what failed, where, and what restored service.
- `Impact`: affected environment, users, workflows, or checks.
- `Timeline`: exact timestamps for detection, diagnosis, mitigation, and verification.
- `Root Cause`: the causal mechanism, not only the visible symptom.
- `Detection Gap`: why existing health checks, monitors, CI, or alerts missed it.
- `Corrective Actions`: split completed, pending, and intentionally deferred work.
- `Lessons`: reusable operating principles.

Keep the note concise. Do not turn it into a narrative transcript.

## Workflow

1. Gather evidence from issues, logs, commands, commits, PRs, monitoring output,
   and exact error text. Do not rely on memory when live artifacts are cheap to
   inspect.
2. Follow existing repo documentation layout. If none exists, use
   `docs/incidents/YYYY-MM-DD-short-incident-name.md`.
3. Use absolute dates and times with timezone when known.
4. Keep language blameless and system-focused.
5. Link related issues, PRs, commits, runbooks, and platform follow-ups.
6. Name detection and prevention gaps separately from the root cause.
7. Verify commands and PR/check status before claiming a corrective action is
   complete.

## Corrective Actions

Good actions are concrete and owned by an artifact:

- a merged or open PR
- a filed platform issue
- a changed runbook
- a monitor or alert
- a verified manual mitigation

Avoid vague actions such as `improve monitoring` unless paired with the exact
signal to monitor.

## Common Mistakes

- Confusing the first broken workflow with the root cause.
- Treating `service is up` as proof that deeper work can execute.
- Saying `no alerting` without naming the missing signal.
- Documenting secrets, tokens, customer data, or raw privileged logs.
- Leaving the lesson only in chat after code or infra changed.
# VAL 02 (HELD OUT — never optimize against this)

## Input (evidence)
- Nightly backup job reported success but restored 0 rows, found 2026-08-21 during restore drill 10:00 EDT.
- Cause chain: pg_dump targeted empty staging schema after connection-string rotation; exit 0 masked empty dump.
- Detection: drill only. No row-count assertion in job.
- Mitigation: fixed connection string, added row-count gate (pending verification).
- Pending: alert on 0-row dump, drill schedule.

## Task
Same shape contract. Used ONLY for final verdict.
