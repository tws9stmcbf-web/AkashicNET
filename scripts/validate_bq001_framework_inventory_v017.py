#!/usr/bin/env python3
"""Fail-closed validation for the v0.17 BQ001 framework inventory."""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "references/big-questions/BQ001/framework-inventory-v0.17-slice1.json"
SCHEMA = ROOT / "schemas/bq001-framework-inventory-v0.17-slice1.schema.json"
EXPECTED_PIN = "4867ca7c8c9a4e1bc139f630815ecf49c79a2ef7"
EXPECTED_SCOPE_DESCRIPTION = (
    "Selected inventory of public-safe models, philosophical frameworks, contemplative "
    "selfhood frameworks, and consciousness theories represented in the governed BQ001 "
    "artifacts. This 11-item slice is not exhaustive: the neural-correlates research "
    "programme (CLAIM-BQ001-KOCH-2016-INTERP-01; SRC-BQ001-KOCH-2016) remains outside "
    "this slice and requires follow-up inventory review."
)
EXPECTED_CORE = {
    "inventory_id": "BQ001-FRAMEWORK-INVENTORY-V017-SLICE1",
    "version": "0.1.0",
    "release_track": "v0.17-evidence-intelligence-beta",
    "question_id": "BQ001",
    "question_status": "UNRESOLVED",
    "mode": "REVIEW_ONLY",
}
EXPECTED_SCOPE_FLAGS = {
    "exhaustive_for_pinned_artifacts": False,
    "exhaustive_beyond_pinned_artifacts": False,
    "synthesis_or_answer": False,
}
EXPECTED_PROMOTION_GUARDS = {
    "truth_inference_allowed": False,
    "framework_count_is_vote": False,
    "source_count_upgrades_evidence": False,
    "shared_source_counts_as_independent_confirmation": False,
    "interpretation_upgrades_to_empirical_evidence": False,
    "randomized_navigation_implies_probability": False,
    "ranking_or_visualization_implies_endorsement": False,
    "scientific_evidence_promotion_allowed": False,
    "rights_or_public_release_promotion_allowed": False,
    "accepted_edge_creation_allowed": False,
}
EXPECTED_OPERATIONAL_BOUNDARIES = {
    "reddit_live_access": "HOLD",
    "private_drive_material_allowed": False,
    "website_publication_allowed": False,
    "analytics_activation_allowed": False,
    "multimedia_generation_allowed": False,
}
ALLOWED_KEYS = {
    "top": frozenset({
        "exclusions", "governed_artifacts", "inherited_v016_readiness_pin",
        "inventory", "inventory_id", "mode", "operational_boundaries",
        "promotion_guards", "question_id", "question_status", "release_track",
        "scope", "summary", "version",
    }),
    "scope": frozenset({
        "description", "exhaustive_beyond_pinned_artifacts",
        "exhaustive_for_pinned_artifacts", "synthesis_or_answer",
    }),
    "artifact": frozenset({"git_blob_sha", "path", "role"}),
    "exclusion": frozenset({"name", "reason"}),
    "item": frozenset({
        "boundary", "canonical_name", "category", "evidence_role",
        "independence_state", "inventory_item_id", "pinned_locators",
        "relation_to_bq001", "represented_by", "status",
    }),
    "summary": frozenset({
        "accepted_edges", "consciousness_theories", "contemplative_frameworks",
        "governed_artifacts", "inventory_items",
        "neuroscientific_explanatory_models", "philosophical_frameworks",
        "resolved_items", "umbrella_models",
    }),
    "promotion_guards": frozenset(EXPECTED_PROMOTION_GUARDS),
    "operational_boundaries": frozenset(EXPECTED_OPERATIONAL_BOUNDARIES),
}

