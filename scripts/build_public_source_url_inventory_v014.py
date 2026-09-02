#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references/community/public-source-url-inventory-v0.14.json"
URL_RE = re.compile(r"https?://[^\s<>'\"`]+")
TRAILING = ".,;:!?)]}"


def git_head() -> str | None:
    try:
        value = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return value if re.fullmatch(r"[0-9a-f]{40}", value) else None


def normalize(url: str) -> str:
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    host = (parts.hostname or "").lower()
    port = parts.port
    netloc = host
    if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
        netloc = f"{host}:{port}"
    path = parts.path or "/"
    if path != "/":
        path = path.rstrip("/")
    return urlunsplit((scheme, netloc, path, parts.query, ""))


def is_external(url: str, scope: dict) -> bool:
    host = (urlsplit(url).hostname or "").lower()
    if host in set(scope["first_party_hosts"]):
        return False
    return not any(url.startswith(prefix) for prefix in scope["internal_github_prefixes"])


def iter_files(scope: dict):
    suffixes = set(scope["included_suffixes"])
    excluded = set(scope["excluded_paths"])
    for root_name in scope["include_roots"]:
        root = ROOT / root_name
        if not root.exists():
            continue
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            relative = path.relative_to(ROOT).as_posix()
            if relative not in excluded and path.suffix.lower() in suffixes:
                yield path, relative


def build(template: dict) -> dict:
    scope = template["scope"]
    rows = []
    for path, relative in iter_files(scope):
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in URL_RE.finditer(line):
                original = match.group(0).rstrip(TRAILING)
                if not is_external(original, scope):
                    continue
                normalized = normalize(original)
                rows.append({
                    "source_id": "URL-" + hashlib.sha256(normalized.encode()).hexdigest()[:16],
                    "original_url": original,
                    "normalized_url": normalized,
                    "host": (urlsplit(normalized).hostname or "").lower(),
                    "repository_path": relative,
                    "line": line_number,
                    "retrieval_status": "UNASSESSED",
                    "retrieved_on": None,
                    "redirect_target": None,
                    "observed_title": None,
                    "retraction_status": "UNCHECKED",
                    "truth_status_changed": False,
                    "repair_candidate": None
                })
    rows.sort(key=lambda row: (row["normalized_url"], row["repository_path"], row["line"], row["original_url"]))
    unique = {row["source_id"] for row in rows}
    output = dict(template)
    output["state"] = "GENERATED_UNASSESSED" if rows else "EMPTY_FAIL_CLOSED"
    output["generated_at"] = date.today().isoformat()
    output["source_commit"] = git_head()
    output["summary"] = {
        "external_url_occurrences": len(rows),
        "unique_normalized_external_urls": len(unique),
        "assessed_unique_urls": 0,
        "unassessed_unique_urls": len(unique)
    }
    output["entries"] = rows
    return output


def canonical(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if committed inventory differs")
    args = parser.parse_args()
    template = json.loads(MANIFEST.read_text(encoding="utf-8"))
    generated = build(template)
    if args.check:
        if canonical(generated) != canonical(template):
            raise SystemExit("FAIL: public source URL inventory is stale or not generated")
        print("PASS: public source URL inventory is deterministic and current")
        return 0
    MANIFEST.write_text(canonical(generated), encoding="utf-8")
    print(
        "GENERATED: "
        f"{generated['summary']['external_url_occurrences']} occurrences / "
        f"{generated['summary']['unique_normalized_external_urls']} unique external URLs; "
        "all retrieval states remain UNASSESSED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
