import numpy as np
import csv

class LogisticRegression:
    def __init__(self, learning_rate=0.01, num_iterations=1000):
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.weights = None
        self.bias = None
        
    def leer_archivo_csv(self):
        datos = []
        etiquetas = []
        with open('assets/logistic_regression.csv', 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            #encabezados = next(lector_csv)  # Leer la primera fila como encabezados
            for fila in lector_csv:
                tmp = list(map(int, fila))  # Convertir cada elemento de la fila a entero y agregar a la lista
                datos.append(tmp[0:2]) 
                etiquetas.append(tmp[2])
        return {'datos':datos, 'etiquetas': etiquetas}
    
    def sigmoid(self, z):
        # Aplicar clipping a los valores de entrada
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))
    
    def initialize_parameters(self, n_features):
        self.weights = np.zeros(n_features)
        self.bias = 0
    
    def fit(self, X, y):
        self.initialize_parameters(X.shape[1])
        print(X)
        for _ in range(self.num_iterations):
            linear_model = np.dot(X, self.weights) + self.bias
            y_pred = self.sigmoid(linear_model)
            
            dw = (1 / len(X)) * np.dot(X.T, (y_pred - y))
            db = (1 / len(X)) * np.sum(y_pred - y)
            
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
    
    def predict(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        y_pred = self.sigmoid(linear_model)
        y_pred_class = [1 if pred > 0.5 else 0 for pred in y_pred]
        return y_pred_class




# Crear e entrenar el modelo
model = LogisticRegression(learning_rate=0.1, num_iterations=10000)

# Datos de entrenamiento
data = model.leer_archivo_csv()
X_train = np.array(data['datos'])
y_train = np.array(data['etiquetas'])

model.fit(X_train, y_train)

# Datos de prueba
X_test = np.array([[4,2], [500,6]])
y_pred = model.predict(X_test)

print("Predicciones:", y_pred)
