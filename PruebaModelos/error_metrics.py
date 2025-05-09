import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

def calculate_errors(y_pred, y_test, title):
    # Calculate Mean Absolute Error (MAE)
    mae = mean_absolute_error(y_test, y_pred)
    
    # Calculate Mean Squared Error (MSE) using scikit-learn
    mse = mean_squared_error(y_test, y_pred)
    
    # Calculate Root Mean Squared Error (RMSE)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    # Print the title and the error metrics
    print(f"{title}:")
    print(f"MAE: {mae}")
    print(f"MSE: {mse}")
    print(f"RMSE: {rmse}")
    print(f"R²: {r2}")
    
def diff_analysis(y_pred, y_test, title):
    diff = y_pred - y_test
    plt.title(f"Differenciales - {title}")
    plt.plot(diff, 'o')
    plt.show()
    
    plt.title(f"Frecuenci de diferenciales - {title}")
    plt.hist(diff)
    plt.show()
    
    