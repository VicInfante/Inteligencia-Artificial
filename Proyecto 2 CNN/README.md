# Proyecto 2: Sistema de Clasificación de Animales con CNN

## 📌 Descripción
Este proyecto implementa un sistema completo de clasificación de imágenes de animales utilizando Redes Neuronales Convolucionales (CNN). El sistema incluye herramientas de preprocesamiento (redimensionamiento y rotación de imágenes), entrenamiento de un modelo de deep learning, y un módulo de prueba para clasificar nuevas imágenes en cinco categorías de animales.

## 🎯 Objetivos
- Implementar un pipeline completo de visión por computadora: preprocesamiento, entrenamiento y evaluación
- Crear herramientas para aumentar datasets mediante rotación de imágenes
- Entrenar una CNN capaz de clasificar 5 categorías de animales
- Desarrollar un sistema modular con scripts específicos para cada tarea
- Evaluar el rendimiento del modelo con métricas precisas y visualizaciones

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.x
- **Librerías:** TensorFlow, Keras, OpenCV, NumPy, Matplotlib, scikit-learn, scikit-image, PIL
- **Arquitectura:** CNN con múltiples capas convolucionales y fully connected
- **Tamaño de imagen:** 28x21 píxeles (formato retrato)
- **Categorías:** 5 clases de animales (gato, hormiga, mariquita, perro, tortuga)

## 🚀 Instalación y Ejecución

### Prerrequisitos
```bash
pip install tensorflow keras opencv-python numpy matplotlib scikit-learn scikit-image pillow
```

### Estructura del Proyecto
```
datasets/                    # Dataset original organizado por categorías
datasets_resized/           # Imágenes redimensionadas automáticamente
models/                     # Modelos entrenados guardados
imagenes/                   # Imágenes para rotación (opcional)
resultados/                 # Imágenes rotadas generadas
```

### Flujo de Ejecución Recomendado:

#### Paso 1: Redimensionar Imágenes del Dataset
```bash
python resize.py
```
- **Función:** Redimensiona todas las imágenes a 28x21 píxeles
- **Entrada:** `datasets/` con subcarpetas por animal
- **Salida:** `datasets_resized/` con estructura mantenida
- **Parámetros:** Tamaño fijo (28,21) con interpolación AREA

#### Paso 2: Aumentar Dataset con Rotaciones (Opcional)
```bash
python rotar.py
```
- **Función:** Genera 360 rotaciones por imagen (1° a 360°)
- **Entrada:** `imagenes/` con imágenes a rotar
- **Salida:** `resultados/` con todas las rotaciones
- **Parámetros:** Expand=True para evitar recorte

#### Paso 3: Entrenar el Modelo CNN
```bash
python cnn.py
```
- **Función:** Entrena la CNN con el dataset redimensionado
- **Entrada:** `datasets_resized/` organizado por categorías
- **Salida:** Modelo guardado en `models/riesgo.h5`
- **Parámetros:** 40 épocas, batch_size=64, learning_rate=0.001

#### Paso 4: Probar el Modelo con Nuevas Imágenes
```bash
python prueba.py
```
- **Función:** Clasifica imágenes nuevas usando el modelo entrenado
- **Entrada:** Archivos especificados en el código (ej: mariquita6.jpg)
- **Salida:** Nombre del archivo y categoría predicha
- **Formato:** `nombre_imagen clase_predicha`

## 📊 Metodología

### 1. Preprocesamiento de Datos (resize.py)
- **Lectura recursiva:** Todas las imágenes en estructura jerárquica
- **Redimensionamiento uniforme:** 28x21 píxeles (alto x ancho)
- **Interpolación AREA:** Adecuada para reducción de tamaño
- **Preservación de estructura:** Mantiene organización por carpetas/categorías

### 2. Aumento de Datos (rotar.py)
- **Rotación completa:** 360 rotaciones por imagen (1° incrementos)
- **Expand=True:** La imagen no se recorta, ajusta tamaño del canvas
- **Generación masiva:** Crea dataset expandido para mejor generalización
- **Organización única:** Todas las rotaciones en una sola carpeta

### 3. Entrenamiento CNN (cnn.py)
**Arquitectura de la red:**
1. **Capa Convolucional 1:** 32 filtros 3x3, LeakyReLU, MaxPooling 2x2, Dropout 50%
2. **Capa Convolucional 2:** 64 filtros 3x3, LeakyReLU, MaxPooling 2x2, Dropout 50%
3. **Capa Convolucional 3:** 128 filtros 3x3, LeakyReLU, MaxPooling 2x2, Dropout 50%
4. **Capas Fully Connected:**
   - Flatten (aplanamiento)
   - Dense 32 neuronas, LeakyReLU, Dropout 50%
   - Dense 5 neuronas (softmax para 5 clases)

**Proceso de entrenamiento:**
- **División de datos:** 80% entrenamiento, 20% prueba
- **Validación:** 20% del entrenamiento para monitoreo
- **Normalización:** Valores de píxeles escalados a [0, 1]
- **One-hot encoding:** Etiquetas categóricas a formato vectorial
- **Optimización:** SGD con learning_rate=0.001
- **Función de pérdida:** Categorical Crossentropy

### 4. Evaluación y Visualización
- **Gráficos de métricas:** Accuracy y Loss durante entrenamiento/validación
- **Predicciones correctas/incorrectas:** Grids 3x3 con ejemplos visuales
- **Reporte de clasificación:** Precision, recall, f1-score por clase
- **Guardado automático:** Modelo en formato H5 para reutilización

### 5. Inferencia (prueba.py)
- **Carga de modelo:** Modelo H5 preentrenado
- **Preprocesamiento:** Mismo redimensionamiento (28x21) y normalización
- **Predicción:** Softmax para probabilidades por clase
- **Resultado:** Muestra la clase con mayor probabilidad

## 🖼️ Evidencias
![prueba](https://github.com/user-attachments/assets/67854224-c78f-4df6-94a6-db520a50b9ed)
