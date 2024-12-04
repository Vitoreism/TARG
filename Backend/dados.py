import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Baixa os dados das acoes do periodo definido
def b_periodo(start:str, end:str, ticker:str='BBAS3.SA'):
    # baixar dados definidos
    data = yf.download(ticker, start=start, end=end)
    data = data[[ 'Open', 'Volume', 'Close', 'Adj Close']]
    data.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)
    data['RSI'] = calculate_rsi(data)
    data['MACD'], data['Signal Line'] = calculate_macd(data)
    data.dropna(inplace=True)
    print(data)
    return data

def calculate_rsi(data, window=14):
    # Calcula a diferença diária nos preços ajustados
    delta = data['Adj_Close'].diff()

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
    ema_short = data['Adj_Close'].ewm(span=short_window, adjust=False).mean()
    ema_long = data['Adj_Close'].ewm(span=long_window, adjust=False).mean()
    macd = ema_short - ema_long
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

def create_sequences(data, window_size):
    X= []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
    return np.array(X)