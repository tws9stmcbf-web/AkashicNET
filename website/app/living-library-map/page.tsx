"use client";

import { useRef, useState, type MouseEvent } from "react";
import styles from "./page.module.css";

type Node = {
  id: string;
  label: string;
  href: string;
  x: number;
  y: number;
  kind: "branch" | "root" | "garden";
  evidence?: string;
  note: string;
};

const nodes: Node[] = [
  { id:"futures", label:"Possible Futures", href:"/akashicvision", x:22, y:18, kind:"branch", evidence:"Speculation", note:"Visionary futures and openly labelled scenarios." },
  { id:"consciousness", label:"Consciousness", href:"/big-questions/bq001", x:35, y:13, kind:"branch", evidence:"Mixed evidence", note:"Research, testimony and competing models. BQ001 remains UNRESOLVED." },
  { id:"science", label:"Science", href:"/big-questions", x:45, y:12, kind:"branch", evidence:"Established Evidence", note:"Methods, sources, counter-evidence and open questions." },
  { id:"psychedelics", label:"Psychedelics", href:"/big-questions", x:57, y:13, kind:"branch", evidence:"Mixed evidence", note:"Science, experience, harm reduction and uncertainty." },
  { id:"meditation", label:"Meditation", href:"/metta-awareness", x:68, y:14, kind:"branch", evidence:"Interpretation", note:"Contemplative practice, loving-kindness and ethical attention." },
  { id:"music", label:"Music & Psytrance", href:"/community", x:81, y:18, kind:"branch", evidence:"Lived Experience/Testimony", note:"Culture, community, creativity and collective experience." },
  { id:"big-questions", label:"Big Questions", href:"/big-questions", x:21, y:31, kind:"branch", evidence:"UNRESOLVED", note:"Governed questions whose uncertainty remains visible." },
  { id:"omni", label:"AkashicOMNI", href:"/akashicomni", x:24, y:42, kind:"branch", evidence:"Interpretation", note:"A governed orchestration framework for many evidence lanes." },
  { id:"timeless", label:"AkashicTIMELESS", href:"/akashictranscendence", x:24, y:50, kind:"branch", evidence:"Interpretation", note:"Time, transformation and carefully bounded continuity inquiry." },
  { id:"garden", label:"Mettā Search Garden", href:"#metta-search-garden", x:66, y:39, kind:"garden", evidence:"Inquiry patterns", note:"Anonymous aggregate patterns, never people or raw personal searches." },
  { id:"neurodiversity", label:"Neurodiversity", href:"/community", x:82, y:30, kind:"branch", evidence:"Mixed evidence", note:"Different minds, accessibility and community knowledge." },
  { id:"heart", label:"Heart & Spirit", href:"/metta-awareness", x:86, y:48, kind:"branch", evidence:"Interpretation", note:"Compassion, contemplative meaning and service." },
  { id:"earth", label:"Earth & Pachamama", href:"/insights/global-food-shortages-one-step-back-two-steps-forward", x:81, y:56, kind:"branch", evidence:"Established Evidence · Interpretation", note:"Planetary systems, food resilience and ecological care." },
  { id:"community", label:"Community", href:"/community", x:83, y:64, kind:"branch", evidence:"Lived Experience/Testimony", note:"Public communities and accountable participation." },
  { id:"evidence", label:"Evidence", href:"/#boundary", x:22, y:82, kind:"root", note:"Claims remain linked to their evidence lane." },
  { id:"provenance", label:"Provenance", href:"/#boundary", x:31, y:84, kind:"root", note:"Origin, date, context and transformation remain traceable." },
  { id:"privacy", label:"Privacy", href:"/#ethics", x:40, y:85, kind:"root", note:"Public learning is separated from protected working data." },
  { id:"rights", label:"Rights", href:"/#ethics", x:48, y:87, kind:"root", note:"Publication follows rights and public-manifest boundaries." },
  { id:"sovereignty", label:"Cultural Sovereignty", href:"/#ethics", x:57, y:87, kind:"root", note:"Cultural material is not flattened, claimed or promoted." },
  { id:"uncertainty", label:"Uncertainty", href:"/#boundary", x:66, y:85, kind:"root", note:"Unknowns remain explicit; similarity never becomes proof." },
  { id:"hold", label:"HOLD / Adjudication", href:"/#architecture", x:74, y:83, kind:"root", note:"Consequential ambiguity pauses for human review." },
  { id:"accessibility", label:"Accessibility", href:"/#ethics", x:82, y:82, kind:"root", note:"The map has keyboard, screen-reader and plain-list paths." },
];

const evidenceLegend = [
  ["Established Evidence", "evidence"],
  ["Lived Experience/Testimony", "testimony"],
  ["Interpretation", "interpretation"],
  ["Hypothesis", "hypothesis"],
  ["Speculation", "speculation"],
] as const;

