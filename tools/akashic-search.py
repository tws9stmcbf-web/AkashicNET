import csv
import sys

INDEX = "references/community/akashic-master-index.csv"

args = sys.argv[1:]
source_filter = "both"
clean_args = []

i = 0
while i < len(args):
    if args[i] == "--source" and i + 1 < len(args):
        source_filter = args[i + 1].lower()
        i += 2
    else:
        clean_args.append(args[i])
        i += 1

if not clean_args:
    print('Usage: python3 tools/akashic-search.py "search terms" [--source drive|reddit|both]')
    sys.exit(1)

query = " ".join(clean_args).lower().split()

with open(INDEX, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

results = []

for r in rows:
    source = r.get("source", "").lower()

    if source_filter != "both":
        if source_filter == "drive" and source != "google drive":
            continue
        if source_filter == "reddit" and source != "reddit":
            continue

    title = r.get("title", "").lower()
    author = r.get("author", "").lower()
    topics = r.get("topics", "").lower()
    path = r.get("path", "").lower()
    url = r.get("url", "").lower()

    text = " ".join([title, author, topics, path, url])

    if not all(term in text for term in query):
        continue

    score = 0

    for term in query:
        if term in title:
            score += 5
        if term in topics:
            score += 4
        if term in author:
            score += 3
        if term in path:
            score += 2
        if term in url:
            score += 1

    results.append((score, r))

results.sort(key=lambda x: (-x[0], x[1].get("title", "")))

print()
print("AKASHIC SEARCH")
print("=" * 70)
print("Query:", " ".join(query))
print("Source:", source_filter)
print("Results:", len(results))
print()

for score, r in results[:50]:
    print(f"SCORE: {score}")
    print("SOURCE:", r["source"])
    print("TITLE:", r["title"] or "(URL-only Reddit record)")
    print("AUTHOR:", r["author"])
    print("TOPICS:", r["topics"])
    print("URL:", r["url"])
    print("-" * 70)
