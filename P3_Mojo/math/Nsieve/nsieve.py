import sys
import time


def nsieve(n):
    count = 0
    flags = [True] * n
    for i in range(2, n):
        if flags[i]:
            count += 1
            for j in range(i << 1, n, i):
                flags[j] = False
    print(f'Números primos hasta {n:8} {count:8}')


if __name__ == '__main__':
    # Obtener el valor límite desde los argumentos de línea de comandos
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4

    start_time = time.time()
    # Calcular y mostrar los números primos para tres valores diferentes
    for i in range(0, 3):
        nsieve(10000 << (n-i))
    end_time = time.time()
    duration = end_time - start_time
    print(f"Tiempo de ejecución: {duration:.6f} segundos")
