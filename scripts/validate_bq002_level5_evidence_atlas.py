#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "references/big-questions/BQ002/evidence-atlas-level5-review-candidate-v0.1.json"
SPEC = ROOT / "references/big-questions/BQ002/spec-v0.1.json"

EXPECTED_BQ002_DOMAINS = frozenset([
    "perception_memory_and_learning",
    "spontaneous_thought_and_mind_wandering",
    "dreaming_and_sleep_cognition",
    "language_action_and_embodied_cognition",
    "neural_dynamics_and_predictive_processing",
    "phenomenology_and_unresolved_origins"
])

EXPECTED_SOURCES = {
    "SRC-BQ002-HUDACHEK-WAMSLEY-2023", "SRC-BQ002-FOX-2015",
    "SRC-BQ002-CHRISTOFF-2016", "SRC-BQ002-SMALLWOOD-SCHOOLER-2015",
    "SRC-BQ002-BARSALOU-2008", "SRC-BQ002-FRISTON-KIEBEL-2009",
    "SRC-BQ002-BRUINEBERG-2018", "SRC-BQ002-SELI-2018",
}
EXPECTED_SOURCE_IDENTITIES = {
    "SRC-BQ002-HUDACHEK-WAMSLEY-2023": ("10.1093/sleep/zsad111", "37058584", "https://pubmed.ncbi.nlm.nih.gov/37058584/"),
    "SRC-BQ002-FOX-2015": ("10.1016/j.neuroimage.2015.02.039", "25725466", "https://pubmed.ncbi.nlm.nih.gov/25725466/"),
    "SRC-BQ002-CHRISTOFF-2016": ("10.1038/nrn.2016.113", "27654862", "https://pubmed.ncbi.nlm.nih.gov/27654862/"),
    "SRC-BQ002-SMALLWOOD-SCHOOLER-2015": ("10.1146/annurev-psych-010814-015331", "25293689", "https://pubmed.ncbi.nlm.nih.gov/25293689/"),
    "SRC-BQ002-BARSALOU-2008": ("10.1146/annurev.psych.59.103006.093639", "17705682", "https://pubmed.ncbi.nlm.nih.gov/17705682/"),
    "SRC-BQ002-FRISTON-KIEBEL-2009": ("10.1098/rstb.2008.0300", None, "https://pmc.ncbi.nlm.nih.gov/articles/PMC2666703/"),
    "SRC-BQ002-BRUINEBERG-2018": ("10.1007/s11229-016-1239-1", "30996493", "https://pubmed.ncbi.nlm.nih.gov/30996493/"),
    "SRC-BQ002-SELI-2018": ("10.1016/j.tics.2018.03.010", None, "https://doi.org/10.1016/j.tics.2018.03.010"),
}
EXPECTED_SOURCE_METADATA = {
    "SRC-BQ002-HUDACHEK-WAMSLEY-2023": ("PEER_REVIEWED_META_ANALYSIS", "A meta-analysis of the relation between dream content and memory consolidation", "Hudachek and Wamsley", 2023, "Existing BQ002 Batch 1 review-candidate source; metadata and bounded summary only."),
    "SRC-BQ002-FOX-2015": ("PEER_REVIEWED_NEUROIMAGING_META_ANALYSIS", "The wandering brain: Meta-analysis of functional neuroimaging studies of mind-wandering and related spontaneous thought processes", "Fox et al.", 2015, "Indexed PubMed bibliographic record and peer-reviewed abstract-level review; metadata and bounded summary only."),
    "SRC-BQ002-CHRISTOFF-2016": ("PEER_REVIEWED_THEORETICAL_REVIEW", "Mind-wandering as spontaneous thought: a dynamic framework", "Christoff et al.", 2016, "Indexed PubMed bibliographic record and abstract reviewed on 2026-09-17."),
    "SRC-BQ002-SMALLWOOD-SCHOOLER-2015": ("PEER_REVIEWED_REVIEW", "The science of mind wandering: empirically navigating the stream of consciousness", "Smallwood and Schooler", 2015, "Indexed PubMed bibliographic record and publisher abstract reviewed on 2026-09-17."),
    "SRC-BQ002-BARSALOU-2008": ("PEER_REVIEWED_REVIEW", "Grounded cognition", "Barsalou", 2008, "Indexed PubMed bibliographic record and abstract-level review; metadata and bounded summary only."),
    "SRC-BQ002-FRISTON-KIEBEL-2009": ("PEER_REVIEWED_THEORETICAL_REVIEW", "Predictive coding under the free-energy principle", "Friston and Kiebel", 2009, "Peer-reviewed open repository record reviewed on 2026-09-17; metadata and bounded summary only."),
    "SRC-BQ002-BRUINEBERG-2018": ("PEER_REVIEWED_METHODOLOGICAL_COUNTERSOURCE", "The anticipating brain is not a scientist: the free-energy principle from an ecological-enactive perspective", "Bruineberg, Kiverstein and Rietveld", 2018, "Indexed PubMed and PubMed Central record reviewed on 2026-09-17."),
    "SRC-BQ002-SELI-2018": ("PEER_REVIEWED_CONCEPTUAL_COUNTERSOURCE", "Mind-Wandering as a Natural Kind: A Family-Resemblances View", "Seli et al.", 2018, "Publisher DOI record and indexed bibliographic search reviewed on 2026-09-17."),
}
EXPECTED_CLAIMS = {
    "CLAIM-BQ002-ATLAS-DREAM-MEMORY-01": ("Established Evidence", "OBSERVATION", "dreaming_and_sleep_cognition", {"SRC-BQ002-HUDACHEK-WAMSLEY-2023"}, set(), "Across the studies synthesized by Hudachek and Wamsley, incorporation of learning-task content into dreams was positively associated with later memory performance."),
    "CLAIM-BQ002-ATLAS-NETWORKS-01": ("Established Evidence", "OBSERVATION", "neural_dynamics_and_predictive_processing", {"SRC-BQ002-FOX-2015"}, {"SRC-BQ002-SELI-2018"}, "A meta-analysis of functional-neuroimaging studies reported convergent recruitment of default-mode and executive-system regions during mind-wandering and related spontaneous-thought tasks."),
    "CLAIM-BQ002-ATLAS-SPONTANEOUS-01": ("Interpretation", "INTERPRETATION", "spontaneous_thought_and_mind_wandering", {"SRC-BQ002-CHRISTOFF-2016", "SRC-BQ002-SMALLWOOD-SCHOOLER-2015"}, {"SRC-BQ002-SELI-2018"}, "Dynamic accounts treat mind-wandering as part of a broader family of spontaneous-thought phenomena whose content and movement reflect interactions among memory, affect, attention and cognitive constraints."),
    "CLAIM-BQ002-ATLAS-GROUNDED-01": ("Interpretation", "INTERPRETATION", "language_action_and_embodied_cognition", {"SRC-BQ002-BARSALOU-2008"}, set(), "Grounded-cognition research supports treating perception, bodily state, action and situated context as contributors to cognitive content rather than assuming thought is isolated from them."),
    "CLAIM-BQ002-ATLAS-PREDICTIVE-01": ("Hypothesis", "HYPOTHESIS", "perception_memory_and_learning", {"SRC-BQ002-FRISTON-KIEBEL-2009"}, {"SRC-BQ002-BRUINEBERG-2018"}, "Predictive-coding and free-energy frameworks offer testable ways to model how prior expectations, sensory signals and action may constrain cognition."),
    "CLAIM-BQ002-ATLAS-PHENOMENAL-01": ("Interpretation", "INTERPRETATION", "phenomenology_and_unresolved_origins", {"SRC-BQ002-CHRISTOFF-2016", "SRC-BQ002-BARSALOU-2008", "SRC-BQ002-FRISTON-KIEBEL-2009"}, {"SRC-BQ002-BRUINEBERG-2018"}, "Evidence about mechanisms, correlates and report constrains accounts of thought content but does not by itself resolve why thoughts are subjectively experienced."),
}
REQUIRED_TRUE_PROMOTION_GUARDS = {
    "correlation_may_not_be_presented_as_complete_causal_explanation",
    "neural_prediction_may_not_be_presented_as_thought_reading",
    "dream_content_may_not_be_presented_as_independent_of_memory",
    "mechanistic_account_may_not_be_presented_as_resolving_phenomenology",
    "testimony_may_not_auto_promote_to_established_evidence",
    "source_count_may_not_upgrade_evidence",
    "retrieval_rank_may_not_upgrade_evidence",
    "semantic_similarity_may_not_upgrade_evidence",
    "ai_synthesis_may_not_be_primary_source",
}
FALSE_GUARDS = {
    "public_beta_gate", "canonical_promotion_applied", "evidence_promotion_applied",
    "public_synthesis_updated", "website_updated", "truth_inference_allowed",
    "scientific_evidence_promotion_allowed", "transpersonal_claim_promoted",
    "rights_promotion_allowed", "privacy_posture_changed", "cultural_safeguarding_relaxed",
}


