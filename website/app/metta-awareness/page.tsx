import styles from "./metta-awareness.module.css";

const lenses = [
  ["01", "Observation", "What was actually said or done?"],
  ["02", "Context", "What happened around it?"],
  ["03", "Tone", "How did the exchange feel, without treating feeling as proof?"],
  ["04", "Body", "What sensations or stress signals arose?"],
  ["05", "Emotion", "What feelings can be named without blame?"],
  ["06", "Need", "What connection, safety or clarity may be needed?"],
  ["07", "Perspective", "What might each person be seeing?"],
  ["08", "Culture", "Which norms or expectations may shape the exchange?"],
  ["09", "Neurodiversity", "Could communication styles differ, without diagnosing?"],
  ["10", "Power", "Who carries risk, authority or vulnerability?"],
  ["11", "Evidence", "Which claims are supported, uncertain or untested?"],
  ["12", "Ethics", "What response preserves dignity and reduces harm?"],
  ["13", "Revision", "What would change the present interpretation?"],
];

const practices = [
  ["Compassion", "Meet the person as a conscious being, not as a label, role or problem to solve."],
  ["Discernment", "Separate observation from interpretation, and meaning from established evidence."],
  ["Humility", "Hold every model lightly. Another person’s inner state cannot be known from messages alone."],
  ["Boundaries", "Care does not require unlimited access, agreement or tolerance of harmful behaviour."],
];

const evidence = [
  ["Established evidence", "Research or documented material with traceable methods, sources and limitations."],
  ["Interpretation", "A reasoned reading of an event, message, symbol or body of material."],
  ["Lived experience", "First-person testimony that may be genuine and meaningful without becoming universal proof."],
  ["Hypothesis", "A proposed explanation that can be investigated and revised."],
  ["Speculation", "A possibility held openly where support is presently insufficient."],
];

