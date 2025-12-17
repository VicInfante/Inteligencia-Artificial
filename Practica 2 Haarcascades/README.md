Práctica 2: Haarcascade
Este proyecto implementa un sistema de detección de rostros en tiempo real utilizando el algoritmo de Viola-Jones y clasificadores Haar Cascades. Esta técnica es un pilar en la Visión Artificial para la identificación rápida de patrones en imágenes.

🧠 Funcionamiento del Código
El script haarcascades.py realiza la detección facial siguiendo este flujo lógico:
Carga del Clasificador: Se importa el archivo haarcascade_frontalface_alt.xml, el cual contiene un modelo pre-entrenado con miles de rasgos faciales positivos y negativos.
Captura de Video: El programa accede a la cámara del equipo en tiempo real mediante la función cv.VideoCapture(0).
Pre-procesamiento (Escala de Grises): Cada frame se convierte a blanco y negro para reducir la carga computacional, ya que el algoritmo Haar se basa en variaciones de intensidad lumínica y no en color.
Detección Multiescala: Se utiliza la función detectMultiScale para localizar rostros de diferentes tamaños dentro del campo de visión.
Visualización: Una vez detectado el rostro, el sistema obtiene las coordenadas $(x, y, w, h)$ y dibuja un rectángulo verde alrededor del área identificada.

🛠️ Tecnologías Utilizadas
Lenguaje: Python.
Librería Principal: OpenCV (cv2) para el procesamiento de video y visión artificial.
Modelo de IA: Clasificador en cascada de Haar (haarcascade_frontalface_alt.xml).

🚀 Instrucciones de Ejecución
Para correr este proyecto localmente, sigue estos pasos:
Requisito de Archivos: Verifica que el archivo XML del clasificador esté en la misma carpeta que el script de Python.
Instalación de Dependencias: pip install opencv-python
Ejecución: python haarcascades.py
Salida: Presiona la tecla 's' (o cierra la ventana) para finalizar la captura de video.

📸 Evidencias
A continuación, se adjuntan las pruebas de funcionamiento del detector de rostros:
👤 Detección Facial en Tiempo Real
