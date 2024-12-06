from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bbas3_data import get_stock_indicators, get_technical_data, get_fundamental_data  # Importações do backend
from GPTnlp import GPT  # Importando o GPT conforme indicado
from ModeloFunc import ModeloPrevisao
from datetime import datetime
from typing import List, Dict
import os
from pymongo import MongoClient
from Scrapping_Banco_de_dados import get_news_by_id, get_id_dict
from urllib.parse import unquote


OPENAI_KEY = os.getenv('OPENAI_KEY')
gpt_instance = GPT(OPENAI_KEY)
modelo_instance = ModeloPrevisao('TARG2.keras')


app = FastAPI()


# Configuração do MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["noticias_db"]  # Nome do banco de dados
news_collection = db["noticias"]  # Nome da coleção de notícias


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

class ModeloPrevisaoResponse(BaseModel):
    X_atual: list
    Y_atual: list
    X_fut: list
    Y_fut: list


class NewsData(BaseModel):
    title: str
    content: str
    date: str #Poderia ser datetime (???)
    analysis: str
# Rotas da API

# Endpoint para recuperar o dicionário de _id e títulos
@app.get("/news/links", response_model=Dict[str, str])
def get_all_news_titles():
    """
    Recupera todos os _id de notícias e seus respectivos títulos.
    """
    try:
        id_links_dict = get_id_dict()
        return id_links_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/news/{news_id}")
async def get_news(news_id: str):
    """
    Recupera uma notícia específica a partir de seu _id.
    """
    # Chama a função de recuperação da notícia com base no _id
    news = get_news_by_id(news_id)
    
    if "error" in news:
        raise HTTPException(status_code=404, detail=news["error"])
    
    return news




# POST: Analisar notícia usando GPT
@app.post("/analyze-news", response_model=NewsAnalysisResponse)
def analyze_news_endpoint(article: NewsArticle):
    try:
        # Combinar título e conteúdo da notícia
        news_text = f"Título: {article.title}\nConteúdo: {article.content}"
        print(news_text)
        # Chamar a função de análise
        analysis = gpt_instance.analyze_news_article(news_text)
        return NewsAnalysisResponse(analysis=analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-prevision", response_model=ModeloPrevisaoResponse)
def get_prevision():
    try:
        prevision = modelo_instance.prever_futuro(5)
        return prevision
    except Exception as e:
        print(f"Erro ao gerar previsão: {e}")

# GET: Obter indicadores de ações do Banco do Brasil (BBAS3)
@app.get("/stock", response_model=StockDataResponse)
def get_stock_data():
    try:
        stock_data = get_stock_indicators()
        return StockDataResponse(
            price=stock_data["price"],
            rsi=stock_data["rsi"],
            macd=stock_data["macd"],
            signal_line=stock_data["signal_line"],
            date=stock_data["date"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter indicadores: {e}")
    
@app.get("/technical-data", response_model=TechnicalDataResponse)
def technical_data(
    start_date: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # Tornamos o start_date obrigatório
):
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = start_date  # Fazendo o end_date ser igual ao start_date
        technical_data = get_technical_data(start_date, end_date)
        return technical_data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados técnicos: {e}")


@app.get("/fundamental-data", response_model=FundamentalDataResponse)
def fundamental_data(year: int = None):
    try:
        fundamental_data = get_fundamental_data(year)
        return fundamental_data
    except ValueError:
        raise HTTPException(status_code=400, detail="Ano inválido. Por favor, forneça um número inteiro.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados fundamentalistas: {e}")