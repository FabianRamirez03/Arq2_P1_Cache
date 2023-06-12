import numpy as np
import time as time
import platform as platform


start = time.time()

# Tamaño de la matriz
matrix_size = 1000

# Crear dos matrices aleatorias
matrix_a = np.random.rand(matrix_size, matrix_size)
matrix_b = np.random.rand(matrix_size, matrix_size)

result = np.dot(matrix_a, matrix_b)

end = time.time()

procesador = platform.processor()
platform = platform.platform()


print("platform:", platform)
print("Procesador:", procesador)
print("Tamaño de la matriz:", matrix_size, "x", matrix_size)
print("Execution time:", end - start)