export default function LivingLibraryMap() {
  const [active, setActive] = useState<Node | null>(null);
  const pointerType = useRef<string | null>(null);
  const touchArmedNodeId = useRef<string | null>(null);

  const preview = (node: Node) => {
    if (pointerType.current !== "touch") {
      touchArmedNodeId.current = null;
      setActive(node);
    }
  };

  const choose = (event: MouseEvent<HTMLButtonElement>, node: Node) => {
    const isKeyboard = event.detail === 0;
    const isTouch = !isKeyboard && pointerType.current === "touch";
    const isTouchFirst = isTouch && touchArmedNodeId.current !== node.id;
    pointerType.current = null;

    if (isTouchFirst) {
      touchArmedNodeId.current = node.id;
      setActive(node);
      return;
    }
    touchArmedNodeId.current = null;
    window.location.href = node.href;
  };

  return (
    <main className={styles.page}>
      <header className={styles.header}>
        <a href="/" className={styles.back}>← AkashicNET.org</a>
        <p>Living Library · Interactive Map</p>
      </header>

      <section className={styles.intro}>
        <p className={styles.eyebrow}>A rainforest of questions, sources and relationships</p>
        <h1>The Living Tree of Knowledge</h1>
        <p>Explore branches, reviewed fruit and governance roots. The artwork is an ecological metaphor—not scientific evidence. Select once to learn; select again to open on touch devices.</p>
      </section>

      <section className={styles.mapSection} aria-labelledby="map-heading">
        <h2 id="map-heading" className={styles.srOnly}>Interactive AkashicNET knowledge map</h2>
        <div className={styles.mapFrame}>
          <img
            src="/images/akashicnet-living-library-tree.webp"
            alt="A luminous rainforest Tree of Knowledge whose branches represent AkashicNET topics and whose roots represent evidence, provenance, privacy, rights, cultural sovereignty, uncertainty, adjudication and accessibility."
            className={styles.tree}
          />
          <div className={styles.hotspots} aria-label="Knowledge-map destinations">
            {nodes.map((node) => (
              <button
                key={node.id}
                type="button"
                className={`${styles.hotspot} ${styles[node.kind]} ${active?.id === node.id ? styles.active : ""}`}
                style={{ left:`${node.x}%`, top:`${node.y}%` }}
                aria-label={`${node.label}: ${node.note}`}
                aria-pressed={active?.id === node.id}
                onPointerDown={(event) => { pointerType.current = event.pointerType; }}
                onPointerEnter={(event) => {
                  if (event.pointerType === "mouse" || event.pointerType === "pen") {
                    touchArmedNodeId.current = null;
                    setActive(node);
                  }
                }}
                onPointerCancel={() => { pointerType.current = null; }}
                onFocus={() => preview(node)}
                onClick={(event) => choose(event, node)}
              >
                <span>{node.label}</span>
              </button>
            ))}
          </div>
        </div>

        <div className={styles.detail} aria-live="polite">
          {active ? (
            <>
              <p className={styles.detailType}>{active.kind === "root" ? "Governance root" : active.kind === "garden" ? "Inquiry garden" : "Knowledge branch"}</p>
              <h2>{active.label}</h2>
              <p>{active.note}</p>
              {active.evidence && <p className={styles.evidenceTag}>{active.evidence}</p>}
              <a href={active.href}>Open {active.label} →</a>
            </>
          ) : (
            <>
              <p className={styles.detailType}>How to explore</p>
              <h2>Choose a glowing node</h2>
              <p>Hover, focus or tap a branch or root to see its meaning and destination.</p>
            </>
          )}
        </div>
      </section>

      <section id="metta-search-garden" className={styles.gardenSection}>
        <p className={styles.eyebrow}>Mettā Search Garden</p>
        <h2>Leaves inquire. Roots verify and protect.</h2>
        <div className={styles.cycle} aria-label="Inquiry lifecycle">
          {["Seed","Leaf","Branch","Trunk","Roots","Bloom","Fruit"].map((step, i) => <span key={step}><b>{String(i + 1).padStart(2,"0")}</b>{step}</span>)}
        </div>
        <p>The proposed garden records anonymous aggregate patterns, not people. Inquiries are classified and counted without publishing raw searches. Only sufficiently reviewed, rights-safe and privacy-safe material can become public fruit.</p>
      </section>

      <section className={styles.legend} aria-labelledby="legend-title">
        <h2 id="legend-title">Evidence colours</h2>
        <div>{evidenceLegend.map(([label,tone]) => <span key={label} className={styles[tone]}>{label}</span>)}</div>
        <p>Colour describes the evidence lane. It does not rank a person, culture or experience.</p>
      </section>

      <nav className={styles.fallback} aria-labelledby="all-destinations">
        <h2 id="all-destinations">All destinations</h2>
        <ul>{nodes.map(node => <li key={node.id}><a href={node.href}>{node.label}</a><span>{node.note}</span></li>)}</ul>
      </nav>
    </main>
  );
}
