import type { Metadata } from "next";
import type { ReactNode } from "react";
import { locale, messages } from "@/i18n";
import { Providers } from "./providers";
import "./globals.css";

export const metadata: Metadata = { title: messages.app.name, description: messages.app.description };

export default function RootLayout({ children }: { children: ReactNode }) {
  return <html lang={locale}><body><Providers>{children}</Providers></body></html>;
}
