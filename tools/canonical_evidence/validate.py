#!/usr/bin/env python3
"""Dependency-free integrity checks for AkashicNET canonical/evidence fixtures."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "data" / "canonical_evidence_v01.example.json"

CANONICAL_DISPOSITIONS = {
    "UNIQUE_CANDIDATE", "DUPLICATE_COPY", "SAME_DRIVE_OBJECT_MULTICOLLECTION",
    "DUPLICATE_WORK", "EDITION_VARIANT", "TRANSLATION_VARIANT",
    "MULTI_VOLUME_MEMBER", "AGGREGATE_COLLECTION", "TECHNICAL_EXCLUSION",
    "REVIEW_REQUIRED",
}
REVIEW_STATES = {"UNREVIEWED", "CANDIDATE", "CONFIRMED", "REJECTED", "HOLD"}
CLAIM_STATUSES = {
    "UNASSESSED", "SUPPORTED", "PARTIALLY_SUPPORTED", "CONTESTED",
    "CONTRADICTED", "INSUFFICIENT_EVIDENCE",
}
EVIDENCE_RELATIONS = {
    "SUPPORTS", "CONTRADICTS", "CONTEXTUALISES", "REPORTS_EXPERIENCE",
    "HISTORICAL_ATTESTATION",
}
EVIDENCE_TIERS = {
    "EMPIRICAL_REFERENCE", "HISTORICAL", "CONTEMPLATIVE_PHILOSOPHICAL",
    "EXPERIENTIAL_ESOTERIC",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    canonical = data["canonical_resolution"]
    evidence = data["evidence"]

    require(canonical.get("resolution_version") == "0.1", "canonical resolution_version must be 0.1")
    require(evidence.get("evidence_model_version") == "0.1", "evidence_model_version must be 0.1")

    record_ids = set()
    for record in canonical.get("records", []):
        rid = record.get("record_id")
        require(bool(rid), "canonical record_id is required")
        require(rid not in record_ids, f"duplicate canonical record_id: {rid}")
        record_ids.add(rid)
        require(record.get("disposition") in CANONICAL_DISPOSITIONS, f"invalid disposition: {rid}")
        require(record.get("review_state") in REVIEW_STATES, f"invalid review_state: {rid}")
        confidence = record.get("confidence", 0)
        require(isinstance(confidence, (int, float)) and 0 <= confidence <= 1, f"invalid confidence: {rid}")
        require(bool(record.get("decision_basis")), f"decision_basis required: {rid}")

        # Metadata-only candidate signals must not silently become confirmed identity.
        weak_only = set(record.get("decision_basis", [])) <= {"TITLE", "SIZE", "AUTHOR", "LANGUAGE"}
        if weak_only:
            require(record.get("review_state") != "CONFIRMED", f"weak metadata cannot confirm identity: {rid}")
            require(record.get("disposition") not in {"DUPLICATE_COPY", "DUPLICATE_WORK"}, f"weak metadata cannot assert duplicate identity: {rid}")

    claims = evidence.get("claims", [])
    claim_ids = set()
    for claim in claims:
        cid = claim.get("claim_id")
        require(bool(cid), "claim_id is required")
        require(cid not in claim_ids, f"duplicate claim_id: {cid}")
        claim_ids.add(cid)
        require(bool(claim.get("statement")), f"claim statement required: {cid}")
        require(claim.get("status") in CLAIM_STATUSES, f"invalid claim status: {cid}")
        require(bool(claim.get("provenance")), f"claim provenance required: {cid}")

    for link in evidence.get("evidence_links", []):
        cid = link.get("claim_id")
        require(cid in claim_ids, f"evidence link references unknown claim: {cid}")
        require(link.get("relation") in EVIDENCE_RELATIONS, f"invalid evidence relation for {cid}")
        require(link.get("evidence_tier") in EVIDENCE_TIERS, f"invalid evidence tier for {cid}")
        require(bool(link.get("provenance")), f"evidence provenance required: {cid}")

    print(
        f"Canonical/evidence fixture valid: {len(record_ids)} canonical records, "
        f"{len(claim_ids)} claims, {len(evidence.get('evidence_links', []))} evidence links"
    )


if __name__ == "__main__":
    validate()
