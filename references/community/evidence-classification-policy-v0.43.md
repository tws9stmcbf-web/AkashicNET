# AkashicNET evidence classification policy v0.43

## Milestone
Introduce an evidence/source-form classification layer while refusing to infer scientific status from generic metadata.

## Supported classes
v0.43 classifies only what the tracked `source_type` field supports:
- `COMMUNITY_POST`
- `COMMUNITY_COLLECTION`
- `BOOK_OR_LONGFORM_METADATA`
- `ARTICLE_UNRESOLVED`
- `UNKNOWN`

An `article` is not automatically primary research, peer reviewed, a review article, journalism, scholarship, or scientific evidence. Those distinctions require richer provenance and/or explicit review.

## Scientific evidence field
Every v0.43 row starts with `scientific_evidence_status=NOT_EVALUATED`. Source form and evidence quality are separate dimensions.

## Review state
Article-unresolved and unknown records remain `UNREVIEWED`. Community/book form can be metadata-classified without implying evidentiary authority.

## Guardrails
- source form ≠ evidence strength
- evidence class ≠ truth
- article ≠ scientific evidence
- book ≠ authoritative evidence
- community post ≠ scientific evidence by default
- no document/post body reads
- no embeddings
- no rights promotion
- no truth inference
