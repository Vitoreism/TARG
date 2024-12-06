'use client';

import { useEffect, useState } from "react";
import { getStockData, getTechnicalData } from "../api";

export default function PredictionsPage() {
  const [stockData, setStockData] = useState(null);
  const [historicalData, setHistoricalData] = useState(null);
  const [error, setError] = useState(null);
  const [startDate, setStartDate] = useState(""); 

  const today = new Date().toISOString().split('T')[0]; // Data atual no formato YYYY-MM-DD
  const minDate = "2010-01-01"; // Data mínima a partir de 2010

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
    if (!startDate) {
      setError("Por favor, selecione uma data válida.");
      return;
    }

    try {
      const data = await getTechnicalData(startDate);  // Passa apenas startDate
      if (data) {
        setHistoricalData(data);
        setError(null);
      } else {
        setHistoricalData(null);
        setError("Nenhum dado encontrado para a data selecionada.");
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

      {/* Seção de Indicadores Atuais */}
      <section className="bg-gray-800 py-8 px-6 rounded-lg mb-8">
        <h2 className="text-3xl text-purple-600 mb-4 flex justify-between items-center">
          Indicadores do Dia 
          <span className="text-lg font-semibold text-white">{date}</span>
        </h2>
        <div className="flex space-x-6 justify-between text-lg">
          <div className="flex-1 text-center">
            <h3 className="font-semibold text-lg mb-2">Preço Atual</h3>
            <p>{price}</p>
          </div>
          <div className="flex-1 text-center">
            <h3 className="font-semibold text-lg mb-2">RSI</h3>
            <p>{rsi}</p>
          </div>
          <div className="flex-1 text-center">
            <h3 className="font-semibold text-lg mb-2">MACD</h3>
            <p>{macd}</p>
          </div>
          <div className="flex-1 text-center">
            <h3 className="font-semibold text-lg mb-2">Signal Line</h3>
            <p>{signalLine}</p>
          </div>
        </div>
      </section>

      {/* Seção de Filtro de Datas */}
      <section className="bg-gray-800 py-8 px-6 rounded-lg mb-8">
        <h2 className="text-3xl text-purple-600 mb-4">Filtrar Dados por Data</h2>
        <div className="mb-4">
          <label className="block mb-2">Data:</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="p-2 bg-gray-700 text-white rounded-lg"
            min={minDate}
            max={today} // Limita a data até o dia atual
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
          <h2 className="text-3xl text-purple-600 mb-4">Dados para o Dia Selecionado</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Campos do TechnicalDataResponse */}
            <div className="bg-gray-700 p-4 rounded-lg shadow-lg">
              <p className="text-xl font-semibold">Data</p>
              <p>{historicalData.Date ? new Date(historicalData.Date).toLocaleDateString('pt-BR') : 'N/A'}</p>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg shadow-lg">
              <p className="text-xl font-semibold">Adjusted Close</p>
              <p>{safeNumber(historicalData.Adj_Close)}</p>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg shadow-lg">
              <p className="text-xl font-semibold">Close</p>
              <p>{safeNumber(historicalData.Close)}</p>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg shadow-lg">
              <p className="text-xl font-semibold">High</p>
              <p>{safeNumber(historicalData.High)}</p>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg shadow-lg">
              <p className="text-xl font-semibold">Low</p>
              <p>{safeNumber(historicalData.Low)}</p>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg shadow-lg">
              <p className="text-xl font-semibold">Open</p>
              <p>{safeNumber(historicalData.Open)}</p>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg shadow-lg">
              <p className="text-xl font-semibold">Volume</p>
              <p>{typeof historicalData.Volume === 'number' ? historicalData.Volume : 'N/A'}</p>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg shadow-lg">
              <p className="text-xl font-semibold">Dividendos</p>
              <p>{safeNumber(historicalData.Dividendos)}</p>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg shadow-lg">
              <p className="text-xl font-semibold">RSI</p>
              <p>{safeNumber(historicalData.RSI)}</p>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg shadow-lg">
              <p className="text-xl font-semibold">MACD</p>
              <p>{safeNumber(historicalData.MACD)}</p>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg shadow-lg">
              <p className="text-xl font-semibold">Signal Line</p>
              <p>{safeNumber(historicalData.Signal_Line)}</p>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
