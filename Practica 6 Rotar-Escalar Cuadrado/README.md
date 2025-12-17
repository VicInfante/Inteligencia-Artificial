# Práctica 6: Control de Cuadrado con Detección de Manos MediaPipe

## 📌 Descripción
Esta práctica implementa un sistema interactivo que utiliza visión por computadora para detectar ambas manos en tiempo real y controlar un cuadrado en pantalla. El sistema permite rotar y escalar un cuadrado azul utilizando gestos de manos: la mano izquierda controla la rotación basada en su orientación, y ambas manos juntas controlan el escalado mediante la distancia entre los dedos índices.

## 🎯 Objetivos
- Implementar detección de manos en tiempo real usando MediaPipe
- Controlar parámetros gráficos (rotación y escalado) mediante gestos de manos
- Calcular y aplicar rotaciones basadas en la orientación de la mano
- Crear una interfaz visual interactiva con OpenCV
- Entender el mapeo entre landmarks de manos y acciones en pantalla

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.x
- **Librerías:** OpenCV, MediaPipe, NumPy
- **Detección de manos:** MediaPipe Hands (máximo 2 manos)
- **Interfaz:** OpenCV con ventana en tiempo real
- **Hardware:** Cámara web

## 🚀 Instalación y Ejecución

### Prerrequisitos
```bash
pip install opencv-python mediapipe numpy
```

### Ejecución del programa
```bash
python prueba.py
```

## 📊 Metodología

### 1. Detección de Manos con MediaPipe
- **Configuración:** `max_num_hands=2` para detectar ambas manos simultáneamente
- **Procesamiento:** Conversión de BGR a RGB (requerido por MediaPipe)
- **Landmarks:** 21 puntos por mano detectados (muñeca, nudillos, puntas de dedos)
- **Confianza:** `min_detection_confidence=0.5` para equilibrio precisión/rendimiento

### 2. Procesamiento de Landmarks
- **Identificación de manos:** Etiqueta 'Left' o 'Right' según la lateralidad
- **Puntos clave extraídos:**
  - **Dedo índice (landmark 8):** Para posición y distancia
  - **Muñeca (landmark 0):** Para cálculo de orientación
  - **Dedo medio (landmark 12):** Para cálculo de ángulo

### 3. Control de Rotación (Mano Izquierda)
1. **Cálculo del ángulo:**
   - Vector entre muñeca (0) y dedo medio (12)
   - Fórmula: `angle = arctan2(dy, dx)` convertido a grados
2. **Aplicación de rotación:**
   - Transformación de los 4 vértices del cuadrado azul
   - Rotación alrededor del centro del cuadrado
   - Visualización actualizada en tiempo real

### 4. Control de Escalado (Ambas Manos)
1. **Detección de dos manos:** Índice izquierdo e índice derecho
2. **Cálculo de distancia:** Distancia euclidiana entre puntos índices
3. **Mapeo a tamaño:**
   - Tamaño del rectángulo verde = distancia entre índices
   - Tamaño del cuadrado azul se escala proporcionalmente
   - Clamping: valores entre 30px y mitad de pantalla para estabilidad

### 5. Visualización Gráfica
- **Cuadrado azul:** Cuadrado rotado y escalado controlado por gestos
- **Rectángulo verde:** Visualiza la distancia entre índices de ambas manos
- **Círculos rojo/azul:** Marcan las posiciones de los dedos índices
- **Textos informativos:**
  - Tamaño actual del cuadrado
  - Ángulo de rotación actual
- **Landmarks de manos:** Esqueleto completo de ambas manos visible

### 6. Algoritmo de Rotación de Puntos
- **Transformación geométrica:** Rotación de cada vértice alrededor del centro
- **Fórmula matemática:**
  ```
  qx = cx + cos(θ)*(px-cx) - sin(θ)*(py-cy)
  qy = cy + sin(θ)*(px-cx) + cos(θ)*(py-cy)
  ```
- **Actualización en tiempo real:** Cada frame recalcula la posición rotada

## 🖼️ Evidencias


https://github.com/user-attachments/assets/eadf9af9-40b8-4dde-8a8c-2aa67a20418d


