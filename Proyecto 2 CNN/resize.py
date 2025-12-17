import cv2
import os

def resize_images(input_folder, output_folder, target_size=(28, 21)):
    # Crear el directorio de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Obtener lista de imágenes en el directorio de entrada
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Procesar solo imágenes
            # Ruta completa de la imagen de entrada
            input_path = os.path.join(input_folder, filename)
            
            # Leer la imagen
            image = cv2.imread(input_path)
            
            if image is not None:
                # Redimensionar la imagen
                resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
                
                # Ruta completa para guardar la imagen redimensionada
                output_path = os.path.join(output_folder, filename)
                
                # Guardar la imagen redimensionada
                cv2.imwrite(output_path, resized_image)
                print(f"Procesada: {filename}")
            else:
                print(f"Error al procesar: {filename}")

# Directorios de entrada y salida para cada categoría
categories = ['perro','gato','tortuga','mariquita','hormiga']
input_base_dir = 'datasets'
output_base_dir = 'datasets_resized'

# Procesar cada categoría
for category in categories:
    input_dir = os.path.join(input_base_dir, category)
    output_dir = os.path.join(output_base_dir, category)
    
    if os.path.exists(input_dir):
        print(f"\nProcesando categoría: {category}")
        resize_images(input_dir, output_dir)
    else:
        print(f"\nDirectorio no encontrado: {input_dir}")
