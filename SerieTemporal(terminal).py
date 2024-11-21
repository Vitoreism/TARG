import numpy as np
import pandas as pd
import plotext as plt  # Biblioteca para gráficos no terminal
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
import torch.optim as optim
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

window_size = 90
X, y = create_sequences(scaled_data, window_size)

# Dividir em treino e teste
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Converter para tensores do PyTorch
X_train = torch.tensor(X_train, dtype=torch.float32).unsqueeze(-1)
X_test = torch.tensor(X_test, dtype=torch.float32).unsqueeze(-1)
y_train = torch.tensor(y_train, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

# 3. Construir o Modelo LSTM
class LSTMModel(nn.Module):
    def __init__(self):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=50, num_layers=2, batch_first=True)
        self.fc = nn.Linear(50, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])  # Apenas a última saída
        return out

model = LSTMModel()

# 4. Configurar o Otimizador e a Função de Perda
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 5. Treinar o Modelo
epochs = 50
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    output = model(X_train)
    loss = criterion(output, y_train)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item()}")

# 6. Fazer Previsões no Conjunto de Teste
model.eval()
with torch.no_grad():
    predictions = model(X_test).numpy()
    predictions = scaler.inverse_transform(predictions)

# 7. Prever Preços Futuros
future_days = 3
last_sequence = torch.tensor(scaled_data[-window_size:], dtype=torch.float32).unsqueeze(0).unsqueeze(-1)
future_predictions = []

model.eval()
with torch.no_grad():
    for _ in range(future_days):
        next_pred = model(last_sequence).item()
        future_predictions.append(next_pred)
        # Atualizar a sequência com a nova previsão
        last_sequence = torch.cat((last_sequence[:, 1:, :], torch.tensor([[[next_pred]]], dtype=torch.float32)), dim=1)

# Reverter a escala das previsões futuras
future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

# Criar datas para as previsões futuras
future_dates = pd.date_range(start=data.index[-1], periods=future_days + 1, inclusive='right')

# 8. Plotar os Resultados no Terminal com `plotext`
# Dados para exibição
real_dates = data.index[-len(y_test):]  # Últimos dias reais
real_prices = scaler.inverse_transform(y_test.numpy().reshape(-1, 1)).flatten()
predicted_prices = predictions.flatten()

# Configurar o gráfico no terminal
plt.plot(real_dates[-100:], real_prices[-100:], label="Preço Real", color="blue")
plt.plot(real_dates[-100:], predicted_prices[-100:], label="Previsão no Teste", color="red")
plt.title("Previsão de Preços BBAS3 com PyTorch")
plt.xlabel("Data")
plt.ylabel("Preço")
plt.legend()
plt.show()
