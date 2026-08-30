#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


def norm(value: str) -> str:
    value = (value or "").strip()
    value = re.sub(r"\s+", " ", value)
    return value


def key(value: str) -> str:
    return norm(value).casefold()


def main() -> None:
    p = argparse.ArgumentParser(description="Conservative metadata topic census for the N2N pilot index")
    p.add_argument("index", type=Path)
    p.add_argument("--concept-seed", type=Path)
    p.add_argument("--json-out", type=Path)
    args = p.parse_args()

    rows = list(csv.DictReader(args.index.open(encoding="utf-8", newline="")))
    categories = Counter()
    frameworks = Counter()
    category_labels: dict[str, str] = {}
    framework_labels: dict[str, str] = {}
    edges = Counter()

    for row in rows:
        c = norm(row.get("category", ""))
        f = norm(row.get("toolkit_framework", ""))
        if c:
            categories[key(c)] += 1
            category_labels.setdefault(key(c), c)
        if f:
            frameworks[key(f)] += 1
            framework_labels.setdefault(key(f), f)
        if c and f:
            edges[(key(c), key(f))] += 1

    union_keys = set(categories) | set(frameworks)
    exact_overlap = set(categories) & set(frameworks)

    concept_count = None
    concept_labels: list[str] = []
    if args.concept_seed and args.concept_seed.exists():
        concepts = list(csv.DictReader(args.concept_seed.open(encoding="utf-8", newline="")))
        concept_labels = [norm(r.get("label", "")) for r in concepts if norm(r.get("label", ""))]
        concept_count = len({key(x) for x in concept_labels})

    result = {
        "schema": "akashicnet.reddit.topic-census.v0.1",
        "method": "exact normalized metadata labels; no semantic clustering or inferred equivalence",
        "records_examined": len(rows),
        "unique_category_labels": len(categories),
        "unique_toolkit_framework_labels": len(frameworks),
        "unique_category_framework_union": len(union_keys),
        "category_framework_exact_label_overlap": len(exact_overlap),
        "distinct_category_framework_edges": len(edges),
        "posts_with_category_framework_edge": sum(edges.values()),
        "formal_reviewed_concept_labels": concept_count,
        "categories": [
            {"label": category_labels[k], "records": categories[k]}
            for k in sorted(categories, key=lambda x: (-categories[x], category_labels[x].casefold()))
        ],
        "toolkit_frameworks": [
            {"label": framework_labels[k], "records": frameworks[k]}
            for k in sorted(frameworks, key=lambda x: (-frameworks[x], framework_labels[x].casefold()))
        ],
        "top_category_framework_edges": [
            {
                "category": category_labels[c],
                "toolkit_framework": framework_labels[f],
                "records": n,
            }
            for (c, f), n in edges.most_common(50)
        ],
        "formal_concepts": sorted(concept_labels, key=str.casefold),
        "caveats": [
            "This is a conservative census of explicit curated metadata labels, not a semantic topic model.",
            "Distinct labels may still represent related or overlapping real-world topics.",
            "The result therefore should not be interpreted as the total number of latent interdisciplinary topics in AkashicNET.",
        ],
    }

    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text, encoding="utf-8")
    print(json.dumps({
        "records_examined": result["records_examined"],
        "unique_category_labels": result["unique_category_labels"],
        "unique_toolkit_framework_labels": result["unique_toolkit_framework_labels"],
        "unique_category_framework_union": result["unique_category_framework_union"],
        "distinct_category_framework_edges": result["distinct_category_framework_edges"],
        "posts_with_category_framework_edge": result["posts_with_category_framework_edge"],
        "formal_reviewed_concept_labels": result["formal_reviewed_concept_labels"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
