import numpy as np

class LinearRegression:
    def __init__(self):
        self.coefficients = None
    
    def fit(self, X, y):
        # Agregar una columna de unos a X para el término de sesgo (intercept)
        X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)

        # Calcular los coeficientes utilizando la fórmula de mínimos cuadrados
        self.coefficients = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)
        
        
    
    def predict(self, X):
        # Agregar una columna de unos a X para el término de sesgo (intercept)
        X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)
        
        # Realizar predicciones utilizando los coeficientes aprendidos
        return X.dot(self.coefficients)

# Ejemplo de uso
X = np.array([[1], [2], [3], [4], [5]])  # Característica: X
y = np.array([2, 4, 6, 8, 10])  # Etiqueta: y

# Crear y entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(X, y)

# Realizar predicciones
X_test = np.array([[6], [7], [8]])  # Nuevos datos para predecir
y_pred = model.predict(X_test)

# Imprimir las predicciones
print("Predicciones:")
for i in range(X_test.shape[0]):
    print("X_test:", X_test[i][0], "y_pred:", y_pred[i])
