import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "The Power of the Doctor · HOMESENSE VR — AKASHICNET.ORG",
  description:
    "A Spiritual Sci-Fi exploration of regeneration, resurrection, reincarnation and continuity through the speculative HOMESENSE VR concept.",
};

const shell = { width: "min(1160px, calc(100% - 32px))", margin: "0 auto" };
const panel = {
  border: "1px solid rgba(216,185,92,.24)",
  borderRadius: 24,
  background: "linear-gradient(145deg, rgba(19,25,47,.94), rgba(8,12,28,.96))",
  boxShadow: "0 24px 80px rgba(0,0,0,.28)",
};

const models = [
  {
    title: "Regeneration",
    source: "Doctor Who",
    continuity: "One continuing being changes body and personality while retaining an accumulated history.",
    question: "How much can change before identity becomes someone new?",
  },
  {
    title: "Resurrection",
    source: "Battlestar Galactica",
    continuity: "A Cylon identity-pattern is transferred into another prepared biological body.",
    question: "Is the awakened being the original consciousness, a continuation or a copy?",
  },
  {
    title: "Reincarnation",
    source: "Religious and philosophical traditions",
    continuity: "Different traditions propose karmic, mental or spiritual continuity across lives, often without ordinary autobiographical recall.",
    question: "What, if anything, must persist for rebirth to count as continuity?",
  },
];

const chambers = [
  ["01 · The Edge", "Encounter former versions of the self as guides. Integrate what they remember without treating them as separate, proven souls."],
  ["02 · The Resurrection Tank", "Reconstruct an identity from fragmented memories. A perfect reconstruction still leaves the player asking whether copying equals survival."],
  ["03 · The Reincarnation Field", "Follow recurring symbols and dispositions across imagined lives. The game never declares whether they are memory, karma, archetype or coincidence."],
];

