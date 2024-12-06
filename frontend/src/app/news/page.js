'use client';

import { useEffect, useState } from "react";
import Link from 'next/link';
import { getNewsLinks, getNewsById, analyzeNews } from "../api";

export default function NewsPage() {
  const [news, setNews] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        // Pega o dicionário de _id e títulos
        const idTitleDict = await getNewsLinks();

        // idTitleDict é algo como { "id1": "Título X", ... }
        // Vamos percorrer cada id e buscar a notícia completa
        const fetchedNews = [];
        for (const [newsId, title] of Object.entries(idTitleDict)) {
          const article = await getNewsById(newsId);
        

          // article deve ter title, content, date, etc.
          // Vamos mapear os campos para o formato desejado no design:
          fetchedNews.push({
            title: article.title,
            description: article.content,
            source: article.date, // usando a data como "Fonte"
            analysis: article.analysis, // Resultado da análise
            url: `/news/${newsId}` // link para a página da notícia
          });
        }

        setNews(fetchedNews);
        setLoading(false);
      } catch (err) {
        setError("Erro ao carregar notícias.");
        setLoading(false);
      }
    };

    fetchNews();
  }, []);

  if (loading) {
    return <div className="text-center text-black mt-12">Carregando notícias...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500">{error}</div>;
  }

  return (
    <div className="bg-gray-900 text-white"> {/* Fundo escuro para toda a página */}
      {/* Seção de Últimas Notícias */}
      <section className="py-16">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-3xl font-semibold mb-6 text-center">Últimas Notícias</h2>

          {/* Mapeando as notícias obtidas da API */}
          <div>
            {news.map((article, index) => (
              <div key={index} className="mb-8 bg-gray-800 p-6 rounded-lg shadow-md hover:bg-gray-700 transition-all">
                <h3 className="text-xl font-semibold">{article.title}</h3>
                <p className="text-lg mb-4">{article.description}</p> {/* Descrição da notícia */}
                <p className="text-sm text-gray-400">Fonte: {article.source}</p>

                {/* Exibe a análise abaixo do título */}
                {article.analysis && (
                  <div className="mt-4 text-gray-300">
                    <strong>Análise:</strong>
                    <p>{article.analysis}</p>
                  </div>
                )}

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
