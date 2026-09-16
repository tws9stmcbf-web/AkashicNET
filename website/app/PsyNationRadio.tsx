"use client";

import { useMemo, useState } from "react";

type Episode = {
  id: string;
  number: string;
  title: string;
  guest: string;
  distinction: string;
  provider: "Apple Podcasts" | "SoundCloud" | "YouTube";
  embedUrl: string;
  sourceUrl: string;
  height: number;
};

const referral = "utm_source=akashicnet.org&utm_medium=referral&utm_campaign=psy_nation_radio";

const episodes: Episode[] = [
  {
    id: "100",
    number: "#100",
    title: "Centenary transmission",
    guest: "Liquid Ace · Liquid Soul & Ace Ventura",
    distinction: "Featured milestone",
    provider: "Apple Podcasts",
    embedUrl: "https://embed.podcasts.apple.com/us/podcast/psy-nation-radio-100-incl-liquid-ace-mix-liquid-soul/id1331677285?i=1000760364629",
    sourceUrl: `https://podcasts.apple.com/us/podcast/psy-nation-radio-100-incl-liquid-ace-mix-liquid-soul/id1331677285?i=1000760364629&${referral}`,
    height: 175,
  },
  {
    id: "73",
    number: "#073",
    title: "Astrix guest mix",
    guest: "Astrix",
    distinction: "Community standout · 56K YouTube views when reviewed",
    provider: "YouTube",
    embedUrl: "https://www.youtube-nocookie.com/embed/xL7quVb9jfE?rel=0&modestbranding=1&origin=https%3A%2F%2Fakashicnet.org&widget_referrer=https%3A%2F%2Fakashicnet.org",
    sourceUrl: `https://www.youtube.com/watch?v=xL7quVb9jfE&${referral}`,
    height: 360,
  },
  {
    id: "85",
    number: "#085",
    title: "GMS guest mix",
    guest: "GMS",
    distinction: "SoundCloud selection",
    provider: "SoundCloud",
    embedUrl: "https://w.soundcloud.com/player/?url=https%3A%2F%2Fsoundcloud.com%2Fpsynationradio%2Fpsy-nation-radio-085-incl-gms%3Futm_source%3Dakashicnet.org%26utm_medium%3Dreferral%26utm_campaign%3Dpsy_nation_radio&color=%23c463ff&auto_play=false&hide_related=true&show_comments=false&show_user=true&show_reposts=false&show_teaser=false&visual=false",
    sourceUrl: `https://soundcloud.com/psynationradio/psy-nation-radio-085-incl-gms?${referral}`,
    height: 166,
  },
  {
    id: "98",
    number: "#098",
    title: "Pixel guest mix",
    guest: "Pixel",
    distinction: "Late-series favourite",
    provider: "YouTube",
    embedUrl: "https://www.youtube-nocookie.com/embed/6sWpkO-1JpI?rel=0&modestbranding=1&origin=https%3A%2F%2Fakashicnet.org&widget_referrer=https%3A%2F%2Fakashicnet.org",
    sourceUrl: `https://www.youtube.com/watch?v=6sWpkO-1JpI&${referral}`,
    height: 360,
  },
  {
    id: "102",
    number: "#102",
    title: "DJ Chicago tribute",
    guest: "Liquid Soul & Ace Ventura",
    distinction: "Special tribute",
    provider: "Apple Podcasts",
    embedUrl: "https://embed.podcasts.apple.com/us/podcast/psy-nation-radio-102-incl-drip-drop-mix-liquid-soul/id1331677285?i=1000771076400",
    sourceUrl: `https://podcasts.apple.com/us/podcast/psy-nation-radio-102-incl-drip-drop-mix-liquid-soul/id1331677285?i=1000771076400&${referral}`,
    height: 175,
  },
  {
    id: "103",
    number: "#103",
    title: "Atmos guest mix",
    guest: "Atmos",
    distinction: "Artist spotlight",
    provider: "Apple Podcasts",
    embedUrl: "https://embed.podcasts.apple.com/us/podcast/psy-nation-radio-103-incl-atmos-mix-ace-ventura-liquid-soul/id1331677285?i=1000776047107",
    sourceUrl: `https://podcasts.apple.com/us/podcast/psy-nation-radio-103-incl-atmos-mix-ace-ventura-liquid-soul/id1331677285?i=1000776047107&${referral}`,
    height: 175,
  },
  {
    id: "105",
    number: "#105",
    title: "Blazy guest mix",
    guest: "Blazy",
    distinction: "Recent transmission",
    provider: "Apple Podcasts",
    embedUrl: "https://embed.podcasts.apple.com/us/podcast/psy-nation-radio-105-incl-blazy-mix-ace-ventura-liquid-soul/id1331677285?i=1000787536456",
    sourceUrl: `https://podcasts.apple.com/us/podcast/psy-nation-radio-105-incl-blazy-mix-ace-ventura-liquid-soul/id1331677285?i=1000787536456&${referral}`,
    height: 175,
  },
];

