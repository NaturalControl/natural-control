import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Natural Control",
  description: "Voice supervision of a computer agent for blind and visually impaired users.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
