import Script from "next/script";

/**
 * Optional, aggregate-only Cloudflare Web Analytics.
 *
 * The beacon is absent unless the deployment supplies a site token. The token
 * is configuration, not evidence, and must never be committed to the repository.
 */
export default function PrivacyAnalytics() {
  const token = process.env.NEXT_PUBLIC_CLOUDFLARE_ANALYTICS_TOKEN;

  if (!token) return null;

  return (
    <Script
      id="akashicnet-privacy-analytics"
      src="https://static.cloudflareinsights.com/beacon.min.js"
      strategy="afterInteractive"
      data-cf-beacon={JSON.stringify({ token })}
    />
  );
}
