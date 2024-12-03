'use client';

import Link from 'next/link';

export default function NewsPage() {
  const staticNews = [
    {
      title: "Banco do Brasil Anuncia Lucro Recorde no Trimestre",
      description: "O Banco do Brasil teve um aumento de 12% no lucro no último trimestre, impulsionado pela alta nas taxas de juros e crescimento no crédito.",
      source: "Fonte: G1",
      url: "#"
    },
    {
      title: "Bolsa de Valores Brasileira Passa por Alta Volatilidade",
      description: "O Ibovespa apresentou grande volatilidade nos últimos dias, refletindo as tensões no cenário político e econômico.",
      source: "Fonte: UOL",
      url: "#"
    },
    {
      title: "Taxa Selic e Impactos no Mercado de Ações",
      description: "A decisão do Banco Central de manter a taxa Selic elevada tem gerado incertezas nos investidores da B3.",
      source: "Fonte: Exame",
      url: "#"
    },
    {
      title: "Cenário do Agronegócio Brasileiro: Expectativas para 2024",
      description: "O agronegócio no Brasil segue sendo um pilar importante da economia, com boas expectativas para o ano seguinte.",
      source: "Fonte: Valor Econômico",
      url: "#"
    }
  ];

  return (
    <div className="bg-gray-900 text-white"> {/* Fundo escuro para toda a página */}
      {/* Seção de Últimas Notícias */}
      <section className="py-16">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-3xl font-semibold mb-6 text-center">Últimas Notícias</h2>

          {/* Mapeando as notícias estáticas */}
          <div>
            {staticNews.map((article, index) => (
              <div key={index} className="mb-8 bg-gray-800 p-6 rounded-lg shadow-md hover:bg-gray-700 transition-all">
                <h3 className="text-xl font-semibold">{article.title}</h3>
                <p className="text-lg mb-4">{article.description}</p>
                <p className="text-sm text-gray-400">Fonte: {article.source}</p>
                <Link href={article.url} passHref>
                  <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-all">
                    Ler mais
                  </button>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
