import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

ticker = "BBAS3.SA"
start_date = "2010-01-01"
end_date = datetime.now().strftime("%Y-%m-%d") #data dinamica

# Baixar os dados históricos
data = yf.download(ticker, start=start_date, end=end_date)

dividends = yf.Ticker(ticker).dividends
data['Dividendos'] = dividends.reindex(data.index).fillna(0)
#Possui os dados diários apenas de: preço de abertura, fechamento, maior  e menor preço do dia, e quantas ações negociadas
data

def calculate_rsi(data, window=14):
    # Calcula a diferença diária nos preços ajustados
    delta = data['Adj Close'].diff()

    # Separa os ganhos e perdas
    gain = delta.clip(lower=0)  # Apenas valores positivos
    loss = -delta.clip(upper=0)  # Apenas valores negativos

    # Cálculo inicial para os primeiros valores (primeiros `window` dias)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    # Evita divisão por zero (se `avg_loss` for 0, define RSI como 100)
    rs = avg_gain / avg_loss
    rs = rs.replace([float('inf'), float('-inf')], 0)  # Substituir infinitos por 0

    rsi = 100 - (100 / (1 + rs))
    rsi[:window] = None  # Define os primeiros valores como NaN, já que não são confiáveis

    return rsi

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    ema_short = data['Adj Close'].ewm(span=short_window, adjust=False).mean()
    ema_long = data['Adj Close'].ewm(span=long_window, adjust=False).mean()
    macd = ema_short - ema_long
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

data['RSI'] = calculate_rsi(data)


data['MACD'], data['Signal Line'] = calculate_macd(data)

# Obter o último valor de RSI
ultimo_rsi = data['RSI'].iloc[-1]

# Obter o último valor de MACD
ultimo_macd = data['MACD'].iloc[-1]

# Se quiser obter o último valor da Linha de Sinal (Signal Line)
ultima_signal_line = data['Signal Line'].iloc[-1]


def calculate_last_rsi(data):
    if isinstance(pd.DataFrame, data):
        ultimo_rsi = data['RSI'].iloc[-1]
        return ultimo_rsi
    else:
        return "Dado inválido"
    
def calculate_last_macd(data):
    if isinstance(pd.DataFrame, data):
        ultimo_macd = data['MACD'].iloc[-1]
        return ultimo_macd
    else:
        return "Dado inválido"

def calculate_last_signal(data):
    if isinstance(pd.DataFrame, data):
        ultima_signal_line = data['Signal Line'].iloc[-1]
        return ultima_signal_line
    else:
        return "Dado inválido"


# Função principal para consolidar os indicadores
def get_stock_indicators():
    """
    Processa os dados históricos do ticker e retorna os últimos valores de indicadores.
    """
    # Verificar se os dados foram carregados corretamente
    if data.empty:
        raise ValueError(f"Não foi possível carregar os dados para o ticker {ticker}.")

    # Obter os últimos valores
    price = data['Adj Close'].iloc[-1]
    ultimo_rsi = calculate_last_rsi(data)
    ultimo_macd = calculate_last_macd(data)
    ultima_signal_line = calculate_last_signal(data)
    date = data.index[-1].strftime('%Y-%m-%d')

    return {
        'price': price,
        'rsi': ultimo_rsi,
        'macd': ultimo_macd,
        'signal_line': ultima_signal_line,
        'date': date
    }

# Teste da função (opcional)
if __name__ == "__main__":
    try:
        indicadores = get_stock_indicators()
        print(indicadores)
    except Exception as e:
        print(f"Erro ao processar indicadores: {e}")
