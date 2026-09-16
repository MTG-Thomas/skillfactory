# Provenance

`incidentrca/` + `configs/default.yaml` are SkillFactory-owned files,
mirrored into a microsoft/SkillOpt checkout at:
- skillopt/envs/incidentrca/ (adapter.py, loader.py, __init__.py)
- configs/incidentrca/default.yaml
- scripts/train.py: registration block appended after swebench entry.

Reward parity verified 2026-09-16: Python grade_note == grade-incident-rca.ps1
on good-example (PASS), bad-example (FAIL 10), skill-spark.t1 (PASS),
baseline-spark.t3 (FAIL 1). See tmp-upstream/parity-check.out (scratch).
