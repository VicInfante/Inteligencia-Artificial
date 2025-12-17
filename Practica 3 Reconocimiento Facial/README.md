# Práctica 3: Reconocimiento Facial con Múltiples Algoritmos

## 📌 Descripción
Esta práctica implementa un sistema completo de reconocimiento facial utilizando tres algoritmos diferentes: LBPH, Eigenfaces y Fisherfaces. El sistema incluye tanto la fase de entrenamiento (creación de modelos a partir de un dataset) como la fase de reconocimiento en tiempo real mediante cámara web, permitiendo comparar el desempeño de cada método.

## 🎯 Objetivos
- Implementar y comparar tres algoritmos de reconocimiento facial: LBPH, Eigenfaces y Fisherfaces
- Crear un sistema completo que incluya entrenamiento y reconocimiento en tiempo real
- Aprender a preparar y estructurar datasets para entrenamiento de modelos faciales
- Entender las diferencias en umbrales y métricas de confianza entre algoritmos
- Desarrollar habilidades en procesamiento de video y análisis facial en tiempo real

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.x
- **Librerías:** OpenCV (cv2), NumPy, OS
- **Módulos de OpenCV:** cv2.face (LBPHFaceRecognizer, EigenFaceRecognizer, FisherFaceRecognizer)
- **Clasificador:** haarcascade_frontalface_alt.xml
- **Hardware:** Cámara web

## 🚀 Instalación y Ejecución

### Prerrequisitos
```bash
pip install opencv-python numpy opencv-contrib-python
```

### Fase 1: Entrenamiento de modelos

**Para LBPH:**
```bash
python Entrenamiento-L.py
```
*Genera: LBPHFace.xml*

**Para Eigenfaces:**
```bash
python Entrenamiento-E.py
```
*Genera: Eigenface.xml*

**Para Fisherfaces:**
```bash
python Entrenamiento-F.py
```
*Genera: FisherFace.xml*

### Fase 2: Reconocimiento en tiempo real

**LBPH:**
```bash
python LBPH.py
```

**Eigenfaces:**
```bash
python eigenfaces.py
```

**Fisherfaces:**
```bash
python fisherface.py
```

## 📊 Metodología

### 1. Preparación del Dataset
- Estructura jerárquica: `datasets/nombre_persona/imagenes.jpg`
- Imágenes en escala de grises
- Etiquetado automático basado en estructura de carpetas

### 2. Entrenamiento de Modelos
- **Carga de datos:** Lectura recursiva de imágenes y asignación de etiquetas
- **Preprocesamiento:** Conversión a escala de grises si es necesario
- **Entrenamiento:** Cada algoritmo extrae características diferentes:
  - **LBPH:** Patrones binarios locales (robusto a cambios de iluminación)
  - **Eigenfaces:** Análisis de componentes principales (PCA)
  - **Fisherfaces:** Análisis discriminante lineal (LDA)

### 3. Reconocimiento en Tiempo Real
1. **Detección facial:** Uso de Haarcascade para localizar rostros
2. **Preprocesamiento:** Recorte y redimensionamiento a 100x100 píxeles
3. **Predicción:** Cada algoritmo devuelve (etiqueta, confianza)
4. **Umbralización:**
   - LBPH: confianza < 70 → reconocido
   - Eigenfaces: confianza > 2800 → desconocido
   - Fisherfaces: confianza < 500 → reconocido
5. **Visualización:** Rectángulo verde (reconocido) o rojo (desconocido) + nombre

## 🖼️ Evidencias

### Reconocimiento con LBPH
![LBPH](https://github.com/user-attachments/assets/fb876ef7-258a-4c0c-a673-898bf2aa8d0f)

### Reconocimiento con Eigenfaces
![eigenfaces](https://github.com/user-attachments/assets/637f395d-1b46-4baa-a651-53616fa707fd)

### Reconocimiento con Fisherfaces
![fisherfaces](https://github.com/user-attachments/assets/991e11cb-13ba-405e-aea6-78ef3889d723)