EXPECTED_EXCLUSIONS = {
    ("cardiac-arrest and NDE reports", "RESEARCH_DOMAIN_OR_OBSERVATION_NOT_A_FRAMEWORK"),
    ("reincarnation-type case literature", "RESEARCH_DOMAIN_AND_CASE_LITERATURE_NOT_A_SINGLE_FRAMEWORK"),
    ("autobiographical memory and self-continuity findings", "EVIDENCE_DOMAIN_NOT_A_METAPHYSICAL_MODEL"),
    ("source-status and synthetic terminal-state fixtures", "PROVENANCE_TEST_MATERIAL_NOT_EVIDENCE_OR_FRAMEWORK"),
}
# Public repository blobs verified against EXPECTED_PIN; never derive from the inventory.
EXPECTED_BLOBS = {
    "references/big-questions/BQ001/spec-v0.1.json": "b35b2397c8ab5341db313ec73c3e45b2bcdf4a5c",
    "references/big-questions/BQ001/public-synthesis-v0.1.json": "b5e793a0ea7d8756f395b9bd49c50ad01a1c79d8",
    "references/big-questions/BQ001/evidence-batch1-v0.1.json": "fc795ea3f224a33e969db6170c9a840dc03ef242",
    "references/big-questions/BQ001/evidence-batch2-v0.1.json": "894ee42a3a2c1b8cf09f8026fac9b03dc74bf5f9",
    "references/big-questions/BQ001/evidence-batch3-v0.1.json": "44ab4a1bb7dc941a52c9d7529e719ed7e91cc3f5",
    "references/big-questions/BQ001/evidence-batch4-v0.1.json": "4d3f4bebc8605290abc62fa1eaa735912d44c60f",
    "references/big-questions/BQ001/evidence-batch5-v0.1.json": "473a64435784412e783b4d6bf590f44859fca006"
}
EXPECTED_IDS = {
    "FW-BQ001-UMBRELLA-BIOLOGICAL-DEPENDENCE",
    "FW-BQ001-UMBRELLA-CONTINUITY",
    "FW-BQ001-PHILOSOPHY-PHYSICALISM",
    "FW-BQ001-PHILOSOPHY-DUALISM",
    "FW-BQ001-PHILOSOPHY-PANPSYCHISM",
    "FW-BQ001-CONTEMPLATIVE-BUDDHIST-NONSELF",
    "FW-BQ001-CONTEMPLATIVE-DAHL-PRACTICE-FAMILIES",
    "FW-BQ001-CONTEMPLATIVE-SART",
    "FW-BQ001-NDE-NEUROSCIENTIFIC-MODEL",
    "FW-BQ001-CONSCIOUSNESS-GNWT",
    "FW-BQ001-CONSCIOUSNESS-IIT",
}
# Fixed semantics for this reviewed slice; changes require explicit review.
SEMANTIC_FIELDS = ("canonical_name", "category", "evidence_role", "status", "independence_state", "represented_by", "pinned_locators", "boundary", "relation_to_bq001")
EXPECTED_SEMANTICS = {
    "FW-BQ001-UMBRELLA-BIOLOGICAL-DEPENDENCE": ("Biological-dependence model", "UMBRELLA_MODEL", "organising_model_only", "UNRESOLVED", "NOT_APPLICABLE_TO_MODEL", ("MODEL-BQ001-BIOLOGICAL-DEPENDENCE",), ("spec-v0.1.json#/models/1", "public-synthesis-v0.1.json#/competing_models/0"), "Observed brain–conscious-state dependence does not prove that post-mortem continuation is impossible.", "Individual conscious experience is treated as dependent on functioning biological systems."),
    "FW-BQ001-UMBRELLA-CONTINUITY": ("Continuity or survival model", "UMBRELLA_MODEL", "organising_model_only", "UNRESOLVED", "NOT_APPLICABLE_TO_MODEL", ("MODEL-BQ001-CONTINUITY",), ("spec-v0.1.json#/models/0", "public-synthesis-v0.1.json#/competing_models/1"), "Anomalous reports and conceptual possibility do not establish personal survival.", "Some aspect of consciousness may continue beyond individual biological functioning."),
    "FW-BQ001-PHILOSOPHY-PHYSICALISM": ("Physicalism", "PHILOSOPHICAL_FRAMEWORK", "INTERPRETATION", "UNRESOLVED", "UNASSESSED_REVIEW_REQUIRED", ("SRC-BQ001-SEP-PHYSICALISM", "CLAIM-BQ001-PHYSICALISM-INTERP-01"), ("evidence-batch4-v0.1.json#/sources/3", "evidence-batch4-v0.1.json#/claims/3"), "A philosophical position is not an experimental result or proof of non-survival.", "Provides philosophical support for physical dependence, with implications varying by version."),
    "FW-BQ001-PHILOSOPHY-DUALISM": ("Dualism", "PHILOSOPHICAL_FRAMEWORK", "INTERPRETATION", "UNRESOLVED", "UNASSESSED_REVIEW_REQUIRED", ("SRC-BQ001-SEP-DUALISM", "CLAIM-BQ001-DUALISM-INTERP-01"), ("evidence-batch4-v0.1.json#/sources/4", "evidence-batch4-v0.1.json#/claims/4"), "Conceptual space for survival is not empirical evidence that survival occurs.", "Provides conceptual space for mind not reducible to standard physicalism."),
    "FW-BQ001-PHILOSOPHY-PANPSYCHISM": ("Panpsychism", "PHILOSOPHICAL_FRAMEWORK", "INTERPRETATION", "UNRESOLVED", "UNASSESSED_REVIEW_REQUIRED", ("SRC-BQ001-SEP-PANPSYCHISM", "CLAIM-BQ001-PANPSYCHISM-INTERP-01"), ("evidence-batch4-v0.1.json#/sources/5", "evidence-batch4-v0.1.json#/claims/5"), "Panpsychism does not entail persistence of an individual's memories, identity, or subjectivity.", "Treats mentality or experience as fundamental or ubiquitous in nature."),
    "FW-BQ001-CONTEMPLATIVE-BUDDHIST-NONSELF": ("Buddhist non-self accounts", "CONTEMPLATIVE_PHILOSOPHICAL_FRAMEWORK", "INTERPRETATION", "UNRESOLVED", "UNASSESSED_REVIEW_REQUIRED", ("SRC-BQ001-SIDERITS-2011", "CLAIM-BQ001-SIDERITS-2011-INTERP-01"), ("evidence-batch4-v0.1.json#/sources/0", "evidence-batch4-v0.1.json#/claims/0"), "A tradition or philosophical doctrine is not empirical proof of survival or non-survival.", "Questions whether a permanent independent self is the correct unit of continuity."),
    "FW-BQ001-CONTEMPLATIVE-DAHL-PRACTICE-FAMILIES": ("Attentional, constructive, and deconstructive meditation families", "PEER_REVIEWED_REVIEW_FRAMEWORK", "INTERPRETATION", "UNRESOLVED", "UNASSESSED_REVIEW_REQUIRED", ("SRC-BQ001-DAHL-2015", "CLAIM-BQ001-DAHL-2015-INTERP-01"), ("evidence-batch4-v0.1.json#/sources/1", "evidence-batch4-v0.1.json#/claims/1"), "Changes in self-processing do not establish external ontology or post-mortem continuation.", "Models trainable cognitive processes and changes in self-processing."),
    "FW-BQ001-CONTEMPLATIVE-SART": ("S-ART: self-awareness, self-regulation, and self-transcendence", "PEER_REVIEWED_THEORETICAL_FRAMEWORK", "INTERPRETATION", "UNRESOLVED", "UNASSESSED_REVIEW_REQUIRED", ("SRC-BQ001-VAGO-2012", "CLAIM-BQ001-VAGO-2012-INTERP-01"), ("evidence-batch4-v0.1.json#/sources/2", "evidence-batch4-v0.1.json#/claims/2"), "Psychological self-transcendence is not consciousness independent of a biological organism.", "Models mindfulness through interacting psychological and neurobiological processes."),
    "FW-BQ001-NDE-NEUROSCIENTIFIC-MODEL": ("Neuroscientific model of near-death experiences", "NEUROSCIENTIFIC_EXPLANATORY_MODEL", "INTERPRETATION", "UNRESOLVED", "UNASSESSED_REVIEW_REQUIRED", ("SRC-BQ001-MARTIAL-2025", "CLAIM-BQ001-MARTIAL-2025-INTERP-01"), ("evidence-batch2-v0.1.json#/sources/4", "evidence-batch2-v0.1.json#/claims/4"), "A plausible neuroscientific model is not proof that every NDE is fully explained or that non-survival is established.", "Proposes biological mechanisms that may account for features of NDE reports."),
    "FW-BQ001-CONSCIOUSNESS-GNWT": ("Global Neuronal Workspace Theory", "CONSCIOUSNESS_THEORY", "Established Evidence", "EMPIRICALLY_TESTED_NOT_ADJUDICATED_FOR_BQ001", "SINGLE_GOVERNED_SOURCE_DO_NOT_COUNT_AS_REPLICATION", ("SRC-BQ001-COGITATE-2025", "CLAIM-BQ001-COGITATE-2025-OBS-01"), ("evidence-batch5-v0.1.json#/sources/1", "evidence-batch5-v0.1.json#/claims/1"), "Adversarial theory testing in living participants does not adjudicate post-mortem continuity.", "A theory of conscious access tested under living-brain experimental conditions."),
    "FW-BQ001-CONSCIOUSNESS-IIT": ("Integrated Information Theory", "CONSCIOUSNESS_THEORY", "Established Evidence", "EMPIRICALLY_TESTED_NOT_ADJUDICATED_FOR_BQ001", "SHARED_SOURCE_WITH_GNWT_DO_NOT_DOUBLE_COUNT", ("SRC-BQ001-COGITATE-2025", "CLAIM-BQ001-COGITATE-2025-OBS-01"), ("evidence-batch5-v0.1.json#/sources/1", "evidence-batch5-v0.1.json#/claims/1"), "The shared comparison supplies one governed evidence source, not two independent confirmations, and does not adjudicate survival.", "A theory of consciousness tested alongside GNWT under a shared adversarial protocol."),
}

