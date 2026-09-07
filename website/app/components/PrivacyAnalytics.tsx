"use client";

import { useEffect } from "react";

const BEACON_SRC = "https://static.cloudflareinsights.com/beacon.min.js";
const BEACON_SELECTOR = 'script[src^="https://static.cloudflareinsights.com/beacon.min.js"]';

/**
 * Opt-in, aggregate operational telemetry.
 *
 * No beacon is created unless the deployment supplies the public Cloudflare Web
 * Analytics token. Existing Cloudflare beacon markup wins, preventing duplicate
 * collection when the hosting layer already injects it.
 */
export default function PrivacyAnalytics() {
  const token = process.env.NEXT_PUBLIC_CLOUDFLARE_ANALYTICS_TOKEN;

  useEffect(() => {
    if (!token || document.querySelector(BEACON_SELECTOR)) return;

    const beacon = document.createElement("script");
    beacon.src = BEACON_SRC;
    beacon.defer = true;
    beacon.dataset.cfBeacon = JSON.stringify({ token });
    beacon.dataset.akashicnetTelemetry = "aggregate-operational-only";
    document.body.appendChild(beacon);

    return () => {
      beacon.remove();
    };
  }, [token]);

  return null;
}
