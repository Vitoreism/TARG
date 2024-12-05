'use client';

import { useEffect, useState } from "react";
import { getStockData, getTechnicalData } from "../api";

export default function PredictionsPage() {
  const [stockData, setStockData] = useState(null);
  const [historicalData, setHistoricalData] = useState(null);
  const [error, setError] = useState(null);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  useEffect(() => {
    const fetchStockData = async () => {
      try {
        const data = await getStockData();
        setStockData(data);
      } catch (err) {
        setError("Erro ao carregar dados da ação");
      }
    };

    fetchStockData();
  }, []);

  // Função para formatar números com segurança
  const safeNumber = (val) => (typeof val === 'number' && !isNaN(val)) ? val.toFixed(2) : 'N/A';

  const fetchTechnicalDataByPeriod = async () => {
    if (!startDate || !endDate) {
      setError("Por favor, selecione datas válidas.");
      return;
    }

    try {
      const data = await getTechnicalData(startDate, endDate);
      if (data) {
        setHistoricalData(data);
        setError(null);
      } else {
        setHistoricalData(null);
        setError("Nenhum dado encontrado para o período selecionado.");
      }
    } catch (err) {
      setHistoricalData(null);
      setError("Erro ao carregar dados para o período selecionado.");
    }
  };

  if (error) {
    return <div className="text-center text-red-500">{error}</div>;
  }

  if (!stockData) {
    return <div className="text-center text-white">Carregando...</div>;
  }

  const price = safeNumber(stockData.price);
  const rsi = safeNumber(stockData.rsi);
  const macd = safeNumber(stockData.macd);
  const signalLine = safeNumber(stockData.signal_line);
  const date = stockData.date ? new Date(stockData.date + "T00:00:00").toLocaleDateString('pt-BR') : 'N/A';

  return (
    <div className="bg-gray-900 text-white p-6 min-h-screen flex flex-col">
      {/* Seção de Título e Introdução */}
      <section className="bg-gradient-to-r from-purple-600 to-blue-800 text-center py-12 rounded-lg mb-8">
        <h1 className="text-4xl font-bold mb-4">BBAS3 - Dados e Histórico</h1>
        <p className="text-xl">
          Aqui estão os dados mais recentes sobre a ação BBAS3 e a opção de consultar o histórico de preços e indicadores em um período específico.
        </p>
      </section>

      {/* Seção de Filtro de Datas */}
      <section className="bg-gray-800 py-8 px-6 rounded-lg mb-8">
        <h2 className="text-3xl text-purple-600 mb-4">Filtrar Dados por Período</h2>
        <div className="mb-4">
          <label className="block mb-2">Data Inicial:</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="p-2 bg-gray-700 text-white rounded-lg"
          />
        </div>
        <div className="mb-4">
          <label className="block mb-2">Data Final:</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="p-2 bg-gray-700 text-white rounded-lg"
          />
        </div>
        <button
          onClick={fetchTechnicalDataByPeriod}
          className="bg-gradient-to-r from-purple-600 to-blue-800 text-white py-2 px-6 rounded-lg hover:opacity-80 transition"
        >
          Buscar Dados
        </button>
      </section>

      {/* Seção com Dados do Período Selecionado (se disponíveis) */}
      {historicalData && (
        <section className="bg-gray-800 py-8 px-6 rounded-lg mb-8">
          <h2 className="text-3xl text-purple-600 mb-4">Dados do Período Selecionado</h2>
          <div className="text-lg">
            {/* Campos do TechnicalDataResponse */}
            <p>Data: <span className="font-semibold">{historicalData.Date ? new Date(historicalData.Date).toLocaleDateString('pt-BR') : 'N/A'}</span></p>
            <p>Adj_Close: <span className="font-semibold">{safeNumber(historicalData.Adj_Close)}</span></p>
            <p>Close: <span className="font-semibold">{safeNumber(historicalData.Close)}</span></p>
            <p>High: <span className="font-semibold">{safeNumber(historicalData.High)}</span></p>
            <p>Low: <span className="font-semibold">{safeNumber(historicalData.Low)}</span></p>
            <p>Open: <span className="font-semibold">{safeNumber(historicalData.Open)}</span></p>
            <p>Volume: <span className="font-semibold">{typeof historicalData.Volume === 'number' ? historicalData.Volume : 'N/A'}</span></p>
            <p>Dividendos: <span className="font-semibold">{safeNumber(historicalData.Dividendos)}</span></p>
            <p>RSI: <span className="font-semibold">{safeNumber(historicalData.RSI)}</span></p>
            <p>MACD: <span className="font-semibold">{safeNumber(historicalData.MACD)}</span></p>
            <p>Signal Line: <span className="font-semibold">{safeNumber(historicalData.Signal_Line)}</span></p>
          </div>
        </section>
      )}

      {/* Seção de Indicadores Atuais da Ação BBAS3 */}
      <section className="bg-gray-800 py-8 px-6 rounded-lg">
        <h2 className="text-3xl text-purple-600 mb-4">Indicadores Atuais da Ação BBAS3</h2>
        <div className="text-lg">
          <p>Preço Atual: <span className="font-semibold">{price}</span></p>
          <p>RSI: <span className="font-semibold">{rsi}</span></p>
          <p>MACD: <span className="font-semibold">{macd}</span></p>
          <p>Signal Line: <span className="font-semibold">{signalLine}</span></p>
          <p>Data de Atualização: <span className="font-semibold">{date}</span></p>
        </div>
      </section>
    </div>
  );
}

