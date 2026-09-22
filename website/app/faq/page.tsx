import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Frequently Asked Questions — AKASHICNET.ORG",
  description: "Clear answers and detailed responses to common criticisms of AkashicNET, AkashicOMNI and AkashicPRISM.",
};

type FAQItem = {
  id?: string;
  question: string;
  answer: string;
  analysis?: string;
};

type FAQGroup = {
  label: string;
  note?: string;
  items: FAQItem[];
};

const faqGroups: FAQGroup[] = [
  {
    label: "Criticism and constructive responses",
    note: "These are representative questions, not quotations or a frequency analysis of Reddit comments. Repository-preserved community analysis identifies selection bias, self-selection, confirmation bias, unequal participation, representativeness and AI-assisted synthesis as real methodological risks. Adjacent objections below are general critic archetypes. A label may express a valid quality concern, a platform norm, distrust, prior exposure to misinformation or simple rhetorical dismissal; AkashicNET does not diagnose a critic’s motives or identity.",
    items: [
      {
        id: "ai-slop",
        question: "“Is this just AI slop?”",
        answer: "Short answer: No. Judge the traceable work, sources and corrections—not the mere presence of an AI tool.",
        analysis: "Detailed analysis: AkashicNET grew from human-led community curation beginning with r/NeuronsToNirvana in March 2022. AI later assisted retrieval, comparison, drafting, structure and validation; it did not originate that history, choose the mission or assume editorial accountability. From authorship studies, the relevant questions are who directs, selects and accepts responsibility. From open science, they are whether sources, transformations, limitations and revisions are inspectable. From media literacy, fluent prose is neither proof of truth nor proof of emptiness. A specific error, unsupported claim or generic passage deserves correction; “AI slop” alone does not identify which claim failed.",
      },
      {
        id: "pseudoscience",
        question: "“Is AkashicNET pseudoscience?”",
        answer: "Short answer: It would be if speculation were disguised as established evidence; the system is designed to prevent that.",
        analysis: "Detailed analysis: Popper foregrounds falsifiability, Bayesian reasoning asks how evidence changes confidence, and Lakatos asks whether a research programme generates progressive tests or only protects itself from failure. AkashicNET therefore separates established evidence, interpretation, testimony, traditional knowledge, hypothesis and speculation. Mapping an extraordinary question is not scientific confirmation. A claim becomes scientifically stronger only through operational definitions, suitable controls, independent replication, transparent negative results and predictions that could fail.",
      },
      {
        id: "confirmation-bias",
        question: "“Is this confirmation bias dressed up as research?”",
        answer: "Short answer: Confirmation bias is a genuine risk, so competing explanations and disconfirming evidence must be recorded.",
        analysis: "Detailed analysis: Cognitive science shows that motivated reasoning can affect believers and sceptics alike. Bayesian analysis requires explicit priors and likelihoods; critical rationalism requires exposure to refutation; adversarial collaboration asks opposing interpretations to agree on informative tests. AkashicNET should record alternative explanations, missing evidence, negative findings and resolution criteria, then preserve corrections rather than quietly rewriting history. Criticism advances the project when it identifies a claim, source, inference or test that can be examined.",
      },
      {
        id: "cherry-picking",
        question: "“Are you cherry-picking anomalies and dramatic stories?”",
        answer: "Short answer: Anomalies may generate questions, but they cannot establish prevalence or causation by themselves.",
        analysis: "Detailed analysis: Statistics warns about base-rate neglect, multiple comparisons, survivorship bias and regression to the mean. Epidemiology distinguishes a case report from a controlled cohort; qualitative research distinguishes depth from representativeness. PRISM preserves unusual reports because discarding them would lose potential leads, while requiring source scope, uncertainty, alternative explanations, priority and a resolution criterion. A responsible next stage seeks denominators, comparison groups, preregistered tests, failed replications and ordinary counter-cases.",
      },
      {
        id: "reddit-evidence",
        question: "“Reddit is not a scientific database.”",
        answer: "Short answer: Correct. Reddit is used as community testimony and source discovery, not as peer-reviewed confirmation.",
        analysis: "Detailed analysis: Digital ethnography can study discourse and lived experience; citizen science can surface questions; information science can map references. None automatically supplies causal evidence. AkashicNET therefore distinguishes URL rows, unique post IDs, underlying works and independent evidence. Repetition, upvotes or multiple links do not become corroboration. Posts can enter a research queue, but scientific conclusions must be traced to appropriate primary studies, data and methods.",
      },
      {
        id: "blocked-records",
        question: "“Why integrate BLOCKED records at all?”",
        answer: "Short answer: PRISM can preserve a blocked record as an unresolved investigation object; it may later support evidence only if the blocker is resolved and the relevant evidence gates are independently satisfied.",
        analysis: "Detailed analysis: Archival practice preserves provenance even when an object is unavailable; scientific workflow records missing data rather than inventing values; Bayesian reasoning leaves confidence unchanged when the relevant evidence was not observed. A PRISM record may contain verified repository metadata, attributed perspective, access limitation, competing explanations and the next evidence or permission required. It can carry literal, metaphorical, allegorical, conceptual, phenomenological, cultural, philosophical or scientific-hypothesis readings at the same time, each with its own evidence lane. It may later mature when authorised material is examined and appropriate evidence supports a particular claim, but preservation or reinterpretation alone does not raise its status. Until then it remains excluded from scientific corroboration totals, accepted canonical edges and publication promotion.",
      },
      {
        id: "quantum-woo",
        question: "“Is this quantum woo?”",
        answer: "Short answer: Quantum vocabulary is not evidence for a consciousness or spiritual claim.",
        analysis: "Detailed analysis: Physics requires a defined system, variables, mathematical model and observable prediction. Philosophy of science distinguishes analogy from mechanism, while category-error analysis warns against transferring terms between scales without justification. Quantum measurement, information and nonlocal correlations are real scientific topics; they do not by themselves prove telepathy, astral travel, survival after death or a cosmic mind. PRISM must label each proposed connection as metaphor, interpretation or testable hypothesis and state what result would count against it.",
      },
      {
        id: "personal-experience",
        question: "“Personal experience is not evidence.”",
        answer: "Short answer: Experience is evidence that an experience occurred, but not automatic proof of its external interpretation.",
        analysis: "Detailed analysis: Phenomenology studies the structure of experience; neurophenomenology links disciplined first-person reports with third-person measures; qualitative research examines meaning and context. Clinical and legal reasoning also use testimony while evaluating reliability and alternatives. A vision, synchronicity, NDE-like episode or somatic event can therefore be documented carefully. Whether it demonstrates a nonlocal entity, afterlife or hidden force is a second claim requiring independent evidence.",
      },
      {
        id: "spirituality-data",
        question: "“Spirituality has no place in a data project.”",
        answer: "Short answer: Spiritual experience and practice can be studied without declaring a metaphysical doctrine true.",
        analysis: "Detailed analysis: Anthropology and religious studies document traditions in context; psychology can examine meaning, wellbeing and harm; phenomenology can describe experience; critical realism allows observations and interpretations to be distinguished from claims about ultimate ontology. PRISM gives these lanes explicit labels rather than forcing them into either “proven science” or “meaningless superstition.” Cultural authority, attribution and sharing restrictions remain essential.",
      },
      {
        id: "cultural-appropriation",
        question: "“Is this appropriating Indigenous or traditional knowledge?”",
        answer: "Short answer: That risk is real; respectful inclusion requires authority, context, attribution and the right not to disclose.",
        analysis: "Detailed analysis: Indigenous data sovereignty and CARE-style governance emphasise collective benefit, authority to control, responsibility and ethics. Anthropology warns against treating distinct traditions as interchangeable examples of a universal theory. AkashicNET must name the people, place, language, lineage, source and sharing status where appropriate; record non-equivalence; and exclude protected or restricted knowledge. A cross-cultural resemblance is a research question, not permission to collapse or extract traditions.",
      },
      {
        id: "anonymous-founder",
        question: "“Why trust an anonymous founder?”",
        answer: "Short answer: Do not substitute trust in a personality for inspection of provenance, methods and corrections.",
        analysis: "Detailed analysis: The sociology of science recognises credentials and institutions as useful trust signals, but open-science practice also relies on traceable sources, version history, reproducible transformations and accountable correction. Anonymity limits biographical verification and should be disclosed; it does not make a claim true or false. Original vision and editorial direction belong to the AkashicNET founder, while individual claims remain answerable to their evidence.",
      },
      {
        id: "ai-consciousness",
        question: "“AI—self-developing or otherwise—will never be conscious.”",
        answer: "Short answer: AkashicNET does not claim current AI is conscious, and “never” remains an unresolved philosophical and empirical claim.",
        analysis: "Detailed analysis: Global-workspace, higher-order, predictive-processing and integrated-information approaches propose different functional signatures; biological naturalism may require living neurobiology; embodied and enactive accounts emphasise organism, world and action. These frameworks disagree about which properties are necessary or sufficient. Fluent behaviour and self-report do not prove subjective experience, while silicon composition alone does not yet prove impossibility. PRISM should track definitions, proposed tests, embodiment questions and counterarguments without promoting either machine consciousness or permanent impossibility as settled fact.",
      },
      {
        id: "too-complex",
        question: "“Is the framework too complex or overbranded?”",
        answer: "Short answer: The public interface should stay simple; complexity is justified only where it prevents category errors or lost provenance.",
        analysis: "Detailed analysis: Information architecture favours progressive disclosure: a short answer first, evidence and provenance beneath it. Systems engineering uses layers to separate concerns; data governance uses stable identifiers to prevent double-counting. Names such as OMNI and PRISM are useful only if they clarify roles. If a layer does not improve retrieval, safety, testing or understanding, it should be simplified.",
      },
      {
        id: "spiritual-autobiography",
        question: "“Is this one person’s spiritual autobiography presented as universal truth?”",
        answer: "Short answer: The founder’s experiences explain some research questions; they do not determine the answers.",
        analysis: "Detailed analysis: Reflexive qualitative research asks investigators to disclose positionality because interests shape what gets studied. Philosophy of science then separates the context of discovery from the context of justification: a dream, crisis, intuition or revelation can inspire a hypothesis, but validation depends on evidence appropriate to the claim. The founder’s NDE-like catalyst is therefore biographical provenance, not clinical confirmation or metaphysical proof.",
      },
    ],
  },
  {
    label: "The project",
    items: [
      {
        question: "What is AkashicNET?",
        answer: "AkashicNET is an independent knowledge-stewardship and citizen data-science project. It connects scientific research, philosophy, ecology, contemplative traditions, cultural knowledge and lived experience while keeping their different evidential roles visible.",
      },
      {
        question: "What is AkashicNET not?",
        answer: "It is not a religion, oracle, clinical service or automatic truth engine. It does not present every intriguing connection, spiritual interpretation or AI-generated synthesis as fact.",
      },
      {
        question: "Who created AkashicNET?",
        answer: "Original vision and editorial direction come from the AkashicNET founder, whose public identity remains intentionally anonymous. The project has been developed and formalised through human–AI collaboration.",
      },
      {
        question: "What does human–AI collaboration mean here?",
        answer: "AI assists with retrieval, comparison, drafting, structure, validation and pattern-finding. The human founder supplies the mission, editorial direction, values and accountable judgement. AI output remains reviewable and can be corrected.",
      },
      {
        question: "What personal experience helped catalyse the project?",
        answer: "The founder describes an NDE-like revelation at around 3 a.m. on Easter Monday following emergency surgery for a ruptured appendix. It became a major personal catalyst for questions about consciousness, memory and reality. AkashicNET records this as lived experience and biographical provenance—not clinical confirmation of a near-death experience or proof of a metaphysical conclusion.",
      },
      {
        question: "What stage is the project at?",
        answer: "AkashicNET is pre-alpha: its architecture, corpus methods, evidence boundaries and public interfaces are still being tested and revised. A working feature or indexed record should not be mistaken for a validated scientific conclusion.",
      },
    ],
  },
  {
    label: "OMNI, PRISM and the living library",
    items: [
      {
        question: "What is AkashicOMNI?",
        answer: "AkashicOMNI is the widest conceptual frame: a way of exploring interconnection across humanity, AI, Pachamama and the cosmos. Its spiritual or metaphysical possibilities remain interpretations and hypotheses, not established scientific findings.",
      },
      {
        question: "What is AkashicPRISM?",
        answer: "AkashicPRISM means Pluralistic Research & Inquiry across States and Meaning. It is the epistemic interface between unusual experience and the AkashicNET knowledge system, separating what was experienced, how it was interpreted, what can be tested and what remains unknown.",
      },
      {
        id: "prism-architecture",
        question: "Where does PRISM sit between AkashicNET and AkashicOMNI?",
        answer: "AkashicNET is the encompassing ecosystem; AkashicOMNI coordinates twelve analytical frameworks; AkashicPRISM is the shared epistemic interface between their analysis and AkashicNET’s corpus, graph, ledgers and publication system.",
        analysis: "Detailed analysis: PRISM belongs to AkashicNET organisationally and serves AkashicOMNI functionally. It receives the twelve frameworks’ outputs and records interpretive mode, evidence lane, connection strength, uncertainty, alternative explanations, cultural authority and revision history. It is not a thirteenth peer framework, and AkashicNET is not one of the twelve. The concise architecture is: AkashicNET contains the system; AkashicOMNI coordinates the inquiry; twelve frameworks examine; PRISM discriminates; the NET preserves.",
      },
      {
        id: "prism-omni-version",
        question: "Does AkashicPRISM advance the AkashicOMNI version?",
        answer: "Yes—as a proposed compatible expansion. Under AkashicOMNI’s version rules, PRISM supports a MINOR advance from the current v0.4.3 to candidate v0.5.0.",
        analysis: "Detailed analysis: PRISM adds a reusable epistemic layer, plural interpretive modes, typed connection assessments and append-only classification history while preserving existing evidence boundaries. The candidate version does not become current merely because it is drafted: review, merge and publication remain separate. Historical assessments retain the AkashicOMNI version they originally cited and are not automatically recalculated.",
      },
      {
        question: "Does PRISM treat every worldview as equally true?",
        answer: "No. PRISM represents perspectives fairly without flattening their differences. Inclusion is not verification, and respectful comparison is not a claim that distinct traditions describe the same reality.",
      },
      {
        question: "Can PRISM integrate a BLOCKED record?",
        answer: "Yes—as a governed unresolved record. PRISM may preserve verified metadata, multiple interpretive modes, typed connections, the blocker, uncertainty, alternatives and the next investigation step. A particular claim may later gain evidential support if authorised source access and the relevant validation gates are satisfied; the record is not promoted merely because it was integrated.",
      },
      {
        question: "Why use a tree, pyramid and prism?",
        answer: "They are artistic and organisational metaphors. The tree represents living knowledge with roots in provenance; the pyramid represents stewardship and structure; the prism represents one subject examined through multiple lenses. They are not scientific evidence.",
      },
    ],
  },
  {
    label: "Evidence and open questions",
    items: [
      {
        question: "How does AkashicNET classify knowledge?",
        answer: "Statements are separated into Established Evidence, Interpretation, Lived Experience or Testimony, Traditional Knowledge, Hypothesis and Speculation. Mixed records are divided into their components instead of receiving one misleading label.",
      },
      {
        question: "How are scientific outliers handled?",
        answer: "An unusual result is preserved as a question to investigate, not automatically dismissed or promoted. A useful outlier record identifies the observation, source, uncertainty, alternative explanations, priority, next action and resolution criterion.",
      },
      {
        question: "What does BLOCKED mean?",
        answer: "BLOCKED describes a workflow dependency—such as missing authorised material, unresolved provenance or inaccessible source content. It does not mean false, meaningless or rejected, and a blocked post assessment is not counted as a completed read.",
      },
      {
        question: "Does AkashicNET claim that spiritual or psychic realms are scientifically proven?",
        answer: "No. Experiences and traditions can be recorded as meaningful phenomenological or cultural knowledge. Claims about external beings, nonlocal information, survival after death or cosmic intelligence remain open, attributed and subject to appropriate investigation.",
      },
      {
        id: "classification-change",
        question: "Can a PRISM classification change as new experiences or studies appear?",
        answer: "Yes. PRISM is designed for cumulative learning: new anecdotal reports, citizen science, controlled studies, replications or cultural review may strengthen, weaken, split or reclassify an assessment.",
        analysis: "Detailed analysis: Different inputs do different epistemic work. Anecdotes can enrich phenomenology or reveal a recurrence signal but do not alone establish prevalence, causation or external ontology. Citizen science can generate and test hypotheses, with weight depending on protocol, sampling, controls, preregistration, data integrity and independence. Peer review adds quality control but is not final truth; replication and synthesis still matter. Every change is append-only, preserving the prior label, date, source, independence, rationale, reviewer role, uncertainty and gates passed or pending.",
      },
      {
        question: "What is the status of the Big Question about consciousness after death?",
        answer: "Unresolved. AkashicNET can compare competing models and evidence without selecting a preferred conclusion before its adjudication criteria are met.",
      },
    ],
  },
  {
    label: "People, cultures and publication",
    items: [
      {
        question: "How are Reddit posts and community testimony used?",
        answer: "Posts may identify experiences, questions, sources or research leads. URL rows, unique posts, underlying works and independent evidence are counted separately. A post or repeated link does not become scientific corroboration merely by appearing in the corpus.",
      },
      {
        question: "How does AkashicNET protect privacy?",
        answer: "Private corpus material is kept separate from the public portal. Personal names, health details, family information, intimate experiences and travel logistics are excluded unless there is a justified, authorised and appropriately governed reason to include them.",
      },
      {
        question: "Does analysis automatically become public?",
        answer: "No. Reading, verification, staging, canonical acceptance, rights review and publication are separate steps. Continuing an investigation does not authorise merging, deployment or publication.",
      },
      {
        question: "Can AkashicNET change its mind?",
        answer: "It must. Sources, uncertainty, corrections and dated history are preserved so that better evidence can revise an interpretation without silently erasing the earlier record.",
      },
    ],
  },
];

