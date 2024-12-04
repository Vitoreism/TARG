import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

ticker = "BBAS3.SA"
start_date = "2010-01-01"
end_date = datetime.now().strftime("%Y-%m-%d") #data dinamica

# Baixa os dados das acoes do periodo definido
def b_periodo(start:str, end:str, ticker:str='BBAS3.SA'):
    # baixar dados definidos
    data = yf.download(ticker, start=start, end=end)
    data = data[[ 'Open', 'Volume', 'Close', 'Adj Close']]
    data['RSI'] = calculate_rsi(data)
    data['MACD'], data['Signal Line'] = calculate_macd(data)
    data.dropna(inplace=True)
    
    return data

# Baixar os dados históricos
while True:
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        break
    except Exception as e:
        print(f"Erro ao baixar os dados: {e}")
        
dividends = yf.Ticker(ticker).dividends
data['Dividendos'] = dividends.reindex(data.index).fillna(0)
#Possui os dados diários apenas de: preço de abertura, fechamento, maior  e menor preço do dia, e quantas ações negociadas
data.columns = [col[0] for col in data.columns]
data.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)

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

data['RSI'] = calculate_rsi(data)
data['MACD'], data['Signal_Line'] = calculate_macd(data)

# Função para obter o último valor dos indicadores
def get_last_indicators(data):
    if data.empty:
        return {
            'price': None,
            'rsi': None,
            'macd': None,
            'signal_line': None,
            'date': None
        }
    
    # Obter o preço ajustado
    price = data['Adj_Close'].iloc[-1] if data['Adj_Close'].iloc[-1] else None


    
    # Últimos valores do RSI, MACD e Signal Line
    last_rsi = data['RSI'].iloc[-1] if pd.notnull(data['RSI'].iloc[-1]) else None
    last_macd = data['MACD'].iloc[-1] if pd.notnull(data['MACD'].iloc[-1]) else None
    last_signal_line = data['Signal_Line'].iloc[-1] if pd.notnull(data['Signal_Line'].iloc[-1]) else None
    
    # Data do último registro
    last_date = data.index[-1].strftime('%Y-%m-%d')

    return {
        'price': price,
        'rsi': last_rsi,
        'macd': last_macd,
        'signal_line': last_signal_line,
        'date': last_date
    }
    



