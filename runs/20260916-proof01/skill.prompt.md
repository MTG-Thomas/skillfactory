Follow this skill exactly:

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


SITUATION:
# Case 01 — CI red after dependency bump

## Input (evidence)
- Repo: example-api, branch renovate/requests-2.32, CI job #4812 failed 2026-09-10 14:02 EDT.
- Error: `ImportError: cannot import name 'Mapping' from 'collections'` in tests/unit/test_auth.py.
- Cause chain: requests 2.32 dropped py2 shim; app pinned Python 3.11, unpinned requests; lockfile regenerated without running unit tests locally.
- Detection: CI only. No local pre-push hook. Dependabot PR merged without focused test run.
- Mitigation: reverted to requests 2.31 in PR #4820, CI green 2026-09-10 15:47 EDT. Pending: pin policy + pre-merge unit gate.
- Related: PR #4819 (bump), PR #4820 (revert), runbook docs/ci.md.

## Task
Write a lightweight incident RCA note following the standard shape
(Summary, Impact, Timeline, Root Cause, Detection Gap, Corrective Actions, Lessons).
Keep it concise, blameless, with absolute timestamps and owned corrective actions.
Do NOT paste raw logs; summarize the causal mechanism.

