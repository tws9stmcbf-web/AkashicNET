#!/usr/bin/env python3
"""Close the explicit-topic audit over source-bearing Reddit Markdown."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "references" / "community" / "reddit-markdown-topic-closure-v0.7.17.json"
SOURCE_DOCUMENTS = [
    "data/reddit/README.md",
    "references/community/REDDIT_HISTORICAL_PROVENANCE_AUDIT_V0.7.md",
    "references/community/reddit-full-public-delta-scan-2026-09-01.md",
    *[
        f"references/community/reddit-manual-delta-checkpoint-{i:04d}.md"
        for i in range(1, 7)
    ],
    "tools/reddit_bridge/README.md",
]
DERIVATIVE_DOCUMENTS = [
    "references/community/reddit-canonical-delta-topic-audit-method-v0.7.14.md",
    "references/community/reddit-corroboration-topic-audit-method-v0.7.15.md",
    "references/community/reddit-csv-topic-closure-method-v0.7.11.md",
    "references/community/reddit-jsonl-metadata-audit-method-v0.7.12.md",
    "references/community/reddit-markdown-topic-closure-method-v0.7.17.md",
    "references/community/reddit-source-registry-topic-audit-method-v0.7.13.md",
    "references/community/reddit-structural-unified-topic-audit-method-v0.7.16.md",
    "references/community/reddit-topic-canonical-review-method-v0.7.9.md",
    "references/community/reddit-topic-census-seal-method-v0.7.18.md",
    "references/community/reddit-topic-promotion-method-v0.7.10.md",
    "references/community/reddit-topic-source-audit-method-v0.7.8.md",
]
FIELD_PATTERN = re.compile(
    r"(?i)^(link_flair_template_id|link_flair_text|categories|category|"
    r"topics|topic|flairs|flair)\s*[:|=]"
)


def explicit_fields(text):
    hits = []
    for line in text.splitlines():
        normalized = line.replace("**", "").replace("__", "").replace(chr(96), "")
        normalized = normalized.lstrip(" \t-*|#")
        match = FIELD_PATTERN.search(normalized)
        if match:
            hits.append(match.group(1).lower())
    return hits


def main() -> int:
    classified = SOURCE_DOCUMENTS + DERIVATIVE_DOCUMENTS
    missing = [path for path in classified if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit(f"missing classified Reddit Markdown: {missing}")

    all_reddit_markdown = sorted(
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*.md")
        if "reddit" in str(path.relative_to(ROOT)).lower()
    )
    unknown = sorted(set(all_reddit_markdown) - set(classified))
    if unknown:
        raise SystemExit(f"unclassified Reddit Markdown: {unknown}")

    hits = {}
    for path in SOURCE_DOCUMENTS:
        matches = explicit_fields((ROOT / path).read_text(encoding="utf-8"))
        if matches:
            hits[path] = matches
    if hits:
        raise SystemExit(f"explicit topic-bearing Markdown fields found: {hits}")

    result = {
        "version": "0.7.17",
        "status": "REDDIT_MARKDOWN_TOPIC_COVERAGE_CLOSED",
        "audited_public_top_level_topic_count": 73,
        "new_top_level_topics": [],
        "promotion_state": "NO_COUNT_CHANGE",
        "coverage": {
            "source_bearing_markdown_documents": len(SOURCE_DOCUMENTS),
            "source_documents": SOURCE_DOCUMENTS,
            "explicit_topic_category_or_flair_declarations": hits,
            "prior_census_method_documents_excluded_as_derivative": len(DERIVATIVE_DOCUMENTS),
            "markdown_explicit_topic_audit": "complete",
        },
        "decision": "The remaining source-bearing Reddit Markdown contains operational, provenance, and structural reporting only. Prior topic-audit methods are derivative governance records, not independent topic evidence.",
        "guardrails": {
            "heading_inference": False,
            "prose_inference": False,
            "url_inference": False,
            "method_document_is_source_evidence": False,
            "unknown_reddit_markdown_fails_closed": True,
            "markdown_formatting_normalized": True,
            "truth_inference": False,
            "rights_promotion": False,
            "scientific_evidence_promotion": False,
        },
    }
    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    if result != checkpoint:
        raise SystemExit("generated audit differs from checked-in checkpoint")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
