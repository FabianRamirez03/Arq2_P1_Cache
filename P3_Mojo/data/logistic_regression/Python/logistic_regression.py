import numpy as np

class LogisticRegression:
    def __init__(self, learning_rate=0.01, num_iterations=1000):
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.weights = None
        self.bias = None
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
    
    def initialize_parameters(self, n_features):
        self.weights = np.zeros(n_features)
        self.bias = 0
    
    def fit(self, X, y):
        self.initialize_parameters(X.shape[1])
        
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


# Datos de entrenamiento
X_train = np.array([[2.0, 1.0], [1.0, 3.0], [0.0, 2.0], [1.0, 1.0], [2.0, 2.0], [4.0, 3.0], [6.0, 5.0], [3.0, 5.0],  [3.0, 3.0], [6.0, 1.0]])
y_train = np.array([0, 0, 0,0,0,1, 1,1,1,1])

# Crear e entrenar el modelo
model = LogisticRegression(learning_rate=0.1, num_iterations=1000)
model.fit(X_train, y_train)

# Datos de prueba
X_test = np.array([[4.0, 2.0], [0.0, 2.0]])
y_pred = model.predict(X_test)

print("Predicciones:", y_pred)
