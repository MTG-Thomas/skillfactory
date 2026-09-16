"""Incident-RCA adapter: rollout under skill, deterministic reward.

Reward is a 1:1 port of SkillFactory scripts/grade-incident-rca.ps1:
7 headings, timestamps, action split + ownership, blameless, concise,
no secrets/log-dumps. hard = all checks pass; soft = fraction passing.
Reflection uses the shared default (no override).
"""
from __future__ import annotations

import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from skillopt.datasets.base import BatchSpec
from skillopt.envs.base import EnvAdapter
from skillopt.envs.incidentrca.loader import IncidentRCALoader
from skillopt.model import chat_target_messages

HEADINGS = (
    "Summary",
    "Impact",
    "Timeline",
    "Root Cause",
    "Detection Gap",
    "Corrective Actions",
    "Lessons",
)
_BLAME = ("blame", "stupid", "careless", "lazy", "incompetent", r"\bfault of\b")
_SECRET = r"ghp_[A-Za-z0-9]+|sk-(live|test)-|xox[bap]-|-----BEGIN .*PRIVATE KEY"
_TS = r"\d{4}-\d{2}-\d{2}|\d{1,2}:\d{2}\s*(EDT|EST|UTC)|2026-"
_OWNED = r"(?i)(PR\s*#\d+|OPS-\d+|runbook|docs/|alert|monitor|DLQ|gate|PR #)"


def grade_note(text: str) -> tuple[bool, float, list[str]]:
    fails: list[str] = []
    for h in HEADINGS:
        if not re.search(rf"(?im)^\s*(#{{1,4}}\s*)?.*\b{h}\b.*$", text):
            fails.append(f"missing-heading:{h}")
    if not re.search(_TS, text):
        fails.append("missing-timestamp")
    if not re.search(r"(?i)completed|pending|deferred", text):
        fails.append("actions-not-split")
    if not re.search(_OWNED, text):
        fails.append("actions-not-owned")
    for b in _BLAME:
        if re.search(rf"(?i){b}", text):
            fails.append(f"blame-language:{b}")
            break
    if re.search(_SECRET, text):
        fails.append("possible-secret")
    if len(text.splitlines()) > 60:
        fails.append("too-long")
    for m in re.finditer(r"```[\s\S]*?```", text):
        if len(m.group(0).split("\n")) > 15:
            fails.append("log-dump")
            break
    total = len(HEADINGS) + 6
    passed = total - len(fails)
    soft = max(0.0, min(1.0, passed / total))
    return (not fails, soft, fails)


SYSTEM_TMPL = (
    "Follow this skill exactly. Reply with ONLY the incident note text, "
    "do not create files.\n\n{skill}\n"
)


class IncidentRCAAdapter(EnvAdapter):
    def __init__(
        self,
        split_dir: str = "",
        data_path: str = "",
        split_mode: str = "split_dir",
        seed: int = 42,
        limit: int = 0,
        workers: int = 4,
        max_completion_tokens: int = 2048,
        analyst_workers: int = 4,
        failure_only: bool = False,
        minibatch_size: int = 8,
        edit_budget: int = 4,
        **kwargs,
    ) -> None:
        self.workers = workers
        self.max_completion_tokens = int(max_completion_tokens)
        self.analyst_workers = analyst_workers
        self.failure_only = failure_only
        self.minibatch_size = minibatch_size
        self.edit_budget = edit_budget
        self.dataloader = IncidentRCALoader(
            split_dir=split_dir,
            data_path=data_path,
            split_mode=split_mode,
            seed=seed,
            limit=limit,
        )

    def setup(self, cfg: dict) -> None:
        super().setup(cfg)
        self.dataloader.setup(cfg)

    def get_dataloader(self):
        return self.dataloader

    def build_env_from_batch(self, batch: BatchSpec, **kwargs):
        return list(batch.payload or [])

    def build_train_env(self, batch_size: int, seed: int, **kwargs):
        batch = self.dataloader.build_train_batch(
            batch_size=batch_size, seed=seed, **kwargs
        )
        return self.build_env_from_batch(batch, **kwargs)

    def build_eval_env(self, env_num: int, split: str, seed: int, **kwargs):
        batch = self.dataloader.build_eval_batch(
            env_num=env_num, split=split, seed=seed, **kwargs
        )
        return self.build_env_from_batch(batch, **kwargs)

    def _run_one(self, item: dict, skill_content: str, pred_dir: str) -> dict:
        messages = [
            {"role": "system", "content": SYSTEM_TMPL.format(skill=skill_content)},
            {"role": "user", "content": item["input"]},
        ]
        text, _ = chat_target_messages(
            messages, max_completion_tokens=self.max_completion_tokens
        )
        text = str(text)
        with open(os.path.join(pred_dir, f"{item['id']}.md"), "w", encoding="utf-8") as f:
            f.write(text)
        ok, soft, fails = grade_note(text)
        return {
            "id": str(item["id"]),
            "hard": 1 if ok else 0,
            "soft": soft,
            "task_type": item.get("task_type", "misc"),
            "fails": fails,
        }

    def rollout(self, env_manager, skill_content: str, out_dir: str, **kwargs):
        pred_dir = os.path.join(out_dir, "predictions")
        os.makedirs(pred_dir, exist_ok=True)
        results: list[dict] = []
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            futs = {
                pool.submit(self._run_one, item, skill_content, pred_dir): item
                for item in env_manager
            }
            for fut in as_completed(futs):
                results.append(fut.result())
        return results

    def get_task_types(self):
        return ["case", "val"]
