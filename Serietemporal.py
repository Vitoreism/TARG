import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, BatchNormalization, Dropout
from tensorflow.keras.optimizers import Adam
import yfinance as yf
import datetime

strategy = tf.distribute.MirroredStrategy()

# 1. Coletar Dados do BBAS3
ticker = 'BBAS3.SA'
data = yf.download(ticker, start='2010-01-01', end='2023-04-20')
data = data[['Low', 'High', 'Close', 'Volume', 'Open']]
print(f"Tamanho dos dados baixados: {len(data)}")

# Normalizar os Dados
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Função para criar sequências
def create_sequences(data, window_size):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
        y.append(data[i + window_size][2])  # O índice 2 corresponde ao 'Close'
    return np.array(X), np.array(y)

window_size = 60  # Utilizar janela de 60 dias
X, y = create_sequences(scaled_data, window_size)

# Dividir em treino e teste
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Ajustar formato para [amostras, timesteps, features]
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], X_train.shape[2]))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], X_test.shape[2]))

# Definindo os hiperparâmetros do modelo
layers_size = 4  # Número de camadas LSTM (escolha entre 2, 4, 6, 8)
hidden_units_size = 200  # Número de unidades ocultas por camada (ex.: 100, 150, ..., 500)
use_batch_normalization = True  # Se deve ou não usar Batch Normalization
dropout_rate = 0.1  # Taxa de Dropout (0.1, 0.2, 0.3, 0.4)
learning_rate = 0.0003  # Taxa de aprendizado (0.01, 0.003, 0.0003, 0.0001)

# Criar o modelo LSTM
model = Sequential()

# Adicionando camadas LSTM
for i in range(layers_size):
    if i == layers_size - 1:  # Última camada LSTM
        model.add(LSTM(hidden_units_size, return_sequences=False, input_shape=(window_size, X_train.shape[2])))
    else:
        model.add(LSTM(hidden_units_size, return_sequences=True, input_shape=(window_size, X_train.shape[2])))

    # Adicionando Batch Normalization, se necessário
    if use_batch_normalization:
        model.add(BatchNormalization())

    # Adicionando Dropout
    model.add(Dropout(dropout_rate))

# Camada densa para a previsão final
model.add(Dense(1))  # Saída final para previsão de preço

# Compilando o modelo com a taxa de aprendizado definida
optimizer = Adam(learning_rate=learning_rate)
model.compile(optimizer=optimizer, loss='mean_squared_error')

# Treinando o modelo
model.fit(X_train, y_train, batch_size=32, epochs=150, validation_data=(X_test, y_test))

# Fazer Previsões no Conjunto de Teste
predictions = model.predict(X_test)

# Reverter a escala das previsões
predictions_full = np.zeros((predictions.shape[0], scaled_data.shape[1]))
predictions_full[:, 2] = predictions[:, 0]  # Preencher apenas a coluna 'Close'
predictions = scaler.inverse_transform(predictions_full)[:, 2]

# Reverter a escala do y_test para comparação
y_test_full = np.zeros((y_test.shape[0], scaled_data.shape[1]))
y_test_full[:, 2] = y_test
y_test_actual = scaler.inverse_transform(y_test_full)[:, 2]

# Calcular Métricas Estatísticas
mae = mean_absolute_error(y_test_actual, predictions)
mse = mean_squared_error(y_test_actual, predictions)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_actual, predictions)

# Exibir as Métricas
print(f"Erro Absoluto Médio (MAE): {mae}")
print(f"Erro Quadrático Médio (MSE): {mse}")
print(f"Raiz do Erro Quadrático Médio (RMSE): {rmse}")
print(f"Coeficiente de Determinação (R²): {r2}")

# 6. Plotar os Resultados para o Período Específico
start_period = '2022-01-01'
end_period = '2023-12-31'
data_specific_period = data.loc[start_period:end_period]

# Extrair as previsões correspondentes ao período específico
specific_dates = data_specific_period.index
predictions_specific_period = pd.Series(predictions[-len(specific_dates):], index=specific_dates)

# Criar datas para as previsões futuras
future_days = 5  # Número de dias a prever
future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=future_days)

# Prever Preços Futuros
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
model.save('TARG1.keras')
# Plotar o Gráfico
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
plt.savefig(f"./Previsoes/Re1{datetime.datetime.now().time()}.png")
plt.show()