# Reviewed qualification and notice contracts; changes require explicit review.
EXPECTED_QUALIFICATIONS = {'CLAIM-BQ002-ATLAS-DREAM-MEMORY-01': (['Association does not establish causal direction or '
                                        'explain all dream content.'],
                                       'Which mechanisms link pre-sleep learning, dream '
                                       'incorporation and later performance remains unresolved.'),
 'CLAIM-BQ002-ATLAS-GROUNDED-01': (['The contribution and necessity of grounding vary across '
                                    'theories, tasks and types of representation.'],
                                   'No single grounded account currently explains every abstract, '
                                   'linguistic or spontaneous thought.'),
 'CLAIM-BQ002-ATLAS-NETWORKS-01': (['Task and construct heterogeneity limits inference from '
                                    'spatial convergence to a single mechanism or origin.'],
                                   'The temporal and causal contributions of interacting networks '
                                   'to specific thought content remain unresolved.'),
 'CLAIM-BQ002-ATLAS-PHENOMENAL-01': (['This is a boundary on inference, not evidence for a '
                                      'transpersonal or non-biological source.'],
                                     'The relationship between mechanistic explanation and '
                                     'phenomenal experience remains disputed.'),
 'CLAIM-BQ002-ATLAS-PREDICTIVE-01': (['The framework has competing interpretations and does not '
                                      'uniquely specify the origin of every thought.'],
                                     'Evidence must distinguish particular implementations and '
                                     "predictions rather than treating the framework's breadth as "
                                     'confirmation.'),
 'CLAIM-BQ002-ATLAS-SPONTANEOUS-01': (['The category is heterogeneous and review-level frameworks '
                                       'are not unique causal explanations.'],
                                      'Prospective measurements do not yet reconstruct a complete '
                                      'causal path from antecedent processes to a particular '
                                      'conscious thought.')}
