import cv2
import time

def aplicar_filtro(imagen):
    # Leer la imagen
    img = cv2.imread(imagen)

    # Convertir la imagen a escala de grises
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar el filtro Sobel
    grad_x = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
    img_filtrada = cv2.addWeighted(grad_x, 0.5, grad_y, 0.5, 0)

    return img_filtrada

# Ruta de la imagen
ruta_imagen = "images/perros.jpg"

# Tiempo inicial de ejecucion
inicio = time.time()

# Aplicacion del filtro
img_resultante = aplicar_filtro(ruta_imagen)

# Tiempo total de ejecucion
tiempo_ejecucion = time.time() - inicio
print("Tiempo de ejecución:", tiempo_ejecucion, "segundos")

# Mostrar imagen con el filtro aplicado
cv2.namedWindow("Imagen Filtrada", cv2.WINDOW_NORMAL)
cv2.imshow("Imagen Filtrada", img_resultante)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Agregar el tiempo de ejecucion en el archivo de texto
nombre_archivo = "images/tiempos_ejecucion.txt"
contenido_existente = {}
try:
    with open(nombre_archivo, "r") as archivo:
        contenido_existente = eval(archivo.read())
except FileNotFoundError:
    pass

contenido_existente["TiempoPython"] = tiempo_ejecucion

# Escribir el contenido actualizado en el archivo
with open(nombre_archivo, "w") as archivo:
    archivo.write(str(contenido_existente))