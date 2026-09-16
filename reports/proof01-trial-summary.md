# Proof01 results (2026-09-16, muse-spark-1.3-contributor via opencode-go + jcode-main)

Runner: jcode-main v0.84.0-dev, isolated -C workspaces, no-files constraint, raw JSON preserved.
Grader: scripts/grade-incident-rca.ps1 (deterministic, no LLM).

| case | baseline | skill |
|---|---|---|
| 01-ci-red t1 | pass (14 lines) | pass (38 lines, full headings + deferred split) |
| 01-ci-red t2 | pass (21 lines) | pass (21 lines) |
| 01-ci-red t3 | FAIL actions-not-owned | pass (34 lines) |
| 02-auth-cert t1 | FAIL 5 headings missing | pass (26 lines) |

Totals: baseline 2/4, skill 4/4.

Read: skill consistently produces the full 7-heading shape with owned
completed/pending/deferred actions; baseline is bimodal (fine on a familiar
CI case, collapses on the auth case). Variance across trials is real, which is
why trials=3 matters. Deterministic grader separates on the harder case but
not the easy one — LLM-judge rubric still needed for quality depth.

Next: judge rubric (root-cause depth, detection-gap separation, action
ownership, 1-5 each, blind), then held-out validation, then SkillOpt candidate.
