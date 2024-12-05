from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from Dados import b_periodo

# carregando modelo
model = load_model('TARG2.keras')
start = '2010-01-01'
end = '2024-06-14'

# normalizando dados
data = b_periodo(start, end)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)
window_size = 60

last_sequence = scaled_data[-window_size:]
future_predictions = []

def create_sequences(data, window_size):
    X= []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
    return np.array(X)
 
X = create_sequences(scaled_data, window_size)

train_size = int(len(X) * 0.8)
X_test = X[train_size:]

# Ajustar formato para [amostras, timesteps, features]
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], X_test.shape[2]))

predictions = model.predict(X_test)

# Reverter a escala das previsões
predictions_full = np.zeros((predictions.shape[0], scaled_data.shape[1]))
predictions_full[:, 2] = predictions[:, 0]  # Preencher apenas a coluna 'Close'
predictions = scaler.inverse_transform(predictions_full)[:, 2]

# defininido o intervalo da previsao
start_period = '2024-01-01'
end_period = '2024-12-31'
data_specific_period = data.loc[start_period:end_period]

# Extrair as previsões correspondentes ao período específico
specific_dates = data_specific_period.index
predictions_specific_period = pd.Series(predictions[-len(specific_dates):], index=specific_dates)

# Criar datas para as previsões futuras
future_days = 5 # Número de dias a prever
future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=future_days)

last_sequence = scaled_data[-window_size:]
future_predictions = []

for _ in range(future_days):
    next_pred = model.predict(last_sequence.reshape(1, window_size, -1))[0][0]
    future_predictions.append(next_pred)
    new_row = last_sequence[-1].copy()  # Copiar a última linha da sequência anterior
    new_row[2] = next_pred  # Atualizar apenas a coluna 'Close'
    last_sequence = np.append(last_sequence[1:], [new_row], axis=0)

# Reverter a escala das previsões futuras
future_predictions_full = np.zeros((len(future_predictions), scaled_data.shape[1]))
future_predictions_full[:, 2] = future_predictions
future_predictions = scaler.inverse_transform(future_predictions_full)[:, 2]

plt.figure(figsize=(14, 7))

# Plotar Preço Real e Previsões do Período Específico
plt.plot(data_specific_period.index, data_specific_period['Close'], label='Preço Real (2022)', color='blue')
plt.plot(predictions_specific_period.index, predictions_specific_period, label='Previsão (2022)', color='orange', linestyle='dashed')

# Plotar as Previsões Futuras
plt.plot(future_dates, future_predictions, label='Previsão Futura', linestyle='dotted', color='red')

# Configurações do Gráfico
plt.title('Preço das Ações do BBAS3 no Ano de 2022 com Previsão e Previsão Futura')
plt.xlabel('Data')
plt.ylabel('Preço de Fechamento')
plt.legend()
plt.savefig(f"./Previsoes/{datetime.datetime.now().time()}.png")
plt.show()