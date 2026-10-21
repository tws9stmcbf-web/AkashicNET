# Eight-dossier fact-check and correction record

**21 October 2026 · AI-assisted · DRAFT / NOT FOR PARTICIPANT USE**

Reviewed [PR #405](https://github.com/tws9stmcbf-web/AkashicNET/pull/405) at commit `9bbbbb3ac6d00f1cf959b9e5f04e0bd218901157`. Materials remain **0.2-candidate**, supporting protocol **0.1**; editorial revision `source-fact-check-2026-10-21`. This record is not independent human review, rights clearance, preregistration or approval to recruit or run an experiment.

## Result and limits

All eight stated Nobel award years/categories and all ordinary keyed answers agree with the checked evidence or fictional premises. The original Markdown and JSON dossiers matched. Of 44 historical assertion records, 29 have support in retrieved institutional page text, 14 remain supported by indexed official text, and one is narrowed to a stated educational aim. Eight final scope disclaimers are authorial boundaries, not historical claims. The [machine-readable record](fact-check-2026-10-21.json) maps every assertion and all 48 items to sources, reasoning and dispositions.

Direct retrieval of 11 original canonical URLs returned HTTP 403 in this session. The remaining URL, S04, yielded a page shell without award text. Seven distinct historical alternative locators also returned 403. These are access limitations, not proof that sources are dead or facts false. Fourteen accessible institutional records supplement the original 12 source records. Indexed text and page-body text are explicitly separated. The user's earlier bounded successful access to Curie/Tagore pages is not rewritten as a failure; these observations are specific to this session/channel.

## Corrections and unresolved findings

| ID | Finding | Disposition |
| --- | --- | --- |
| FC01 | Outcome-sounding wording overstates what the cited Nobel account presents as educational intent. | NARROW_CORRECTION_APPLIED |
| FC02 | Distractors are other real scattering properties; a general physical reading could compete with the intended passage-recall reading. | NARROW_CORRECTION_APPLIED |
| FC03 | Curie has more than one Nobel award. Existing passage context supports 1911; explicit passage-only phrasing reduces ambiguity without exposing the L2 category. | NARROW_CORRECTION_APPLIED_KEYS_UNCHANGED |
| FC04 | All eight correct keys are o2 and second-earliest year; all option sets have offsets [-9,0,+6,+12] relative to the key. Sorting the years and choosing the second yields 8/8 without historical recall. Shuffling display position does not remove chronological-rank information. | OPEN_METHODS_REVIEW_NO_REDESIGN: Independent stimulus/methods reviewer must approve varied, nonpredictive distractor sets and a new freeze before participant use. This is an ordinary-recognition weakness, not disclosure of a hidden-symbol key. |
| FC05 | Eleven original canonical URLs and all seven distinct alternative locators returned 403 in this session; S04 returned a page shell without award evidence. A response or URL alone does not verify a claim. | SUPPLEMENTED_WITH_14_INSTITUTIONAL_RECORDS_ORIGINAL_ACCESS_HISTORY_PRESERVED: Resolve original-page/full-lecture access or accept signed alternative-source verification; no 403 is treated as proof of a dead or false source. |
| FC06 | Examples are not an exhaustive frozen field/synonym codebook; plausible distractors, reading difficulty, familiarity, accessibility, cultural acceptability and inference ceiling effects remain unvalidated. | NO_APPROVAL_OR_SCORING_CHANGE |
| FC07 | All eight original displayed dossiers, recall questions/keys, counts and seven manifest hashes agreed. S09’s indexed text does include the 1901 school date; this was not a missing-date citation defect. | MIRRORS_UPDATED_TOGETHER |
| FC08 | Institutional factual support is not rights clearance or independent human review. Source assertions do not establish the experiment’s hypothesized mechanism. | ALL_PENDING_RIGHTS_AND_REVIEW_FLAGS_RETAINED |

The three correction groups change **one dossier sentence and three question prompts**, plus Raman’s rationale. No keyed answer, option set, item/person ID, timing, randomization rule, outcome definition or analysis code changes. Curie’s wording stays passage-specific without naming Chemistry in L1 or delayed recognition, which would disclose information to another task or condition.

**Unresolved ordinary-recognition flaw:** the four years are always `award_year + [-9, 0, 6, 12]`. The second-earliest answer is correct for all eight people. A deterministic sort-and-pick rule scores 8/8 without recalling a biography; randomizing screen positions cannot remove that rank cue. This does not expose concealed symbol assignments (none exist). Distractor redesign requires its own reviewed freeze and is intentionally left open under the instruction to preserve the design.

## Dossier findings

| Figure | Stated Nobel award | Verified recall key | Qualifications |
| --- | --- | --- | --- |
| F01 Marie Curie | Chemistry, 1911 | Radium and polonium | Public Warsaw/Paris, joint element work and Sorbonne role supported; polonium naming still indexed-only. Curie also had a separate 1903 Physics award. |
| F02 C. V. Raman | Physics, 1930 | The frequency of the light | Frequency comparison supported; recall stem narrowed because other optical properties can also vary. Explicit monochromatic formulation still indexed-only. |
| F03 Dorothy Crowfoot Hodgkin | Chemistry, 1964 | Vitamin B12 | All three molecular subjects supported. Insulin structure in 1969 must not be represented as the basis of the 1964 award; the dossier makes no such claim. |
| F04 Barbara McClintock | Physiology or Medicine, 1983 | Maize | Maize and award corroborated directly; generation/trait-expression details supported in indexed Nobel text. |
| F05 Niels Bohr | Physics, 1922 | Hydrogen | 1913 hydrogen model, spectrum and Copenhagen institution supported. Treat electron-orbit language as the historical model; downward-transition wording is also in indexed Nobel text. |
| F06 Rabindranath Tagore | Literature, 1913 | Bengali | School date independently corroborated by institutional records; school founded in 1901 is distinct from later university. Aim wording narrowed; literary/language details remain indexed-only. |
| F07 Wangari Maathai | Peace, 2004 | Green Belt Movement | Biological training, 1977 movement, women’s tree planting, Kenya/environment/social work and award supported by the movement’s institutional records. |
| F08 Santiago Ramón y Cajal | Physiology or Medicine, 1906 | Camillo Golgi | Distinct-cell/contact account and staining corroborated by CSIC; joint award and method refinement supported in indexed Nobel records. Full Nobel lecture not appraised. |

## Historical assertion map

“Page” means relevant institutional page text was retrieved and inspected by this assistant. “Index” means the cited publisher’s indexed text supports the claim, while original-page verification remains unresolved. Neither means independent human sign-off. The final disclaimer in each dossier is excluded from historical fact counts and preserved unchanged.

| Assertion | Reviewed statement | Evidence status and sources | Note |
| --- | --- | --- | --- |
| F01-A1 | Marie Curie investigated radioactivity through physics and chemistry. | Page: [S13](https://curie.fr/lheritage-de-marie-curie-perpetuer-lesprit-dune-pionniere) | Physics/chemistry research and radioactivity are described in Institut Curie’s history. |
| F01-A2 | Born in Warsaw, she later worked in Paris. | Page: [S13](https://curie.fr/lheritage-de-marie-curie-perpetuer-lesprit-dune-pionniere) | Warsaw birthplace and move to Paris are explicit; Warsaw was then under Russian rule, so homeland wording is not a claim about sovereignty. |
| F01-A3 | Research with Pierre Curie identified polonium and radium. | Page: [S13](https://curie.fr/lheritage-de-marie-curie-perpetuer-lesprit-dune-pionniere) | Joint work with Pierre and both elements are named. |
| F01-A4 | The name polonium referred to the country of her birth. | Index: [S02](https://www.nobelprize.org/prizes/chemistry/1911/marie-curie/biographical/) | The indexed Nobel biography directly links the element name to her birth country; direct page remains inaccessible. |
| F01-A5 | She later held a physics professorship at the Sorbonne. | Page: [S13](https://curie.fr/lheritage-de-marie-curie-perpetuer-lesprit-dune-pionniere) | Sorbonne professorship and Paris physics laboratory are described. No appointment year is added. |
| F01-A6 | Her Nobel Prize in Chemistry was awarded in 1911. | Page: [S14](https://curiotheque.musee.curie.fr/s/fr/item/15332) | Museum catalogue identifies the 1911 Chemistry award; it is not the separate 1903 Physics award. |
| F02-A1 | C. V. Raman investigated the scattering of light. | Page: [S15](https://www.acs.org/education/whatischemistry/landmarks/ramaneffect.html) | ACS/IACS landmark describes his light-scattering investigations. |
| F02-A2 | His work examined light after it interacted with matter. | Page: [S15](https://www.acs.org/education/whatischemistry/landmarks/ramaneffect.html) | Liquid samples and interaction with matter are documented. |
| F02-A3 | Some scattered light has a different frequency from the incoming light. | Index: [S05](https://www.nobelprize.org/prizes/themes/the-nobel-prize-in-physics-1901-2000/), [S15](https://www.acs.org/education/whatischemistry/landmarks/ramaneffect.html) | S05 explicitly describes frequency shifts; S15 corroborates changed colour/wavelength and energy. |
| F02-A4 | This frequency change is associated with the Raman effect. | Index: [S05](https://www.nobelprize.org/prizes/themes/the-nobel-prize-in-physics-1901-2000/), [S15](https://www.acs.org/education/whatischemistry/landmarks/ramaneffect.html) | The frequency-shift description identifies the Raman effect, not all light scattering. |
| F02-A5 | The incoming light can have a single frequency while the scattered light includes shifted components. | Index: [S05](https://www.nobelprize.org/prizes/themes/the-nobel-prize-in-physics-1901-2000/) | S05 explicitly contrasts shifted components with incident monochromatic light. |
| F02-A6 | Raman received the Nobel Prize in Physics in 1930. | Page: [S15](https://www.acs.org/education/whatischemistry/landmarks/ramaneffect.html) | Institutional landmark records the 1930 Nobel Prize in Physics. |
| F03-A1 | Dorothy Crowfoot Hodgkin studied the structures of important biochemical molecules. | Page: [S16](https://www.mhs.ox.ac.uk/backfromthedead/exhibition/the-structure-of-penicillin/index.html) | Molecular structures of penicillin, B12 and insulin support this summary. |
| F03-A2 | Her work used X-ray crystallography to investigate how atoms were arranged. | Page: [S16](https://www.mhs.ox.ac.uk/backfromthedead/exhibition/the-structure-of-penicillin/index.html) | X-ray crystallography and atom positions are explained. |
| F03-A3 | Molecules examined in her research included penicillin, vitamin B12 and insulin. | Page: [S16](https://www.mhs.ox.ac.uk/backfromthedead/exhibition/the-structure-of-penicillin/index.html) | All three molecules are listed. Insulin’s structure was resolved in 1969; dossier does not claim it was part of the 1964 award. |
| F03-A4 | These studies connected chemistry with the structures of substances relevant to biology. | Page: [S16](https://www.mhs.ox.ac.uk/backfromthedead/exhibition/the-structure-of-penicillin/index.html) | A concise synthesis of the listed biochemical research, not a new causal claim. |
| F03-A5 | She received the Nobel Prize in Chemistry in 1964. | Page: [S16](https://www.mhs.ox.ac.uk/backfromthedead/exhibition/the-structure-of-penicillin/index.html) | The 1964 Chemistry award is explicit. |
| F04-A1 | Barbara McClintock studied genetics using maize plants. | Page: [S17](https://facultyprofiles.cshl.edu/barbara.mcclintock) | Cytogenetics and maize kernel observations are explicit. |
| F04-A2 | She followed inherited traits across successive generations. | Index: [S07](https://www.nobelprize.org/stories/women-who-changed-science/barbara-mcclintock/) | Indexed Nobel text explicitly describes successive maize generations. |
| F04-A3 | Her research showed that some genetic elements could move to different positions within chromosomes. | Index: [S07](https://www.nobelprize.org/stories/women-who-changed-science/barbara-mcclintock/), [S17](https://facultyprofiles.cshl.edu/barbara.mcclintock) | S07 describes transposition within chromosomes; S17 confirms discovery of transposable elements. |
| F04-A4 | Such movement can influence the expression of traits. | Index: [S07](https://www.nobelprize.org/stories/women-who-changed-science/barbara-mcclintock/) | Indexed text links mobile controlling elements to trait expression. |
| F04-A5 | These findings challenged the idea that genetic elements always remain in fixed positions. | Index: [S07](https://www.nobelprize.org/stories/women-who-changed-science/barbara-mcclintock/) | Indexed text contrasts mobility with the former fixed-position picture; not a claim that all genes move. |
| F04-A6 | McClintock received the Nobel Prize in Physiology or Medicine in 1983. | Page: [S17](https://facultyprofiles.cshl.edu/barbara.mcclintock) | Institutional profile records Physiology or Medicine 1983. |
| F05-A1 | Niels Bohr worked on atomic structure and the radiation emitted by atoms. | Page: [S18](https://nbi.ku.dk/english/www/niels/bohr/bohratomet/), [S20](https://nbi.ku.dk/english/www/niels/bohr/nobelprisen/) | Model and radiation narrative, plus Nobel award context, support public atomic-physics work. |
| F05-A2 | In 1913 he proposed a model of the hydrogen atom. | Page: [S18](https://nbi.ku.dk/english/www/niels/bohr/bohratomet/) | 1913 papers and hydrogen spectrum are explicit. |
| F05-A3 | In that model electrons occupy prescribed energy states, and a transition to a lower energy releases radiation. | Index: [S08](https://www.nobelprize.org/prizes/physics/1922/bohr/facts/), [S18](https://nbi.ku.dk/english/www/niels/bohr/bohratomet/) | S08 explicitly states emission on a downward energy transition; S18 corroborates allowed orbits and radiation transitions. |
| F05-A4 | The model helped explain distinct wavelengths in atomic light. | Page: [S18](https://nbi.ku.dk/english/www/niels/bohr/bohratomet/) | Balmer’s hydrogen spectrum is tied to Bohr’s theoretical prediction; bounded to the historical model. |
| F05-A5 | Bohr directed an institute for theoretical physics in Copenhagen. | Page: [S19](https://nbi.ku.dk/english/www/institute/history/history/) | Institution’s history describes Bohr establishing and defining the institute’s activities; this supports the general leadership statement. |
| F05-A6 | He received the Nobel Prize in Physics in 1922. | Page: [S20](https://nbi.ku.dk/english/www/niels/bohr/nobelprisen/) | Opening paragraph records the 1922 Nobel Prize in Physics. |
| F06-A1 | Rabindranath Tagore wrote poetry, songs, stories and plays. | Index: [S09](https://www.nobelprize.org/prizes/literature/1913/tagore/facts/) | Indexed official Facts text lists poetry, songs, stories and drama. |
| F06-A2 | He originally wrote in Bengali and later recast poetry in English, reaching additional readers. | Index: [S09](https://www.nobelprize.org/prizes/literature/1913/tagore/facts/) | Indexed official text explicitly states Bengali originals and English recasting. |
| F06-A3 | His work also addressed philosophy and social questions. | Index: [S09](https://www.nobelprize.org/prizes/literature/1913/tagore/facts/) | Indexed official text names philosophy and social issues. |
| F06-A4 | In 1901 he founded an experimental school at Shantiniketan, aiming to bring Indian and Western learning traditions together. | Aim clarified; date supported: [S09](https://www.nobelprize.org/prizes/literature/1913/tagore/facts/), [S21](https://www.visvabharati.ac.in/history.html), [S22](https://www.visvabharati.ac.in/home/wp-content/uploads/2026/03/AboutVB.pdf) | 1901 and Shantiniketan are supported directly. Nobel S09 describes an attempt/aim to blend traditions, so the outcome-sounding wording was narrowed. Shantiniketan/Santiniketan are spelling variants; 1901 is the school, not the later university. |
| F06-A5 | Tagore received the Nobel Prize in Literature in 1913. | Page: [S22](https://www.visvabharati.ac.in/home/wp-content/uploads/2026/03/AboutVB.pdf) | University history PDF page 1 records the 1913 Literature award. |
| F07-A1 | Wangari Maathai worked in Kenya on environmental protection and public life. | Page: [S23](https://www.greenbeltmovement.org/wangari-maathai/), [S24](https://www.greenbeltmovement.org/history/) | Kenyan context, environmental conservation and public/civic work are documented. |
| F07-A2 | She had academic training in biology. | Page: [S23](https://www.greenbeltmovement.org/wangari-maathai/) | Biological Sciences degree and later study are documented. |
| F07-A3 | In 1977 she started the Green Belt Movement, encouraging women to plant trees in local communities. | Page: [S24](https://www.greenbeltmovement.org/history/), [S25](https://www.greenbeltmovement.org/taking-root-documentary/) | S24 dates the movement’s founding to 1977; S25 explicitly describes encouraging rural women to plant trees. |
| F07-A4 | The movement responded to deforestation and linked ecological work with wider social concerns. | Page: [S24](https://www.greenbeltmovement.org/history/) | Deforestation and wider social/political concerns are described. |
| F07-A5 | Maathai received the Nobel Peace Prize in 2004. | Page: [S23](https://www.greenbeltmovement.org/wangari-maathai/) | Biography identifies the 2004 Nobel Peace Prize. |
| F08-A1 | Santiago Ramón y Cajal investigated the structure of the nervous system. | Page: [S26](https://www.csic.es/en/cajal-legacy) | Scientific legacy describes microscopic anatomy of the nervous system. |
| F08-A2 | He used staining methods to make nerve cells visible for study. | Page: [S26](https://www.csic.es/en/cajal-legacy) | Preserved stained slides and Golgi method are described. |
| F08-A3 | His account treated neurons as distinct cells that contact one another, rather than as one continuous network of cell material. | Page: [S26](https://www.csic.es/en/cajal-legacy) | Individual entities and contact rather than continuity are explicit, attributed to Cajal’s account. |
| F08-A4 | He used and developed methods associated with Camillo Golgi. | Index: [S11](https://www.nobelprize.org/stories/cells-nerves-genes/), [S12](https://www.nobelprize.org/uploads/2018/06/cajal-lecture.pdf) | S11 says Golgi and Cajal used/refined staining; S12 indexed lecture opening confirms use. Full lecture not appraised. |
| F08-A5 | Cajal and Golgi shared the Nobel Prize in Physiology or Medicine in 1906. | Index: [S11](https://www.nobelprize.org/stories/cells-nerves-genes/), [S26](https://www.csic.es/en/cajal-legacy) | S11’s 1906 nervous-system timeline explicitly names both laureates and category; S26 corroborates Cajal’s award. |

## Ordinary keys and distractors

All 48 item records, including every four-option distractor set, appear in the JSON. Baseline field examples are supported but nonexhaustive; a signed synonym/codebook policy remains pending. Award-year/category learning keys match their dossiers. All eight delayed-recognition historical keys are correct, subject to FC04’s rank shortcut.

| Figure | Fictional-inference key | Why other choices do not follow |
| --- | --- | --- |
| F01 | Sample Q is labelled blue. | Converse fails if a blue sample is outside L; exclusivity and uniqueness fail if another blue sample exists. |
| F02 | 5 units | 3, 11 and 8 do not satisfy the specified subtraction. |
| F03 | Model K cannot be in cabinet R. | Red need not imply R; blue is not specified; K in R contradicts the necessary condition. |
| F04 | At least one dry packet is in drawer B. | Allow one wet packet in B and a dry packet elsewhere; premises do not force B to contain all/only dry packets or A to contain none. |
| F05 | 5 units | 4, 9 and 13 do not equal the emitted difference. |
| F06 | The premises do not establish whether W belongs to P. | Both W in P and W outside P fit the premises. Neither membership, exclusion, nor all poems in P is entailed. |
| F07 | 10 | 2, 24 and 6 are not the sum of the specified disjoint groups. |
| F08 | Slide Z cannot be in box N. | N may contain another stained slide; not every stained slide need be in N; Z in N contradicts the premise. |

Recall distractors are nonanswers to the specified passage, not assertions that a person never studied another subject. In particular, Hodgkin’s other vitamin options are simply absent from this passage; Maathai’s constructed movement names are not represented as a verified list of nonexistent organizations. Inference items remain simple and unvalidated for difficulty/ceiling effects.

## Source access and provenance

Original 18 October access dates, locators, summaries, pending independence and rights statuses remain intact. New `ai_assisted_check` fields record this pass without promoting those statuses. S04’s shell is not accepted as award evidence; S15 supplies the accessible award corroboration. S09 does include the 1901 school date in indexed text, so no unsupported-date allegation is made. Its malformed-looking historical locator remains in the history; the canonical URL and new S21/S22 records provide review routes.

| Sources | Current inspection | Remaining limit |
| --- | --- | --- |
| S01, S02, S03, S05–S12 | Canonical URL returned 403 | Body not verified through direct open; claim-specific indexed support is recorded where actually found. |
| S04 | Page shell, no award payload | Not proof of the title, award year or recipient; use S15. |
| Seven distinct alternative locators | 403 | Retained as historical retrieval metadata, not preferred new citations. |
| S13–S26 | Relevant body text retrieved | AI-assisted institutional corroboration only; no rights clearance. S22 is PDF text extraction; S14 is catalogue metadata, not an imported image. |

- **S13** [L’héritage de Marie Curie, perpétuer l’esprit d’une pionnière](https://curie.fr/lheritage-de-marie-curie-perpetuer-lesprit-dune-pionniere) — Institut Curie. Sections Une femme d’exception and La découverte de la radioactivité; Warsaw/Paris, Sorbonne, joint element research. Do not infer a professorship appointment date from this dossier.
- **S14** [Prix Nobel de chimie décerné à Marie Curie, 1911](https://curiotheque.musee.curie.fr/s/fr/item/15332) — Musée Curie. Catalogue record MCP141: award identity, Chemistry and 1911; metadata inspected, image not reproduced.
- **S15** [C.V. Raman The Raman Effect - Landmark](https://www.acs.org/education/whatischemistry/landmarks/ramaneffect.html) — American Chemical Society / Indian Association for the Cultivation of Science landmark. Raman Measures the Effect of Light Scattering; Physicist’s Tool; Biography; 1930 Physics award. The indexed S05 passage supplies the explicit monochromatic/frequency formulation.
- **S16** [Modelling the Structure of Penicillin](https://www.mhs.ox.ac.uk/backfromthedead/exhibition/the-structure-of-penicillin/index.html) — University of Oxford, Museum of the History of Science. Model and atom-position discussion; penicillin, vitamin B12, insulin; Chemistry 1964. Insulin structure dated 1969, after the award.
- **S17** [Barbara McClintock | About](https://facultyprofiles.cshl.edu/barbara.mcclintock) — Cold Spring Harbor Laboratory. BIO: cytogenetics, maize, transposable elements and Physiology or Medicine 1983. Profile text was readable despite a generic JavaScript warning.
- **S18** [Bohr’s atomic model](https://nbi.ku.dk/english/www/niels/bohr/bohratomet/) — Niels Bohr Institute, University of Copenhagen. Atomic-model narrative: discrete orbits, radiation transitions, Balmer/hydrogen spectrum, three 1913 papers.
- **S19** [The establishment of an institute](https://nbi.ku.dk/english/www/institute/history/history/) — Niels Bohr Institute, University of Copenhagen; Finn Aaserud, Niels Bohr Archive. Bohr’s role in establishing and defining the Copenhagen theoretical-physics institute; 1921 opening.
- **S20** [The Nobel Prize](https://nbi.ku.dk/english/www/niels/bohr/nobelprisen/) — Niels Bohr Institute, University of Copenhagen. Opening award paragraph: Bohr’s 1922 Nobel Prize in Physics. Other anecdotes on page outside scope.
- **S21** [History](https://www.visvabharati.ac.in/history.html) — Visva-Bharati. Opening history: Tagore’s school at Santiniketan formally began 22 December 1901. No claim that university inauguration occurred in 1901.
- **S22** [Santiniketan & Visva-Bharati: A Brief History](https://www.visvabharati.ac.in/home/wp-content/uploads/2026/03/AboutVB.pdf) — Visva-Bharati. PDF page 1, Brahmacharyashrama section: 1901 school and 1913 Literature award; later international educational aspirations. Text extraction inspected, not a complete scholarly appraisal.
- **S23** [Wangari Maathai](https://www.greenbeltmovement.org/wangari-maathai/) — Green Belt Movement. Biography: Kenyan background, biological-science education, movement founder, 2004 Nobel Peace Prize.
- **S24** [History](https://www.greenbeltmovement.org/history/) — Green Belt Movement. Our History and Our Journey of Empowerment: 1977 founding, rural Kenyan women, environment and social/political concerns.
- **S25** [Taking Root Documentary](https://www.greenbeltmovement.org/taking-root-documentary/) — Green Belt Movement. Institutional synopsis below newsletter form: 1977 encouragement of rural women’s tree planting; environment and rights. Film itself not viewed.
- **S26** [The Cajal Legacy](https://www.csic.es/en/cajal-legacy) — Spanish National Research Council (CSIC). Opening scientific legacy; individual neurons, contact versus continuity, preserved Golgi-stained slides, 1906 Physiology or Medicine award. No images imported.

## Preserved boundaries and handoff

The original [18 October manifest](history/manifest-2026-10-18.json) is preserved byte for byte; [the current manifest](manifest.json) binds this editorial revision. Historical evidence and validation files remain unchanged. No source text, image or full document was imported for redistribution, and no source publisher endorsement is implied.

All independent stimulus, methods, statistics, ethics, cultural/accessibility and security reviews remain open. No human reviewer has signed off, no participant work or concealed assignments were created, and no registration, acquisition implementation, website publication, merge or evidence promotion occurred. The source-linked corrections are candidate authoring work only. PR #405 must remain draft and unsuitable for participant use.

The next stimulus reviewer should resolve FC04, approve the frozen free-response codebook, inspect the indexed-only statements against accessible originals or signed acceptable alternatives, and record source/rights dispositions against the corrected hashes. Broader statistical, ethical and implementation requirements remain in the separate [review packet](../review/review-packet.md).
