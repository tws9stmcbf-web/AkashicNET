from __future__ import annotations

from typing import Dict, List


SUBJECT_TAXONOMY = {
    "consciousness",
    "philosophy",
    "neuroscience",
    "contemplative practices",
    "wisdom traditions",
    "human development",
    "cultural memory",
    "symbolic systems",
    "literature",
    "art / visual culture",
    "ecology / nature",
    "community discourse",
    "speculative frameworks",
    "unknown",
}

SOURCE_TYPES = {
    "book",
    "article",
    "essay",
    "transcript",
    "lecture",
    "image",
    "diagram",
    "audio",
    "video",
    "notebook",
    "archive bundle",
    "unknown",
}


def classify_subject(title: str, folder_path: str = "") -> str:
    combined = f"{title} {folder_path}".lower()
    if any(term in combined for term in ["philosophy", "wisdom", "spiritual", "mystic"]):
        return "philosophy"
    if any(term in combined for term in ["consciousness", "mind", "awareness", "experience"]):
        return "consciousness"
    if any(term in combined for term in ["memory", "archive", "library", "codex"]):
        return "cultural memory"
    if any(term in combined for term in ["art", "image", "visual", "symbol"]):
        return "art / visual culture"
    if any(term in combined for term in ["science", "neuro", "brain"]):
        return "neuroscience"
    if any(term in combined for term in ["community", "forum", "discussion", "thread"]):
        return "community discourse"
    return "unknown"


def classify_source_type(title: str, mime_hint: str = "") -> str:
    combined = f"{title} {mime_hint}".lower()
    if any(term in combined for term in ["pdf", "essay", "article", "paper", "report"]):
        return "article"
    if any(term in combined for term in ["audio", "mp3", "wav", "podcast"]):
        return "audio"
    if any(term in combined for term in ["video", "mp4", "mov", "youtube"]):
        return "video"
    if any(term in combined for term in ["image", "png", "jpg", "jpeg", "svg"]):
        return "image"
    if "transcript" in combined or "notes" in combined:
        return "transcript"
    if "book" in combined or "library" in combined:
        return "book"
    return "unknown"


def classify_reuse_decision(licence_status: str, title: str = "") -> str:
    normalized = (licence_status or "").lower()
    if any(term in normalized for term in ["cc0", "cc-by", "public domain", "open licence", "creative commons", "permitted"]):
        return "IMPORT"
    if any(term in normalized for term in ["unknown", "unclear", "not stated", "review required"]):
        return "INDEX_ONLY"
    if any(term in normalized for term in ["copyright", "all rights reserved", "restricted", "not permitted"]):
        return "INDEX_ONLY"
    if "link" in normalized:
        return "LINK_PLUS_METADATA"
    return "INDEX_ONLY"


def classify_licence_status(raw_note: str = "") -> str:
    lowered = (raw_note or "").lower()
    if not lowered:
        return "unknown"
    if any(term in lowered for term in ["cc0", "creative commons", "public domain", "open licence", "open access"]):
        return "explicit_open_licence"
    if any(term in lowered for term in ["copyright", "all rights reserved", "restricted"]):
        return "restricted"
    if any(term in lowered for term in ["review required", "unclear", "unknown", "not stated"]):
        return "unknown"
    return "unknown"
