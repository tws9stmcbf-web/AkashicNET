from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class ItemRecord:
    drive_id: str
    title: str
    parent_folder_id: Optional[str] = None
    parent_folder_path: str = ""
    file_type: str = "unknown"
    mime_type: str = "unknown"
    size_bytes: Optional[int] = None
    drive_url: str = ""
    canonical_source_url: str = ""
    author_name: str = "unknown"
    source_name: str = "unknown"
    date_raw: str = "unknown"
    year: Optional[int] = None
    subject_category: str = "unknown"
    source_type: str = "unknown"
    licence_status: str = "unknown"
    reuse_decision: str = "INDEX_ONLY"
    provenance_status: str = "link_only"
    last_seen_at: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    content_hash: Optional[str] = None
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "drive_id": self.drive_id,
            "title": self.title,
            "parent_folder_id": self.parent_folder_id,
            "parent_folder_path": self.parent_folder_path,
            "file_type": self.file_type,
            "mime_type": self.mime_type,
            "size_bytes": self.size_bytes,
            "drive_url": self.drive_url,
            "canonical_source_url": self.canonical_source_url,
            "author_name": self.author_name,
            "source_name": self.source_name,
            "date_raw": self.date_raw,
            "year": self.year,
            "subject_category": self.subject_category,
            "source_type": self.source_type,
            "licence_status": self.licence_status,
            "reuse_decision": self.reuse_decision,
            "provenance_status": self.provenance_status,
            "last_seen_at": self.last_seen_at,
            "content_hash": self.content_hash,
            "notes": self.notes,
        }


@dataclass
class CheckpointState:
    run_id: str
    source_url: str
    last_folder_id: Optional[str] = None
    last_cursor: Optional[str] = None
    batch_index: int = 0
    processed_count: int = 0
    skipped_count: int = 0
    duplicate_count: int = 0
    error_count: int = 0
    discovered_count: int = 0
    index_only_count: int = 0
    link_plus_metadata_count: int = 0
    import_count: int = 0
    updated_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    completed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "source_url": self.source_url,
            "last_folder_id": self.last_folder_id,
            "last_cursor": self.last_cursor,
            "batch_index": self.batch_index,
            "processed_count": self.processed_count,
            "skipped_count": self.skipped_count,
            "duplicate_count": self.duplicate_count,
            "error_count": self.error_count,
            "discovered_count": self.discovered_count,
            "index_only_count": self.index_only_count,
            "link_plus_metadata_count": self.link_plus_metadata_count,
            "import_count": self.import_count,
            "updated_at_utc": self.updated_at_utc,
            "completed": self.completed,
        }


@dataclass
class BatchSummary:
    run_id: str
    batch_index: int
    items_seen: int
    items_processed: int
    items_skipped: int
    duplicates: int
    failures: int
    index_only: int
    link_plus_metadata: int
    import_approved: int
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "batch_index": self.batch_index,
            "items_seen": self.items_seen,
            "items_processed": self.items_processed,
            "items_skipped": self.items_skipped,
            "duplicates": self.duplicates,
            "failures": self.failures,
            "index_only": self.index_only,
            "link_plus_metadata": self.link_plus_metadata,
            "import_approved": self.import_approved,
            "timestamp_utc": self.timestamp_utc,
        }
