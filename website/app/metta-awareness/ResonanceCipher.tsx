"use client";

import { useState } from "react";
import styles from "./metta-awareness.module.css";

const states = [
  { word:"Curiosity", line:"The cat approaches the threshold.", mode:"outside" },
  { word:"Uncertainty", line:"The box holds more than one imagined possibility.", mode:"between" },
  { word:"Observation", line:"Attention changes what becomes visible to the observer.", mode:"inside" },
  { word:"What is love?", line:"The question crosses the field before any answer arrives.", mode:"between" },
  { word:"Mettā", line:"Goodwill meets uncertainty without trying to possess it.", mode:"outside" },
];

export default function ResonanceCipher(){
  const [index,setIndex]=useState(0);
  const state=states[index];

  return (
    <section className={styles.cipher} aria-labelledby="cipher-title">
      <div className={styles.cipherCopy}>
        <p className={styles.label}>2.9D · Personal resonance cipher</p>
        <h2 id="cipher-title">Curiosity opens the box.</h2>
        <p>A playful constellation of private associations translated into public visual language. Recognition is optional. The framework still works without decoding the references.</p>
        <p className={styles.cipherBoundary}>Cultural allusions and altered-state associations are presented as creative and biographical provenance, not evidence of causation or a recommendation to use substances.</p>
      </div>
      <div className={styles.cipherStage}>
        <div className={styles.oceanRings} aria-hidden="true">
          {Array.from({length:12}).map((_,i)=><i key={i}/>)}
        </div>
        <button
          type="button"
          className={styles.catBox}
          data-mode={state.mode}
          onClick={()=>setIndex((index+1)%states.length)}
          aria-describedby="cipher-state"
        >
          <span className={styles.cat} aria-hidden="true"><i/><b/><em>?</em></span>
          <span className={styles.boxLid} aria-hidden="true"/>
          <span className={styles.boxFace} aria-hidden="true">2.5 + 0.4</span>
          <span className={styles.clickHint}>Click the curiosity cipher</span>
        </button>
        <div className={styles.cipherState} id="cipher-state" aria-live="polite">
          <span>{String(index+1).padStart(2,"0")} / 05</span>
          <strong>{state.word}</strong>
          <p>{state.line}</p>
        </div>
        <div className={styles.vapourCircle} aria-hidden="true"/>
      </div>
      <p className={styles.hiddenCaption}>The pointer opens a wormhole, twelve oceans ripple, and the cat remains within and beyond the frame until attention chooses a doorway.</p>
    </section>
  );
}