EXPECTED_NOTICES = {'SRC-BQ002-BARSALOU-2008': None,
 'SRC-BQ002-BRUINEBERG-2018': None,
 'SRC-BQ002-CHRISTOFF-2016': None,
 'SRC-BQ002-FOX-2015': {'doi': '10.1016/j.neuroimage.2016.02.052',
                        'pmid': '27320028',
                        'type': 'CORRIGENDUM'},
 'SRC-BQ002-FRISTON-KIEBEL-2009': None,
 'SRC-BQ002-HUDACHEK-WAMSLEY-2023': None,
 'SRC-BQ002-SELI-2018': None,
 'SRC-BQ002-SMALLWOOD-SCHOOLER-2015': None}


EXPECTED_SOURCE_LIMITATIONS = {'SRC-BQ002-BARSALOU-2008': ['The review covers multiple grounded-cognition theories rather than '
                             'one settled mechanism.',
                             'Evidence for sensorimotor and situated contributions does not show '
                             'that every concept or thought is fully grounded in the same way.',
                             'Grounding mechanisms do not resolve why cognition is subjectively '
                             'experienced.'],
 'SRC-BQ002-BRUINEBERG-2018': ['The paper presents a philosophical and theoretical critique rather '
                               'than a direct experimental refutation.',
                               'Its ecological-enactive interpretation is itself one contested '
                               'framework.',
                               'Disagreement over the meaning of inference constrains '
                               'interpretation but does not eliminate empirical '
                               'predictive-processing findings.'],
 'SRC-BQ002-CHRISTOFF-2016': ['The article proposes a theoretical framework rather than reporting '
                              'one decisive experiment.',
                              'Large-scale network recruitment does not by itself identify the '
                              'complete causal or phenomenal origin of a thought.',
                              'Mind-wandering, dreaming and creative thought should not be treated '
                              'as one homogeneous phenomenon.'],
 'SRC-BQ002-FOX-2015': ['The synthesis pooled 24 functional-neuroimaging studies with '
                        'heterogeneous tasks and definitions.',
                        'Spatial convergence identifies correlates and does not establish a unique '
                        'causal origin of thought.',
                        'A corrigendum exists and must remain linked as provenance rather than '
                        'treated as a retraction.'],
 'SRC-BQ002-FRISTON-KIEBEL-2009': ['The free-energy formulation is a broad theoretical framework '
                                   'and is not a direct observation of thought generation.',
                                   'Model fit or explanatory scope does not establish that '
                                   'predictive coding is the unique cognitive architecture.',
                                   'The framework does not by itself resolve phenomenal '
                                   'consciousness.'],
 'SRC-BQ002-HUDACHEK-WAMSLEY-2023': ['The association does not establish that dream incorporation '
                                     'causes improved memory.',
                                     'Tasks, dream collection and analytic methods varied across '
                                     'studies.',
                                     'The findings do not explain the complete origin of thought '
                                     'or subjective awareness.'],
 'SRC-BQ002-SELI-2018': ['Conceptual analysis does not quantify the prevalence or neural basis of '
                         'particular thought types.',
                         'A family-resemblances account may improve classification without '
                         'resolving causal origin.',
                         'Operational heterogeneity remains an empirical problem even after '
                         'terminology is refined.'],
 'SRC-BQ002-SMALLWOOD-SCHOOLER-2015': ['Review-level synthesis depends on heterogeneous '
                                       'self-report and task-probe methods.',
                                       'Retrospective awareness and report may miss or reshape the '
                                       'processes that preceded conscious access.',
                                       'Functional costs and benefits vary with content, context '
                                       'and meta-awareness.']}

