from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Datos de entrada
X = [[1, 2], [2, 3], [3, 1], [2, 1], [0, 1], [4,0], [1, 3],
     [4, 3], [5, 3], [6, 2], [9, 0], [0, 6], [4,2], [7,1]]
y = [0, 0, 0, 0, 0, 0, 0, 1,1,1,1 ,1, 1, 1]

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo de regresión logística
model = LogisticRegression()

# Entrenar el modelo
model.fit(X_train, y_train)

# Realizar predicciones en los datos de prueba
y_pred = model.predict(X_test)

# Calcular la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)
print("Datos de prueba: ", y_test, "Datos resultantes: ", len(y_pred))
print("Precisión del modelo:", accuracy)
