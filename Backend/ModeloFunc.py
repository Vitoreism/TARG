import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
from dados import b_periodo
from datetime import datetime, timedelta

class ModeloPrevisao:
    def __init__(self, modelo_path, window_size=60):
        """
        Inicializa a classe com o caminho do modelo .keras.
        """
        self.window_size = window_size
        self.model = self.carregar_modelo(modelo_path)
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def carregar_modelo(self, modelo_path):
        """
        Carrega o modelo salvo a partir de um arquivo .keras.
        """
        try:
            model = tf.keras.models.load_model(modelo_path)
            print(f"Modelo carregado de {modelo_path}")
            return model
        except Exception as e:
            print(f"Erro ao carregar o modelo: {e}")
            return None

    def baixar_dados(self, start, end):
        """
        Baixa os dados históricos entre as datas fornecidas.
        """
        print(f"Baixando dados de {start} até {end}...")
        data = b_periodo(start, end)
        scaled_data = self.scaler.fit_transform(data)
        return data, scaled_data

    def create_sequences(self, data):
        """
        Cria sequências para o modelo LSTM.
        """
        X, y = [], []
        for i in range(len(data) - self.window_size):
            X.append(data[i:i + self.window_size])
            y.append(data[i + self.window_size][2])  # O índice 2 corresponde ao 'Close'
        return np.array(X), np.array(y)

    def prever_precos(self, start, end):
        """
        Faz previsões de preços para o intervalo fornecido.
        """
        data, scaled_data = self.baixar_dados(start, end)
                
        # Criar as sequências para o modelo
        X, y = self.create_sequences(scaled_data)
        
        # Ajustar o formato para [amostras, timesteps, features]
        X = X.reshape((X.shape[0], X.shape[1], X.shape[2]))
        
        predictions = self.model.predict(X)

        # Reverter a escala das previsões
        predictions_full = np.zeros((predictions.shape[0], scaled_data.shape[1]))
        predictions_full[:, 2] = predictions[:, 0]  # Preencher apenas a coluna 'Close'
        predictions = self.scaler.inverse_transform(predictions_full)[:, 2]
        
        # Reverter a escala do y real para comparação
        y_full = np.zeros((y.shape[0], scaled_data.shape[1]))
        y_full[:, 2] = y
        y_actual = self.scaler.inverse_transform(y_full)[:, 2]

        mae = mean_absolute_error(y_actual, predictions)
        mse = mean_squared_error(y_actual, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_actual, predictions)

        print(f"Erro Absoluto Médio (MAE): {mae}")
        print(f"Erro Quadrático Médio (MSE): {mse}")
        print(f"Raiz do Erro Quadrático Médio (RMSE): {rmse}")
        print(f"Coeficiente de Determinação (R²): {r2}")

        specific_dates = data.index[-len(predictions):]
        predictions_series = pd.Series(predictions, index=specific_dates)

        plt.figure(figsize=(14, 7))
        plt.plot(data.index, data['Close'], label='Preço Real', color='blue')
        plt.plot(predictions_series.index, predictions_series, label='Previsão', color='orange', linestyle='dashed')
        plt.title(f"Previsões de Preço para o Intervalo {start} a {end}")
        plt.xlabel('Data')
        plt.ylabel('Preço de Fechamento')
        plt.legend()
        plt.show()
        plt.savefig(f'../Previsoes/{datetime.now().time()}.png')

        return predictions_series

    def prever_futuro(self, future_days):
        """
        Faz previsões de preços para os próximos 'future_days' dias.
        """
        diaAtual = datetime.now().date()
        diaPass = diaAtual - timedelta(days=120)
        
        ## Colocar para prever a data mais recente
        data, scaled_data = self.baixar_dados(f"{diaPass}", f"{diaAtual}")
        print(len(data))
        scaled_data =  self.scaler.fit_transform(data)
        last_sequence = scaled_data[-self.window_size:]
        print(f"\n{last_sequence.shape}\n") 
        
        future_predictions = []
        for _ in range(future_days):
            next_pred = self.model.predict(last_sequence.reshape(1, self.window_size, -1))[0][0]
            future_predictions.append(next_pred)
            new_row = last_sequence[-1].copy()  # Copiar a última linha da sequência anterior
            new_row[2] = next_pred  # Atualizar apenas a coluna 'Close'
            last_sequence = np.append(last_sequence[1:], [new_row], axis=0)

        # Reverter a escala das previsões futuras
        future_predictions_full = np.zeros((len(future_predictions), 7))  # 7 features
        future_predictions_full[:, 2] = future_predictions
        future_predictions = self.scaler.inverse_transform(future_predictions_full)[:, 2]

        future_dates = pd.date_range(start=datetime.now(), periods=future_days, freq='B')

        plt.figure(figsize=(14, 7))
        plt.plot(data.index, data['Close'], label='Preço Real (2022)', color='blue')
        plt.plot(future_dates, future_predictions, label='Previsão Futura', color='red', linestyle='dotted')
        plt.title(f"Previsão para os próximos {future_days} dias")
        plt.xlabel('Data')
        plt.ylabel('Preço de Fechamento')
        plt.legend()
        plt.show()
        plt.savefig(f'../Previsoes/2:{datetime.now().time()}.png')

        dataC = list(data['Close']['BBAS3.SA'])
        return {"X_atual": data.index, "Y_atual": dataC, "X_fut": future_dates, "Y_fut": future_predictions}