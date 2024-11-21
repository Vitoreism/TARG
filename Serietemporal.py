import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import yfinance as yf

# 1. Coletar Dados do BBAS3
ticker = 'BBAS3.SA'
data = yf.download(ticker, start='2010-01-01', end='2024-11-20')
data = data[['Close']]

# 2. Normalizar os Dados
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Função para criar sequências
def create_sequences(data, window_size):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
        y.append(data[i + window_size])
    return np.array(X), np.array(y)

window_size = 60
X, y = create_sequences(scaled_data, window_size)

# Dividir em treino e teste
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Ajustar formato para [amostras, timesteps, features]
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

# 3. Construir o Modelo LSTM
model = Sequential([
    LSTM(150, return_sequences=True, input_shape=(window_size, 1)),
    LSTM(100, return_sequences=False),
    Dense(50),
    Dense(1)
])
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, batch_size=32, epochs=100, validation_data=(X_test, y_test))

# 4. Fazer Previsões no Conjunto de Teste
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)
y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))

# 5. Prever Preços Futuros
future_days = 3  # Número de dias a prever
last_sequence = scaled_data[-window_size:]  # Últimos 60 dias da série
future_predictions = []

for _ in range(future_days):
    next_pred = model.predict(last_sequence.reshape(1, window_size, 1))[0][0]
    future_predictions.append(next_pred)
    # Atualizar a sequência com a nova previsão
    last_sequence = np.append(last_sequence[1:], [[next_pred]], axis=0)

# Reverter a escala das previsões futuras
future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

# Criar datas para as previsões futuras
future_dates = pd.date_range(start=data.index[-1], periods=future_days + 1, inclusive='right')

# 6. Plotar os Resultados
#plt.figure(figsize=(14, 7))
#plt.plot(data.index, data['Close'], label='Preço Real')
#plt.plot(data.index[-len(predictions):], predictions, label='Previsão no Teste')
#plt.plot(future_dates, future_predictions, label='Previsão Futura', linestyle='dashed')
#plt.title('Previsão de Preço das Ações do BBAS3 com LSTM')
#plt.xlabel('Data')
#plt.ylabel('Preço de Fechamento')
#plt.legend()
#plt.show()


real_dates = data.index[-len(y_test_actual):]  # Últimos dias reais
real_prices = y_test_actual.flatten()[-100:]  # Apenas os últimos 100 valores
predicted_prices = predictions.flatten()[-100:]

plt.plot(real_dates[-100:], real_prices, label="Preço Real", color="blue")
plt.plot(real_dates[-100:], predicted_prices, label="Previsão no Teste", color="red")
plt.title("Previsão de Preços BBAS3")
plt.xlabel("Data")
plt.ylabel("Preço")
#plt.legend()
plt.show()
