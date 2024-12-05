// Definir a URL base da API usando a variável de ambiente
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Função para lidar com erros da API
const handleError = async (response) => {
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || 'Erro na requisição à API');
  }
};

// Função para analisar notícias
export const analyzeNews = async (title, content) => {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze-news`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title, content }),
    });
    await handleError(response);
    const data = await response.json();
    return data.analysis;
  } catch (error) {
    throw new Error(`Erro ao analisar a notícia: ${error.message}`);
  }
};

// Função para obter previsão (exemplo: previsão de dados financeiros)
export const getPrevision = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/get-prevision`);
    await handleError(response);
    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error(`Erro ao obter previsão: ${error.message}`);
  }
};

// Função para obter dados de ações (BBAS3)
export const getStockData = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/stock`);
    await handleError(response);
    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error(`Erro ao obter dados de ações: ${error.message}`);
  }
};

// Função para obter dados técnicos em um intervalo de datas
export const getTechnicalData = async (startDate, endDate) => {
  try {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);

    const response = await fetch(`${API_BASE_URL}/technical-data?${params.toString()}`);
    await handleError(response);
    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error(`Erro ao obter dados técnicos: ${error.message}`);
  }
};

// Função para obter dados fundamentalistas de um ano específico
export const getFundamentalData = async (year) => {
  try {
    const response = await fetch(`${API_BASE_URL}/fundamental-data?year=${year}`);
    await handleError(response);
    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error(`Erro ao obter dados fundamentalistas: ${error.message}`);
  }
};

// Função para obter indicadores de uma ação (exemplo: RSI, MACD, etc.)
export const getIndicators = async (stockSymbol) => {
  try {
    const response = await fetch(`${API_BASE_URL}/indicators?symbol=${stockSymbol}`);
    await handleError(response);
    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error(`Erro ao obter indicadores: ${error.message}`);
  }
};