"use client";

import { useEffect, useState } from "react";

type TickerItem = { label: string; href: string };

const latest: TickerItem[] = [
  { label: "🌍 Akashic Symbiosis", href: "/akashic-symbiosis" },
  { label: "🧠 AkashicOMNI Update", href: "/akashicomni" },
  { label: "🌌 Big Questions Expand", href: "/big-questions" },
  { label: "🌳 Living Knowledge Map", href: "/living-library-map" },
  { label: "💗 Mettā Awareness", href: "/metta-awareness" },
  { label: "🌐 Global Food Systems", href: "/insights/global-food-shortages-one-step-back-two-steps-forward" },
  { label: "☀️ Schumann Activity Window", href: "/insights/interstellar-weather-schumann-september-2026" },
];

const archive: TickerItem[] = [
  { label: "✨ AkashicVISION", href: "/akashicvision" },
  { label: "💗 Boundless Awareness", href: "/metta-awareness" },
  { label: "🌳 Living Library Origins", href: "/living-library-map" },
  { label: "🌐 Food Systems & Resilience", href: "/insights/global-food-shortages-one-step-back-two-steps-forward" },
  { label: "☀️ Interstellar Weather", href: "/insights/interstellar-weather-schumann-september-2026" },
  { label: "🌀 The Power of the Doctor", href: "/spiritual-sci-fi/power-of-the-doctor" },
];

export function NewsTicker({ variant = "latest" }: { variant?: "latest" | "archive" }) {
  const items = variant === "latest" ? latest : archive;
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(true);

  useEffect(() => {
    if (!playing) return;
    const timer = window.setInterval(() => setIndex((value) => (value + 1) % items.length), variant === "latest" ? 4600 : 6200);
    return () => window.clearInterval(timer);
  }, [items.length, playing, variant]);

  const step = (delta: number) => setIndex((value) => (value + delta + items.length) % items.length);
  const item = items[index];

  return (
    <section className={"news-ticker " + (variant === "archive" ? "news-ticker-archive" : "")} aria-label={variant === "latest" ? "Latest AkashicNET headlines" : "From the AkashicNET archive"}>
      <span className="news-ticker-label">{variant === "latest" ? "NOW" : "♾ FROM THE ARCHIVE"}</span>
      <button type="button" onClick={() => step(-1)} aria-label="Previous headline">‹</button>
      <a className="news-ticker-headline" href={item.href}>{item.label}</a>
      <span className="news-ticker-count" aria-hidden="true">{index + 1}/{items.length}</span>
      <button type="button" onClick={() => step(1)} aria-label="Next headline">›</button>
      <button type="button" className="news-ticker-play" onClick={() => setPlaying((value) => !value)} aria-label={playing ? "Pause headlines" : "Play headlines"} aria-pressed={!playing}>
        {playing ? "❚❚" : "▶"}
      </button>
      {variant === "archive" && <a className="news-ticker-archive-link" href="#latest-highlights">Explore highlights →</a>}
    </section>
  );
}
