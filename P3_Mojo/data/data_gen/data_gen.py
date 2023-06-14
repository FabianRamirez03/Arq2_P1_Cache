import csv
import random

def generar_bayes_csv():
    # Generar los datos
    datos = []
    for _ in range(1000000):
        fila = [random.choice([0, 1]) for _ in range(100)]
        suma_fila = sum(fila)
        etiqueta = "B" if suma_fila > 50 else "A"
        fila.append(etiqueta)
        datos.append(fila)
    
    # Guardar los datos en un archivo CSV
    with open('assets/naive_bayes.csv', 'w', newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerows(datos)
    
    print("Naive Bayes CSV generado satisfactoriamente")


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

    print("Regresion lineal CSV generado exitosamente.")

generar_lineal_csv()
generar_bayes_csv()
