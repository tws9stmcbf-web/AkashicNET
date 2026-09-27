import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Schumann Activity Window · AkashicNET Interstellar Weather Report",
  description: "A dated AkashicNET 13D analysis of the Schumann-resonance activity visible across 11–12 September 2026, its cofactors, testimony and open questions.",
};

const shell = { width: "min(1160px, calc(100% - 32px))", margin: "0 auto" };
const panel = {
  border: "1px solid rgba(216,185,92,.24)",
  borderRadius: 24,
  background: "linear-gradient(145deg, rgba(19,25,47,.94), rgba(8,12,28,.97))",
  boxShadow: "0 24px 80px rgba(0,0,0,.28)",
};
const evidence = [
  ["Established Evidence", "Schumann resonances are lightning-excited electromagnetic modes within the Earth–ionosphere cavity. Space weather and geomagnetic variation are measurable physical phenomena."],
  ["Observation", "The MeteoAgent three-day widget displayed stronger visible activity across 11–12 September and labelled conditions Quiet on 13 September. It did not expose a calibrated amplitude or exact event peak in the accessible view."],
  ["Lived Experience/Testimony", "Many people report disrupted sleep, vivid dreams, fatigue, mood changes or somatic sensitivity during solar, geomagnetic, lunar or Schumann-resonance events. Testimony is preserved without universalising it."],
  ["Hypothesis", "Circadian, melatonin, autonomic, electromagnetic, nutritional and neurodiversity-related pathways can be investigated using synchronized and blinded observations."],
  ["Speculation", "Collective-consciousness, societal-conflict and wider interstellar-field interpretations remain possibilities for inquiry, not established explanations of this event."],
];
const dimensions = [
  ["01", "AWAKEN", "Notice the disturbance without deciding what it means."],
  ["02", "HIERATIC", "Explore Earth as a living resonant symbol and preserve spiritual meaning as interpretation."],
  ["03", "HOMESENSE", "Listen to sleep, mood, dream and somatic testimony as lived experience."],
  ["04", "ADAPT", "Separate source signal, explanatory story and plausible confounders."],
  ["05", "REGENERATE", "Respond with rest, grounding, reflection and compassionate care."],
  ["06", "TRANSCEND", "Place Sun, Pachamama, biosphere and consciousness within a wider system."],
  ["07", "#METAD v2.1", "Compare competing explanations and search for contradictions."],
  ["08", "ACTC v2.0", "Map agency, context, temporal order and candidate causal pathways."],
  ["09", "MultidimensionalCUT v4.0.0 · PAST", "Compare prior solar, geomagnetic, lunar and resonance patterns."],
  ["10", "MultidimensionalCUT v4.0.0 · PRESENT", "Describe the dated 11–12 September activity window precisely."],
  ["11", "MultidimensionalCUT v4.0.0 · FUTURE", "Pre-register what to measure during the next comparable event."],
  ["12", "UMASC v7.2", "Relate matter, awareness, systems and culture without collapsing their differences."],
  ["13", "AKASHICNET", "Synthesize the whole field while leaving unresolved questions open."],
];
const sources = [
  ["MeteoAgent live Schumann forecast", "https://meteoagent.com/schumann-resonance-forecast"],
  ["NOAA Space Weather Prediction Center", "https://www.spaceweather.gov/"],
  ["Solar and geomagnetic activity and plasma B-complex vitamins · Scientific Reports (2024)", "https://www.nature.com/articles/s41598-024-75253-z"],
  ["Autonomic rhythms and geomagnetic activity · Scientific Reports (2017)", "https://pmc.ncbi.nlm.nih.gov/articles/PMC5551208/"],
  ["Lunar cycle and human sleep · Current Biology (2013)", "https://pubmed.ncbi.nlm.nih.gov/23891110/"],
  ["Synchronization of human sleep with the Moon cycle · Science Advances (2021)", "https://www.science.org/doi/10.1126/sciadv.abe0465"],
  ["Solar activity and spontaneous social processes · 2014", "https://doi.org/10.1134/S0001433814040045"],
  ["N2N · solar maximum and historic planetary shifts", "https://www.reddit.com/r/NeuronsToNirvana/comments/1jvtj6p/why_global_conflict_is_rising_due_to_solar/"],
];

