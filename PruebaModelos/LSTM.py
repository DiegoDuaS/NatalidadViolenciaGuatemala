import torch.nn as nn
import numpy as np
import torch


# Definir el modelo LSTM
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # Definir la capa LSTM
        self.lstm = nn.LSTM(input_size=input_size, 
                            hidden_size=hidden_size, 
                            num_layers=num_layers, 
                            batch_first=True)
        
        # Capa totalmente conectada (fully connected)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # Inicializar el estado oculto y el estado de la celda
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        # Pasar los datos por la capa LSTM
        out, _ = self.lstm(x, (h0, c0))
        
        # Solo tomar la salida del último tiempo (el último valor de la secuencia)
        out = self.fc(out[:, -1, :])  # Toma el último valor de la secuencia

        return out

    
def preparar_series_lstm(df, n_lags=3):
    X = []
    y = []

    for i in range(n_lags, len(df)):
        # Las características son las columnas de violencia de los años previos
        features = []
        
        for lag in range(n_lags, 0, -1):  # Los años previos
            features.append(df.iloc[i-lag][df.columns.str.startswith('VI')])  # Tomar solo las columnas de VI
        
        # El valor objetivo es el total de nacimientos del año actual
        target = df.iloc[i]['Total Nacimientos']
        
        # Agregar los datos a las listas
        X.append(features)
        y.append(target)
    
    # Convertir a matrices NumPy
    X = np.array(X)
    y = np.array(y)
    
    # Reorganizar X para que sea (samples, time_steps, features) para LSTM
    X = X.reshape(X.shape[0], n_lags, X.shape[2])

    return X, y

