# Práctica 5: Clasificación de Deportes con Redes Neuronales Convolucionales (CNN)

## 📌 Descripción
Esta práctica implementa un sistema completo de clasificación de imágenes deportivas utilizando Redes Neuronales Convolucionales (CNN). El sistema incluye tanto el entrenamiento de un modelo de deep learning desde cero como su posterior uso para clasificar nuevos deportes, demostrando el flujo completo de un proyecto de visión por computadora.

## 🎯 Objetivos
- Implementar una CNN desde cero para clasificación de imágenes deportivas
- Aprender el flujo completo de un proyecto de deep learning: preprocesamiento, entrenamiento, validación y evaluación
- Entender la arquitectura de capas convolucionales, pooling y fully connected
- Visualizar métricas de entrenamiento (accuracy, loss) y resultados de predicción
- Crear un modelo reutilizable guardado en formato H5 para inferencia posterior

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.x
- **Librerías:** TensorFlow, Keras, NumPy, Matplotlib, scikit-learn, scikit-image
- **Arquitectura:** Red Neuronal Convolucional (CNN) personalizada
- **Tamaño de imagen:** 21x28 píxeles con 3 canales (RGB)
- **Deportes clasificados:** 10 categorías diferentes

## 🚀 Instalación y Ejecución

### Prerrequisitos
```bash
pip install tensorflow keras numpy matplotlib scikit-learn scikit-image
```

### Estructura del Dataset
```
sportimages/
├── americano/      # Imágenes de fútbol americano
├── basket/         # Imágenes de baloncesto
├── beisball/       # Imágenes de béisbol
├── boxeo/          # Imágenes de boxeo
├── ciclismo/       # Imágenes de ciclismo
├── f1/             # Imágenes de Fórmula 1
├── futbol/         # Imágenes de fútbol
├── golf/           # Imágenes de golf
├── natacion/       # Imágenes de natación
└── tenis/          # Imágenes de tenis
```

### Paso 1: Entrenamiento del Modelo
```bash
python cnn.py
```
Este script realiza:
- Carga y preprocesamiento de todas las imágenes del dataset
- División en conjuntos de entrenamiento (80%) y prueba (20%)
- Construcción y entrenamiento de la CNN
- Guardado del modelo entrenado en `models/riesgo.h5`
- Generación de gráficos de métricas y predicciones

### Paso 2: Prueba del Modelo Entrenado
```bash
python prueba.py
```
Este script:
- Carga el modelo preentrenado `models/riesgo2.h5`
- Procesa nuevas imágenes (ej: `natacion.jpg`)
- Realiza predicciones y muestra el deporte clasificado
- Formato de salida: `nombre_imagen deporte_detectado`

### Parámetros de Entrenamiento:
- **Tasa de aprendizaje (INIT_LR):** 0.001
- **Épocas:** 40 iteraciones completas
- **Tamaño de batch:** 64 imágenes por lote
- **División de datos:** 80% entrenamiento, 20% prueba
- **Validación:** 20% del entrenamiento para validación

## 📊 Metodología

### 1. Preprocesamiento de Datos
- **Carga recursiva:** Lectura automática de todas las imágenes organizadas por carpetas
- **Filtrado:** Solo imágenes con 3 canales (color RGB)
- **Redimensionamiento:** Uniformización a 21x28 píxeles
- **Normalización:** Escalado de valores de píxeles a rango [0, 1]
- **One-hot encoding:** Conversión de etiquetas categóricas a formato vectorial

### 2. Arquitectura de la CNN
La red consta de 3 bloques convolucionales seguidos de capas fully connected:

1. **Bloque 1:**
   - Conv2D (32 filtros, kernel 3x3)
   - LeakyReLU (alpha=0.1)
   - MaxPooling2D (2x2)
   - Dropout (50%)

2. **Bloque 2:**
   - Conv2D (64 filtros, kernel 3x3)
   - LeakyReLU (alpha=0.1)
   - MaxPooling2D (2x2)
   - Dropout (50%)

3. **Bloque 3:**
   - Conv2D (128 filtros, kernel 3x3)
   - LeakyReLU (alpha=0.1)
   - MaxPooling2D (2x2)
   - Dropout (50%)

4. **Capas Fully Connected:**
   - Flatten (aplanamiento)
   - Dense (32 neuronas)
   - LeakyReLU (alpha=0.1)
   - Dropout (50%)
   - Dense (10 neuronas, softmax) - Salida para 10 deportes

### 3. Entrenamiento
- **Función de pérdida:** Categorical Crossentropy
- **Optimizador:** SGD (Stochastic Gradient Descent)
- **Métrica principal:** Accuracy
- **Validación:** Durante entrenamiento con 20% de datos
- **Guardado automático:** Modelo en formato H5 después del entrenamiento

### 4. Evaluación y Visualización
- **Gráficos de métricas:** Accuracy y Loss para entrenamiento/validación
- **Predicciones correctas:** Muestra 9 ejemplos bien clasificados
- **Predicciones incorrectas:** Muestra 9 ejemplos mal clasificados
- **Reporte de clasificación:** Métricas por clase (precision, recall, f1-score)

### 5. Inferencia (prueba.py)
- **Carga de modelo:** Modelo H5 preentrenado
- **Preprocesamiento:** Redimensionamiento y normalización igual que en entrenamiento
- **Predicción:** Usa softmax para obtener probabilidades por clase
- **Resultado:** Muestra el deporte con mayor probabilidad

## 🖼️ Evidencias

### Predicciones
![natacion](https://github.com/user-attachments/assets/d08afe0a-bc84-42ff-81d1-fa509fac6e33)
![boxeo](https://github.com/user-attachments/assets/8699f682-4f63-4525-acbf-66ea8b958b16)
![Prueba](https://github.com/user-attachments/assets/723aa2b3-eb28-4037-b06f-0003ada9c008)
