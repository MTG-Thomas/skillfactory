# SkillFactory

Harness-agnostic Agent Skill lifecycle: **create, inspect, validate, evaluate, optimize, compare, approve, adopt**.

Status: proof-out spike. Public under MTG-Thomas until the methodology earns its existence.

## Principle

Separate: skill artifact, eval corpus, execution harness, model/provider, evaluator, optimizer.
A skill must never become "a jcode skill tested by Muse." Test `skill x harness x model x provider`.

## Layout

```text
.skillfactory/config
experiments/
corpora/lightweight-incident-rca/{train,validation}/
corpora/thread-open-loop-reviewer/{train,validation}/
candidates/
runs/
reports/
scripts/
```

## Proof skills

1. `lightweight-incident-rca` — structured generation, deterministic shape checks.
2. `thread-open-loop-reviewer` — detection precision/recall, blind A/B friendly.

## Usage (target)

```text
skillfactory inspect <skill>
skillfactory validate <skill>
skillfactory eval <skill>
skillfactory optimize <skill>
skillfactory compare <run-a> <run-b>
skillfactory adopt <candidate>
```

See `experiments/proof-01.yaml`. Raw artifacts preserved under `runs/`.
