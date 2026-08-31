import csv
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

API = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": (
        "AkashicNET/0.3 "
        "(research metadata importer; "
        "https://github.com/tws9stmcbf-web/AkashicNET)"
    )
}

TOPICS = [
    "consciousness",
    "neuroscience",
    "meditation",
    "psychedelics",
    "panpsychism",
    "philosophy of mind",
    "quantum physics",
    "cosmology",
    "archaeology",
    "anthropology",
    "mycology",
    "artificial intelligence",
]

OUT = Path("references/community/wikipedia-akashic-pilot.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

rows = []
seen = set()

for topic in TOPICS:
    params = {
        "action": "query",
        "list": "search",
        "srsearch": topic,
        "srnamespace": 0,
        "srlimit": 10,
        "format": "json",
        "maxlag": 5,
    }

    r = requests.get(
        API,
        params=params,
        headers=HEADERS,
        timeout=20,
    )
    r.raise_for_status()

    for item in r.json()["query"]["search"]:
        page_id = str(item["pageid"])

        if page_id in seen:
            continue

        seen.add(page_id)

        rows.append({
            "source": "Wikipedia",
            "page_id": page_id,
            "title": item["title"],
            "topic_seed": topic,
            "url": (
                "https://en.wikipedia.org/wiki/"
                + item["title"].replace(" ", "_")
            ),
            "retrieved_utc": datetime.now(
                timezone.utc
            ).isoformat(),
        })

        if len(rows) >= 100:
            break

    if len(rows) >= 100:
        break

    time.sleep(0.5)

fields = [
    "source",
    "page_id",
    "title",
    "topic_seed",
    "url",
    "retrieved_utc",
]

with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"Created {OUT}")
print(f"Records: {len(rows)}")