FORBIDDEN_KEYS = {
    "driveid", "drivefileid", "driveobjectid", "fileid", "objectid",
    "filename", "filepath", "privatepath", "parentid", "objecthash",
    "objectsha256", "md5checksum", "sha256checksum", "privatedriveid",
}


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def load_json(raw):
    def unique_pairs(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError("duplicate JSON key")
            out[key] = value
        return out
    def reject_constant(_):
        raise ValueError("non-finite JSON number")
    return json.loads(raw, object_pairs_hook=unique_pairs, parse_constant=reject_constant)


def decode_percent(text):
    decoded = text
    for _ in range(32):
        updated = unquote(unicodedata.normalize("NFKC", decoded))
        if updated == decoded:
            return decoded
        decoded = updated
    raise ValueError("encoding did not stabilize")


def privacy_check(value):
    def check(text, is_key=False):
        decoded = decode_percent(text)
        folded = unicodedata.normalize("NFKC", decoded).casefold().replace("\\", "/")
        folded = folded.translate(str.maketrans({"。": ".", "．": ".", "｡": "."}))
        # Browsers and IDNA processing can discard Unicode format controls in hosts.
        folded = "".join(
            character for character in folded
            if unicodedata.category(character) != "Cf"
        )
        if any(marker in folded for marker in (
            "drive.google.com", "docs.google.com", "/my drive/", "akm-",
            "file://", "gdrive://",
        )):
            raise ValueError("private metadata rejected")
        if not is_key and re.search(r"(?<![a-f0-9])[a-f0-9]{64}(?![a-f0-9])", folded):
            raise ValueError("unscoped digest rejected")
    if isinstance(value, dict):
        for key, child in value.items():
            check(key, True)
            normalized_key = re.sub(
                r"[^a-z0-9]", "", unicodedata.normalize(
                    "NFKC", decode_percent(key)
                ).casefold()
            )
            if normalized_key in FORBIDDEN_KEYS:
                raise ValueError("private metadata rejected")
            if key == "git_blob_sha":
                is_expected_artifact_pin = (
                    isinstance(child, str)
                    and isinstance(value.get("path"), str)
                    and EXPECTED_BLOBS.get(value["path"]) == child
                )
                is_expected_schema_field = child == {
                    "type": "string", "pattern": "^[a-f0-9]{40}$"
                }
                if not (is_expected_artifact_pin or is_expected_schema_field):
                    raise ValueError("unscoped git blob rejected")
                continue
            if key == "inherited_v016_readiness_pin" and child == EXPECTED_PIN:
                continue
            privacy_check(child)
    elif isinstance(value, list):
        for child in value:
            privacy_check(child)
    elif isinstance(value, str):
        check(value)


def git_blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def resolve_pointer(document, pointer):
    current = document
    for token in pointer.split("/")[1:]:
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            if not re.fullmatch(r"(?:0|[1-9][0-9]*)", token):
                raise ValueError("invalid governed locator")
            current = current[int(token)]
        elif isinstance(current, dict) and token in current:
            current = current[token]
        else:
            raise ValueError("invalid governed locator")
    return current


def validate_locators(item, by_name):
    records = []
    observed = set()
    identity_fields = {
        "models": "model_id", "competing_models": "model_id",
        "sources": "source_id", "claims": "claim_id",
    }
    for locator in item["pinned_locators"]:
        filename, pointer = locator.split("#", 1)
        match = re.fullmatch(r"/(models|competing_models|sources|claims)/(0|[1-9][0-9]*)", pointer)
        if filename not in by_name or match is None:
            raise ValueError("locator must identify an exact governed record")
        record = resolve_pointer(by_name[filename], pointer)
        field = identity_fields[match.group(1)]
        if not isinstance(record, dict) or not isinstance(record.get(field), str):
            raise ValueError("locator lacks terminal record identity")
        observed.add(record[field])
        records.append(record)
    if set(item["represented_by"]) != observed:
        raise ValueError("represented identity is not bound to terminal record")
    sources = {record["source_id"] for record in records if "source_id" in record}
    claims = [record for record in records if "claim_id" in record]
    if sources or claims:
        if not sources or not claims or any(
            not record.get("source_ids") or not set(record["source_ids"]).issubset(sources)
            for record in claims
        ) or sources != {source for record in claims for source in record["source_ids"]}:
            raise ValueError("source and claim relationship drift")


def validate_shared_sources(items):
    owners = {}
    for item in items:
        for identity in item["represented_by"]:
            if identity.startswith(("SRC-", "CLAIM-")):
                owners.setdefault(identity, set()).add(item["inventory_item_id"])
    shared = {identity: users for identity, users in owners.items() if len(users) > 1}
    pair = {"FW-BQ001-CONSCIOUSNESS-GNWT", "FW-BQ001-CONSCIOUSNESS-IIT"}
    expected = {identity: pair for identity in (
        "SRC-BQ001-COGITATE-2025", "CLAIM-BQ001-COGITATE-2025-OBS-01"
    )}
    if shared != expected:
        raise ValueError("shared source membership requires review")
    states = {item["inventory_item_id"]: item["independence_state"] for item in items}
    if states.get("FW-BQ001-CONSCIOUSNESS-GNWT") != "SINGLE_GOVERNED_SOURCE_DO_NOT_COUNT_AS_REPLICATION" or states.get("FW-BQ001-CONSCIOUSNESS-IIT") != "SHARED_SOURCE_WITH_GNWT_DO_NOT_DOUBLE_COUNT":
        raise ValueError("shared source independence state drift")


def require_exact_keys(value, expected, label):
    if not isinstance(value, dict) or set(value) != expected:
        raise ValueError(f"{label} exact allowed-key set drift")


def validate_allowed_keys(data):
    require_exact_keys(data, ALLOWED_KEYS["top"], "top-level inventory")
    require_exact_keys(data["scope"], ALLOWED_KEYS["scope"], "scope")
    require_exact_keys(data["summary"], ALLOWED_KEYS["summary"], "summary")
    require_exact_keys(
        data["promotion_guards"], ALLOWED_KEYS["promotion_guards"], "promotion guards"
    )
    require_exact_keys(
        data["operational_boundaries"],
        ALLOWED_KEYS["operational_boundaries"],
        "operational boundaries",
    )
    for artifact in data["governed_artifacts"]:
        require_exact_keys(artifact, ALLOWED_KEYS["artifact"], "governed artifact")
    for exclusion in data["exclusions"]:
        require_exact_keys(exclusion, ALLOWED_KEYS["exclusion"], "exclusion")
    for item in data["inventory"]:
        require_exact_keys(item, ALLOWED_KEYS["item"], "inventory item")


def validate(data):
    from jsonschema import Draft202012Validator

    privacy_check(data)
    validate_allowed_keys(data)
    schema = load_json(SCHEMA.read_bytes())
    privacy_check(schema)
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path))
    if errors:
        raise ValueError("framework inventory schema violation")

    if any(data.get(field) != expected for field, expected in EXPECTED_CORE.items()):
        raise ValueError("review-only core invariant drift")
    if data["inherited_v016_readiness_pin"] != EXPECTED_PIN:
        raise ValueError("v0.16 pin drift")
    if data["scope"]["description"] != EXPECTED_SCOPE_DESCRIPTION:
        raise ValueError("review-only scope description drift")
    if any(data["scope"].get(field) != expected for field, expected in EXPECTED_SCOPE_FLAGS.items()):
        raise ValueError("review-only scope invariant drift")
    exclusions = {(item["name"], item["reason"]) for item in data["exclusions"]}
    if len(exclusions) != len(data["exclusions"]) or exclusions != EXPECTED_EXCLUSIONS:
        raise ValueError("framework exclusion drift")

    artifacts = data["governed_artifacts"]
    paths = [item["path"] for item in artifacts]
    roles = [item["role"] for item in artifacts]
    if len(set(paths)) != len(paths) or len(set(roles)) != len(roles):
        raise ValueError("duplicate governed artifact or role")

    if set(paths) != set(EXPECTED_BLOBS):
        raise ValueError("governed artifact set drift")
    expected_roles = {
        "references/big-questions/BQ001/spec-v0.1.json": "question_and_umbrella_model_contract",
        "references/big-questions/BQ001/public-synthesis-v0.1.json": "public_safe_synthesis",
        "references/big-questions/BQ001/evidence-batch1-v0.1.json": "neuroscience_and_cardiac_arrest",
        "references/big-questions/BQ001/evidence-batch2-v0.1.json": "memory_identity_and_nde_methods",
        "references/big-questions/BQ001/evidence-batch3-v0.1.json": "reincarnation_reports_and_methods",
        "references/big-questions/BQ001/evidence-batch4-v0.1.json": "contemplative_and_philosophy",
        "references/big-questions/BQ001/evidence-batch5-v0.1.json": "supplemental_science_and_theory_testing",
    }

    loaded = {}
    by_name = {}
    for artifact in artifacts:
        if artifact["git_blob_sha"] != EXPECTED_BLOBS[artifact["path"]]:
            raise ValueError("governed artifact pin drift")
        if artifact["role"] != expected_roles[artifact["path"]]:
            raise ValueError("governed artifact role drift")
        path = ROOT / artifact["path"]
        raw = path.read_bytes()
        if git_blob_sha(raw) != artifact["git_blob_sha"]:
            raise ValueError("governed artifact drift")
        document = load_json(raw)
        privacy_check(document)
        loaded[artifact["path"]] = document
        if path.name in by_name:
            raise ValueError("ambiguous governed artifact name")
        by_name[path.name] = document

    items = data["inventory"]
    ids = [item["inventory_item_id"] for item in items]
    if set(ids) != EXPECTED_IDS or len(ids) != len(set(ids)):
        raise ValueError("framework inventory identity drift")
    names = [item["canonical_name"] for item in items]
    if len(names) != len(set(names)):
        raise ValueError("duplicate canonical framework name")

    validate_shared_sources(items)
    for item in items:
        validate_locators(item, by_name)
        semantics = tuple(tuple(item[field]) if isinstance(item[field], list) else item[field]
                          for field in SEMANTIC_FIELDS)
        if semantics != EXPECTED_SEMANTICS[item["inventory_item_id"]]:
            raise ValueError("framework identity semantics drift")
        if item["evidence_role"] == "Established Evidence" and item["category"] != "CONSCIOUSNESS_THEORY":
            raise ValueError("empirical label applied outside bounded theory test")
        if item["evidence_role"] == "organising_model_only" and item["category"] != "UMBRELLA_MODEL":
            raise ValueError("organising role applied outside umbrella model")
        if item["category"] == "UMBRELLA_MODEL":
            if item["independence_state"] != "NOT_APPLICABLE_TO_MODEL":
                raise ValueError("model assigned evidence independence")
        elif item["independence_state"] == "NOT_APPLICABLE_TO_MODEL":
            raise ValueError("evidence-bearing item lacks review state")

    counts = {
        "governed_artifacts": len(artifacts),
        "inventory_items": len(items),
        "umbrella_models": sum(i["category"] == "UMBRELLA_MODEL" for i in items),
        "philosophical_frameworks": sum(i["category"] == "PHILOSOPHICAL_FRAMEWORK" for i in items),
        "contemplative_frameworks": sum(i["category"] in {
            "CONTEMPLATIVE_PHILOSOPHICAL_FRAMEWORK",
            "PEER_REVIEWED_REVIEW_FRAMEWORK",
            "PEER_REVIEWED_THEORETICAL_FRAMEWORK",
        } for i in items),
        "neuroscientific_explanatory_models": sum(i["category"] == "NEUROSCIENTIFIC_EXPLANATORY_MODEL" for i in items),
        "consciousness_theories": sum(i["category"] == "CONSCIOUSNESS_THEORY" for i in items),
        "resolved_items": sum(i["status"] == "RESOLVED" for i in items),
        "accepted_edges": 0,
    }
    if data["summary"] != counts:
        raise ValueError("framework inventory summary drift")
    if data["promotion_guards"] != EXPECTED_PROMOTION_GUARDS:
        raise ValueError("promotion guard mapping drift")
    if data["operational_boundaries"] != EXPECTED_OPERATIONAL_BOUNDARIES:
        raise ValueError("operational boundary mapping drift")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=str(INVENTORY))
    args = parser.parse_args()
    try:
        target = Path(args.path)
        data = load_json(target.read_bytes())
        validate(data)
        if target == INVENTORY and target.read_text(encoding="utf-8") != canonical(data):
            raise ValueError("noncanonical serialization")
    except (ValueError, TypeError, KeyError, OSError, IndexError, AttributeError) as exc:
        print(f"BQ001 v0.17 framework inventory FAIL: {exc}; no synthesis or promotion", file=sys.stderr)
        return 1
    print("BQ001 v0.17 framework inventory PASS; unresolved; review-only; zero accepted edges")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
