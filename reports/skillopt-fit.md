# SkillOpt fit assessment (2026-09-16, source read of microsoft/SkillOpt @ main)

Verdict: consume, do not reinvent. SkillOpt already provides the optimizer leg.

1. Skill document is the trainable state; output is `best_skill.md` (300-2000
   tokens). Maps directly to our `candidates/` dir. Canonical skill untouched
   during optimization, as our spike requires.
2. Validation-gated by default: candidate accepted only on strict held-out
   improvement. Matches our train/validation split.
3. `skillopt/model/openai_compatible_backend.py`: generic OpenAI-compatible
   backend (base_url + api_key via openai SDK). Our runner maps to it with
   zero new code: base_url=https://opencode.ai/zen/go/v1,
   model=muse-spark-1.3-contributor, key=OPENCODE_GO_API_KEY.
4. `skillopt/model/codex_harness.py`: subprocess CLI harness pattern
   (cf. our `jcode-main run --json` adapter). If we want jcode-as-harness
   inside SkillOpt rather than direct endpoint, mirror this file.
5. Custom env needed: `skillopt/envs/` is per-benchmark (alfworld, searchqa,
   ...). Our corpus (4 train + 2 held-out) + `grade-incident-rca.ps1` becomes
   one small env module. That is the intended extension point.

Rejected: writing our own optimizer loop (redundant), Harbor for this phase
(still fallback only), full SkillOpt harness adoption before one custom-env
trial proves the reward signal transfers.

Next: implement minimal incident-rca env, run SkillOpt train on our 4 train
cases, evaluate `best_skill.md` on held-out validation + cross-check with a
second harness before any adopt decision.
