import Header from '@/components/layout/Header';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'MapStack - モダンな学習プラットフォーム',
  description: 'AIを活用した体系的な学習パスを提供するプラットフォーム',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body className={inter.className}>
        <Providers>
          <Header />
          <main>{children}</main>
          <footer className="bg-gray-100 py-6">
            <div className="container mx-auto px-4 text-center text-gray-600">
              <p>© {new Date().getFullYear()} MapStack. All rights reserved.</p>
            </div>
          </footer>
        </Providers>
      </body>
    </html>
  );
}
