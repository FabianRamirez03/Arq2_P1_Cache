import numpy as np
import csv
import time as time


class LinearRegression:
    def __init__(self):
        self.coefficients = None

    def leer_archivo_csv(self):
        datos = []
        etiquetas = []
        with open("assets/lineal_regression.csv", "r") as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            # encabezados = next(lector_csv)  # Leer la primera fila como encabezados
            for fila in lector_csv:
                tmp = list(
                    map(int, fila)
                )  # Convertir cada elemento de la fila a entero y agregar a la lista
                datos.append(tmp[0:1])
                etiquetas.append(tmp[1])
        return {"datos": datos, "etiquetas": etiquetas}

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


start_time = time.time()

# Crear y entrenar el modelo de regresión lineal
model = LinearRegression()
# Datos de entrenamiento
data = model.leer_archivo_csv()
X_train = np.array(data["datos"])
y_train = np.array(data["etiquetas"])
model.fit(X_train, y_train)

# Realizar predicciones
X_test = np.array([[500], [1500], [7000]])  # Nuevos datos para predecir
y_pred = model.predict(X_test)

# Fin del procesamiento
end_time = time.time()
# Calcular tiempo de procesamiento
processing_duration = end_time - start_time

print("Tiempo de procesamiento total: {:.2f} segundos".format(processing_duration))

