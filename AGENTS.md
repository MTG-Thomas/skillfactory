# SkillFactory agent guide

SkillFactory is a proof-out spike for harness-independent skill evaluation. Read [README.md](README.md), [experiments/proof-01.yaml](experiments/proof-01.yaml), and the relevant reports before adding machinery. The CLI commands in the README are explicitly target usage, not evidence that an implemented CLI exists.

## Working areas

Keep skill artifacts, evaluation corpora, execution harnesses, model/provider selection, evaluators, and optimizers separate. `corpora/` separates training from validation; `candidates/` holds variants; `runs/` preserves raw trial artifacts; `reports/` records comparisons. Record the exact skill, harness, model, provider, prompt, and evaluator so results can be reproduced.

Never optimize against held-out validation cases and then describe the result as independent validation. Preserve baseline and candidate outputs, failures, and trial counts. Do not replace raw artifacts with a favorable summary or promote a candidate merely because its formatting score improved.

## Verification and limits

Inspect `scripts/` before using it. `scripts/eval.ps1` currently creates a run directory and prints a TODO; it does not execute the advertised evaluation lifecycle. `scripts/run-one.py` invokes an external harness and stores output, so running it can incur provider calls and expose prompt contents.

No CI suite or complete automated adoption gate was found. Validate the changed script or rubric directly and state the limitations. Use synthetic or sanitized cases; keep customer data, authentication material, and provider secrets out of corpora and run artifacts. Adoption into the versioned MTG skill package is a separate reviewed change, not a side effect of this experiment.
