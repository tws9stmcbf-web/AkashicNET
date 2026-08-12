import csv
import argparse
from pathlib import Path

INDEX = Path("references/community/n2n-index.csv")

parser = argparse.ArgumentParser(
    description="Search the NeuronsToNirvana community archive."
)
parser.add_argument("query", help="Search title, topic, category, author, summary, framework, etc.")
parser.add_argument("-n", "--limit", type=int, default=20)
args = parser.parse_args()

query = args.query.lower().strip()

if not INDEX.exists():
    raise SystemExit(f"Metadata index not found: {INDEX}")

fields = [
    "title",
    "Reddit URL",
    "date",
    "post type",
    "author",
    "topic",
    "category",
    "short summary",
    "external source URL",
    "related Toolkit framework",
    "research-question potential",
    "visual/audio/art flag",
    "evidence classification",
    "provenance/licensing status",
]

matches = []

with INDEX.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        searchable = " ".join(
            row.get(field, "") for field in fields
        ).lower()

        if query in searchable:
            matches.append(row)

print(f"Archive: {len(matches)} matching records")
print()

for row in matches[:args.limit]:
    print(f"TITLE: {row.get('title', '')}")
    print(f"TOPIC: {row.get('topic', '')}")
    print(f"CATEGORY: {row.get('category', '')}")
    print(f"AUTHOR: {row.get('author', '')}")
    print(f"FRAMEWORK: {row.get('related Toolkit framework', '')}")
    print(f"URL: {row.get('Reddit URL', '')}")
    print("-" * 80)

if len(matches) > args.limit:
    print(f"Showing first {args.limit} of {len(matches)} matches.")