EXPECTED_CANONICAL_CLAIMS = [{'claim_id': 'CLAIM-BQ002-FRAMEWORK-001',
  'contradicts': [],
  'domain': 'phenomenology_and_unresolved_origins',
  'evidence_label': 'Established Evidence',
  'provenance': ['references/big-questions/BQ002/spec-v0.1.json'],
  'reviewed_support': True,
  'scope': 'project_state_only',
  'source_ids': [],
  'supports_models': [],
  'text': 'BQ002 currently has no adjudicated substantive answer.',
  'uncertainty': 'No empirical or metaphysical conclusion is implied by this project-state '
                 'statement.'}]
EXPECTED_CANONICAL_MODELS = {'MODEL-BQ002-COGNITIVE-GENERATION': {'model_id': 'MODEL-BQ002-COGNITIVE-GENERATION',
                                      'name': 'cognitive_generation_model',
                                      'position': 'Thought content arises through interacting '
                                                  'perceptual, mnemonic, predictive, affective, '
                                                  'linguistic and action-related processes '
                                                  'implemented by biological cognitive systems.',
                                      'status': 'UNRESOLVED'},
 'MODEL-BQ002-PHENOMENAL-GAP': {'model_id': 'MODEL-BQ002-PHENOMENAL-GAP',
                                'name': 'phenomenal_origin_unresolved_model',
                                'position': 'Mechanistic accounts of thought content and access '
                                            'may remain incomplete as accounts of why thought is '
                                            'subjectively experienced.',
                                           'status': 'UNRESOLVED'}}
EXPECTED_MATURITY_MEANING = (
    "Research maturity only; not truth probability, evidence strength, transpersonal support, "
    "or readiness for canonical or public promotion."
)
EXPECTED_CANONICAL_SOURCES = [{
    "source_id": "SRC-BQ002-SEED-001",
    "source_type": "FRAMEWORK_PLACEHOLDER",
    "citation": "Seed placeholder only; replace with a reproducible primary or secondary source before supporting a substantive claim.",
    "publication_date": None,
    "url": None,
    "limitations": ["Not evidence", "Cannot support Established Evidence"],
}]
EXPECTED_EVIDENCE_LABELS = [
    "Established Evidence", "Interpretation", "Lived Experience/Testimony", "Hypothesis", "Speculation",
]
EXPECTED_OPEN_QUESTIONS = [
    "Which measurable processes generate or constrain specific thought content?",
    "How do memory, perception, affect, language and action interact in spontaneous and deliberate thought?",
    "What distinguishes the causal origin of a thought from retrospective awareness or report of it?",
    "Which findings explain thought content, and which bear on subjective experience?",
    "Which claims are empirical, philosophical, interpretive, testimonial or speculative?",
]

def fail(message):
    raise ValueError(message)