export default function PowerOfTheDoctorPage() {
  return (
    <main style={{ minHeight: "100vh", color: "#f5f0e7", background: "radial-gradient(circle at 50% 15%, #182c59 0, #0a1026 34%, #050711 76%)" }}>
      <header className="nav-shell">
        <a className="wordmark" href="/" aria-label="AkashicNET.org home">
          <img className="brand-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt="" />
          <span className="brand-name">AKASHICNET.ORG</span>
        </a>
        <nav aria-label="Page navigation">
          <a href="/spiritual-sci-fi">Spiritual Sci-Fi</a>
          <a href="#continuity">Three models</a>
          <a href="#experience">VR concept</a>
          <a href="/big-questions/bq001">BQ001</a>
        </nav>
      </header>

      <section style={{ ...shell, padding: "clamp(72px,10vw,130px) 0 54px", textAlign: "center" }}>
        <p className="section-label">SPIRITUAL SCI-FI · CULTURAL INTERPRETATION · FUTURE / EXPLORATORY</p>
        <h1 style={{ margin: "20px auto", maxWidth: 980, fontSize: "clamp(3rem,8vw,7.4rem)", lineHeight: .92 }}>
          The Power<br /><em style={{ color: "#d8b95c" }}>of the Doctor</em>
        </h1>
        <blockquote style={{ maxWidth: 920, margin: "30px auto 0", color: "#f2d98e", fontSize: "clamp(1.25rem,2.8vw,2rem)", lineHeight: 1.45 }}>
          “The mad quantum spacetime traveller with two hearts, trying their best to make the cosmos a slightly nicer place to live, microdosing wonder step by step since 23 November 1963.”
        </blockquote>
        <p style={{ maxWidth: 780, margin: "12px auto 0", color: "#9fa7ba", lineHeight: 1.6 }}>
          “Microdosing wonder” is playful wordplay for encountering the story episode by episode. It is not advice about substance use. Doctor Who first aired on 23 November 1963.
        </p>
        <p style={{ maxWidth: 800, margin: "28px auto 0", fontSize: "clamp(1.1rem,2.2vw,1.45rem)", lineHeight: 1.75, color: "#d7d9e4" }}>
          What science fiction can teach us about continuity when a body, personality or world changes.
          A bridge from regeneration and resurrection to reincarnation, meta-awareness and mettā-awareness.
        </p>
        <div style={{ display: "flex", justifyContent: "center", flexWrap: "wrap", gap: 12, marginTop: 30 }}>
          {["MICRO", "META", "METTĀ", "MACRO"].map((word) => (
            <span key={word} style={{ border: "1px solid rgba(216,185,92,.38)", borderRadius: 99, padding: "9px 16px", color: "#e6ce85", letterSpacing: ".12em", fontWeight: 800 }}>{word}</span>
          ))}
        </div>
      </section>

      <section style={{ ...shell, ...panel, overflow: "hidden", padding: 0 }}>
        <img
          src="/images/homesense-vr-power-of-the-doctor-storyboard.png"
          alt="Six-panel HOMESENSE VR concept storyboard: a traveller enters a small blue portal, puts on a headset inside a spherical chamber, sees sound create cymatic forms, explores a 360-degree neural and cosmic environment, aligns symbols, and returns through a warm doorway marked Home."
          style={{ display: "block", width: "100%", height: "auto" }}
        />
        <p style={{ margin: 0, padding: "18px 22px", color: "#b9bfd0", lineHeight: 1.65 }}>
          <strong style={{ color: "#f3dc96" }}>AkashicNET concept artwork.</strong> A speculative storyboard, not a functioning VR product and not scientific evidence that quantum phenomena, dark matter or post-mortem consciousness can be perceived directly.
        </p>
      </section>

      <section style={{ ...shell, padding: "84px 0 24px" }}>
        <p className="section-label">THE SCENE YOU REMEMBER</p>
        <div style={{ ...panel, padding: "clamp(24px,5vw,52px)", marginTop: 18 }}>
          <h2 style={{ fontSize: "clamp(2rem,5vw,4rem)", marginTop: 0 }}>The Guardians of the Edge</h2>
          <p style={{ color: "#d7d9e4", lineHeight: 1.85, fontSize: "1.08rem" }}>
            In Jodie Whittaker&apos;s final special, <em>The Power of the Doctor</em> (2022), the Master forces the Thirteenth Doctor into regeneration. Within a liminal mental landscape called the Edge, manifestations of earlier Doctors appear as Guardians of the Edge. They represent previous incarnations remaining present within a continuing identity. The Doctor&apos;s actual final regeneration occurs later in the story.
          </p>
          <p style={{ color: "#d7d9e4", lineHeight: 1.85 }}>
            This resembles reincarnation symbolically, but it is not the same claim. <em>Doctor Who</em> presents fictional biological regeneration with unusually strong continuity of memory. The Edge becomes useful here as a cultural thought experiment: <strong>can former selves remain accessible without being separate selves?</strong>
          </p>
          <p style={{ marginBottom: 0 }}>
            <a href="https://www.youtube.com/watch?v=0SuDVcTv25g">Watch the official “Guardians of the Edge” clip ↗</a>
          </p>
        </div>
      </section>

      <section id="continuity" style={{ ...shell, padding: "70px 0 30px" }}>
        <p className="section-label">THREE FICTIONAL AND PHILOSOPHICAL LENSES</p>
        <h2 style={{ maxWidth: 840, fontSize: "clamp(2.2rem,5vw,4.4rem)", lineHeight: 1.05 }}>Three ways to ask what continues.</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))", gap: 18, marginTop: 34 }}>
          {models.map((model) => (
            <article key={model.title} style={{ ...panel, padding: 26 }}>
              <span style={{ color: "#d8b95c", fontWeight: 900, letterSpacing: ".1em" }}>{model.source}</span>
              <h3 style={{ fontSize: "1.7rem", marginBottom: 12 }}>{model.title}</h3>
              <p style={{ color: "#cbd0dd", lineHeight: 1.7 }}>{model.continuity}</p>
              <p style={{ borderTop: "1px solid rgba(216,185,92,.2)", paddingTop: 16, lineHeight: 1.65 }}><strong>Identity puzzle:</strong> {model.question}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="experience" style={{ ...shell, padding: "86px 0 30px" }}>
        <p className="section-label">HOMESENSE VR · PLACEHOLDER CONCEPT</p>
        <h2 style={{ maxWidth: 900, fontSize: "clamp(2.2rem,5vw,4.6rem)", lineHeight: 1.04 }}>
          A confined chamber.<br />An infinite perceptual interior.
        </h2>
        <p style={{ maxWidth: 820, color: "#d7d9e4", fontSize: "1.08rem", lineHeight: 1.85 }}>
          The player enters a TARDIS-like spherical room filled with 360° imagery and spatial sound. Resonant tones produce visible cymatic patterns. Solving puzzles changes scale from quantum possibility to embodied experience to the largely unobserved cosmos. The altered states are simulated through audiovisual design; no substance use is required or depicted.
        </p>
        <div style={{ display: "grid", gap: 16, marginTop: 34 }}>
          {chambers.map(([title, text]) => (
            <article key={title} style={{ ...panel, padding: "24px clamp(22px,4vw,42px)", display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(min(100%,260px),1fr))", gap: 24, alignItems: "start" }}>
              <h3 style={{ margin: 0, color: "#e7cd7e" }}>{title}</h3>
              <p style={{ margin: 0, color: "#cbd0dd", lineHeight: 1.75 }}>{text}</p>
            </article>
          ))}
        </div>
      </section>


      <section style={{ ...shell, padding: "86px 0 24px" }}>
        <p className="section-label">WATCH THE IDEAS</p>
        <h2 style={{ maxWidth: 900, fontSize: "clamp(2.2rem,5vw,4.4rem)", lineHeight: 1.05 }}>Trailers and canonical clips as thought-experiment portals.</h2>
        <p style={{ maxWidth: 840, color: "#d7d9e4", lineHeight: 1.8 }}>
          These links lead to official franchise channels or authorised material. They provide cultural context; their stories and imagery remain the property of their respective rights holders.
        </p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(235px,1fr))", gap: 16, marginTop: 30 }}>
          {[
            ["Doctor Who", "Regeneration trailer · 1m 50s · Everything Is About to Change", "https://www.reddit.com/r/NeuronsToNirvana/comments/yb8fkk/regeneration_trailer_1m50s_everything_is_about_to/"],
            ["Doctor Who", "Guardians of the Edge · official clip", "https://www.youtube.com/watch?v=0SuDVcTv25g"],
            ["Doctor Who", "The crack in time · a new regeneration cycle received through connection", "https://www.reddit.com/r/NeuronsToNirvana/comments/1i2odsm/the_crack_in_time_ms_the_time_of_the_doctor/"],
            ["Doctor Who", "The Thirteenth Doctor regenerates · regeneration sequence", "https://www.reddit.com/r/NeuronsToNirvana/comments/1e15hj6/the_thirteenth_doctor_regenerates_regenerations/"],
            ["Doctor Who", "60th anniversary trailer · destiny, Donna Noble and erased memory", "https://www.reddit.com/r/NeuronsToNirvana/comments/16txyk3/official_trailer_2m37s_i_dont_believe_in_destiny/"],
            ["Doctor Who", "Joy to the World · transformation into shared light across time", "https://www.reddit.com/r/NeuronsToNirvana/comments/1i29ewt/beautiful_ending_to_doctor_who_christmas_special/"],
            ["Doctor Who", "Was LSD an influence? · Reuters historical-cultural question", "https://www.reddit.com/r/NeuronsToNirvana/comments/18f2hx9/was_lsd_an_influence_on_doctor_who_reuters_apr/"],
            ["Battlestar Galactica", "Resurrection · official SYFY video portal", "https://www.youtube.com/@SYFY/search?query=Battlestar%20Galactica%20resurrection"],
            ["Star Trek", "Joined identity · official Star Trek video portal", "https://www.youtube.com/@StarTrekOfficial/search?query=Trill"],
            ["Avatar", "The Avatar cycle · official Netflix video portal", "https://www.youtube.com/@Netflix/search?query=Avatar%20The%20Last%20Airbender%20trailer"],
            ["Dune", "Memory restored · official Warner Bros. portal", "https://www.youtube.com/@WarnerBrosPictures/search?query=Dune%20trailer"],
            ["The Matrix", "Constructed reality · official Warner Bros. portal", "https://www.youtube.com/@WarnerBrosPictures/search?query=The%20Matrix%20trailer"],
          ].map(([title, note, href]) => (
            <a key={title} href={href} style={{ ...panel, display: "block", padding: 22, color: "inherit", textDecoration: "none" }}>
              <span style={{ color: "#d8b95c", fontWeight: 900, letterSpacing: ".08em" }}>WATCH ↗</span>
              <h3 style={{ fontSize: "1.45rem", marginBottom: 8 }}>{title}</h3>
              <p style={{ color: "#cbd0dd", lineHeight: 1.6, marginBottom: 0 }}>{note}</p>
            </a>
          ))}
        </div>
        <p style={{ color: "#9fa7ba", lineHeight: 1.65, marginTop: 20 }}>
          Availability varies by country. No video is copied, hosted or presented as an endorsement by the rights holders. “Joy to the World” uses fictional and theological imagery, including the Star of Bethlehem; this page does not present that narrative as a verified historical event. The LSD item is retained as a historical-cultural question: aesthetic similarity and chronological overlap do not establish direct creative influence.
        </p>
      </section>

      <section style={{ ...shell, padding: "76px 0 20px" }}>
        <p className="section-label">FURTHER PORTALS · MANY LENSES, NO FORCED CONCLUSION</p>
        <h2 style={{ maxWidth: 920, fontSize: "clamp(2.2rem,5vw,4.2rem)", lineHeight: 1.06 }}>Character, fragments, reality and possible worlds.</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))", gap: 16, marginTop: 30 }}>
          {[
            ["One thread, many Doctors", "From TARDIS to complex spacetime event: the synthesis portal connecting incarnations, worlds and infinite possibilities.", "https://www.reddit.com/r/NeuronsToNirvana/comments/1vom25d/doctor_who_from_tardis_to_complex_spacetime_event/"],
            ["The ethical traveller", "Ask ChatGPT: interpret the Doctor through another philosophical lens.", "https://www.reddit.com/r/NeuronsToNirvana/comments/1lkuogk/ask_chatgpt_is_the_doctor_from_doctor_who/"],
            ["The Key to Time", "A crystalline whole scattered into segments: unity recovered without erasing the parts.", "https://www.reddit.com/r/NeuronsToNirvana/comments/1e16gt2/an_allegory_key_to_time_a_perfect_crystalline/"],
            ["The Pandorica Opens", "Containment, preserved memory and a cosmic reboot after spacetime fractures around the TARDIS.", "https://www.reddit.com/r/NeuronsToNirvana/comments/1cpic32/the_pandorica_opens_ft_the_tardis_time_and/"],
            ["The Reality War", "A finale-scale puzzle about contested reality, identity and which world becomes actual.", "https://www.reddit.com/r/NeuronsToNirvana/comments/1kyk7la/the_doctor_whoseason_2_finale_is_titled_the/"],
            ["Develop a MIND-TARDIS", "Lucid dreaming, meditation and breathwork as practices for navigating expansive inner landscapes.", "https://www.reddit.com/r/NeuronsToNirvana/comments/1mpeb6p/multidimensional_consciousness_perspective/"],
            ["The Harmonic Singularity V", "A speculative bridge from quantum-field language through resonance towards consciousness and cosmic-scale questions.", "https://www.reddit.com/r/NeuronsToNirvana/comments/1vjslod/the_harmonic_singularity_v_from_quantum_fields/"],
            ["You’ll Never Walk Alone", "From lived insight to research questions about companionship, co-regulation and relational experience.", "https://www.reddit.com/r/NeuronsToNirvana/comments/1q7q9no/youll_never_walk_alone_from_lived_insight_to/"],
            ["Never fail to be kind", "The Doctor’s ethical compass: expanded capability remains accountable to courage, love and kindness.", "https://www.reddit.com/r/NeuronsToNirvana/comments/1e5m8gg/never_be_cruel_never_be_cowardly_and_never_ever/"],
            ["The Juggling Jedi Jester", "A playful composite archetype for holding many perspectives with dexterity, humour and compassionate connection.", "https://www.reddit.com/r/NeuronsToNirvana/comments/1lz5uls/the_juggling_jedi_jester_with_jazz_hands_hugging/"],
            ["Holodeck × TARDIS", "A parallel future timeline for an adaptive, larger-on-the-inside perceptual environment.", "https://www.reddit.com/r/NeuronsToNirvana/comments/1mxw8mt/the_holodeck_tardis_a_parallel_future_timeline/"],
            ["The pyramid prototype", "Can symbolic geometry become a safe physical shell for immersive sound and 360° experience?", "https://www.reddit.com/r/NeuronsToNirvana/comments/1vleddp/need_help_building_a_structurally_sound_pyramid/"],
          ].map(([title, text, href]) => (
            <article key={title} style={{ ...panel, padding: 24 }}>
              <span style={{ color: "#d8b95c", fontWeight: 900, letterSpacing: ".08em" }}>N2N PORTAL</span>
              <h3 style={{ fontSize: "1.5rem", marginBottom: 10 }}>{title}</h3>
              <p style={{ color: "#cbd0dd", lineHeight: 1.65 }}>{text}</p>
              <a href={href}>Explore the source post →</a>
            </article>
          ))}
        </div>
        <p style={{ color: "#9fa7ba", lineHeight: 1.65, marginTop: 20 }}>
          These community posts are interpretive and exploratory inputs. Their juxtaposition generates questions; it does not establish equivalence, causation or external ontology. Shared terms such as “field”, “frequency”, “resonance” and “singularity” do not by themselves establish a physical connection between quantum theory and consciousness. The Harmonic Singularity remains speculative. The “You’ll Never Walk Alone” post is preserved as lived insight and hypothesis-generating interpretation, not proof of a single neural mechanism; specific claims about mirror systems, oxytocin or vagal activity require appropriately matched sources and context. Any physical pyramid or immersive enclosure would require qualified structural, fire, electrical, accessibility and event-safety review before construction or public use.
        </p>
      </section>

      <section style={{ ...shell, padding: "86px 0" }}>
        <div style={{ ...panel, padding: "clamp(28px,6vw,64px)", textAlign: "center", background: "radial-gradient(circle at 50% 0, rgba(116,75,185,.3), rgba(10,14,32,.96) 58%)" }}>
          <p className="section-label">THE BIGGER AND SMALLER PICTURE</p>
          <h2 style={{ fontSize: "clamp(2rem,5vw,4rem)" }}>What can we observe, infer, imagine and HOMESENSE?</h2>
          <p style={{ maxWidth: 850, margin: "0 auto", color: "#d7d9e4", lineHeight: 1.85 }}>
            Human senses and instruments reveal only limited ranges and scales. Science extends observation through measurement; philosophy tests concepts; contemplative practice examines experience; art and science fiction let us rehearse possibilities. None should silently replace the others.
          </p>
          <blockquote style={{ margin: "34px auto 0", maxWidth: 790, color: "#f2d98e", fontSize: "clamp(1.35rem,3vw,2.2rem)", lineHeight: 1.45 }}>
            “Meta-awareness recognises the lens. Mettā-awareness cares for every being seen through it.”
          </blockquote>
        </div>
      </section>

      <section style={{ ...shell, paddingBottom: 86 }}>
        <div style={{ borderLeft: "4px solid #d8b95c", padding: "8px 0 8px 24px", maxWidth: 920 }}>
          <p className="section-label">EVIDENCE BOUNDARY</p>
          <p style={{ color: "#cbd0dd", lineHeight: 1.8 }}>
            <strong>Interpretation:</strong> the comparison among regeneration, resurrection and reincarnation is a cultural and philosophical analysis. <strong>Speculation:</strong> HOMESENSE VR is a future creative concept. It does not establish survival after death, direct perception of dark matter, quantum consciousness or any franchise&apos;s fictional mechanism as physically possible. This is independent cultural commentary and is not affiliated with or endorsed by the referenced rights holders.
          </p>
          <p style={{ color: "#f0d98f", fontWeight: 800 }}>BQ001 remains UNRESOLVED. Fund the question, not the answer.</p>
          <a href="/big-questions/bq001">Explore BQ001: Does consciousness continue beyond the individual? →</a>
        </div>
      </section>


      <section style={{ ...shell, padding: "20px 0 70px", textAlign: "center" }}>
        <div style={{ ...panel, padding: "clamp(28px,6vw,58px)" }}>
          <p className="section-label">FROM INNER SPACE TO THE FESTIVAL FIELD</p>
          <h2 style={{ margin: "16px auto", maxWidth: 850, fontSize: "clamp(2rem,4.5vw,3.8rem)", lineHeight: 1.08 }}>One signal. Thousands of bodies. A shared moment in time.</h2>
          <p style={{ maxWidth: 760, margin: "20px auto 28px", color: "#d7d9e4", lineHeight: 1.8 }}>
            Orbital&apos;s Doctor Who theme at Glastonbury 2010 turns a television signal into collective music, movement and memory: a cultural example of how one pattern can be carried by many minds.
          </p>
          <a href="https://www.reddit.com/r/NeuronsToNirvana/comments/1dt6v7f/doctor_who_orbital_glastonbury_2010_bbc_music/">
            Doctor Who × Orbital · Glastonbury 2010 <span>→</span>
          </a>
        </div>
      </section>

      <section style={{ ...shell, padding: "0 0 70px", textAlign: "center" }}>
        <div style={{ ...panel, padding: "clamp(28px,6vw,58px)" }}>
          <p className="section-label">MUSICAL REGENERATION · 2018</p>
          <h2 style={{ margin: "16px auto", maxWidth: 850, fontSize: "clamp(2rem,4.5vw,3.8rem)", lineHeight: 1.08 }}>The signal changes its body but keeps its pulse.</h2>
          <p style={{ maxWidth: 740, margin: "20px auto 28px", color: "#d7d9e4", lineHeight: 1.8 }}>
            Segun Akinola&apos;s electronic reconstruction offers another continuity puzzle: timbre, rhythm and production can regenerate while the underlying musical identity remains recognisable.
          </p>
          <a href="https://www.reddit.com/r/NeuronsToNirvana/comments/1kd2fx0/doctor_who_segun_akinola_full_theme_remix_2018/">
            Doctor Who · Segun Akinola full theme remix · 2018 <span>→</span>
          </a>
        </div>
      </section>

      <section style={{ ...shell, padding: "0 0 70px", textAlign: "center" }}>
        <div style={{ ...panel, padding: "clamp(28px,6vw,58px)" }}>
          <p className="section-label">THE SIGNAL REGENERATES</p>
          <h2 style={{ margin: "16px auto", maxWidth: 850, fontSize: "clamp(2rem,4.5vw,3.8rem)", lineHeight: 1.08 }}>A familiar identity enters a new visual spacetime.</h2>
          <p style={{ maxWidth: 740, margin: "20px auto 28px", color: "#d7d9e4", lineHeight: 1.8 }}>
            The title sequence introduced with <em>The Star Beast</em> preserves the programme&apos;s recognisable signal while transforming its sound, scale and visual language.
          </p>
          <a href="https://youtu.be/X_1bgdz7vig">The New Doctor Who Title Sequence · official video <span>→</span></a>
        </div>
      </section>

      <section style={{ ...shell, padding: "10px 0 96px", textAlign: "center" }}>
        <div style={{ ...panel, padding: "clamp(32px,7vw,72px)", background: "radial-gradient(circle at 50% 100%, rgba(62,181,214,.25), rgba(10,14,32,.97) 62%)" }}>
          <p className="section-label">FINAL PORTAL · SOUND THROUGH TIME</p>
          <h2 style={{ margin: "16px auto", maxWidth: 850, fontSize: "clamp(2.2rem,5vw,4.5rem)", lineHeight: 1.04 }}>The same theme.<br />Always regenerating.</h2>
          <p style={{ maxWidth: 720, margin: "22px auto 30px", color: "#d7d9e4", lineHeight: 1.8 }}>
            End the journey by hearing one musical identity pass through changing technologies, arrangements and eras while remaining recognisably itself.
          </p>
          <a className="primary-link" href="https://www.reddit.com/r/NeuronsToNirvana/comments/1dyp4r3/evolution_of_the_doctor_who_theme_tune/">
            Evolution of the Doctor Who Theme Tune <span>→</span>
          </a>
        </div>
      </section>

      <footer>
        <div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt="" /><p className="brand-name">AKASHICNET.ORG</p></div>
        <p>Spiritual Sci-Fi · Wonder with discernment</p>
        <p>Awaken within · Serve without · 2026</p>
      </footer>
    </main>
  );
}
