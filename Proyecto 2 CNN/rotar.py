from PIL import Image
import os

def rotar_imagenes_en_carpeta_unica(ruta_carpeta_entrada, nombre_carpeta_salida, num_rotaciones):
    """
    Procesa todas las imágenes de una carpeta de entrada, rotándolas 
    un número específico de veces (incrementando 1° en cada rotación), 
    y guarda TODOS los resultados en una única carpeta de salida.

    Args:
        ruta_carpeta_entrada (str): Ruta a la carpeta que contiene las imágenes originales.
        nombre_carpeta_salida (str): Nombre de la única carpeta donde se guardarán todos los resultados.
        num_rotaciones (int): Número total de imágenes a generar por cada imagen original.
    """

    print(f"--- Iniciando proceso de rotación masiva (de 1° a {num_rotaciones}°) ---")

    # 1. Crear la carpeta única de salida si no existe
    try:
        os.makedirs(nombre_carpeta_salida, exist_ok=True)
        print(f"Carpeta de salida única '{nombre_carpeta_salida}' lista.")
    except OSError as e:
        print(f"Error al crear la carpeta de salida: {e}")
        return

    # Extensiones de archivo que consideraremos como imágenes
    EXTENSIONES_IMAGEN = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
    contador_total = 0

    # 2. Iterar sobre todos los archivos en la carpeta de entrada
    for nombre_archivo in os.listdir(ruta_carpeta_entrada):
        ruta_imagen_original = os.path.join(ruta_carpeta_entrada, nombre_archivo)

        # 2.1. Verificar si es un archivo y si es una imagen
        if os.path.isfile(ruta_imagen_original) and nombre_archivo.lower().endswith(EXTENSIONES_IMAGEN):

            print(f"\nProcesando: **{nombre_archivo}**")

            try:
                # Cargar la imagen original
                imagen_original = Image.open(ruta_imagen_original)
                nombre_base, extension = os.path.splitext(nombre_archivo)

                # 2.2. Rotar y guardar la imagen
                for i in range(1, num_rotaciones + 1):
                    angulo_rotacion = i

                    # Rotar la imagen
                    # El parámetro expand=True es crucial para que la imagen no se recorte
                    imagen_rotada = imagen_original.rotate(angulo_rotacion, expand=True)

                    # Crear el nombre del archivo de salida: "[nombre_base]_[angulo]grados.[ext]"
                    nombre_archivo_salida = f"{nombre_base}_{angulo_rotacion}grados{extension}"
                    ruta_guardado = os.path.join(nombre_carpeta_salida, nombre_archivo_salida)

                    # Guardar la imagen
                    imagen_rotada.save(ruta_guardado)
                    contador_total += 1
                    # Opcional: print(f"  > Guardada rotación de {angulo_rotacion}°.")

                print(f"  > Generadas {num_rotaciones} rotaciones.")

            except Exception as e:
                print(f"Error al procesar la imagen {nombre_archivo}: {e}")
        
        else:
            print(f"Ignorando archivo/carpeta (no es imagen): {nombre_archivo}")


    print(f"\n--- Proceso completado. Total de archivos generados: {contador_total} ---")
    print(f"Todos los resultados se encuentran en la carpeta: {nombre_carpeta_salida}")

# --- Configuración y Llamada a la Función ---

# Carpeta que contiene las imágenes originales
CARPETA_DE_ENTRADA = 'imagenes' 

# Nombre de la ÚNICA carpeta donde se guardarán TODOS los resultados
CARPETA_DE_SALIDA_UNICA = 'resultados'

# Número de rotaciones (e.g., 360 para 1° a 360°)
NUMERO_DE_ROTACIONES = 360 

# Ejecutar la función
rotar_imagenes_en_carpeta_unica(CARPETA_DE_ENTRADA, CARPETA_DE_SALIDA_UNICA, NUMERO_DE_ROTACIONES)