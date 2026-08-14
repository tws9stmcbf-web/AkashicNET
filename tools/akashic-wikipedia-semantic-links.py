import csv
import re
from pathlib import Path

WIKI = Path("references/community/wikipedia-reference-index.csv")
MASTER = Path("references/community/akashic-master-index.csv")
OUT = Path("references/community/wikipedia-akashic-semantic-links.csv")

# Concept families for the reincarnation proof-of-concept.
CONCEPTS = {
    "reincarnation": [
        "reincarnation", "rebirth", "transmigration",
        "metempsychosis", "samsara", "saṃsāra"
    ],
    "karma": [
        "karma", "karmic"
    ],
    "buddhist_continuity": [
        "buddhism", "buddhist", "rebirth", "samsara", "saṃsāra"
    ],
    "hindu_continuity": [
        "hinduism", "hindu", "vedanta", "vedānta",
        "yoga", "upanishad", "upaniṣad"
    ],
    "consciousness": [
        "consciousness", "self-consciousness",
        "mind", "metaphysics", "mysticism"
    ],
    "past_life_research": [
        "stevenson", "past life", "previous life",
        "reincarnation research"
    ],
}

def normalise(text):
    text = text.lower()
    return re.sub(r"\s+", " ", text)

with WIKI.open(encoding="utf-8") as f:
    wiki = list(csv.DictReader(f))

with MASTER.open(encoding="utf-8") as f:
    master = list(csv.DictReader(f))

links = []

for w in wiki:
    wiki_title = w.get("title", "")
    wiki_text = normalise(
        " ".join([
            wiki_title,
            w.get("description", ""),
            w.get("extract", "")
        ])
    )

    active_families = []

    for family, terms in CONCEPTS.items():
        if any(term in wiki_text for term in terms):
            active_families.append(family)

    for r in master:
        record_text = normalise(
            " ".join([
                r.get("title", ""),
                r.get("author", ""),
                r.get("subject_category", ""),
                r.get("semantic_topics", ""),
                r.get("topics", ""),
                r.get("source_type", ""),
            ])
        )

        matched = []

        for family in active_families:
            terms = CONCEPTS[family]
            hits = sum(1 for term in terms if term in record_text)

            if hits:
                matched.append((family, hits))

        if not matched:
            continue

        # Weighted candidate score.
        score = sum(hits * 2 for _, hits in matched)

        if "consciousness" in [x[0] for x in matched]:
            score += 1

        if "reincarnation" in [x[0] for x in matched]:
            score += 2

        families = "|".join(x[0] for x in matched)

        links.append({
            "wikipedia_title": wiki_title,
            "akasha_source": r.get("source", ""),
            "akasha_title": r.get("title", ""),
            "matched_concept_families": families,
            "semantic_score": score,
            "subject_category": r.get("subject_category", ""),
            "semantic_topics": r.get("semantic_topics", ""),
            "url": r.get("url", ""),
        })

links.sort(
    key=lambda x: (
        -int(x["semantic_score"]),
        x["wikipedia_title"],
        x["akasha_title"]
    )
)

with OUT.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "wikipedia_title",
            "akasha_source",
            "akasha_title",
            "matched_concept_families",
            "semantic_score",
            "subject_category",
            "semantic_topics",
            "url",
        ],
    )
    writer.writeheader()
    writer.writerows(links)

print("AKASHIC SEMANTIC RELATIONSHIP TEST")
print("=" * 60)
print("Wikipedia records:", len(wiki))
print("Akashic records:", len(master))
print("Candidate semantic relationships:", len(links))
print("Output:", OUT)

print()
print("TOP 20 RELATIONSHIPS")
print("=" * 60)

for row in links[:20]:
    print(
        f'{row["semantic_score"]:>3} | '
        f'{row["wikipedia_title"]} → '
        f'{row["akasha_title"]} | '
        f'{row["matched_concept_families"]}'
    )
