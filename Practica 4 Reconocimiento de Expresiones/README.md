# Práctica 4: Reconocimiento de Expresiones Faciales

## 📌 Descripción
Esta práctica implementa un sistema de reconocimiento de expresiones faciales en tiempo real utilizando el algoritmo Fisherfaces. El sistema es capaz de detectar y clasificar siete emociones básicas (enfado, disgusto, miedo, felicidad, neutral, tristeza, sorpresa) a partir del video capturado por una cámara web, mostrando el resultado directamente sobre el rostro detectado.

## 🎯 Objetivos
- Implementar un sistema de reconocimiento de expresiones faciales en tiempo real
- Utilizar el algoritmo Fisherfaces para clasificación de emociones
- Crear y entrenar un modelo con dataset de expresiones faciales
- Aprender a preprocesar imágenes faciales para análisis de emociones
- Visualizar resultados de clasificación directamente sobre el video en tiempo real

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.x
- **Librerías:** OpenCV (cv2), NumPy, OS
- **Algoritmo:** FisherFaceRecognizer de OpenCV
- **Clasificador:** haarcascade_frontalface_alt.xml (para detección facial)
- **Hardware:** Cámara web
- **Tamaño de imagen:** 48x48 píxeles (estándar para reconocimiento de emociones)

## 🚀 Instalación y Ejecución

### Prerrequisitos
```bash
pip install opencv-python numpy opencv-contrib-python
```

### Paso 1: Entrenamiento del Modelo
```bash
python Entrenamiento-F.py
```
Este script:
- Lee todas las imágenes del dataset organizadas por carpetas
- Asigna etiquetas numéricas automáticamente (0=angry, 1=disgust, etc.)
- Entrena el modelo Fisherfaces
- Guarda el modelo entrenado en `FisherFace.xml`

### Paso 2: Reconocimiento en Tiempo Real
```bash
python fisherface.py
```
Este script:
- Carga el modelo entrenado `FisherFace.xml`
- Inicia la cámara web
- Detecta rostros en cada frame
- Clasifica la expresión facial
- Muestra el resultado en pantalla

## 📊 Metodología

### 1. Preparación del Dataset de Entrenamiento
- **Estructura:** Una carpeta por cada emoción con imágenes correspondientes
- **Formato:** Imágenes en escala de grises (parámetro `0` en `cv.imread`)
- **Etiquetado automático:** Asigna etiquetas numéricas basadas en el orden de las carpetas

### 2. Proceso de Entrenamiento (Entrenamiento-F.py)
1. **Lectura recursiva:** Recorre todas las carpetas del dataset
2. **Carga de imágenes:** Carga cada imagen en escala de grises
3. **Asignación de etiquetas:** Cada carpeta representa una clase (emoción)
4. **Entrenamiento Fisherfaces:** 
   - Utiliza Análisis Discriminante Lineal (LDA)
   - Maximiza la separación entre clases
   - Minimiza la varianza intra-clase
5. **Guardado del modelo:** Serializa el modelo entrenado en XML

### 3. Reconocimiento en Tiempo Real (fisherface.py)
1. **Detección facial:** Usa Haarcascade para localizar rostros
2. **Preprocesamiento:**
   - Extracción de ROI (región del rostro)
   - Redimensionamiento a 48x48 píxeles (tamaño óptimo para emociones)
   - Interpolación CUBIC para mantener calidad
3. **Clasificación:**
   - El modelo devuelve: `(etiqueta_predicha, confianza)`
   - Umbral: confianza < 500 → emoción reconocida
   - confianza ≥ 500 → "Desconocido"
4. **Visualización:**
   - **Rectángulo verde + nombre de emoción:** Reconocimiento exitoso
   - **Rectángulo rojo + "Desconocido":** Confianza baja
   - **Valor de confianza:** Mostrado sobre el rostro

### 4. Emociones Reconocidas
El sistema clasifica 7 emociones básicas:
1. **angry** (0) - Enfado
2. **disgust** (1) - Disgusto
3. **fear** (2) - Miedo
4. **happy** (3) - Felicidad
5. **neutral** (4) - Neutral
6. **sad** (5) - Tristeza
7. **surprise** (6) - Sorpresa

## 🖼️ Evidencias

### Reconocimiento en tiempo real
![prueba](https://github.com/user-attachments/assets/abcd3f31-873d-45e5-b300-de97af83cd31)