export default function MettaAwarenessPage() {
  return (
    <main className={styles.page}>
      <header className={styles.nav}>
        <a className={styles.wordmark} href="/" aria-label="AkashicNET.org home">
          <img src="/images/akashicnet-toroidal-love-logo.png" alt="" />
          <span>AKASHICNET.ORG</span>
        </a>
        <nav aria-label="Mettā-Awareness navigation">
          <a href="#meaning">Meaning</a>
          <a href="#sigil">Sigil</a>
          <a href="#thirteen">13 lenses</a>
          <a href="#practice">Practice</a>
          <a href="#transparency">Transparency</a>
        </nav>
      </header>

      <section className={styles.hero} id="top">
        <div className={styles.heroSky} aria-hidden="true">
          <span className={styles.city} />
          <span className={styles.temple} />
          <span className={styles.mountains} />
          <span className={styles.water} />
        </div>
        <div className={styles.foregroundField} aria-hidden="true">
          {Array.from({length:18}).map((_,i)=><i key={i} />)}
        </div>
        <div className={styles.heroCopy}>
          <p className={styles.eyebrow}>AkashicNET 13D · wisdom-tradition lens · in development</p>
          <h1>Mettā<br/><em>Awareness</em></h1>
          <p className={styles.lede}>A practice of meeting complexity with loving-kindness, discernment and the willingness to correct our model without reducing the person.</p>
          <div className={styles.actions}>
            <a href="#meaning">Enter the field <span>↓</span></a>
            <a href="#transparency">Read the knowledge boundary →</a>
          </div>
        </div>
        <div className={styles.heroSigil} aria-label="Artistic heart-torus sigil symbolising care flowing inward and outward">
          <img src="/images/akashicnet-toroidal-love-logo.png" alt="" />
          <span /><span /><span />
        </div>
        <p className={styles.heroNote}>Many places · many traditions · shared dignity</p>
      </section>

      <section className={styles.intro} id="meaning">
        <div>
          <p className={styles.label}>01 · Meaning</p>
          <h2>Awareness shaped by goodwill.</h2>
        </div>
        <div className={styles.longCopy}>
          <p><strong>Mettā</strong> is commonly translated from Pāli as loving-kindness, goodwill or benevolence. Within Buddhist traditions it belongs among the four <em>brahmavihāras</em>, alongside compassion, appreciative joy and equanimity.</p>
          <p><strong>Mettā-Awareness</strong> is AkashicNET’s developing synthesis. It asks how attention changes when goodwill is not merely a feeling but part of the method: listening before interpreting, describing before diagnosing, testing assumptions and retaining humane boundaries.</p>
          <aside>This page offers a contemplative and ethical framework. It is not a diagnostic system, a clinical treatment or proof of a metaphysical claim.</aside>
        </div>
      </section>

      <section className={styles.portalMap} aria-labelledby="portal-map-title">
        <div className={styles.portalIntro}>
          <p className={styles.label}>Portal constellation</p>
          <h2 id="portal-map-title">Choose your depth.</h2>
          <p>Begin anywhere. Move inward when the language, context and uncertainty boundaries feel clear. “Deeper” describes the level of inquiry, never the value or awareness of a person.</p>
        </div>
        <nav className={styles.portals} aria-label="Mettā-Awareness depth map">
          <a className={styles.portalOne} href="#practice"><span>01</span><strong>Arrive</strong><small>Pause and notice</small></a>
          <a className={styles.portalTwo} href="#capacities"><span>02</span><strong>Relate</strong><small>Four capacities</small></a>
          <a className={styles.portalThree} href="#thirteen"><span>03</span><strong>Inquire</strong><small>13 revisable lenses</small></a>
          <a className={styles.portalFour} href="#listen"><span>04</span><strong>Listen</strong><small>Guided media</small></a>
          <a className={styles.portalFive} href="#cymatics"><span>05</span><strong>Contemplate</strong><small>Sound, symbol, unknown</small></a>
        </nav>
      </section>

      <section className={styles.places} aria-label="A worldwide field of practice">
        <article><span>City</span><h3>Amid movement</h3><p>Practise attention in crowds, transit, work and ordinary encounters.</p></article>
        <article><span>Temple</span><h3>Within tradition</h3><p>Approach inherited practices with context, respect and cultural humility.</p></article>
        <article><span>Nature</span><h3>Beyond enclosure</h3><p>Let forests, coasts, deserts and mountains widen the frame of concern.</p></article>
        <article><span>Home</span><h3>Where care becomes real</h3><p>Bring insight into messages, disagreements, family life and daily choices.</p></article>
      </section>

      <section className={styles.sigilSection} id="sigil">
        <div className={styles.sigilVisual}>
          <svg viewBox="0 0 640 640" role="img" aria-labelledby="sigil-title sigil-desc">
            <title id="sigil-title">AkashicNET Mettā-Awareness sigil</title>
            <desc id="sigil-desc">A central heart-like infinity form surrounded by thirteen points and reciprocal inner and outer rings.</desc>
            <defs>
              <radialGradient id="halo"><stop offset="0" stopColor="#f1d48b" stopOpacity=".5"/><stop offset=".55" stopColor="#8be6c7" stopOpacity=".13"/><stop offset="1" stopColor="#080f17" stopOpacity="0"/></radialGradient>
              <linearGradient id="flow"><stop stopColor="#e9c76e"/><stop offset=".5" stopColor="#8be6c7"/><stop offset="1" stopColor="#bda6ff"/></linearGradient>
            </defs>
            <circle cx="320" cy="320" r="290" fill="url(#halo)"/>
            <circle cx="320" cy="320" r="226" fill="none" stroke="#d9c686" strokeOpacity=".28"/>
            <circle cx="320" cy="320" r="174" fill="none" stroke="#8be6c7" strokeOpacity=".24" strokeDasharray="3 12"/>
            <path d="M320 434 C228 350 184 306 184 245 C184 190 252 165 320 251 C388 165 456 190 456 245 C456 306 412 350 320 434Z" fill="none" stroke="url(#flow)" strokeWidth="10"/>
            <path d="M173 320 C222 230 285 230 320 320 C355 410 418 410 467 320 C418 230 355 230 320 320 C285 410 222 410 173 320Z" fill="none" stroke="url(#flow)" strokeWidth="5" opacity=".85"/>
            {Array.from({length:13}).map((_,i)=>{
              const a=(i/13)*Math.PI*2-Math.PI/2;
              const x=320+226*Math.cos(a), y=320+226*Math.sin(a);
              return <g key={i}><circle cx={x} cy={y} r="10" fill="#091716" stroke="#e9c76e" strokeWidth="2"/><text x={x} y={y+4} textAnchor="middle" fill="#f4ecd7" fontSize="10">{i+1}</text></g>;
            })}
            <circle cx="320" cy="320" r="18" fill="#f2d47e"/>
          </svg>
        </div>
        <div className={styles.sigilCopy}>
          <p className={styles.label}>02 · The enhanced sigil</p>
          <h2>A reciprocal field of attention.</h2>
          <dl>
            <div><dt>Heart form</dt><dd>Goodwill and compassionate intention.</dd></div>
            <div><dt>Infinity crossing</dt><dd>Listening moving between self and other.</dd></div>
            <div><dt>Inner and outer rings</dt><dd>Care that includes inner experience, relationship and wider ecology.</dd></div>
            <div><dt>Thirteen points</dt><dd>The 13D lenses used to examine a question from multiple viewpoints.</dd></div>
            <div><dt>Open space</dt><dd>Uncertainty, silence and what the present model cannot contain.</dd></div>
          </dl>
          <p className={styles.boundary}><strong>Symbolic boundary:</strong> the heart-torus is an artistic metaphor for reciprocal care and meta-awareness. It is not presented as a measured energy field or a scientific model of the cosmos.</p>
        </div>
      </section>

      <section className={styles.capacities} id="capacities">
        <div className={styles.sectionHead}>
          <p className={styles.label}>03 · Four capacities</p>
          <h2>Warmth needs structure.</h2>
          <p>Mettā-Awareness joins kindness to intellectual and relational discipline.</p>
        </div>
        <div className={styles.practiceGrid}>
          {practices.map(([title,text],i)=><article key={title}><span>0{i+1}</span><h3>{title}</h3><p>{text}</p></article>)}
        </div>
      </section>

      <section className={styles.thirteen} id="thirteen">
        <div className={styles.sectionHead}>
          <p className={styles.label}>04 · AkashicNET 13D</p>
          <h2>Thirteen lenses.<br/><em>One revisable model.</em></h2>
          <p>“13D” names a thirteen-lens method for widening inquiry. It does not claim thirteen physical dimensions.</p>
        </div>
        <div className={styles.lensGrid}>
          {lenses.map(([n,title,text])=><article key={n}><span>{n}</span><h3>{title}</h3><p>{text}</p></article>)}
        </div>
        <blockquote>Correct the model. Never reduce the person.</blockquote>
      </section>

      <section className={styles.flow} id="practice">
        <div className={styles.sectionHead}>
          <p className={styles.label}>05 · Conversation practice</p>
          <h2>From reaction to responsive care.</h2>
        </div>
        <ol>
          <li><span>1</span><div><strong>Pause</strong><p>Notice activation before explaining the other person.</p></div></li>
          <li><span>2</span><div><strong>Describe</strong><p>Name the words or behaviour you observed without assigning motive.</p></div></li>
          <li><span>3</span><div><strong>Locate</strong><p>State your feeling, need and uncertainty in first-person language.</p></div></li>
          <li><span>4</span><div><strong>Ask</strong><p>Invite clarification: “Is that what you meant?”</p></div></li>
          <li><span>5</span><div><strong>Boundary</strong><p>Choose whether to continue, pause, redirect or leave.</p></div></li>
          <li><span>6</span><div><strong>Revise</strong><p>Update the interpretation when new evidence appears.</p></div></li>
        </ol>
      </section>

      <section className={styles.evidence} id="transparency">
        <div className={styles.sectionHead}>
          <p className={styles.label}>06 · Epistemic transparency</p>
          <h2>Keep different kinds of knowing visible.</h2>
        </div>
        <div className={styles.evidenceGrid}>
          {evidence.map(([title,text],i)=><article key={title}><span>{String(i+1).padStart(2,"0")}</span><h3>{title}</h3><p>{text}</p></article>)}
        </div>
        <div className={styles.provenance}>
          <div><span>User contribution</span><p>Questions, selected messages, lived context, interpretation and creative direction.</p></div>
          <div><span>AkashicNET contribution</span><p>The 13-lens structure, evidence ladder, ethical commitments and model-refinement principle.</p></div>
          <div><span>AI-assisted synthesis</span><p>Language, organisation, accessibility, bias checks and visual translation. AI did not witness the events and cannot infer another person’s inner state.</p></div>
        </div>
      </section>

      <section className={styles.media} id="listen">
        <div>
          <p className={styles.label}>07 · Listen and practise</p>
          <h2>Two doorways into the practice.</h2>
          <p>These external teachings are offered as related resources, not endorsements of every claim or substitute for professional support.</p>
        </div>
        <article>
          <div className={styles.video}>
            <iframe src="https://www.youtube-nocookie.com/embed/FyKKvCO_vSA" title="10-minute guided loving-kindness meditation with Sharon Salzberg" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />
          </div>
          <h3>Loving-kindness meditation</h3>
          <p>A short guided practice with Sharon Salzberg.</p>
          <a href="https://www.youtube.com/watch?v=FyKKvCO_vSA">Open on YouTube ↗</a>
        </article>
        <article>
          <div className={styles.video}>
            <iframe src="https://www.youtube-nocookie.com/embed/O5Cw_7f43mA" title="Guided meditation for compassionate listening" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />
          </div>
          <h3>Compassionate listening</h3>
          <p>A guided practice connected with the Plum Village tradition.</p>
          <a href="https://www.youtube.com/watch?v=O5Cw_7f43mA">Open on YouTube ↗</a>
        </article>
      </section>

      <section className={styles.audiovisual} id="cymatics" aria-labelledby="audiovisual-title">
        <div className={styles.audiovisualCopy}>
          <p className={styles.label}>08 · Optional audiovisual</p>
          <h2 id="audiovisual-title">Sound made visible.</h2>
          <p>Cymatics makes vibration patterns visible in physical media. Some people also describe sound-based practices as calming, meaningful or “healing”. Those subjective reports can be recorded as lived experience. Broader “quantum sound healing” explanations require separate definitions and evidence, and are not established by the geometry alone.</p>
          <div className={styles.mediaLegend}>
            <span><b>Observable</b> vibration producing visible patterns</span>
            <span><b>Experiential</b> a listener’s reported response</span>
            <span><b>Speculative</b> wider energetic or quantum interpretation</span>
          </div>
          <p className={styles.mediaCaution}>Optional sensory experience. Start quietly, stop if uncomfortable and do not use it as a substitute for healthcare.</p>
        </div>
        <article className={styles.cymaticPlayer}>
          <div className={styles.cymaticHalo} aria-hidden="true"><span/><span/><span/></div>
          <div className={styles.video}>
            <iframe src="https://www.youtube-nocookie.com/embed/NdUL6yZu6uo" title="Fractal cymatics visualisation across a range of sound frequencies" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />
          </div>
          <div>
            <h3>Fractal cymatics study</h3>
            <p>A visual meditation on changing patterns. The accompanying music is separate from the cymatic source, according to the video description.</p>
            <a href="https://www.youtube.com/watch?v=NdUL6yZu6uo">Open on YouTube ↗</a>
          </div>
        </article>
      </section>

      <section className={styles.closing}>
        <p className={styles.label}>A compass, not a ranking</p>
        <h2>May awareness deepen care.<br/><em>May care sharpen awareness.</em></h2>
        <p>Observe · Connect · Test · Update · Serve</p>
        <a href="/">Return to AkashicNET.org →</a>
      </section>

      <footer className={styles.footer}>
        <div><img src="/images/akashicnet-toroidal-love-logo.png" alt=""/><strong>AKASHICNET.ORG</strong></div>
        <p>Mettā-Awareness · In development</p>
        <p>Wisdom-tradition lens · Evidence boundaries visible</p>
      </footer>
    </main>
  );
}
