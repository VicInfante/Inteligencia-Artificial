# Proyecto 1: Algoritmo A* con Visualización Interactiva

## 📌 Descripción
Este proyecto implementa una visualización interactiva del algoritmo de búsqueda A* (A-star) para encontrar el camino óptimo entre dos puntos en una cuadrícula. El sistema permite al usuario colocar paredes, definir nodos de inicio y fin, y observar en tiempo real cómo el algoritmo explora el espacio de búsqueda para encontrar la ruta más eficiente, incluyendo movimientos diagonales.

## 🎯 Objetivos
- Implementar el algoritmo A* con soporte para movimientos diagonales
- Crear una interfaz gráfica interactiva para visualizar el proceso de búsqueda
- Permitir la colocación dinámica de obstáculos, nodo inicio y nodo fin
- Visualizar el proceso de exploración y el camino óptimo encontrado
- Entender los componentes del algoritmo: función g, función h, y función f

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.x
- **Librerías:** PyGame, PriorityQueue
- **Algoritmo:** A* con heurística Manhattan y soporte diagonal
- **Interfaz:** Ventana gráfica interactiva 800x800 píxeles
- **Estructura de datos:** Grid bidimensional de nodos

## 🚀 Instalación y Ejecución

### Prerrequisitos
```bash
pip install pygame
```

### Ejecución del programa
```bash
python algoritmo.py
```

### Controles de la interfaz:

**Interacción con mouse:**
- **Click izquierdo:** Colocar/modificar elementos
  1. Primer click: Define nodo inicio (naranja)
  2. Segundo click: Define nodo fin (morado)
  3. Clicks posteriores: Colocar paredes (negro)
- **Click derecho:** Eliminar elementos (restablecer a blanco)

**Teclado:**
- **ESPACIO:** Inicia/ejecuta el algoritmo A* (requiere inicio y fin definidos)
- **ESC o cerrar ventana:** Salir del programa

**Configuración inicial:**
- Grid de 11x11 nodos (121 nodos totales)
- Ventana de 800x800 píxeles
- Movimiento diagonal con costo 1.4 vs ortogonal con costo 1.0

## 📊 Metodología

### 1. Representación del Espacio de Búsqueda
- **Grid 11x11:** Matriz bidimensional de nodos
- **Cada nodo contiene:**
  - Posición (fila, columna)
  - Estado (inicio, fin, pared, vacío, visitado, camino)
  - Costos g, h, f para el algoritmo A*
  - Lista de vecinos accesibles

### 2. Algoritmo A* Implementado
- **Función de costo g(n):** Costo acumulado desde el nodo inicio
- **Función heurística h(n):** Distancia Manhattan al nodo objetivo
- **Función de evaluación f(n):** f(n) = g(n) + h(n)
- **Cola de prioridad:** Mantiene nodos ordenados por f(n)

### 3. Movimientos y Costos
- **Movimientos ortogonales (4 direcciones):** Costo = 1.0
  - Arriba, abajo, izquierda, derecha
- **Movimientos diagonales (4 direcciones):** Costo = 1.4 (√2 aproximado)
  - Diagonal superior izquierda, superior derecha, etc.

### 4. Proceso de Búsqueda Visualizado
1. **Inicialización:** Nodo inicio con g=0, f=h(inicio,fin)
2. **Exploración:** Extraer nodo con menor f de la cola de prioridad
3. **Expansión:** Evaluar todos los vecinos accesibles (no paredes)
4. **Actualización:** Recalcular costos g y f si se encuentra mejor camino
5. **Marcado visual:**
   - **Gris:** Nodos en cola de prioridad (open set)
   - **Rojo:** Nodos ya procesados (closed set)
   - **Verde:** Camino óptimo encontrado
6. **Terminación:** Cuando se alcanza el nodo objetivo o no hay más nodos

### 5. Reconstrucción del Camino
- **Diccionario came_from:** Almacena el predecesor de cada nodo
- **Trazado inverso:** Desde el nodo fin hasta el inicio
- **Visualización:** Camino marcado en verde

### 6. Interactividad del Sistema
- **Actualización dinámica:** Los vecinos se recalculan antes de cada ejecución
- **Reinicio visual:** Click derecho restablece nodos individualmente
- **Feedback en tiempo real:** Cambios de color inmediatos durante la búsqueda

## 🖼️ Evidencias
![prueba](https://github.com/user-attachments/assets/b3094db7-3e5e-4cdd-a7f3-20ad9750a463)
