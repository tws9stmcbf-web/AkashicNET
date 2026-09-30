import type { Metadata } from "next";
import { headers } from "next/headers";
import "./globals.css";

export const metadata: Metadata = {
  title: "AkashicNET — A Living Knowledge Network",
  description:
    "Explore the vision, architecture, ethical commitments and public roadmap of AkashicNET — a human-governed knowledge network for consciousness, evidence and planetary flourishing.",
  icons: {
    icon: "/images/akashicnet-toroidal-love-logo.png",
    shortcut: "/images/akashicnet-toroidal-love-logo.png",
  },
};

export default async function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const requestedLanguage = (await headers()).get("x-akashicnet-document-language");
  const language = ["de", "es", "pt-BR", "fr"].includes(requestedLanguage ?? "")
    ? requestedLanguage! : "en";
  return <html lang={language}><body>{children}</body></html>;
}