export default function InterstellarWeatherReport() {
  return (
    <main style={{ minHeight: "100vh", color: "#f5f0e7", background: "radial-gradient(circle at 50% 8%, #17315a 0, #0a1026 34%, #050711 78%)" }}>
      <header className="nav-shell">
        <a className="wordmark" href="/" aria-label="AkashicNET.org home"><img className="brand-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt="" /><span className="brand-name">AKASHICNET.ORG</span></a>
        <nav aria-label="Page navigation"><a href="/">Home</a><a href="#event">Event</a><a href="#analysis">13D analysis</a><a href="#evidence">Evidence</a><a href="#sources">Sources</a></nav>
      </header>

      <article>
        <section style={{ ...shell, padding: "clamp(70px,10vw,132px) 0 50px", textAlign: "center" }}>
          <p className="section-label">INSIGHTS NEWS DESK · INTERDIMENSIONAL LIGHTEXPLORERS HOTLINE</p>
          <h1 style={{ margin: "18px auto", maxWidth: 1060, fontSize: "clamp(3rem,7.5vw,7rem)", lineHeight: .94 }}>Schumann<br/><em style={{ color: "#d8b95c" }}>Activity Window</em></h1>
          <p style={{ color: "#e7cd7e", fontWeight: 800, letterSpacing: ".08em" }}>11–12 SEPTEMBER 2026 UTC · QUIET BY 13 SEPTEMBER · STARDATE 2026.09.12</p>
          <p style={{ maxWidth: 850, margin: "24px auto 0", color: "#d7d9e4", fontSize: "clamp(1.1rem,2.2vw,1.42rem)", lineHeight: 1.75 }}>A 13D spiritual-science exploration of a visible source-plot disturbance, its solar, geomagnetic, lunar and human cofactors, and the difference between meaningful connection and demonstrated causality.</p>
        </section>

        <figure style={{ ...shell, ...panel, overflow: "hidden", padding: 0 }}>
          <img src="/images/interstellar-weather-schumann-event-2026-09-12.png" alt="AkashicNET event overview showing the Sun, heliosphere, ionosphere, lightning, Earth resonance, sleeping humanity and a conceptual three-day activity band." style={{ display: "block", width: "100%", height: "auto" }} />
          <figcaption style={{ padding: "16px 20px", color: "#b9bfd0", lineHeight: 1.65 }}><strong style={{ color: "#f3dc96" }}>Event overview.</strong> The activity band in this artwork is a conceptual reconstruction, not copied raw instrument data. It communicates the timing visible on the source widget without inventing amplitude or peak values.</figcaption>
        </figure>

        <section id="event" style={{ ...shell, padding: "78px 0 24px" }}>
          <p className="section-label">THE OBSERVATION</p>
          <div style={{ ...panel, padding: "clamp(26px,5vw,52px)" }}>
            <h2 style={{ fontSize: "clamp(2.2rem,5vw,4.4rem)", marginTop: 0 }}>What appeared on the chart?</h2>
            <p style={{ color: "#d7d9e4", lineHeight: 1.85, fontSize: "1.08rem" }}>The MeteoAgent widget showed visibly stronger activity across 11–12 September, concentrated mainly across the lower displayed harmonic bands. By the time of review on 13 September, the widget labelled conditions <strong>Quiet</strong>. Because the accessible display did not supply a calibrated amplitude, named station, uncertainty interval or exact event peak, this report does not assign one.</p>
            <p style={{ color: "#d7d9e4", lineHeight: 1.85 }}>The source page correctly distinguishes frequency from amplitude and notes that Schumann resonances are excited primarily by global lightning. It then moves from geophysics into proposed health explanations. AkashicNET preserves that shift as a question boundary: the physical signal is established; the claimed biological pathway remains under investigation.</p>
            <p style={{ marginBottom: 0 }}><a href="https://meteoagent.com/schumann-resonance-forecast">Open the originating live forecast ↗</a></p>
          </div>
        </section>

        <section style={{ ...shell, padding: "62px 0 20px" }}>
          <p className="section-label">INTERSTELLAR WEATHER CONTEXT</p>
          <h2 style={{ maxWidth: 940, fontSize: "clamp(2.2rem,5vw,4.5rem)", lineHeight: 1.04 }}>One event. Many possible pathways.</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))", gap: 16, marginTop: 28 }}>
            {[
              ["Sun and heliosphere", "Coronal-hole solar wind and minor radio-blackout conditions belong to the wider dated context. They do not by themselves explain the source-plot pattern or a person’s sleep."],
              ["Earth and ionosphere", "Lightning, ionospheric conductivity, station geometry, season, time of day and local interference can all shape a Schumann-resonance record."],
              ["Moon and light", "The event occurred near the new-Moon threshold, at roughly 1–3% illumination—not a full Moon. Lunar phase remains a cofactor to record rather than a presumed cause."],
              ["Body and environment", "Sleep timing, artificial light, stress, weather, medication, substances and baseline health may interact with any environmental sensitivity."],
            ].map(([title,text]) => <article key={title} style={{ ...panel, padding: 24 }}><h3 style={{ color: "#e7cd7e", fontSize: "1.45rem" }}>{title}</h3><p style={{ color: "#cbd0dd", lineHeight: 1.7 }}>{text}</p></article>)}
          </div>
        </section>

        <section id="analysis" style={{ ...shell, padding: "76px 0 22px" }}>
          <p className="section-label">TRUE 13D ANALYSIS</p>
          <h2 style={{ maxWidth: 900, fontSize: "clamp(2.2rem,5vw,4.5rem)", lineHeight: 1.04 }}>Thirteen lenses. No premature closure.</h2>
          <figure style={{ ...panel, overflow: "hidden", padding: 0, marginTop: 30 }}>
            <img src="/images/interstellar-weather-schumann-13d-2026-09-12.png" alt="Thirteen-dimensional AkashicNET analysis displaying AWAKEN, HIERATIC, HOMESENSE, ADAPT, REGENERATE, TRANSCEND, METAD v2.1, ACTC v2.0, three MultidimensionalCUT v4.0.0 time lenses, UMASC v7.2 and AkashicNET synthesis." style={{ display: "block", width: "100%", height: "auto" }} />
            <figcaption style={{ padding: "16px 20px", color: "#b9bfd0", lineHeight: 1.65 }}><strong style={{ color: "#f3dc96" }}>The 13D architecture.</strong> “Dimensions” means analytical perspectives, not a claim that thirteen additional physical dimensions have been demonstrated.</figcaption>
          </figure>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(245px,1fr))", gap: 16, marginTop: 26 }}>
            {dimensions.map(([number,title,text]) => <article key={number} style={{ ...panel, padding: 22 }}><span style={{ color: "#d8b95c", fontWeight: 900 }}>{number}</span><h3 style={{ fontSize: "1.25rem", margin: "8px 0" }}>{title}</h3><p style={{ color: "#cbd0dd", lineHeight: 1.65, marginBottom: 0 }}>{text}</p></article>)}
          </div>
          <p style={{ color: "#aeb5c6", lineHeight: 1.75, marginTop: 22 }}><strong>r/NeuronsToNirvana is the integrated Evidence and Source Commons.</strong> It supplies research, testimony and competing perspectives across the dimensions rather than becoming an additional fourteenth dimension.</p>
        </section>

        <section id="evidence" style={{ ...shell, padding: "78px 0 22px" }}>
          <p className="section-label">EVIDENCE MAP</p>
          <h2 style={{ maxWidth: 860, fontSize: "clamp(2.2rem,5vw,4.4rem)", lineHeight: 1.04 }}>Wonder and discernment belong together.</h2>
          <div style={{ display: "grid", gap: 14, marginTop: 30 }}>
            {evidence.map(([title,text],index) => <article key={title} style={{ ...panel, padding: "22px clamp(22px,4vw,42px)", display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(min(100%,240px),1fr))", gap: 22 }}><h3 style={{ margin: 0, color: ["#8de6ff","#8fcfff","#a7f0c1","#e7cd7e","#d9a6ff"][index] }}>{title}</h3><p style={{ margin: 0, color: "#cbd0dd", lineHeight: 1.72 }}>{text}</p></article>)}
          </div>
        </section>

        <section style={{ ...shell, padding: "72px 0 20px" }}>
          <div style={{ ...panel, padding: "clamp(28px,5vw,54px)", background: "radial-gradient(circle at 20% 10%,rgba(36,154,190,.2),rgba(9,13,31,.97) 58%)" }}>
            <p className="section-label">FROM EXPERIENCE TO SHARED INQUIRY</p>
            <h2 style={{ fontSize: "clamp(2.1rem,5vw,4.2rem)", marginTop: 12 }}>How could the next event be tested?</h2>
            <p style={{ color: "#d7d9e4", lineHeight: 1.85 }}>Record sleep, dreams, mood and somatic experiences before viewing environmental dashboards. Synchronize timestamps with calibrated local electromagnetic measurements, geomagnetic indices, solar wind, lightning, lunar illumination, weather and ordinary sleep cofactors. Pre-register predictions, compare blinded event and control periods, and invite independent replication.</p>
            <blockquote style={{ color: "#f2d98e", fontSize: "clamp(1.3rem,2.8vw,2rem)", lineHeight: 1.45, margin: "28px 0 0" }}>“Not everything unmeasured is unreal. Not everything correlated is caused.”</blockquote>
          </div>
        </section>

        <section id="sources" style={{ ...shell, padding: "76px 0 24px" }}>
          <p className="section-label">SOURCES AND FURTHER PORTALS</p>
          <h2 style={{ fontSize: "clamp(2.1rem,5vw,4rem)" }}>Follow the evidence trail.</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))", gap: 14 }}>
            {sources.map(([title,href]) => <a key={href} href={href} style={{ ...panel, padding: 20, display: "block", color: "inherit", textDecoration: "none" }}><span style={{ color: "#d8b95c", fontWeight: 900 }}>SOURCE ↗</span><h3 style={{ lineHeight: 1.35 }}>{title}</h3></a>)}
          </div>
          <p style={{ color: "#9fa7ba", lineHeight: 1.7, marginTop: 22 }}>Sources have different designs and evidential strengths. Their inclusion maps the inquiry; it does not imply AkashicNET endorsement of every claim they contain. The 2024 vitamin study reports cohort-level associations and does not establish that this event altered anyone’s vitamin status. Solar–social correlations do not demonstrate that the Sun caused a conflict.</p>
        </section>

        <section style={{ ...shell, padding: "70px 0 90px", textAlign: "center" }}>
          <p className="section-label">THE INTERDIMENSIONAL LIGHTEXPLORERS HOTLINE</p>
          <h2 style={{ maxWidth: 940, margin: "16px auto", fontSize: "clamp(2.2rem,5vw,4.6rem)", lineHeight: 1.05 }}>We are not separate from cosmic weather—but connection must still be tested.</h2>
          <p style={{ color: "#e7cd7e", fontSize: "1.2rem" }}>Observe · Breathe · Reflect · Choose Compassion</p>
          <p style={{ maxWidth: 720, margin: "32px auto 0", color: "#cbd0dd", lineHeight: 1.7 }}>If this independent report helped, support future open-access analyses with a suggested €13 contribution.</p>
          <a href="https://buymeacoffee.com/akashicnet" style={{ display: "inline-block", marginTop: 16, padding: "14px 22px", borderRadius: 999, background: "#d8b95c", color: "#090d1c", fontWeight: 900, textDecoration: "none" }}>☕ Support AkashicNET</a>
          <p style={{ color: "#9fa7ba" }}>Fund the question—not the answer.</p>
        </section>
      </article>
      <footer><div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt="" /><p className="brand-name">AKASHICNET.ORG</p></div><p>Unity through neurodiversity.</p><p>Awaken within · Serve without · 2026</p></footer>
    </main>
  );
}
