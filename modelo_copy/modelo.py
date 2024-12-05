from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from scikeras.wrappers import KerasRegressor 
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.base import BaseEstimator
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from Dados import b_periodo
import matplotlib.pyplot as plt

strategy = tf.distribute.MirroredStrategy()

start='2010-01-01'
end='2023-04-20'
 
data = b_periodo(start, end)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data =scaler.fit_transform(data) 
print(scaled_data)

# Normalizar os Dados

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

# Definir a função de construção do modelo
def create_model(
                 units1=150, units2 = 100, units3 = 75,  units4 = 50,
                 dropout_rate1=0.1, dropout_rate2=0.05, dropout_rate3=0.05, dropout_rate4=0.1,
                 learning_rate=0.001,
                 activation='relu'):
    model = Sequential()
    
    model.add(LSTM(units=units1, return_sequences=True, input_shape=(60, 6)))
    model.add(Dropout(dropout_rate1))
    
    model.add(LSTM(units=units2, return_sequences=True))
    model.add(Dropout(dropout_rate2))
    
    model.add(LSTM(units=units3, return_sequences=True))
    model.add(Dropout(dropout_rate3))
    
    model.add(LSTM(units=units4))
    model.add(Dropout(dropout_rate4))
    
    model.add(Dense(1, activation=activation))
    
    # Compilar o modelo
    model.compile(optimizer=Adam(learning_rate=learning_rate), loss='mean_squared_error')
    
    return model

param_grid = {
    'units1': [200, 150],
    'units2': [150, 100],
    'units3': [100, 75],
    'learning_rate': [0.001, 0.0001],
    'activation': ['relu','swish'],
    'epochs': [100,150],
    'batch_size': [64, 108]
}

# Envolver o modelo em um KerasRegressor
model = KerasRegressor(activation='swish', units1=150, units2 = 100, units3 = 50,
                 learning_rate=0.001, model=create_model, epochs=150, batch_size=32, verbose=1)

grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, verbose=1)
grid_result = grid_search.fit(X_train, y_train)

best_model = grid_result.best_estimator_

predictions = best_model.predict(X_test)

print("Melhores Hiperparâmetros:", grid_result.best_params_)
print("Melhor Score:", grid_result.best_score_)

mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100
std_error = np.std(y_test - predictions)

print(f"Erro Quadrático Médio (MSE) no Teste: {mse}")
print(f"Coeficiente de Determinação (R²): {r2}")
print(f"Erro Absoluto Médio Percentual (MAPE): {mape}%")
print(f"Desvio Padrão do Erro: {std_error}")


plt.scatter(y_test, predictions)
plt.xlabel('Valores reais')
plt.ylabel('Previsões')
plt.title('Gráfico de Dispersão: Valores reais vs Previsões')
plt.savefig('Scatter_plot_gridsearchcv.png')

residuals = y_test - predictions
plt.scatter(predictions, residuals)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Previsões')
plt.ylabel('Resíduos')
plt.title('Gráfico de Resíduos')
plt.savefig('Residual_plot_gridsearchcv.png')