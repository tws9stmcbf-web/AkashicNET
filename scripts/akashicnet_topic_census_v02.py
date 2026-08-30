#!/usr/bin/env python3
"""AkashicNET topic census v0.2.

Deterministic, metadata-only census. This script does not crawl Google Drive,
Reddit, Wikipedia or Wikidata. It counts tracked source labels, applies a small
explicit alias table, excludes known non-topic expansion records, and reports
strict/inclusive vocabulary statistics without claiming semantic completeness.
"""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"
TOPICS = ROOT / "references" / "topics"

ALIASES = {
    "catholocism": "catholicism",
    "rosicurcianism": "rosicrucianism",
    "rosicrucianism": "rosicrucianism",
}

NON_TOPIC_ROOTS = {"pdf", "uncategorized", "textbooks", "reference", "biographies", "fiction"}


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").strip()
    value = re.sub(r"\s+", " ", value)
    key = value.casefold()
    return ALIASES.get(key, key)


def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def find_col(row: dict, candidates: tuple[str, ...]):
    lookup = {norm(k): k for k in row}
    for c in candidates:
        if norm(c) in lookup:
            return row.get(lookup[norm(c)], "")
    return ""


def collect_drive_roots():
    rows = read_csv(COMMUNITY / "drive-metadata-root-census.csv")
    labels = set()
    excluded = set()
    for row in rows:
        raw = find_col(row, ("root_name", "name", "folder_name", "collection", "label", "topic"))
        if not raw:
            # Census files have evolved; choose the first non-numeric descriptive field.
            for v in row.values():
                if v and not str(v).strip().isdigit() and "/" not in str(v):
                    raw = str(v).strip(); break
        n = norm(raw)
        if not n:
            continue
        if n in NON_TOPIC_ROOTS:
            excluded.add(n)
        else:
            labels.add(n)
    return labels, excluded, len(rows)


def collect_n2n():
    rows = read_csv(COMMUNITY / "n2n-pilot-index.csv")
    categories, frameworks, edges = set(), set(), set()
    for r in rows:
        c, f = norm(r.get("category", "")), norm(r.get("toolkit_framework", ""))
        if c: categories.add(c)
        if f: frameworks.add(f)
        if c and f: edges.add((c, f))
    return categories, frameworks, edges, len(rows)


def collect_expansion():
    rows = read_csv(TOPICS / "topic-expansion-cross-source-v0.1.csv")
    accepted = set()
    for r in rows:
        if norm(r.get("adjudication", "")) == "accept" and norm(r.get("provisional_additive", "")) == "yes":
            accepted.add(norm(r.get("canonical_topic", "")))
    return accepted, len(rows)


def main():
    roots, root_excluded, root_rows = collect_drive_roots()
    cats, frameworks, edges, n2n_rows = collect_n2n()
    expansion, expansion_rows = collect_expansion()

    # v0.7.4 historical checkpoint: 53 WikiSpine seeds is independently recorded
    # in repository history but the complete historical batch set is not guaranteed
    # to exist on this active branch. Therefore it is reported, not silently added.
    tracked_union = roots | cats | frameworks | expansion
    report = {
        "version": "0.2",
        "method": "tracked_metadata_explicit_labels_only",
        "drive_crawl_performed": False,
        "drive_root_rows_examined": root_rows,
        "drive_root_semantic_topics": len(roots),
        "drive_root_excluded_non_topic_labels": sorted(root_excluded),
        "n2n_records_examined": n2n_rows,
        "n2n_unique_categories": len(cats),
        "n2n_unique_frameworks": len(frameworks),
        "n2n_category_framework_edges": len(edges),
        "expansion_records_examined": expansion_rows,
        "expansion_provisional_additive_topics": len(expansion),
        "tracked_active_branch_union": len(tracked_union),
        "historical_wikispine_seed_checkpoint": 53,
        "historical_wikispine_note": "Reported separately until all historical v0.7.x seed batches are materialised or deterministically reconstructed on the active branch.",
        "audited_333_reached": False,
        "counting_warning": "Do not add the 53 WikiSpine checkpoint to tracked_active_branch_union without identity-level deduplication.",
    }
    out = ROOT / "artifacts" / "akashicnet-topic-census-v0.2.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
