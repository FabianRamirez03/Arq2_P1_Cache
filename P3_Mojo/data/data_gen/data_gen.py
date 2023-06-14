import csv
import random

def generar_logistic_csv():
    parejas = []

    # Generar parejas que sumen menos de 500
    for _ in range(5000):
        num1 = random.randint(1, 4999)
        num2 = random.randint(1, 5000 - num1)
        parejas.append((num1, num2, 0))

    # Generar parejas que sumen más de 500 pero menos de 1000
    for _ in range(5000):
        num1 = random.randint(1, 9999)
        num2 = random.randint(1, 10000 - num1)
        parejas.append((num1, num2, 1))


    # Escribir las parejas en un archivo CSV
    with open('assets/logistic_regression.csv', 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)

        for pareja in parejas:
            escritor_csv.writerow(pareja)

    print("Archivo CSV generado exitosamente.")


def generar_lineal_csv():
    parejas = []

    # Generar parejas de números según los rangos
    for _ in range(2500000):
        num = random.randint(0, 4999999)
        parejas.append((num, num*2))

    for _ in range(2500000):
        num = random.randint(5000000, 9999999)
        parejas.append((num, num*2))

    for _ in range(2500000):
        num = random.randint(10000000, 14999999)
        parejas.append((num, num*2))

    for _ in range(2500000):
        num = random.randint(15000000, 20000000)
        parejas.append((num, num*2))


    # Escribir las parejas en un archivo CSV
    with open('assets/lineal_regression.csv', 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        for pareja in parejas:
            escritor_csv.writerow(pareja)

    print("Archivo CSV generado exitosamente.")

generar_lineal_csv()
generar_logistic_csv()
