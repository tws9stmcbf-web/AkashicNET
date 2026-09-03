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
FIELD_PATTERN = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?(?:topic|topics|category|categories|flair|flairs|"
    r"link_flair_text|link_flair_template_id)\s*[:|=]"
)


def main() -> int:
    missing = [path for path in SOURCE_DOCUMENTS if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit(f"missing Reddit Markdown sources: {missing}")

    hits = {}
    for path in SOURCE_DOCUMENTS:
        text = (ROOT / path).read_text(encoding="utf-8")
        matches = FIELD_PATTERN.findall(text)
        if matches:
            hits[path] = matches
    if hits:
        raise SystemExit(f"explicit topic-bearing Markdown fields found: {hits}")

    all_reddit_markdown = sorted(
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*.md")
        if "reddit" in str(path.relative_to(ROOT)).lower()
    )
    prior_census_methods = [
        path for path in all_reddit_markdown
        if path not in SOURCE_DOCUMENTS
    ]

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
            "prior_census_method_documents_excluded_as_derivative": len(prior_census_methods),
            "markdown_explicit_topic_audit": "complete",
        },
        "decision": "The remaining source-bearing Reddit Markdown contains operational, provenance, and structural reporting only. Prior topic-audit methods are derivative governance records, not independent topic evidence.",
        "guardrails": {
            "heading_inference": False,
            "prose_inference": False,
            "url_inference": False,
            "method_document_is_source_evidence": False,
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
