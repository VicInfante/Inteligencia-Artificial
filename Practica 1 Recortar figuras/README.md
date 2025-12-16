Práctica 1: Recortar Figuras
Este proyecto implementa técnicas de Visión Artificial para la segmentación y aislamiento de objetos en una imagen digital. El objetivo principal es filtrar elementos basándose en sus propiedades cromáticas dentro de un espacio de color controlado.

🧠 Funcionamiento del Código
El script Recortar-Figuras.py procesa la imagen siguiendo una lógica de filtrado por umbrales:

Lectura y Conversión: El programa carga una imagen llamada figura.png y la convierte del espacio de color BGR al espacio HSV (Hue, Saturation, Value). Esta conversión es fundamental para la IA y Visión Artificial, ya que el modelo HSV es más robusto ante variaciones de iluminación.

Segmentación por Rangos: Se definen tuplas de límites bajos y altos para identificar colores específicos:

Rojo: Se utilizan dos rangos (umbralBajoRojo1 a umbralAltoRojo2) para capturar el matiz rojo en ambos extremos del espectro.

Verde, Azul y Amarillo: Se establecen rangos únicos que permiten aislar estas tonalidades con precisión.

Generación de Máscaras: Utilizando cv.inRange(), el código crea imágenes binarias donde solo los píxeles que coinciden con el color buscado se mantienen visibles, permitiendo así "recortar" visualmente las figuras del fondo.

🛠️ Tecnologías
Lenguaje: Python.

Librerías: * OpenCV (cv2) para el procesamiento de imágenes.

NumPy para la manipulación de arreglos multidimensionales.

🚀 Instrucciones
Asegúrate de tener el archivo figura.png en el mismo directorio que el script.

Ejecuta el código: python Recortar-Figuras.py.

Se abrirán cuatro ventanas independientes mostrando las figuras filtradas por color.


📸 Evidencias
En esta sección se presentan los resultados obtenidos tras la ejecución del algoritmo de segmentación:

🔴 Figuras Rojas
![Captura de pantalla 2025-12-16 155627](https://github.com/user-attachments/assets/834dd999-b9d7-4221-88ed-8f711058aa58)

🟢 Figuras Verdes
![Captura de pantalla 2025-12-16 155615](https://github.com/user-attachments/assets/319555f9-9e3a-4fbf-99ba-62c41432f346)

🔵 Figuras Azules
![Captura de pantalla 2025-12-16 155600](https://github.com/user-attachments/assets/78476bb7-e3d1-418f-bb5b-f7a77f53f786)

🟡 Figuras Amarillas
![Captura de pantalla 2025-12-16 155521](https://github.com/user-attachments/assets/ff55721f-b3ce-4ef9-8a2c-bc2847d7a212)

