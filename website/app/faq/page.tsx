import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Frequently Asked Questions — AKASHICNET.ORG",
  description: "Clear answers about AkashicNET, AkashicOMNI, AkashicPRISM, evidence, privacy, cultural respect and human–AI collaboration.",
};

const faqGroups = [
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
        question: "Is AkashicNET just “AI slop”?",
        answer: "No. Its present outputs rest on human-led curation and community work accumulated since r/NeuronsToNirvana was created in March 2022. AI can accelerate drafting, retrieval and formalisation, but it did not create that history, choose the project’s values or replace editorial judgement. Quality is demonstrated through provenance, dated records, corrections, evidence labels and review—not by pretending AI was absent.",
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
        question: "Does PRISM treat every worldview as equally true?",
        answer: "No. PRISM represents perspectives fairly without flattening their differences. Inclusion is not verification, and respectful comparison is not a claim that distinct traditions describe the same reality.",
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
        question: "Does quantum physics prove consciousness creates reality?",
        answer: "No. Quantum theory raises profound questions about measurement, information and reality, but it does not by itself demonstrate telepathy, astral travel, survival after death or an intelligent Akashic field. Such connections must remain clearly labelled hypotheses or metaphors unless supported by specific evidence.",
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
        question: "How is Indigenous and traditional knowledge treated?",
        answer: "Each tradition should retain its own people, language, place, lineage, authority and sharing restrictions. Public, protected and restricted knowledge are not interchangeable. Cross-tradition similarities require sources, differences and a clear non-equivalence note.",
      },
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
        <p>Plain answers about what AkashicNET is building, how it handles extraordinary questions and where evidence, experience and interpretation remain distinct.</p>
      </section>

      <section className="faq-directory" aria-label="Frequently asked questions">
        {faqGroups.map((group) => (
          <section className="faq-group" key={group.label}>
            <p className="section-label">{group.label}</p>
            <div className="faq-list">
              {group.items.map((item, index) => (
                <details className="faq-item" key={item.question} open={group === faqGroups[0] && index === 0}>
                  <summary>{item.question}<span aria-hidden="true">+</span></summary>
                  <p>{item.answer}</p>
                </details>
              ))}
            </div>
          </section>
        ))}
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
