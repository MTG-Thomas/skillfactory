# SkillOpt custom env build spec: incident-rca (2026-09-16, from source)

Goal: train SkillOpt on our 4 train cases, validate on our 2 held-out cases,
reward from scripts/grade-incident-rca.ps1. All extension points verified in
microsoft/SkillOpt @ main (see tmp-upstream/, git-ignored).

## Files to add (inside a SkillOpt checkout, NOT this repo)

1. `skillopt/envs/incidentrca/adapter.py` — subclass `EnvAdapter`
   (contract: skillopt/envs/base.py):
   - `build_train_env` / `build_eval_env`: serve items straight through
     (`build_env_from_batch` default: `list(batch.payload)`). Loader can be
     trivial: read our 4 train + 2 validation case files by id.
   - `rollout(env_manager, skill_content, out_dir)`: per item, call
     `chat_target_messages` (skillopt.model) with system=skill_content,
     user=case input (mirrors officeqa/rollout.py chat path, ~line 385).
     Save note text under out_dir/predictions. Grade each note with the
     ported deterministic checks (7 headings, timestamps, action split +
     ownership, blameless, concise, no secrets/log-dump) -> hard 0/1.
     Soft = fraction of checks passing (mirrors RolloutResult contract:
     id str, hard 0/1, soft 0.0-1.0).
   - `reflect`: inherit default (shared minibatch reflect). No override.
   - `get_task_types`: ["ci-red", "auth-cert", "queue-stall", "bad-deploy"].
2. Register in `scripts/train.py` `_register_builtins`:
   `_ENV_REGISTRY["incidentrca"] = IncidentRCAAdapter`.
3. `configs/incidentrca/default.yaml` (copy env _template config):
   env.name=incidentrca, split_mode=split_dir pointing at our corpora,
   model.optimizer_backend + target_backend=openai_compatible,
   base_url=https://opencode.ai/zen/go/v1, model=muse-spark-1.3-contributor,
   key from OPENCODE_GO_API_KEY. Keep train tiny: epochs 2-3, batch 4
   (whole train set per batch), validation gate ON.

## Grader port

`scripts/grade-incident-rca.ps1` logic ports 1:1 to Python inside rollout
(regex set already proven: good-example passes, bad-example fails 10 ways).
Keep the .ps1 as the cross-harness re-check so SkillOpt-internal reward and
our independent eval cannot drift apart silently.

## Eval protocol (unchanged from spike)

- Never touch validation/ during training; SkillOpt gate reads it only.
- After train: take `best_skill.md` -> candidates/, run OUR independent loop
  (jcode-main + spark, trials=3, deterministic + blind judge rubric) on
  train AND held-out validation, plus a second harness before adopt.
- Optimizer (spark-via-SkillOpt) must not be the sole evaluator: our
  jcode-main loop re-scores every candidate from raw artifacts.

## Cost guard

Train rollouts ~= epochs(3) x cases(4) x target calls + reflection calls,
all on the cheap contributor model. No changes to SkillOpt core, no fork:
env module + config + registration line only. Upstream-contributable as-is.
