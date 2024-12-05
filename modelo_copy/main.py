from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from modelo1 import ModeloPrevisao
from datetime import datetime
from typing import List
import os

modelo_instance = ModeloPrevisao('TARG2.keras')


app = FastAPI()

# Configuração do CORS
origins = [
    "http://localhost:3000",  # Seu frontend rodando no localhost na porta 3000
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Define as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],          # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],          # Permite todos os cabeçalhos
)

# Modelos de Dados
class NewsArticle(BaseModel):
    title: str
    content: str

class NewsAnalysisResponse(BaseModel):
    analysis: str

class StockDataResponse(BaseModel):
    price: float
    rsi: float
    macd: float
    signal_line: float
    date: str

class TechnicalDataResponse(BaseModel):
    Date: datetime
    Adj_Close: float
    Close: float
    High: float
    Low: float
    Open: float
    Volume: int
    Dividendos: float
    RSI: float
    MACD: float
    Signal_Line: float

class FundamentalDataResponse(BaseModel):
    Ano: int
    PL: float
    PSR: float
    PVP: float
    Margem_Liquida: float
    ROE: float
    Margem_Bruta: float
    Margem_EBIT: float
    PEBIT: float
    ROA: float


class NewsData(BaseModel):
    title: str
    content: str
    date: str #Poderia ser datetime (???)
    analysis: str


class ModeloPrevisaoResponse(BaseModel):
    X_atual: list
    Y_atual: list
    X_fut: list
    Y_fut: list
# Rotas da API

@app.get("/get-prevision", response_model=ModeloPrevisaoResponse)
def get_prevision():
    try:
        prevision = modelo_instance.prever_futuro(5)
        return prevision
    except Exception as e:
        print(f"Erro ao gerar previsão: {e}")
