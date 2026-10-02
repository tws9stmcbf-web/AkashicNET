"use client";

import { useEffect, useMemo, useState } from "react";

import styles from "./NewsDeskTicker.module.css";
import type { NewsroomItem } from "./newsroom";

const UTC_TIMESTAMP = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/;

function formatStamp(value: string): string {
  if (!UTC_TIMESTAMP.test(value)) return "Timestamp unavailable";
  return new Date(value).toLocaleString("en-GB", {
    timeZone: "UTC",
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }) + " UTC";
}

type Props = {
  readonly items: readonly NewsroomItem[];
  readonly kindnessItems: readonly NewsroomItem[];
  readonly snapshotTimestamp: string;
};

export default function NewsDeskTicker({ items, kindnessItems, snapshotTimestamp }: Props) {
  const [isPaused, setIsPaused] = useState(false);
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);
  const [isInteracting, setIsInteracting] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    const syncPreference = () => setPrefersReducedMotion(mediaQuery.matches);
    syncPreference();
    if (typeof mediaQuery.addEventListener === "function") {
      mediaQuery.addEventListener("change", syncPreference);
      return () => mediaQuery.removeEventListener("change", syncPreference);
    }
    mediaQuery.addListener(syncPreference);
    return () => mediaQuery.removeListener(syncPreference);
  }, []);

  const shouldRenderStatic = prefersReducedMotion || items.length <= 1;
  const trackPaused = shouldRenderStatic || isPaused || isInteracting;
  const marqueeItems = useMemo(() => items, [items]);

  return (
    <section className={styles.shell} aria-label="Insights newsroom latest 24 hours">
      <div className={styles.broadcastCard}>
        <div className={styles.header}>
          <div className={styles.labelRow}>
            <span className={styles.broadcastLabel}>
              <span className={styles.bug} aria-label="AkashicNET News 24">AKN24</span>
              <span className={styles.expandedLabel}>AkashicNET News 24</span>
            </span>
            <strong>LATEST 24 HOURS</strong>
            <span className={styles.snapshot}>Static newsroom snapshot through {formatStamp(snapshotTimestamp)}. No live telemetry implied.</span>
          </div>
          <button
            className={styles.toggle}
            type="button"
            onClick={() => setIsPaused((value) => !value)}
            aria-pressed={isPaused}
            aria-label={isPaused ? "Play newsroom strip" : "Pause newsroom strip"}
            disabled={shouldRenderStatic}
          >
            {shouldRenderStatic ? "Static" : isPaused ? "Play" : "Pause"}
          </button>
        </div>

        {shouldRenderStatic ? (
          <ul className={styles.staticList}>
            {items.map((item) => (
              <li key={item.id} className={styles.staticItem}>
                <span className={styles.bug} aria-label="AkashicNET News 24">AKN24</span>
                <span className={styles.category}>{item.category}</span>
                <a className={styles.storyLink} href={item.sourceUrl}>{item.headline}</a>
                <p className={styles.summary}>{item.shortSummary}</p>
                <p className={styles.meta}>Source {formatStamp(item.sourceTimestamp)} · Published {formatStamp(item.publishedAt)} · Updated {formatStamp(item.updatedAt)} · {item.evidenceLabel}</p>
              </li>
            ))}
          </ul>
        ) : (
          <div
            className={styles.window}
            onMouseEnter={() => setIsInteracting(true)}
            onMouseLeave={() => setIsInteracting(false)}
            onFocusCapture={() => setIsInteracting(true)}
            onBlurCapture={(event) => {
              if (!event.currentTarget.contains(event.relatedTarget as Node | null)) {
                setIsInteracting(false);
              }
            }}
          >
            <div className={`${styles.track} ${trackPaused ? styles.trackPaused : ""}`}>
              <ul className={styles.list}>
                {marqueeItems.map((item) => (
                  <li key={item.id} className={styles.item}>
                    <span className={styles.bug} aria-label="AkashicNET News 24">AKN24</span>
                    <span className={styles.category}>{item.category}</span>
                    <a className={styles.storyLink} href={item.sourceUrl}>{item.headline}</a>
                    <p className={styles.summary}>{item.shortSummary}</p>
                    <p className={styles.meta}>Source {formatStamp(item.sourceTimestamp)} · Published {formatStamp(item.publishedAt)} · Updated {formatStamp(item.updatedAt)} · {item.evidenceLabel}</p>
                  </li>
                ))}
              </ul>
              <ul className={styles.list} aria-hidden="true">
                {marqueeItems.map((item) => (
                  <li key={`${item.id}-duplicate`} className={styles.item}>
                      <span className={styles.bug} aria-label="AkashicNET News 24">AKN24</span>
                      <span className={styles.category}>{item.category}</span>
                      <span className={styles.storyLink}>{item.headline}</span>
                      <p className={styles.summary}>{item.shortSummary}</p>
                      <p className={styles.meta}>Source {formatStamp(item.sourceTimestamp)} · Published {formatStamp(item.publishedAt)} · Updated {formatStamp(item.updatedAt)} · {item.evidenceLabel}</p>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        <p className={styles.boundary}><strong>Newsroom boundary:</strong> BQ001 remains UNRESOLVED. AkashicOMNI remains the field-level orchestration frame; AkashicONE is a coherent assessment within it, not a higher evidence tier. No automatic truth, evidence, rights or framework promotion occurs here.</p>

        <aside className={styles.kindnessCard} aria-label="Kindness Across Species segment">
          <div className={styles.kindnessIntro}>
            <span className={styles.kindnessTitle}>Kindness Across Species</span>
            <span className={styles.meta}>Hopeful counterweight · verified items only</span>
          </div>
          {kindnessItems.length ? (
            <ul className={styles.kindnessList}>
              {kindnessItems.map((item) => (
                <li key={item.id} className={styles.kindnessItem}>
                  <span className={styles.kindnessHeading}>{item.kindnessHeading ?? "Communities Cooperating"}</span>
                  <a className={styles.storyLink} href={item.sourceUrl}>{item.headline}</a>
                  <p className={styles.summary}>{item.shortSummary}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p className={styles.kindnessEmpty}>No current publishable Habitat Restored, Wildlife Rescued or Communities Cooperating items appear in this 24-hour window, so this segment stays static rather than overclaiming.</p>
          )}
        </aside>
      </div>
    </section>
  );
}
