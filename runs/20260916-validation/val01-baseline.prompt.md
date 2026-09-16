Write an incident note for this situation. Be concise. Reply with ONLY the note text, do not create files.
# VAL 01 (HELD OUT — never optimize against this)

## Input (evidence)
- Docs site deploy preview 404s for all /guides/* routes, 2026-08-28 11:05-12:30 EDT.
- Cause chain: base-path change in vite.config without updating preview rewrite rules.
- Detection: reviewer click-through, no link-check in CI.
- Mitigation: rewrite fix + redeploy 12:30 EDT. Pending: preview link-check job.

## Task
Same shape contract as train. Used ONLY for final verdict.
