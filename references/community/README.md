# Community archive notes

This directory contains a pilot dataset for the r/NeuronsToNirvana community archive used by the Noetic Sciences Toolkit.

## Pilot status

This is a pilot only. It exists to test the archive schema, categorisation, and provenance approach before broader expansion.

The full archive will only be expanded after the schema and provenance approach are reviewed and approved by the project maintainers.

## Import schema

Each record uses the same structure for consistent future imports:

- title
- reddit_url
- author
- attribution_note
- date
- source_type
- category
- short_summary
- external_source_url
- toolkit_framework
- research_question_potential
- visual_audio_art_flag
- evidence_status
- provenance_status

## Classification rules

- source_type describes the kind of source (for example: discussion, personal_experience, art_discussion, framework_discussion)
- category describes the top-level theme (for example: Consciousness, Music, Frameworks, Nature / Ecology)
- evidence_status describes the epistemic status (for example: community_observation, lived_experience, creative_cultural_material, speculation)
- toolkit_framework is used only when it is genuinely relevant; otherwise use a neutral or general value

## Scope

- Preserve original Reddit URLs and attribution.
- Link to the original source rather than reproduce text or images where rights are uncertain.
- Distinguish community observation, lived experience, creative/cultural material, speculation, and scientific evidence.
- Avoid treating Reddit material as scientific evidence merely because it appears in the archive.
