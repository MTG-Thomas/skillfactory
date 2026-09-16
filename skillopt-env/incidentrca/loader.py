"""Loader: markdown case files. id = filename stem, input = file text."""
from __future__ import annotations

from pathlib import Path

from skillopt.datasets.base import SplitDataLoader


def _normalize_item(path: Path) -> dict:
    stem = path.stem
    prefix = stem.split("-")[0] if "-" in stem else "misc"
    return {
        "id": stem,
        "input": path.read_text(encoding="utf-8"),
        "task_type": prefix,
    }


class IncidentRCALoader(SplitDataLoader):
    def load_split_items(self, split_path: str) -> list[dict]:
        path = Path(split_path)
        return [_normalize_item(p) for p in sorted(path.glob("*.md"))]

    def load_raw_items(self, data_path: str) -> list[dict]:
        path = Path(data_path)
        items: list[dict] = []
        for sub in ("train", "validation", "test", "val"):
            d = path / sub
            if d.is_dir():
                items.extend(_normalize_item(p) for p in sorted(d.glob("*.md")))
        return items