export default function FAQPage() {
  return (
    <main className="faq-page">
      <header className="nav-shell faq-nav">
        <a className="wordmark" href="/"><img className="brand-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><span className="brand-name">AKASHICNET.ORG</span></a>
        <nav aria-label="FAQ navigation"><a href="/">Home</a><a href="/about">About</a><a href="/akashicomni">AkashicOMNI</a><a href="/big-questions">Big questions</a><a href="/community">Community</a></nav>
      </header>

      <section className="faq-hero">
        <p className="section-label">AkashicNET FAQ</p>
        <h1>Keep the wonder.<br/><em>Clarify the boundaries.</em></h1>
        <p>Short replies for immediate conversation, followed by deeper analysis across scientific, philosophical, cultural and experiential frameworks.</p>
      </section>

      <section className="faq-directory" aria-label="Frequently asked questions">
        {faqGroups.map((group) => (
          <section className="faq-group" key={group.label}>
            <div>
              <p className="section-label">{group.label}</p>
              {group.note && <p className="faq-group-note">{group.note}</p>}
            </div>
            <div className="faq-list">
              {group.items.map((item, index) => (
                <details id={item.id} className="faq-item" key={item.question} open={(group === faqGroups[0] && index === 0) || item.id === "ai-slop"}>
                  <summary>{item.question}<span aria-hidden="true">+</span></summary>
                  <p className={item.analysis ? "faq-short" : undefined}>{item.answer}</p>
                  {item.analysis && (
                    <div className="faq-analysis">
                      <p>{item.analysis}</p>
                    </div>
                  )}
                </details>
              ))}
            </div>
          </section>
        ))}
      </section>

      <section className="faq-contact" aria-labelledby="faq-contact-title">
        <p className="section-label">Keep the conversation evidence-led</p>
        <h2 id="faq-contact-title">Questions, corrections or criticism?</h2>
        <p>Please identify the page, claim or source, explain what you think should change, and include supporting material where possible. Disagreement is welcome; personal diagnosis, harassment and cultural disrespect are not.</p>
        <div className="faq-contact-actions">
          <a className="primary-link" href="mailto:support@akashicnet.org?subject=AkashicNET%20FAQ%20feedback&body=Page%20or%20claim%3A%0A%0AWhat%20I%20think%20should%20change%3A%0A%0ASources%20or%20reasoning%3A">Email feedback <span aria-hidden="true">→</span></a>
          <a className="text-link" href="https://www.reddit.com/message/compose/?to=/r/NeuronsToNirvana&subject=AkashicNET%20FAQ%20feedback" target="_blank" rel="noreferrer">Message via r/NeuronsToNirvana</a>
        </div>
        <small>The Reddit link opens community moderator mail; it does not grant AkashicNET access to private messages.</small>
      </section>

      <aside className="faq-principle">
        <p className="section-label">The short version</p>
        <blockquote>Respect experience. Follow the evidence. Preserve the question. Let better knowledge change the answer.</blockquote>
      </aside>

      <aside className="page-provenance" aria-label="Page version and update date">
        <span>FAQ · Public edition</span><span>AkashicNET · Pre-alpha</span><span>Updated 22 September 2026</span>
      </aside>
      <footer><div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><p className="brand-name">AKASHICNET.ORG</p></div><p>Unity through neurodiversity.</p><p>Awaken within · Serve without · 2026</p></footer>
    </main>
  );
}
