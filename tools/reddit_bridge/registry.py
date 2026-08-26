from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from .models import RedditSource

DEFAULT_REGISTRY_PATH = Path(__file__).resolve().parents[2] / "references" / "community" / "reddit-source-registry.json"


def load_registry(path: Path | str = DEFAULT_REGISTRY_PATH) -> List[RedditSource]:
    registry_path = Path(path)
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    sources = [RedditSource.from_dict(item) for item in payload.get("sources", [])]
    source_ids = [source.source_id for source in sources]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("Duplicate source_id values in Reddit source registry")
    return sources


def registry_by_id(path: Path | str = DEFAULT_REGISTRY_PATH) -> Dict[str, RedditSource]:
    return {source.source_id: source for source in load_registry(path)}
