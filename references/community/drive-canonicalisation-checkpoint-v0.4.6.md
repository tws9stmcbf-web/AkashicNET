# AkashicNET Drive canonicalisation checkpoint

Status: PRE-ALPHA v0.4.6-dev
Scope: nominated Akashic Library Drive tree only

## Current verified floor

The structural and metadata census remains complete against the current denominator:

- traversal: 66 / 66 top-level roots closed = 40.0 / 40 points
- metadata inventory: 195 / 195 known folder nodes exact = 25.0 / 25 points
- verified AKASHICNET-004 lower bound: 65.0%

No additional global completion points are awarded yet for canonicalisation, privacy/public-status classification, or validation. Canonicalisation work is being measured separately until a defensible corpus-wide denominator exists.

## Canonicalisation queue checkpoint

`drive-canonicalisation-candidates.csv` now contains 29 identified work/copy/edition families.

- 27 families: REVIEWED
- 2 families: CANDIDATE
- 130 physical Drive manifestations represented in these families
- 61 logical units represented after work/volume-level reconciliation
- 69 redundant or alternate physical manifestations exposed inside the identified clusters

These numbers describe only the identified candidate clusters. They are not a claim that the full Drive corpus contains only 61 canonical works or only 69 duplicates.

## Canonicalisation hierarchy

AkashicNET should preserve the following levels rather than flattening PDFs directly into works:

`Drive object -> usable document -> copy/edition/translation -> logical volume -> canonical work -> appears_in collection`

Examples:

- a byte-identical copy candidate can share one manifestation identity after hash verification;
- two editions of the same work remain separate edition nodes;
- translations remain separate manifestations of one canonical work;
- multi-volume sets retain volume structure;
- a work appearing in multiple library folders gets multiple `appears_in` relationships rather than duplicate work nodes.

## Match classes

- `DUPLICATE_COPY`: normalised title plus supporting metadata such as identical size; hash verification still required for byte identity.
- `DUPLICATE_WORK`: same work/title in separate collection paths; edition identity not yet asserted.
- `DUPLICATE_SERIES`: matching logical volume sequence across collection paths.
- `ALTERNATE_COPY_SERIES`: same logical series but copy/edition-level differences are visible.
- `TRANSLATION_EDITION_FAMILY`: same canonical work represented by distinct translations or editions.
- `EDITION_OR_COLLECTION_FAMILY`: one canonical work represented through different packaging or volume structures.
- `EDITION_OR_COPY_FAMILY`: same canonical work appears in an author/thematic collection pair but copy identity is unresolved.
- `WORK_FAMILY`: title/author evidence supports a common work but edition/copy relationships still need resolution.

## Normalisation rules for the next pass

Normalised-title matching should be case-insensitive and punctuation-insensitive, collapse underscores/hyphens/extra whitespace, and strip obvious copy suffixes such as `(1)` only when other metadata supports equivalence. Roman and Arabic volume numbers should be normalised into a comparable volume field. Author prefixes and common filename boilerplate should be separated from the work title rather than discarded.

Do not treat identical filenames as proof of byte identity. Do not merge translations. Do not merge collected editions with individual works. Do not merge a multi-volume edition into one physical file node. Preserve source collection and Drive provenance for every manifestation.

## Strong families added in this pass

Newly reconciled families include Lao-tse's `Tao Teh King` across Buddhism/Taoism; Timothy Leary's `Psychedelic Prayers` across Taoism/Shamanism; Ibn al-Arabi's `Tarjuman al-Ashwaq` across Sufism/Islam; internal duplicate-copy candidates for `Twelve Keys`, `Alchemy Ancient and Modern`, and Alice Bailey's `Discipleship in the New Age` Volumes 1 and 2; Leadbeater's `The Hidden Life in Freemasonry`; John Yarker's `The Arcane Schools`; Albert Pike's `Morals and Dogma`; `Egyptian Ideas of the Future Life`; `The Book of Am-Tuat`; `The Art Planet Chronicles`; `The Sutra of Recollecting the Three Jewels`; a Vimalakirti duplicate/variant candidate; Crowley's `Eight Lectures on Yoga`; Aldous Huxley's `The Doors of Perception`; Rudolf Steiner's `Knowledge of the Higher Worlds`; and Kahlil Gibran's `The Forerunner`.

## Version gate

The project remains at PRE-ALPHA v0.4.6-dev with a 65.0% verified global lower bound. v0.4.7 is not awarded from the candidate-family count alone. The next gate requires a defensible denominator for at least part of the 15-point canonicalisation component, or verified progress from the privacy/public-status and validation components.