const bars = Array.from({ length: 24 }, (_, index) => index);

export default function PsyNationRadio() {
  const [selectedId, setSelectedId] = useState("100");
  const [loaded, setLoaded] = useState(false);
  const selected = useMemo(
    () => episodes.find((episode) => episode.id === selectedId) ?? episodes[0],
    [selectedId],
  );

  function chooseEpisode(id: string) {
    setSelectedId(id);
    setLoaded(false);
  }

  return (
    <section className="psy-radio" aria-labelledby="psy-radio-title">
      <div className="psy-radio__halo" aria-hidden="true" />
      <div className="psy-radio__identity">
        <img
          src="/images/psy-nation-radio-listening-portal.png"
          alt="Original AkashicNET Psy-Nation Radio listening portal badge with a cosmic radio-wave mandala."
          loading="lazy"
          decoding="async"
        />
        <div>
          <p className="section-label">Culture · Conscious listening</p>
          <h2 id="psy-radio-title">Psy-Nation Radio listening portal</h2>
          <p>
            Begin with the centenary transmission, or choose a notable episode from the official archive.
            The selectors are curated signposts—not a definitive popularity ranking.
          </p>
        </div>
      </div>

      <div className="psy-radio__console">
        <div className="psy-radio__selection">
          <label htmlFor="psy-radio-episode">Choose an episode</label>
          <select
            id="psy-radio-episode"
            value={selectedId}
            onChange={(event) => chooseEpisode(event.target.value)}
          >
            {episodes.map((episode) => (
              <option key={episode.id} value={episode.id}>
                {episode.number} · {episode.guest} · {episode.distinction}
              </option>
            ))}
          </select>

          <div className="psy-radio__now" aria-live="polite">
            <span>{selected.distinction}</span>
            <strong>{selected.number} · {selected.title}</strong>
            <p>{selected.guest} · hosted by {selected.provider}</p>
          </div>

          <div className="psy-radio__links">
            <a
              href={selected.sourceUrl}
              target="_blank"
              rel="noopener"
              referrerPolicy="strict-origin-when-cross-origin"
            >
              Open on {selected.provider} ↗
            </a>
            <a
              href={`https://soundcloud.com/psynationradio?${referral}`}
              target="_blank"
              rel="noopener"
              referrerPolicy="strict-origin-when-cross-origin"
            >
              Official SoundCloud archive ↗
            </a>
          </div>
        </div>

        <div className="psy-radio__player">
          <div className={`psy-radio__equalizer ${loaded ? "is-active" : ""}`} aria-hidden="true">
            {bars.map((bar) => <i key={bar} />)}
          </div>
          <p className="psy-radio__visual-note">
            Artistic playback visualisation · not a measured audio spectrum
          </p>

          {loaded ? (
            <iframe
              key={selected.id}
              src={selected.embedUrl}
              title={`Psy-Nation Radio ${selected.number} on ${selected.provider}`}
              height={selected.height}
              loading="lazy"
              allow="autoplay; encrypted-media; fullscreen; picture-in-picture"
              sandbox="allow-forms allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-presentation"
              referrerPolicy="strict-origin-when-cross-origin"
              allowFullScreen
            />
          ) : (
            <div className="psy-radio__consent">
              <strong>Ready when you are.</strong>
              <p>
                Loading connects your browser to {selected.provider}, which may receive your IP address,
                the AkashicNET site origin and its own cookies according to its privacy policy.
              </p>
              <button type="button" onClick={() => setLoaded(true)}>
                Load {selected.provider} player
              </button>
            </div>
          )}
        </div>
      </div>

      <p className="psy-radio__boundary">
        Independent listening gateway. Audio remains hosted by its original platform; AkashicNET does not
        copy or re-host it. Outbound links carry a non-personal AkashicNET referral tag so hosts may identify
        this portal as the source.
      </p>
    </section>
  );
}
