# Provenance

`incidentrca/` + `configs/default.yaml` are SkillFactory-owned files,
mirrored into a microsoft/SkillOpt checkout at:
- skillopt/envs/incidentrca/ (adapter.py, loader.py, __init__.py)
- configs/incidentrca/default.yaml
- scripts/train.py: registration block appended after swebench entry.

Reward parity verified 2026-09-16: Python grade_note == grade-incident-rca.ps1
on good-example (PASS), bad-example (FAIL 10), skill-spark.t1 (PASS),
baseline-spark.t3 (FAIL 1). See tmp-upstream/parity-check.out (scratch).

## Endpoint correction (2026-09-16, from https://opencode.ai/docs/go/)
Muse Spark serves ONLY /v1/responses, not /v1/chat/completions, so
SkillOpt openai_compatible backend cannot drive it directly (500s).
Train on deepseek-v4-flash via chat/completions (proven direct OK);
keep jcode-main + spark as the independent cross-model check.
Bonus: flash has 0-day retention; spark-contributor trains on prompts.
## Session header (2026-09-16)
opencode Go chat/completions 400s MissingSessionID without x-opencode-session. Scratch patch adds _session_headers to openai_compatible_backend._build_client (env OPENAI_COMPATIBLE_SESSION_ID or generated id, opencode hosts only). Upstream contribution candidate.
## Mirror fixes (2026-09-16)
train.py incidentrca registration had broken try/except nesting; repaired to sequential blocks in scratch checkout.
adapter now takes gradient/optimizer init params (analyst_workers, failure_only, minibatch_size, edit_budget) or base reflect crashes. Fixed in owned adapter and mirrored.
split/ is gitignored scratch: train = 4 train cases, val = 2 validation cases, test = empty. Rebuild from corpora.
