#!/usr/bin/env python3
"""AkashicNET v0.7.5 deterministic topic census over public repository metadata.

This deliberately counts topic-bearing labels, not posts, documents, works, authors,
or Drive folder nodes as such. The current repository does not publish the live Drive
folder-label CSV, so Drive contributes provenance coverage but not unreviewed labels.
"""
from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"

WIKISPINE_FILES = [
    "wikispine-seed-v0.7.0.json",
    "wikispine-batch-a-v0.7.1.json",
    "wikispine-batch-b-v0.7.1.json",
    "wikispine-batch-c-v0.7.2.json",
    "wikispine-batch-d-v0.7.2.json",
    "wikispine-batch-e-science-v0.7.3.json",
    "wikispine-batch-f-v0.7.4.json",
]
ONTOLOGY_FILE = "concept-seed-v0.20.csv"
N2N_FILE = "n2n-pilot-index.csv"
DRIVE_CHECKPOINT = "drive-live-full-census-checkpoint-v0.5.0.md"

# Only deterministic spelling/format aliases. No semantic merging by similarity.
ALIASES = {
    "qabbalah": "kabbalah",
    "quabbalah": "kabbalah",
    "cabala": "kabbalah",
    "contemplative practice": "meditation",
    "psychedelic": "psychedelics",
}


def norm(label: str) -> str:
    s = label.strip().lower()
    s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return ALIASES.get(s, s)


def load_ontology() -> list[str]:
    with (COMMUNITY / ONTOLOGY_FILE).open(newline="", encoding="utf-8") as f:
        return [r["label"].strip() for r in csv.DictReader(f) if r.get("label", "").strip()]


def records_from_json(obj):
    if isinstance(obj, dict):
        if isinstance(obj.get("records"), list):
            return obj["records"]
        if isinstance(obj.get("resolved_records"), list):
            return obj["resolved_records"]
    return []


def load_wikispine() -> list[str]:
    out = []
    for name in WIKISPINE_FILES:
        p = COMMUNITY / name
        obj = json.loads(p.read_text(encoding="utf-8"))
        for r in records_from_json(obj):
            label = (r.get("akashic_concept") or r.get("concept") or r.get("label") or "").strip()
            if label:
                out.append(label)
    return out


def load_n2n_categories() -> list[str]:
    with (COMMUNITY / N2N_FILE).open(newline="", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        return sorted({r.get("category", "").strip() for r in rows if r.get("category", "").strip()})


def main() -> int:
    ontology = load_ontology()
    wiki = load_wikispine()
    n2n = load_n2n_categories()

    source_sets = {
        "reviewed_ontology": {norm(x) for x in ontology},
        "wikispine": {norm(x) for x in wiki},
        "n2n_metadata_categories": {norm(x) for x in n2n},
    }
    union = set().union(*source_sets.values())

    drive_text = (COMMUNITY / DRIVE_CHECKPOINT).read_text(encoding="utf-8")
    m_folders = re.search(r"unique folder IDs:\s*\*\*(\d+)\*\*", drive_text)
    m_objects = re.search(r"unique non-folder object IDs:\s*\*\*(\d+)\*\*", drive_text)
    drive_folder_count = int(m_folders.group(1)) if m_folders else None
    drive_object_count = int(m_objects.group(1)) if m_objects else None

    # Stable display list: choose title-cased source spellings where possible.
    display = {}
    for source, labels in (("ontology", ontology), ("wikispine", wiki), ("n2n", n2n)):
        for label in labels:
            display.setdefault(norm(label), {"label": label, "sources": []})
            if source not in display[norm(label)]["sources"]:
                display[norm(label)]["sources"].append(source)

    result = {
        "version": "0.7.5",
        "milestone": "AUDITED_PUBLIC_METADATA_TOPIC_CENSUS",
        "method": "deterministic normalized union of topic-bearing labels from reviewed ontology, WikiSpine concepts, and N2N metadata categories",
        "source_counts": {k: len(v) for k, v in source_sets.items()},
        "audited_unique_topics": len(union),
        "topics": [display[k] for k in sorted(union)],
        "drive_context": {
            "unique_folder_ids": drive_folder_count,
            "unique_non_folder_object_ids": drive_object_count,
            "folder_labels_in_public_repo": False,
            "included_in_topic_union": False,
            "reason": "The live Drive folder-label CSV is not present in main; counting unpublished labels would break reproducibility and the privacy boundary.",
        },
        "full_cross_source_total_status": "INCOMPLETE_PENDING_SANITIZED_DRIVE_TOPIC_LABELS",
        "public_claim": "300+ remains an estimate until a privacy-safe Drive topic-label snapshot is reviewed and incorporated.",
        "guardrails": {
            "document_count_is_topic_count": False,
            "folder_node_count_is_topic_count": False,
            "semantic_similarity_auto_merge": False,
            "truth_inference": False,
            "rights_promotion": False,
            "scientific_evidence_promotion": False,
            "drive_access_performed": False,
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
