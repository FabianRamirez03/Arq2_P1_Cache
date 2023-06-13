import time
from PIL import Image
from PIL import ImageFilter

def aplicar_filtro(imagen):
    # Leer la imagen
    img = Image.open(imagen)

    # Convertir la imagen a escala de grises
    img_gray = img.convert("L")

    # Aplicar el filtro Sobel
    img_filtrada = img_gray.filter(ImageFilter.FIND_EDGES)

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
img_resultante.show()

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
