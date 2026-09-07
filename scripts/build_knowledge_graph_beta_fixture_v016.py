#!/usr/bin/env python3
"""Deterministically build the first review-only v0.16 Knowledge Graph Beta fixture."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "references/big-questions/BQ001/knowledge-graph-beta-fixture-v0.16.json"

SOURCE_SPECS = {
    "artifact:bq001-spec:0.1": {
        "repository_path": "references/big-questions/BQ001/spec-v0.1.json",
        "sha256": "0a0f1fc57b55df100fb8583fc6e28cd38324737c460465ea2269a51f637d4819",
        "independence_key": "source:bq001:spec-v0.1",
    },
    "artifact:bq001-evidence-batch2:0.1": {
        "repository_path": "references/big-questions/BQ001/evidence-batch2-v0.1.json",
        "sha256": "ddcf9bf5f909a98f289b7ef816673f23cd0ec8ae26b8416c15d87b8690926cc1",
        "independence_key": "source:bq001:evidence-batch2-v0.1",
    },
}

BOUNDARIES = {
    "automated_truth_inference_allowed": False,
    "automated_acceptance_allowed": False,
    "scientific_evidence_promotion_allowed": False,
    "rights_promotion_allowed": False,
    "canonical_identity_promotion_allowed": False,
    "circular_confidence_allowed": False,
    "private_drive_metadata_allowed": False,
}


def load_governed_sources(root=ROOT):
    sources = {}
    for artifact_id, spec in SOURCE_SPECS.items():
        raw = (root / spec["repository_path"]).read_bytes()
        sources[artifact_id] = {
            "data": json.loads(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
    return sources


def provenance(artifact_id, record_locator, derivation_method, actual_sha256):
    spec = SOURCE_SPECS[artifact_id]
    return {
        "artifact_id": artifact_id,
        "repository_path": spec["repository_path"],
        "sha256": actual_sha256,
        "record_locator": record_locator,
        "independence_key": spec["independence_key"],
        "derivation_method": derivation_method,
        "public_safe": True,
    }


def build(sources=None):
    sources = sources or load_governed_sources()
    spec = sources["artifact:bq001-spec:0.1"]["data"]
    batch = sources["artifact:bq001-evidence-batch2:0.1"]["data"]

    def prov(artifact_id, record_locator, derivation_method):
        return provenance(
            artifact_id,
            record_locator,
            derivation_method,
            sources[artifact_id]["sha256"],
        )
    continuity, biological = spec["models"]
    martial_source = batch["sources"][4]
    martial_claim = batch["claims"][4]
    correction = martial_source["related_notices"][0]

    nodes = [
        {
            "node_id": "node:question:BQ001",
            "node_type": "QUESTION",
            "label": spec["title"],
            "question_status": spec["status"],
            "provenance": prov("artifact:bq001-spec:0.1", "/id", "DIRECT_RECORD"),
        },
        {
            "node_id": "node:model:MODEL-BQ001-CONTINUITY",
            "node_type": "MODEL",
            "label": continuity["name"],
            "provenance": prov("artifact:bq001-spec:0.1", "/models/0/model_id", "DIRECT_RECORD"),
        },
        {
            "node_id": "node:model:MODEL-BQ001-BIOLOGICAL-DEPENDENCE",
            "node_type": "MODEL",
            "label": biological["name"],
            "provenance": prov("artifact:bq001-spec:0.1", "/models/1/model_id", "DIRECT_RECORD"),
        },
        {
            "node_id": "node:source:SRC-BQ001-MARTIAL-2025",
            "node_type": "SOURCE",
            "label": martial_source["title"],
            "provenance": prov("artifact:bq001-evidence-batch2:0.1", "/sources/4/source_id", "DIRECT_RECORD"),
        },
        {
            "node_id": "node:claim:CLAIM-BQ001-MARTIAL-2025-INTERP-01",
            "node_type": "CLAIM",
            "label": martial_claim["text"],
            "provenance": prov("artifact:bq001-evidence-batch2:0.1", "/claims/4/claim_id", "DIRECT_RECORD"),
        },
        {
            "node_id": "node:notice:10.1038/s41582-025-01111-9",
            "node_type": "NOTICE",
            "label": correction["title"],
            "provenance": prov("artifact:bq001-evidence-batch2:0.1", "/sources/4/related_notices/0/doi", "DIRECT_RECORD"),
        },
    ]

    edges = [
        {
            "edge_id": "edge:bq001:has-model:biological-dependence",
            "source_node_id": "node:question:BQ001",
            "target_node_id": "node:model:MODEL-BQ001-BIOLOGICAL-DEPENDENCE",
            "relationship_type": "HAS_MODEL",
            "assertion_class": "DIRECT_SOURCE_METADATA",
            "review_state": "SOURCE_ASSERTED",
            "edge_state": "ACTIVE",
            "accepted_edge": False,
            "evidence_independence_keys": ["source:bq001:spec-v0.1"],
            "parent_edge_ids": [],
            "provenance": prov("artifact:bq001-spec:0.1", "/models/1/model_id", "DIRECT_RECORD"),
        },
        {
            "edge_id": "edge:bq001:claim-supports-biological-dependence:candidate",
            "source_node_id": "node:claim:CLAIM-BQ001-MARTIAL-2025-INTERP-01",
            "target_node_id": "node:model:MODEL-BQ001-BIOLOGICAL-DEPENDENCE",
            "relationship_type": "SUPPORTS_MODEL_CANDIDATE",
            "assertion_class": "INFERRED_CANDIDATE",
            "review_state": "REVIEW_REQUIRED",
            "edge_state": "REVIEW_ONLY",
            "accepted_edge": False,
            "evidence_independence_keys": ["source:bq001:evidence-batch2-v0.1"],
            "parent_edge_ids": [],
            "provenance": prov("artifact:bq001-evidence-batch2:0.1", "/claims/4/supports_models/0", "HUMAN_REVIEW_CANDIDATE"),
        },
        {
            "edge_id": "edge:bq001:models-compete:candidate",
            "source_node_id": "node:model:MODEL-BQ001-BIOLOGICAL-DEPENDENCE",
            "target_node_id": "node:model:MODEL-BQ001-CONTINUITY",
            "relationship_type": "COMPETES_WITH_CANDIDATE",
            "assertion_class": "INFERRED_CANDIDATE",
            "review_state": "REVIEW_REQUIRED",
            "edge_state": "REVIEW_ONLY_CONTRADICTION",
            "accepted_edge": False,
            "evidence_independence_keys": ["source:bq001:spec-v0.1"],
            "parent_edge_ids": [],
            "provenance": prov("artifact:bq001-spec:0.1", "/models", "HUMAN_REVIEW_CANDIDATE"),
        },
        {
            "edge_id": "edge:bq001:author-correction:martial-2025",
            "source_node_id": "node:notice:10.1038/s41582-025-01111-9",
            "target_node_id": "node:source:SRC-BQ001-MARTIAL-2025",
            "relationship_type": "CORRECTS",
            "assertion_class": "DIRECT_SOURCE_METADATA",
            "review_state": "SOURCE_ASSERTED",
            "edge_state": "CORRECTED_NOT_RETRACTED",
            "accepted_edge": False,
            "evidence_independence_keys": ["source:bq001:evidence-batch2-v0.1"],
            "parent_edge_ids": [],
            "provenance": prov("artifact:bq001-evidence-batch2:0.1", "/sources/4/related_notices/0/doi", "DIRECT_RECORD"),
        },
    ]

    return {
        "schema_version": "0.16.0-beta.1",
        "mode": "REVIEW_FIXTURE_ONLY",
        "issue": 277,
        "baseline_locks": {
            "v0.14": "7b6cfd89de570c4b945d574dad570c37825645fe",
            "v0.15_release": "ea46629558ff57970f6efd2485a7e9a288dc55f2",
            "v0.15_seal": "5ba6989aade68461c8f3953c4a82cc0e158b0730",
        },
        "question_id": "BQ001",
        "question_status": "UNRESOLVED",
        "boundaries": BOUNDARIES,
        "source_artifacts": [
            {
                "artifact_id": artifact_id,
                **source_spec,
                "sha256": sources[artifact_id]["sha256"],
                "public_safe": True,
            }
            for artifact_id, source_spec in SOURCE_SPECS.items()
        ],
        "nodes": nodes,
        "edges": edges,
        "summary": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "accepted_edge_count": 0,
            "inferred_candidate_count": 2,
            "unresolved_question_count": 1,
        },
    }


def main():
    output = json.dumps(build(), indent=2, ensure_ascii=False) + "\n"
    OUTPUT.write_text(output)
    print(f"WROTE {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
