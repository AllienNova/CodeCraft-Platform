import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Codopia - Code Your Future, Change Your World",
  description: "Transform children into confident programmers through magical, age-appropriate learning experiences. Where coding feels like play, but builds real skills.",
  keywords: ["coding for kids", "programming education", "STEM learning", "children coding", "educational technology"],
  authors: [{ name: "Codopia Team" }],
  creator: "Codopia",
  publisher: "Codopia",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'),
  openGraph: {
    title: "Codopia - Code Your Future, Change Your World",
    description: "Transform children into confident programmers through magical, age-appropriate learning experiences.",
    url: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000',
    siteName: "Codopia",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Codopia - Coding Education for Children",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Codopia - Code Your Future, Change Your World",
    description: "Transform children into confident programmers through magical, age-appropriate learning experiences.",
    images: ["/og-image.png"],
    creator: "@codopia",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  verification: {
    google: "your-google-verification-code",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} antialiased`}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
