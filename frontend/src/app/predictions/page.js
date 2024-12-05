'use client';

import { useState } from 'react';
import { analyzeNews } from '../api'; // Supondo que a função analyzeNews esteja em um arquivo chamado api.js

const TestPage = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await analyzeNews(title, content);
      setAnalysis(result);
      setError(null); // Limpar qualquer erro anterior
    } catch (err) {
      setError(err.message);
      setAnalysis(null); // Limpar análise anterior em caso de erro
    }
  };

  return (
    <div>
      <h1>Teste de Análise de Notícias</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="title">Título da Notícia:</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="content">Conteúdo da Notícia:</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
          />
        </div>
        <button type="submit">Analisar Notícia</button>
      </form>

      {error && <p style={{ color: 'red' }}>Erro: {error}</p>}
      {analysis && (
        <div>
          <h3>Resultado da Análise:</h3>
          <p>{analysis}</p>
        </div>
      )}
    </div>
  );
};

export default TestPage;