def validate(atlas, spec):
    if spec.get("sources") != EXPECTED_CANONICAL_SOURCES:
        fail("canonical placeholder-source contract changed")
    if spec.get("canonical_evidence_labels") != EXPECTED_EVIDENCE_LABELS:
        fail("canonical evidence-label taxonomy changed")
    if spec.get("conclusion_policy") != "UNDETERMINED_AT_INGESTION":
        fail("canonical conclusion policy must remain undetermined")
    if spec.get("claims") != EXPECTED_CANONICAL_CLAIMS:
        fail("canonical bounded claim contract changed")
    if spec.get("open_questions") != EXPECTED_OPEN_QUESTIONS:
        fail("canonical open-question contract changed")
    canonical_models = spec.get("models", [])
    if {m.get("model_id"): m for m in canonical_models} != EXPECTED_CANONICAL_MODELS:
        fail("canonical bounded model definitions changed")
    if spec.get("id") != "BQ002" or spec.get("status") != "UNRESOLVED":
        fail("canonical BQ002 spec must remain UNRESOLVED")
    if spec.get("public_beta_gate") is not False:
        fail("canonical BQ002 public beta gate must remain closed")
    canonical_claims = spec.get("claims")
    if not isinstance(canonical_claims, list) or not canonical_claims:
        fail("canonical claims must be present")
    if any(claim.get("supports_models") != [] for claim in canonical_claims):
        fail("canonical claims must retain empty model support")
    for claim in canonical_claims:
        if any(claim.get(key) != [] for key in ("source_ids", "contradicts")):
            fail("canonical source and contradiction edges must remain empty")
    models = spec.get("models", [])
    expected_models = {"MODEL-BQ002-COGNITIVE-GENERATION", "MODEL-BQ002-PHENOMENAL-GAP"}
    if len(models) != 2 or {m.get("model_id") for m in models} != expected_models:
        fail("canonical model identities changed")
    if any(m.get("status") != "UNRESOLVED" for m in models):
        fail("canonical models must remain UNRESOLVED")
    graph = spec.get("graph", {})
    if graph.get("truth_inference_allowed") is not False or graph.get("edge_state_may_upgrade_evidence") is not False:
        fail("canonical graph truth and evidence-upgrade boundaries weakened")
    promotion_guards = spec.get("promotion_guards", {})
    if any(promotion_guards.get(key) is not True for key in REQUIRED_TRUE_PROMOTION_GUARDS):
        fail("canonical no-promotion prohibition missing or weakened")
    if promotion_guards.get("rights_promotion_allowed") is not False or promotion_guards.get("scientific_truth_inference_allowed") is not False:
        fail("canonical rights or scientific truth-inference boundary weakened")
    if atlas.get("status") != "REVIEW_CANDIDATE":
        fail("evidence atlas must remain a review candidate")
    if atlas.get("question_id") != "BQ002" or atlas.get("question_status") != "UNRESOLVED":
        fail("BQ002 must remain UNRESOLVED")
    maturity = atlas.get("maturity", {})
    if maturity.get("current_level") != 4 or maturity.get("candidate_level") != 5:
        fail("atlas must describe the bounded Level 4 to Level 5 transition")
    if maturity.get("candidate_level_applied") is not False:
        fail("Level 5 may not be applied before review")
    if maturity.get("meaning") != EXPECTED_MATURITY_MEANING:
        fail("maturity meaning must remain claim bounded")

    scope = atlas.get("scope", {})
    for key in ("complete_origin_theory_claimed", "phenomenology_resolved", "transpersonal_information_established", "source_count_advances_level"):
        if scope.get(key) is not False:
            fail(f"scope boundary weakened: {key}")

    sources = atlas.get("sources", [])
    source_map = {item.get("source_id"): item for item in sources}
    if set(source_map) != EXPECTED_SOURCES or len(source_map) != len(sources):
        fail("source set changed or duplicated")
    for source in sources:
        if source.get("related_notice") != EXPECTED_NOTICES[source["source_id"]]:
            fail("source related-notice provenance changed")
        if not source.get("title") or not source.get("provenance"):
            fail("source provenance incomplete")
        expected_doi, expected_pmid, expected_url = EXPECTED_SOURCE_IDENTITIES[source["source_id"]]
        if (source.get("doi"), source.get("pmid"), source.get("url")) != (expected_doi, expected_pmid, expected_url):
            fail(f"source identity changed: {source['source_id']}")
        expected_type, expected_title, expected_authors, expected_year, expected_provenance = EXPECTED_SOURCE_METADATA[source["source_id"]]
        if (
            source.get("source_type"), source.get("title"), source.get("authors_short"),
            source.get("year"), source.get("provenance")
        ) != (expected_type, expected_title, expected_authors, expected_year, expected_provenance):
            fail(f"source bibliographic or provenance metadata changed: {source['source_id']}")
        if source.get("limitations") != EXPECTED_SOURCE_LIMITATIONS[source["source_id"]]:
            fail("every source requires limitations")

    allowed_labels = set(spec.get("canonical_evidence_labels", []))
    claims = atlas.get("claims", [])
    claim_map = {item.get("claim_id"): item for item in claims}
    if set(claim_map) != set(EXPECTED_CLAIMS) or len(claim_map) != len(claims):
        fail("claim set changed or duplicated")
    used_sources = set()
    for claim_id, claim in claim_map.items():
        expected_label, expected_type, expected_domain, expected_source_ids, expected_counter_ids, expected_text = EXPECTED_CLAIMS[claim_id]
        label = claim.get("evidence_label")
        if label != expected_label or label not in allowed_labels:
            fail("claim evidence label changed")
        if claim.get("claim_type") != expected_type:
            fail("claim type changed")
        if claim.get("domain") != expected_domain:
            fail("claim domain changed")
        if (claim.get("limitations"), claim.get("unresolved_gap")) != EXPECTED_QUALIFICATIONS[claim_id]:
            fail("bounded claim qualifications changed")
        if claim.get("text") != expected_text:
            fail("bounded claim text changed")
        source_ids = claim.get("source_ids", [])
        counter_ids = claim.get("counter_source_ids", [])
        if len(source_ids) != len(set(source_ids)) or len(counter_ids) != len(set(counter_ids)):
            fail("claim source bindings must be unique")
        if set(source_ids) != expected_source_ids or set(counter_ids) != expected_counter_ids:
            fail("claim source binding invalid")
        if claim.get("supports_models") != []:
            fail("claim model support must remain empty")
        if not claim.get("limitations") or not claim.get("unresolved_gap"):
            fail("claim limitations or unresolved gap missing")
        used_sources.update(source_ids)
        used_sources.update(counter_ids)
    if used_sources != EXPECTED_SOURCES:
        fail("every source must be used by a bounded claim or counter-interpretation")

    domains = set(spec.get("domains", []))
    if domains != EXPECTED_BQ002_DOMAINS:
        fail("canonical BQ002 domain set changed")
    coverage = atlas.get("coverage", [])
    if {item.get("domain") for item in coverage} != EXPECTED_BQ002_DOMAINS or len(coverage) != len(EXPECTED_BQ002_DOMAINS):
        fail("all six canonical BQ002 domains must be mapped exactly once")
    for item in coverage:
        ids = item.get("claim_ids", [])
        if len(ids) != len(set(ids)):
            fail("coverage claim bindings must be unique")
        if not ids or not set(ids).issubset(claim_map):
            fail("coverage claim binding invalid")
        if any(claim_map[claim_id].get("domain") != item.get("domain") for claim_id in ids):
            fail("coverage domain does not match its bound claims")

    rights = atlas.get("rights", {})
    if rights.get("record_type") != "bibliographic_metadata_and_bounded_summary":
        fail("rights scope changed")
    for key in ("full_text_republished", "audio_or_transcript_republished", "quotations_republished"):
        if rights.get(key) is not False:
            fail("rights boundary weakened")

    governance = atlas.get("governance", {})
    if governance.get("question_status") != "UNRESOLVED":
        fail("governed question status changed")
    if governance.get("accepted_canonical_edges") != 0 or governance.get("supports_models") != []:
        fail("canonical/model edges must remain empty")
    for key in FALSE_GUARDS:
        if governance.get(key) is not False:
            fail(f"governance guard weakened: {key}")


def main():
    try:
        validate(json.loads(ATLAS.read_text(encoding="utf-8")), json.loads(SPEC.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BQ002 LEVEL 5 EVIDENCE ATLAS FAIL: {exc}", file=sys.stderr)
        return 1
    print("BQ002 LEVEL 5 EVIDENCE ATLAS PASS: review candidate; BQ002 UNRESOLVED; accepted edges 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
