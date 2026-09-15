import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AkashicNET — Portal to Infinity",
  description:
    "Enter AkashicNET: Portal to Infinity — a human-governed, evidence-aware knowledge network connecting consciousness, meta-intelligence, metta and planetary flourishing.",
  icons: {
    icon: "/images/akashicnet-toroidal-love-logo.png",
    shortcut: "/images/akashicnet-toroidal-love-logo.png",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
