import './globals.css';
import Link from 'next/link';
import Image from 'next/image';
import { IBM_Plex_Sans } from 'next/font/google';

const ibmPlexSans = IBM_Plex_Sans({ subsets: ['latin'], weight: ['400', '600'] });

export const metadata = {
  title: 'TARG',
  description: 'Portal de notícias e previsões para a bolsa de ações brasileira',
};

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <head>
        <link rel="icon" href="/just_image.png" type="image/png"/>
      </head>
      <body className={`${ibmPlexSans.className}`}>
        <nav className="bg-gray-800 fixed top-0 w-full shadow-md z-50">
          <div className="container mx-auto px-4 py-4 flex justify-between items-center h-20">
            <Link href="/">
              <Image
                src="/logo-removebg.png"
                alt="Logo"
                width={120}
                height={120}
                className="max-h-28 w-auto"
              />
            </Link>
            <ul className="flex space-x-6">
              <li>
                <Link href="/" className="text-gray-300 hover:text-white">
                  Início
                </Link>
              </li>
              <li>
                <Link href="/news" className="text-gray-300 hover:text-white">
                  Notícias
                </Link>
              </li>
              <li>
                <Link href="/predictions" className="text-gray-300 hover:text-white">
                  Indicadores
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-gray-300 hover:text-white">
                  Sobre
                </Link>
              </li>
            </ul>
          </div>
        </nav>
        <main className="pt-16">{children}</main>
      </body>
    </html>
  );
}
