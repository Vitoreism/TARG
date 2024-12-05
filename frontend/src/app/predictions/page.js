'use client';

import { useState } from 'react';
import { getTechnicalData } from '../api'; // Supondo que a função getTechnicalData esteja em um arquivo chamado api.js

const TechnicalDataPage = () => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [technicalData, setTechnicalData] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Chama a função getTechnicalData com as datas fornecidas
      const result = await getTechnicalData(startDate, endDate);
      setTechnicalData(result);  // Armazena os dados técnicos retornados
      setError(null); // Limpar qualquer erro anterior
    } catch (err) {
      setError(err.message);  // Define a mensagem de erro em caso de falha
      setTechnicalData(null); // Limpa os dados técnicos anteriores em caso de erro
    }
  };

  return (
    <div>
      <h1>Teste de Dados Técnicos</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="startDate">Data Inicial:</label>
          <input
            type="date"
            id="startDate"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="endDate">Data Final:</label>
          <input
            type="date"
            id="endDate"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </div>
        <button type="submit">Obter Dados Técnicos</button>
      </form>

      {error && <p style={{ color: 'red' }}>Erro: {error}</p>}
      
      {technicalData && (
        <div>
          <h3>Dados Técnicos</h3>
          <p><strong>Data:</strong> {technicalData.Date}</p>
          <p><strong>Preço de Fechamento:</strong> {technicalData.Close}</p>
          <p><strong>RSI:</strong> {technicalData.RSI}</p>
          <p><strong>MACD:</strong> {technicalData.MACD}</p>
          <p><strong>Volume:</strong> {technicalData.Volume}</p>
        </div>
      )}
    </div>
  );
};

export default TechnicalDataPage;
