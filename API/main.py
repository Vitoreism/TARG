from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Backend.GPTnlp import GPT  # Importando o GPT conforme indicado
from Backend.bbas3_data import get_stock_indicators  # Importando a função que calcula os indicadores

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

# Função do Backend para Análise de Notícias
def analyze_news_article(news_text: str) -> str:
    try:
        gpt_instance = GPT()
        analysis = gpt_instance.call_gpt(news_text)
        return analysis
    except Exception as e:
        raise Exception(f"Erro ao chamar o GPT: {e}")

# Rotas da API

# POST: Analisar notícia usando GPT
@app.post("/analyze-news", response_model=NewsAnalysisResponse)
def analyze_news_endpoint(article: NewsArticle):
    try:
        # Combinar título e conteúdo da notícia
        news_text = f"Título: {article.title}\nConteúdo: {article.content}"
        # Chamar a função de análise
        analysis = analyze_news_article(news_text)
        return NewsAnalysisResponse(analysis=analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET: Obter indicadores de ações do Banco do Brasil (BBAS3)
@app.get("/stock", response_model=StockDataResponse)
def get_stock_data():
    """
    Endpoint para retornar os indicadores financeiros do Banco do Brasil (BBAS3).
    """
    try:
        # Chamar a função que calcula os indicadores
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
