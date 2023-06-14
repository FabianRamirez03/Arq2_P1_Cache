import pandas as pd
import time

# Archivo de datos de muestra (puede reemplazarlo con su propio archivo)
data_file = "rotten_tomatoes_movie_reviews.csv"

# Medir tiempo de carga de datos
start_time = time.time()

df = pd.read_csv(data_file)

# Ejemplo de procesamiento: obtener el promedio de una columna
most_common_value = df["criticName"].mode().values[0]

# Fin del procesamiento
end_time = time.time()

# Calcular tiempo de procesamiento
processing_duration = end_time - start_time

print("Tiempo de procesamiento total: {:.2f} segundos".format(processing_duration))
print("Moda de la columna criticName: {}".format(most_common_value))
