import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Space Exploration Agent',
  description: 'AI-powered space exploration research assistant with DALL-E image generation',
  keywords: ['AI', 'Space Exploration', 'NASA', 'DALL-E', 'LangGraph', 'Astronomy'],
  authors: [{ name: 'Space Exploration Agent Team' }],
  openGraph: {
    title: 'Space Exploration Agent',
    description: 'AI-powered space exploration research assistant',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
          {children}
        </div>
      </body>
    </html>
  );
} 