data_anualbb = [
    {
       'Ano': 2011 ,  
       'PL': 5.35,
       'PSR': 0.73,
       'PVP': 1.17,
       'Margem_Liquida': 13.61,
       'ROE': 19.91,
       'Margem_Bruta': 32.48,
       'Margem_EBIT': 19.21,
       'PEBIT': 3.79,
       'ROA': 1.31,
    },
    {
        'Ano': 2012,
        'PL': 6.52,
        'PSR': 0.78,
        'PVP': 1.20,
        'Margem_Liquida': 11.94,
        'ROE': 16.26,
        'Margem_Bruta': 32.05,
        'Margem_EBIT': 15.94,
        'PEBIT': 4.89,
        'ROA': 0.99,
    },
    {
        'Ano': 2013,
        'PL': 6.70,
        'PSR': 0.67,
        'PVP': 1.00,
        'Margem_Liquida': 9.98,
        'ROE': 14.49,
        'Margem_Bruta': 28.88,
        'Margem_EBIT': 12.30,
        'PEBIT': 5.44,
        'ROA': 0.90,
    },
    {
        'Ano': 2014,
        'PL': 5.10,
        'PSR': 0.49,
        'PVP': 0.90,
        'DY': 6.97,
        'Margem_Liquida': 8.60,
        'ROE': 14.49,
        'Margem_Bruta': 23.13,
        'Margem_EBIT': 11.33,
        'PEBIT': 4.36,
        'ROA': 0.93,
    },
    {
        'Ano': 2015,
        'PL': 2.67,
        'PSR': 0.23,
        'PVP': 0.61,
        'DY': 11.42,
        'Margem_Liquida': 7.71,
        'ROE': 17.04,
        'Margem_Bruta': 12.32,
        'Margem_EBIT': 5.56,
        'PEBIT': 4.17,
        'ROA': 1.01,
    },
    {
        'Ano': 2016,
        'PL': 11.45,
        'PSR': 0.46,
        'PVP': 1.06,
        'DY': 2.65,
        'Margem_Liquida': 3.99,
        'Margem_EBIT': 6.18,
        'ROE': 8.14,
        'Margem_Bruta': 17.58,
        'PEBIT': 7.39,
        'ROA': 0.51,
    },
    {
        'Ano': 2017,
        'PL': 8.58,
        'PSR': 0.62,
        'PVP': 1.04,
        'DY': 2.96,
        'Margem_Liquida': 7.23,
        'Margem_EBIT': 10.83,
        'ROE': 10.92,
        'Margem_Bruta': 21.31,
        'PEBIT': 5.72,
        'ROA': 0.79,
    },
    {
        'Ano': 2018,
        'PL': 9.63,
        'PSR': 1.11,
        'PVP': 1.45,
        'DY': 3.26,
        'Margem_Liquida': 11.50,
        'Margem_EBIT': 16.98,
        'ROE': 13.57,
        'Margem_Bruta': 31.68,
        'PEBIT': 6.53,
        'ROA': 0.99,
    },
    {
        'Ano': 2019,
        'PL': 9.23,
        'PSR': 1.23,
        'PVP': 1.53,
        'DY': 4.84,
        'Margem_Liquida': 13.32,
        'Margem_EBIT': 9.05,
        'ROE': 15.22,
        'Margem_Bruta': 27.50,
        'PEBIT': 13.59,
        'ROA': 1.07,
    },
    {
        'Ano': 2020,
        'PL': 8.36,
        'PSR': 1.13,
        'PVP': 0.95,
        'DY': 3.81,
        'Margem_Liquida': 13.47,
        'Margem_EBIT': 11.73,
        'ROE': 10.63,
        'Margem_Bruta': 56.18,
        'PEBIT': 9.60,
        'ROA': 0.75,
    },
    {
        'Ano': 2021,
        'PL': 4.19,
        'PSR': 0.66,
        'PVP': 0.58,
        'DY': 7.86,
        'Margem_Liquida': 15.66,
        'Margem_EBIT': 19.05,
        'ROE': 13.82,
        'Margem_Bruta': 47.38,
        'PEBIT': 3.45,
        'ROA': 0.99,
    },
    {
        'Ano': 2022,
        'PL': 3.32,
        'PSR': 0.42,
        'PVP': 0.62,
        'DY': 12.01,
        'Margem_Liquida': 12.68,
        'Margem_EBIT': 16.26,
        'ROE': 18.79,
        'Margem_Bruta': 31.43,
        'PEBIT': 2.59,
        'ROA': 1.49,
    },
    {
        'Ano': 2023,
        'PL': 4.79,
        'PSR': 0.60,
        'PVP': 0.94,
        'DY': 8.26,
        'Margem_Liquida': 12.49,
        'Margem_EBIT': 15.50,
        'ROE': 19.60,
        'Margem_Bruta': 33.43,
        'PEBIT': 3.86,
        'ROA': 1.54,
    },
    {
        'Ano': 2024,
        'PL': 4.56,
        'PSR': 0.55,
        'PVP': 0.82,
        'DY': 8.34,
        'Margem_Liquida': 12.13,
        'Margem_EBIT': 12.73,
        'ROE': 17.87,
        'Margem_Bruta': 37.76,
        'PEBIT': 4.35,
        'ROA': 1.37,
    }
]

# Converter para DataFrame
df_fundamental = pd.DataFrame(data_anualbb)


# Função para obter dados técnicos com filtragem por datas
def get_technical_data(start_date=None, end_date=None):
    """
    Retorna os dados técnicos filtrados por intervalo de datas.
    """
    try:
        # Validações de datas
        if start_date:
            start_date = pd.to_datetime(start_date, errors='coerce')
            if pd.isnull(start_date):
                raise ValueError("Data de início inválida. Por favor, use 'YYYY-MM-DD'.")

        if end_date:
            end_date = pd.to_datetime(end_date, errors='coerce')
            if pd.isnull(end_date):
                raise ValueError("Data de término inválida. Por favor, use 'YYYY-MM-DD'.")
        # Aplicar filtros
        filtered_data = data
        if start_date:
            filtered_data = filtered_data[filtered_data.index >= start_date]
            
        if end_date:
            filtered_data = filtered_data[filtered_data.index <= end_date]
        if filtered_data.empty:
            return {"message": "Nenhum dado técnico encontrado no intervalo fornecido."}
        return filtered_data.reset_index().to_dict(orient="records")
    except Exception as e:
        return {"error": f"Erro ao obter dados técnicos: {str(e)}"}


# Função para obter dados fundamentalistas com filtro por ano
def get_fundamental_data(year=None):
    """
    Retorna os dados fundamentalistas filtrados por ano.
    """
    try:
        if year:
            if not isinstance(year, int):
                raise ValueError("O ano deve ser um número inteiro.")
            filtered_data = df_fundamental[df_fundamental['Ano'] == year]
            if filtered_data.empty:
                return {"message": f"Nenhum dado fundamentalista encontrado para o ano {year}."}
            return filtered_data.to_dict(orient="records")[0]
        return df_fundamental.to_dict(orient="records")
    except Exception as e:
        return {"error": f"Erro ao obter dados fundamentalistas: {str(e)}"}



def get_stock_indicators():
    return get_last_indicators(data)

if __name__ == "__main__":
    try:
        indicadores = get_stock_indicators()
        print(indicadores)
    except Exception as e:
        print(f"Erro ao processar indicadores: {e}")


