import type { Metadata } from "next";
import "./globals.css";
import PrivacyAnalytics from "./components/PrivacyAnalytics";

export const metadata: Metadata = {
  title: "AkashicNET — A Living Knowledge Network",
  description:
    "Explore the vision, architecture, ethical commitments and public roadmap of AkashicNET — a human-governed knowledge network for consciousness, evidence and planetary flourishing.",
  icons: {
    icon: "/images/akashicnet-toroidal-love-logo.png",
    shortcut: "/images/akashicnet-toroidal-love-logo.png",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        {children}
        <PrivacyAnalytics />
      </body>
    </html>
  );
}
