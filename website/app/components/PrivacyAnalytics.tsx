import Script from "next/script";

/**
 * Privacy-safe aggregate analytics.
 *
 * The beacon is loaded only when NEXT_PUBLIC_CLOUDFLARE_ANALYTICS_TOKEN is
 * configured by the deployment environment. No token is committed to source.
 * Cloudflare Web Analytics is used here specifically to avoid cookies and
 * cross-site user profiling in the AkashicNET website layer.
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
