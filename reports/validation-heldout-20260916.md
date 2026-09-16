# Held-out validation 2026-09-16
Runner: jcode-main v0.84.0-dev, provider opencode-go, model muse-spark-1.3-contributor.
Grader: scripts/grade-incident-rca.ps1 deterministic.
| case | baseline | skill |
| val-01 docs-404 | FAIL 6 headings missing | FAIL actions-not-owned only |
| val-02 empty-backup | PASS | PASS |
Read: skill lift holds on held-out cases. Train was baseline 2/4 skill 4/4.
Val-01 shows the gap crisply: baseline collapses to 7 lines, skill keeps 30-line full shape.
Next: LLM-judge depth rubric, SkillOpt candidate, cross-harness via codex exec.
