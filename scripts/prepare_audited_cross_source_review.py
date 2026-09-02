#!/usr/bin/env python3
"""Build a deterministic, public-safe cross-source review packet.

This extractor proposes review candidates only from exact public metadata anchors.
It never creates graph edges, accepts candidates, or uses graph-derived signals.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REDDIT = ROOT / "references/community/n2n-test-batch-25.csv"
DEFAULT_DRIVE = ROOT / "references/community/knowledge-graph-seed-v0.1.md"
DEFAULT_OUTPUT = ROOT / "references/community/cross-source-orchestrator-review-v0.1.8.json"
EXTRACTOR_VERSION = "0.1.8"

BOUNDARIES = {
    "automated_truth_inference_allowed": False,
    "automated_acceptance_allowed": False,
    "rights_promotion_allowed": False,
    "scientific_evidence_promotion_allowed": False,
    "canonical_identity_promotion_allowed": False,
    "circular_confidence_allowed": False,
    "private_drive_metadata_allowed": False,
}


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def normalize(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def reddit_id(url: str) -> str:
    match = re.search(r"/comments/([a-z0-9]+)/", url)
    if not match:
        raise ValueError(f"unsupported Reddit URL: {url}")
    return match.group(1)


def parse_drive_seed(text: str) -> list[dict[str, str]]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 4 or cells[0] in {"family_id", "---"} or set(cells[0]) == {"-"}:
            continue
        if not re.fullmatch(r"[A-Z0-9-]+", cells[0]):
            continue
        rows.append({"family_id": cells[0], "title": cells[1]})
    return rows


def parse_reddit_csv(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text)))


def exact_anchors(source: dict[str, str], target: dict[str, str]) -> list[tuple[str, str, str]]:
    """Return (type, value, field) anchors; deliberately excludes fuzzy matches."""
    anchors: list[tuple[str, str, str]] = []
    family_id = target["family_id"]
    identifier_pattern = rf"(?<![A-Z0-9-]){re.escape(family_id)}(?![A-Z0-9-])"
    for field in ("title", "short_summary", "toolkit_framework", "research_question_potential"):
        value = source.get(field, "") or ""
        if re.search(identifier_pattern, value.upper()):
            anchors.append(("EXPLICIT_IDENTIFIER", family_id.casefold(), "identifier"))
            break

    source_title = normalize(source.get("title", ""))
    target_title = normalize(target["title"])
    if source_title and source_title == target_title:
        anchors.append(("EXACT_FULL_TITLE", target_title, "title"))
    return anchors


def endpoint_for_reddit(row: dict[str, str]) -> dict:
    rid = reddit_id(row["reddit_url"])
    return {
        "endpoint_id": f"endpoint:reddit:{rid}",
        "endpoint_type": "SOURCE_RECORD",
        "label": row["title"],
        "provenance": {
            "artifact_id": "artifact:reddit-n2n-test-batch-25:public",
            "record_id": row["reddit_url"],
            "independence_key": "source:reddit-index:n2n-test-batch-25",
            "public_safe": True,
        },
    }


def endpoint_for_drive(row: dict[str, str]) -> dict:
    slug = row["family_id"].casefold()
    return {
        "endpoint_id": f"endpoint:drive-publication:{slug}",
        "endpoint_type": "PUBLICATION",
        "label": row["title"],
        "provenance": {
            "artifact_id": "artifact:drive-knowledge-graph-seed:0.1",
            "record_id": row["family_id"],
            "independence_key": "source:drive-public-seed:stage-b-v0.1",
            "public_safe": True,
        },
    }


def build_packet(reddit_raw: bytes, drive_raw: bytes) -> dict:
    reddit_rows = parse_reddit_csv(reddit_raw.decode("utf-8-sig"))
    drive_rows = parse_drive_seed(drive_raw.decode("utf-8"))
    proposals = []
    for source in reddit_rows:
        for target in drive_rows:
            found = exact_anchors(source, target)
            if not found:
                continue
            source_endpoint = endpoint_for_reddit(source)
            target_endpoint = endpoint_for_drive(target)
            pair_digest = sha256_bytes(
                json.dumps(
                    {"source": source_endpoint, "target": target_endpoint},
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode()
            )
            anchors = []
            for index, (anchor_type, value, field) in enumerate(found, 1):
                anchors.append(
                    {
                        "anchor_id": f"anchor:auto:{pair_digest[:16]}:{index:02d}",
                        "anchor_type": anchor_type,
                        "normalized_value": value,
                        "source_endpoint_id": source_endpoint["endpoint_id"],
                        "target_endpoint_id": target_endpoint["endpoint_id"],
                        "provenance": {
                            "artifact_id": source_endpoint["provenance"]["artifact_id"],
                            "record_id": source_endpoint["provenance"]["record_id"],
                            "public_safe": True,
                        },
                        "extraction": {
                            "method": "EXACT_MATCH",
                            "extractor_version": EXTRACTOR_VERSION,
                            "public_metadata_field": field,
                        },
                        "independence_key": source_endpoint["provenance"]["independence_key"],
                        "graph_derived": False,
                        "representation_only": False,
                        "review_explanation": "Deterministic exact public-metadata anchor; human semantic review remains required.",
                        "input_digest": pair_digest,
                    }
                )
            proposals.append(
                {
                    "candidate_id": f"candidate:auto:{pair_digest[:20]}",
                    "assertion_class": "INFERRED_CANDIDATE",
                    "review_state": "REVIEW_REQUIRED",
                    "accepted_edge": False,
                    "source_endpoint": source_endpoint,
                    "target_endpoint": target_endpoint,
                    "anchor_evidence": anchors,
                }
            )

    proposals.sort(key=lambda item: item["candidate_id"])
    return {
        "schema_version": EXTRACTOR_VERSION,
        "mode": "REVIEW_PACKET_ONLY",
        "boundaries": BOUNDARIES,
        "inputs": [
            {
                "artifact_id": "artifact:reddit-n2n-test-batch-25:public",
                "sha256": sha256_bytes(reddit_raw),
                "public_safe": True,
            },
            {
                "artifact_id": "artifact:drive-knowledge-graph-seed:0.1",
                "sha256": sha256_bytes(drive_raw),
                "public_safe": True,
            },
        ],
        "proposed_candidates": proposals,
        "accepted_edges": [],
        "summary": {
            "exact_anchor_candidates": len(proposals),
            "accepted_edges": 0,
            "human_review_required": True,
        },
    }


def validate_packet(packet: dict) -> list[str]:
    errors = []
    if packet.get("schema_version") != EXTRACTOR_VERSION or packet.get("mode") != "REVIEW_PACKET_ONLY":
        errors.append("version or mode")
    if packet.get("boundaries") != BOUNDARIES or any(packet.get("boundaries", {}).values()):
        errors.append("unsafe boundaries")
    if packet.get("accepted_edges") != []:
        errors.append("accepted edges prohibited")
    candidates = packet.get("proposed_candidates")
    if not isinstance(candidates, list):
        errors.append("candidate list")
        candidates = []
    ids = []
    for candidate in candidates:
        ids.append(candidate.get("candidate_id"))
        if candidate.get("assertion_class") != "INFERRED_CANDIDATE":
            errors.append("assertion class")
        if candidate.get("review_state") != "REVIEW_REQUIRED" or candidate.get("accepted_edge") is not False:
            errors.append("review gate")
        if not candidate.get("anchor_evidence"):
            errors.append("anchor required")
        for endpoint_name in ("source_endpoint", "target_endpoint"):
            provenance = candidate.get(endpoint_name, {}).get("provenance", {})
            if provenance.get("public_safe") is not True or not provenance.get("independence_key"):
                errors.append("endpoint provenance")
        for anchor in candidate.get("anchor_evidence", []):
            if anchor.get("anchor_type") not in {"EXPLICIT_IDENTIFIER", "EXACT_FULL_TITLE"}:
                errors.append("non-deterministic anchor")
            if anchor.get("graph_derived") is not False or anchor.get("representation_only") is not False:
                errors.append("derived signal")
            if not re.fullmatch(r"[a-f0-9]{64}", str(anchor.get("input_digest", ""))):
                errors.append("anchor digest")
    if None in ids or len(ids) != len(set(ids)):
        errors.append("candidate IDs")
    summary = packet.get("summary", {})
    if summary != {
        "exact_anchor_candidates": len(candidates),
        "accepted_edges": 0,
        "human_review_required": True,
    }:
        errors.append("summary")
    serialized = json.dumps(packet)
    if any(key in serialized for key in ('"drive_id"', '"filename"', '"private_path"', "/My Drive/")):
        errors.append("private metadata")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reddit", type=Path, default=DEFAULT_REDDIT)
    parser.add_argument("--drive", type=Path, default=DEFAULT_DRIVE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    packet = build_packet(args.reddit.read_bytes(), args.drive.read_bytes())
    errors = validate_packet(packet)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    rendered = json.dumps(packet, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != rendered:
            print("ERROR: review packet is stale")
            return 1
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(json.dumps(packet["summary"], sort_keys=True))
    print("AKASHICNET AUDITED CROSS-SOURCE ORCHESTRATOR v0.1.8 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
