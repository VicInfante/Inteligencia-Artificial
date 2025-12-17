# Práctica 2: Detección de Rostros con Haarcascade

## 📌 Descripción
Esta práctica implementa un sistema de detección de rostros en tiempo real utilizando el clasificador en cascada de Haar. El programa captura video desde la cámara web, detecta rostros en cada frame, los recorta, redimensiona y guarda automáticamente para crear un dataset de entrenamiento facial.

## 🎯 Objetivos
- Implementar detección facial en tiempo real con clasificadores Haarcascade
- Capturar y procesar video en streaming usando OpenCV
- Crear un dataset de imágenes faciales para entrenamiento de modelos
- Aprender a extraer y procesar ROI (Regiones de Interés)
- Entender los parámetros de `detectMultiScale` para optimizar la detección

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.x
- **Librerías:** OpenCV (cv2), NumPy
- **Clasificador:** haarcascade_frontalface_alt.xml (clasificador preentrenado)
- **Hardware:** Cámara web

## 🚀 Instalación y Ejecución

1. **Instalar dependencias:**
```bash
pip install opencv-python numpy
```

2. **Descargar el clasificador Haarcascade:**
   - Descargar `haarcascade_frontalface_alt.xml` desde el repositorio oficial de OpenCV
   - Colocarlo en el mismo directorio que el script

3. **Crear carpeta de almacenamiento:**
```bash
mkdir victor
```

4. **Ejecutar el programa:**
```bash
python haarcascades.py
```

5. **Controles durante la ejecución:**
   - El programa inicia automáticamente la cámara web
   - Presiona **ESC** (tecla 27) para salir
   - Las imágenes se guardan automáticamente en la carpeta `victor/`

## 📊 Metodología

1. **Inicialización:**
   - Carga del clasificador Haarcascade preentrenado
   - Inicio de captura de video (cámara índice 0)

2. **Procesamiento por frame:**
   - Captura de frame desde la cámara
   - Conversión a escala de grises (mejora el rendimiento del clasificador)
   - Detección de rostros con `detectMultiScale(scaleFactor=1.3, minNeighbors=5)`

3. **Extracción y procesamiento de rostros:**
   - Para cada rostro detectado (coordenadas x, y, w, h):
     - Extracción de la región facial (ROI)
     - Redimensionamiento a 100x100 píxeles usando interpolación INTER_AREA
     - Visualización en ventana separada

4. **Almacenamiento automático:**
   - Guarda una imagen por cada frame procesado
   - Nomenclatura: `victor/victor{i}.jpg` (donde i es un contador incremental)
   - Se guarda en cada iteración del bucle principal

## 🖼️ Evidencias

### Detección en tiempo real
![Captura de pantalla 2025-12-16 163122](https://github.com/user-attachments/assets/25e18f52-c566-4513-bb79-3c6068ac09cc)
