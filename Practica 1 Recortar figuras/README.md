# Práctica 1: Segmentación de Figuras por Color

## 📌 Descripción
Esta práctica implementa un sistema de segmentación de imágenes que utiliza el espacio de color HSV para identificar y aislar figuras geométricas según su color. El objetivo es demostrar técnicas básicas de procesamiento de imágenes y visión por computadora para la detección de objetos basada en color.

## 🎯 Objetivos
- Aprender a utilizar el espacio de color HSV para segmentación de imágenes
- Implementar máscaras de color para aislar objetos específicos
- Desarrollar habilidades en procesamiento de imágenes con OpenCV
- Entender la importancia de los umbrales en la detección de colores

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.x
- **Librerías:** OpenCV (cv2), NumPy
- **Herramientas:** Visual Studio Code / Editor de texto

## 🚀 Instalación y Ejecución

1. **Instalar dependencias:**
```bash
pip install opencv-python numpy
```

2. **Colocar los archivos:**
   - Asegúrate de tener `figura.png` en el mismo directorio que `Recortar-Figuras.py`

3. **Ejecutar el programa:**
```bash
python Recortar-Figuras.py
```

4. **Interacción:**
   - El programa mostrará 4 ventanas con las figuras segmentadas
   - Presiona cualquier tecla para cerrar todas las ventanas

## 📊 Metodología

1. **Conversión a espacio HSV:** La imagen BGR se convierte a HSV para mejor segmentación
2. **Definición de umbrales:** Se establecen rangos específicos para cada color:
   - Rojo: 0-10 y 170-180 (dos rangos por naturaleza circular)
   - Verde: 35-80
   - Azul: 100-130
   - Amarillo: 20-30
3. **Aplicación de máscaras:** Se crean máscaras binarias con `cv.inRange()`
4. **Visualización:** Se muestran las 4 máscaras resultantes

## 🖼️ Evidencias

### Resultados de Segmentación

#### Figuras Rojas

#### Figuras Verdes

#### Figuras Azules

#### Figuras Amarillas
