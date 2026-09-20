"use client";

import { useEffect, useState } from "react";
import styles from "./symbiosis.module.css";

const visions = [
  { title: "Symbiosis", line: "We are not alone. We are interconnected.", image: "/images/akashicnet-portal-to-infinity-7d-hero.webp", href: "/akashicomni" },
  { title: "Co-Evolution", line: "Together we evolve.", image: "/images/akashicnet-living-library-tree.webp", href: "/living-library-map" },
  { title: "Shared Tomorrow", line: "A brighter future is a shared creation.", image: "/images/akashicvision-nde-merkaba-flower-of-life.webp", href: "/akashicvision" },
  { title: "Knowledge", line: "Bridging worlds. Expanding minds.", image: "/images/akashicomni-metadimensional-gateway.webp", href: "/big-questions" },
  { title: "United Humanity", line: "Many cultures. One family.", image: "/images/akashicnet-toroidal-love-logo.png", href: "/metta-awareness" },
  { title: "Conscious Planet", line: "A living Earth. A thriving future.", image: "/images/akn24-global-food-shortages.webp", href: "/insights/global-food-shortages-one-step-back-two-steps-forward" },
] as const;

const nav = [
  ["Explore", "/#latest-highlights"],
  ["Library", "/living-library-map"],
  ["Research", "/big-questions"],
  ["Initiatives", "/akashicomni"],
  ["Community", "/community"],
  ["About", "/about"],
] as const;

export default function AkashicSymbiosisGallery() {
  const [active, setActive] = useState(0);
  const [autoPlay, setAutoPlay] = useState(false);

  const move = (delta: number) =>
    setActive((current) => (current + delta + visions.length) % visions.length);

  useEffect(() => {
    if (!autoPlay) return;
    const timer = window.setInterval(() => move(1), 6500);
    return () => window.clearInterval(timer);
  }, [autoPlay]);

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "ArrowLeft") move(-1);
      if (event.key === "ArrowRight") move(1);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const vision = visions[active];

  return (
    <main className={styles.page}>
      <header className={styles.nav}>
        <a className={styles.brand} href="/" aria-label="AkashicNET home">
          <img src="/images/akashicnet-toroidal-love-logo.png" alt="" />
          <span>AKASHICNET</span>
        </a>
        <nav aria-label="AkashicNET">
          {nav.map(([label, href]) => <a key={label} href={href}>{label}</a>)}
        </nav>
        <a className={styles.infinity} href="/" aria-label="AkashicNET home">∞</a>
      </header>

      <section className={styles.hero}>
        <p className={styles.eyebrow}>Different perspectives. One interconnected future.</p>
        <h1>Akashic <em>Symbiosis</em></h1>
        <p className={styles.sequence}>Six Visions of Symbiosis → Co-Evolution → Shared Tomorrow → Knowledge → United Humanity → Conscious Planet ♾️</p>
      </section>

      <section className={styles.gallery} aria-label="Six visions of Akashic Symbiosis">
        <button className={styles.arrow} onClick={() => move(-1)} aria-label="Previous vision">‹</button>
        <article className={styles.stage}>
          <span className={styles.counter}>{active + 1} / {visions.length}</span>
          <img src={vision.image} alt={vision.title + " — Akashic Symbiosis conceptual artwork"} />
          <div className={styles.caption}>
            <small>{String(active + 1).padStart(2, "0")}</small>
            <h2>{vision.title}</h2>
            <p>{vision.line}</p>
            <a href={vision.href}>Explore this vision →</a>
          </div>
        </article>
        <button className={styles.arrow} onClick={() => move(1)} aria-label="Next vision">›</button>
      </section>

      <div className={styles.thumbs} role="tablist" aria-label="Choose a vision">
        {visions.map((item, index) => (
          <button key={item.title} onClick={() => setActive(index)} className={index === active ? styles.selected : ""} role="tab" aria-selected={index === active}>
            <img src={item.image} alt="" />
            <span>{index + 1}. {item.title}</span>
          </button>
        ))}
      </div>

      <div className={styles.controls}>
        <button onClick={() => setAutoPlay((value) => !value)} aria-pressed={autoPlay}>{autoPlay ? "❚❚ Pause" : "▶ Auto Play"}</button>
        <button onClick={() => document.documentElement.requestFullscreen?.()}>⛶ Full Screen</button>
        <a href="/living-library-map">View Living Library →</a>
      </div>

      <blockquote>“Symbiosis is not just an idea — it is a pathway to a more conscious, connected and compassionate world.”</blockquote>

      <footer className={styles.footer}>
        <span>Boundless Awareness Is Infinite Love ♾️</span>
        <span>Explore · Learn · Connect · Co-create</span>
      </footer>
    </main>
  );
}
