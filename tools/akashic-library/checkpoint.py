from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Optional

module_path = Path(__file__).with_name("models.py")
if module_path.exists():
    spec = importlib.util.spec_from_file_location("akashic_library_models", module_path)
    if spec is not None and spec.loader is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        CheckpointState = module.CheckpointState
    else:  # pragma: no cover
        raise ImportError("Could not load models.py for CheckpointState")
else:  # pragma: no cover
    raise ImportError("models.py was not found alongside checkpoint.py")


class CheckpointStore:
    """Persist processing state so a batch can resume without restarting."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Optional[CheckpointState]:
        if not self.path.exists():
            return None

        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return CheckpointState(
            run_id=raw.get("run_id", "unknown"),
            source_url=raw.get("source_url", ""),
            last_folder_id=raw.get("last_folder_id"),
            last_cursor=raw.get("last_cursor"),
            batch_index=int(raw.get("batch_index", 0)),
            processed_count=int(raw.get("processed_count", 0)),
            skipped_count=int(raw.get("skipped_count", 0)),
            duplicate_count=int(raw.get("duplicate_count", 0)),
            error_count=int(raw.get("error_count", 0)),
            discovered_count=int(raw.get("discovered_count", 0)),
            index_only_count=int(raw.get("index_only_count", 0)),
            link_plus_metadata_count=int(raw.get("link_plus_metadata_count", 0)),
            import_count=int(raw.get("import_count", 0)),
            updated_at_utc=raw.get("updated_at_utc", ""),
            completed=bool(raw.get("completed", False)),
        )

    def save(self, state: CheckpointState) -> None:
        self.path.write_text(json.dumps(state.to_dict(), indent=2), encoding="utf-8")

    def reset(self) -> None:
        if self.path.exists():
            self.path.unlink()
