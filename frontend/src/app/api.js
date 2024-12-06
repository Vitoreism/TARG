import axios from "axios";

const baseURL = "http://localhost:8000"; // Ajuste se necessário

// Função para obter o dicionário de _id e títulos
export const getNewsLinks = async () => {
  try {
    const response = await axios.get(`${baseURL}/news/links`);
    return response.data; // Retorna algo como { "id1": "Título X", ... }
  } catch (error) {
    throw new Error("Erro ao obter links de notícias");
  }
};

// Função para obter uma notícia específica pelo _id
export const getNewsById = async (newsId) => {
  try {
    const response = await axios.get(`${baseURL}/news/${newsId}`);
    return response.data; // Retorna a notícia com title, content, date, etc.
  } catch (error) {
    throw new Error("Erro ao obter notícia pelo ID");
  }
};

// Função para analisar notícia usando GPT
export const analyzeNews = async (title, content) => {
  try {
    const response = await axios.post(`${baseURL}/analyze-news`, {
      title,
      content
    });
    return response.data; // { analysis: string }
  } catch (error) {
    throw new Error("Erro ao analisar notícia");
  }
};

// Função para obter previsão de preço (ModeloPrevisaoResponse)
export const getPrevision = async () => {
  try {
    const response = await axios.get(`${baseURL}/get-prevision`);
    return response.data;
  } catch (error) {
    throw new Error("Erro ao obter previsão");
  }
};

// Função para obter indicadores atuais da ação BBAS3 (price, rsi, macd, signal_line, date)
export const getStockData = async () => {
  try {
    const response = await axios.get(`${baseURL}/stock`);
    return response.data;
  } catch (error) {
    throw new Error("Erro ao obter dados da ação BBAS3");
  }
};

// Função para obter dados técnicos em um intervalo de datas
// startDate e endDate devem estar no formato yyyy-mm-dd
export const getTechnicalData = async (startDate, endDate) => {
  try {
    const response = await axios.get(`${baseURL}/technical-data`, {
      params: {
        start_date: startDate,
        end_date: endDate
      }
    });
    return response.data;
  } catch (error) {
    throw new Error("Erro ao obter dados técnicos no período selecionado");
  }
};

// Função para obter dados fundamentalistas da ação BBAS3 por ano (opcional)
export const getFundamentalData = async (year) => {
  try {
    const params = {};
    if (year) {
      params.year = year;
    }
    const response = await axios.get(`${baseURL}/fundamental-data`, { params });
    return response.data;
  } catch (error) {
    throw new Error("Erro ao obter dados fundamentalistas");
  }
};
