# AkashicNET Drive canonicalisation checkpoint

Status: PRE-ALPHA v0.4.6-dev
Scope: nominated Akashic Library Drive tree only

## Current verified floor

The structural and metadata census remains complete against the current denominator:

- traversal: 66 / 66 top-level roots closed = 40.0 / 40 points
- metadata inventory: 195 / 195 known folder nodes exact = 25.0 / 25 points
- canonicalisation denominator: 2,152 observed document objects
- explicitly reconciled manifestations: 130
- canonicalisation object coverage: 130 / 2,152 = 6.0409%
- canonicalisation contribution: 0.9061 / 15 points
- verified AKASHICNET-004 lower bound: 65.9061%

Privacy/public-status classification and validation remain scored at zero until each receives an independent denominator.

## Canonicalisation queue checkpoint

`drive-canonicalisation-candidates.csv` contains 29 identified work/copy/edition families.

- 27 families: REVIEWED
- 2 families: CANDIDATE
- 130 physical Drive manifestations represented in these families
- 61 logical units represented after work/volume-level reconciliation
- 69 redundant or alternate physical manifestations exposed inside the identified clusters

These numbers describe only the identified candidate clusters. They are not a claim that the full Drive corpus contains only 61 canonical works or only 69 duplicates.

## Corpus denominator

The current physical-document denominator is derived from the complete metadata census:

- 1,287 direct document objects in the 66 top-level roots
- 865 document objects represented in descendant collections
- 2,152 observed document objects total

Known document-level technical exclusions currently represented inside that denominator are at least eight: one zero-byte Magick PDF, one zero-byte Buddhism PDF, five zero-byte PDF/Bookz objects, and one `.crdownload` artefact in Black's Law Dictionary. Three `.DS_Store` artefacts in Theosophy are tracked separately because they are outside the document-only counts.

See `drive-canonicalisation-denominator.md` for the scoring method and exclusion treatment.

## Canonicalisation hierarchy

AkashicNET preserves the following levels rather than flattening PDFs directly into works:

`Drive object -> usable document -> copy/edition/translation -> logical volume -> canonical work -> appears_in collection`

Examples:

- a byte-identical copy candidate can share one manifestation identity after hash verification;
- two editions of the same work remain separate edition nodes;
- translations remain separate manifestations of one canonical work;
- multi-volume sets retain volume structure;
- a work appearing in multiple library folders gets multiple `appears_in` relationships rather than duplicate work nodes.

## Match classes

- `DUPLICATE_COPY`: normalised title plus supporting metadata such as identical size; hash verification still required for byte identity.
- `SAME_DRIVE_OBJECT_MULTICOLLECTION`: one Drive object is associated with more than one collection path; do not manufacture duplicate manifestation nodes.
- `DUPLICATE_WORK`: same work/title in separate physical objects; edition identity unresolved.
- `DUPLICATE_SERIES`: matching logical volume sequence across collection paths.
- `ALTERNATE_COPY_SERIES`: same logical series but copy/edition-level differences are visible.
- `TRANSLATION_EDITION_FAMILY`: same canonical work represented by distinct translations or editions.
- `EDITION_OR_COLLECTION_FAMILY`: one canonical work represented through different packaging or volume structures.
- `EDITION_OR_COPY_FAMILY`: same canonical work appears in an author/thematic collection pair but copy identity is unresolved.
- `WORK_FAMILY`: title/author evidence supports a common work but edition/copy relationships still need resolution.

## Normalisation rules

Normalised-title matching is case-insensitive and punctuation-insensitive, collapses underscores/hyphens/extra whitespace, and strips obvious copy suffixes such as `(1)` only when supporting metadata makes the equivalence plausible. Roman and Arabic volume numbers are normalised into a comparable volume field. Author prefixes and common filename boilerplate should be separated from the work title rather than discarded.

Do not treat identical filenames as proof of byte identity. Do not merge translations. Do not merge collected editions with individual works. Do not merge a multi-volume edition into one physical file node. Preserve source collection and Drive provenance for every manifestation.

## Strong families currently represented

Reconciled families include the Lovecraft/Necronomicon five-title set; Mushrooms Russia and History; Techniques of Modern Shamanism; Forbidden History of Europe; Echoes from the Gnosis; Abramelin; The Law of One; Gospel of Thomas; Ramayana; Lao-tse's `Tao Teh King`; Timothy Leary's `Psychedelic Prayers`; Ibn al-Arabi's `Tarjuman al-Ashwaq`; internal duplicate-copy candidates for `Twelve Keys`, `Alchemy Ancient and Modern`, and Alice Bailey's `Discipleship in the New Age` Volumes 1 and 2; Leadbeater's `The Hidden Life in Freemasonry`; John Yarker's `The Arcane Schools`; Albert Pike's `Morals and Dogma`; `Egyptian Ideas of the Future Life`; `The Book of Am-Tuat`; `The Art Planet Chronicles`; `The Sutra of Recollecting the Three Jewels`; a Vimalakirti duplicate/variant candidate; Crowley's `Eight Lectures on Yoga`; Aldous Huxley's `The Doors of Perception`; Rudolf Steiner's `Knowledge of the Higher Worlds`; and Kahlil Gibran's `The Forerunner`.

## Version gate

The project remains PRE-ALPHA v0.4.6-dev with a verified global lower bound of 65.9061%.

- v0.4.6 / 60%: earned
- v0.4.7 / 70%: not yet earned
- gap to v0.4.7: 4.0939 percentage points

Under the current conservative object-coverage rule, canonicalisation alone would need at least 718 of the 2,152 document objects explicitly screened/reconciled to provide five canonicalisation points and carry the global score to 70%, assuming privacy and validation remain at zero. Progress in independently scored privacy or validation workstreams can reduce that requirement.
