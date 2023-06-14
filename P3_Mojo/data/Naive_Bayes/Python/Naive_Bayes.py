import numpy as np
import csv
import time

class NaiveBayes:
    def __init__(self):
        self.classes = None
        self.class_priors = None
        self.feature_probs = None
    
    def fit(self, X, y):
        num_samples, num_features = X.shape
        self.classes = np.unique(y)
        num_classes = len(self.classes)
        
        self.class_priors = np.zeros(num_classes)
        self.feature_probs = np.zeros((num_classes, num_features))
        
        for i, c in enumerate(self.classes):
            X_c = X[y == c]
            self.class_priors[i] = len(X_c) / num_samples
            self.feature_probs[i] = np.mean(X_c, axis=0)
    
    def predict(self, X):
        num_samples, num_features = X.shape
        num_classes = len(self.classes)
        
        predictions = []
        for i in range(num_samples):
            sample_probs = np.zeros(num_classes)
            for j in range(num_classes):
                class_prior = self.class_priors[j]
                feature_probs = self.feature_probs[j]
                sample_probs[j] = np.sum(np.log(feature_probs + 1e-9) * X[i] + np.log(1 - feature_probs + 1e-9) * (1 - X[i])) + np.log(class_prior)
            predicted_class = self.classes[np.argmax(sample_probs)]
            predictions.append(predicted_class)
        
        return predictions

start_time = time.time()

# Leer datos de entrenamiento desde archivo CSV
X_train = []
y_train = []
with open('assets/naive_bayes.csv', 'r') as archivo:
    lector_csv = csv.reader(archivo)
    for fila in lector_csv:
        X_train.append(fila[:-1])  # Todos los valores de la fila excepto el último
        y_train.append(fila[-1])   # Último valor de la fila

# Convertir a arrays de NumPy
X_train = np.array(X_train, dtype=int)
y_train = np.array(y_train)

# Crear y ajustar el modelo Naive Bayes
model = NaiveBayes()
model.fit(X_train, y_train)

# Datos de prueba
X_test = np.array([[1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,1,1,0,0,0,1,1,0,0,1,0,0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,1,0,1,1,0,0,0,0,0,1,1,0,0,1,0,1,0,0,1,0,1,1,1,0,0,1,1,0,1,0,1,0,1,1,0,0,1,1,1,0,1,1,1,1],
                   [1,1,0,1,0,1,1,1,1,0,1,0,0,0,1,0,0,0,0,1,1,0,1,1,1,0,0,1,0,1,0,0,1,0,1,1,1,1,0,0,0,0,1,0,1,0,1,1,0,0,1,1,0,0,0,0,0,1,1,0,0,1,1,0,1,0,1,0,1,1,1,1,0,1,1,0,1,1,0,1,0,0,0,1,1,1,1,0,0,0,1,1,1,0,0,1,0,0,1,0]])

# Realizar predicciones
y_pred = model.predict(X_test)

# Fin del procesamiento
end_time = time.time()

# Calcular tiempo de procesamiento
processing_duration = end_time - start_time

print("Tiempo de procesamiento total: {:.2f} segundos".format(processing_duration))

print("Predicciones:", y_pred)
