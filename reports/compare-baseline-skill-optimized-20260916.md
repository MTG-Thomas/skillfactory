# Baseline vs skill vs optimized 2026-09-16
Deterministic grader only (scripts/grade-incident-rca.ps1 + parity port). No LLM judge yet.
## Spark via jcode-main (opencode-go, muse-spark-1.3-contributor)
| case | baseline | skill |
| train 4 cases | 2/4 | 4/4 |
| val-01 docs-404 | FAIL 6 headings missing | FAIL actions-not-owned only |
| val-02 empty-backup | PASS | PASS |
## Flash via SkillOpt (deepseek-v4-flash, openai_compatible + session header)
| leg | result |
| selection baseline | hard=0.5 (val-01 FAIL actions-not-owned, val-02 PASS) |
| step1 train | hard=1.0 4/4 |
| step2 train | hard=1.0 4/4 |
| optimizer | 0 patches, best=initial, 10 calls, 35873 tokens |
## Verdict
Skill beats baseline structurally on both models. Optimizer found no headroom on train (ceiling) and correctly held the gate. No adoption: candidate == canonical modulo trailing newline.
Failure signature is cross-model: action-ownership reference flakes on val-01 under spark AND flash. Next: LLM-judge depth rubric, bigger val set (gate ceiling at 2 items), codex cross-harness.
