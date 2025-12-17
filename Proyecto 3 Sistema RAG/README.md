# Proyecto 3: Sistema RAG (Retrieval Augmented Generation) Académico

## 📌 Descripción
Este proyecto implementa un sistema completo RAG (Retrieval Augmented Generation) para consultas académicas sobre filosofía de la tecnología, psicología digital y estudios sociales de la IA. El sistema incluye todas las etapas del pipeline RAG: recolección de corpus, preprocesamiento, creación de embeddings, indexación vectorial y generación de respuestas usando modelos de lenguaje locales (Ollama).

## 🎯 Objetivos
- Implementar un pipeline completo RAG desde la recolección de datos hasta la generación de respuestas
- Crear un sistema de recuperación de información basado en embeddings vectoriales con FAISS
- Integrar modelos de lenguaje local (Ollama) para generación contextualizada
- Desarrollar herramientas de preprocesamiento de textos académicos en múltiples formatos
- Construir una interfaz interactiva para consultas académicas especializadas

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.x
- **Librerías principales:** Ollama, Sentence-Transformers, FAISS, PyPDF2, BeautifulSoup, NumPy
- **Modelos de embeddings:** paraphrase-multilingual-MiniLM-L12-v2 (multilingüe)
- **Modelo de lenguaje:** Llama 3.2 (local via Ollama)
- **Indexación vectorial:** FAISS con índice HNSW
- **Formatos soportados:** PDF, TXT, DOCX, HTML

## 🚀 Instalación y Ejecución

### Prerrequisitos
```bash
# Instalación completa de dependencias
pip install ollama sentence-transformers faiss-cpu PyPDF2 beautifulsoup4 requests numpy scikit-learn
ollama pull llama3.2  # Descargar modelo de lenguaje
```

### Estructura del Proyecto
```
faiss_index/            # Índices vectoriales FAISS generados
corpus/                # Documentos originales descargados
corpus_procesado/      # Documentos preprocesados y fragmentados
corpus_embeddings/     # Embeddings generados y metadatos
consultas_guardadas/   # Historial de consultas y respuestas
```

### Flujo de Ejecución Secuencial:

#### Paso 1: Recolección del Corpus
```bash
python 01_recolectar_corpus.py
```
- **Función:** Descarga y extrae textos de fuentes web y PDFs
- **Formatos soportados:** HTML, PDF (online y local)
- **Salida:** Archivos TXT en carpeta `corpus/`
- **Interfaz:** Opciones para URLs web, PDFs online o PDFs locales

#### Paso 2: Preprocesamiento de Textos
```bash
python 02_preprocesar_textos.py
```
- **Función:** Limpia, normaliza y fragmenta documentos
- **Operaciones:** Eliminación de URLs, correos, caracteres especiales
- **Fragmentación:** Divide en chunks de ~400 palabras con preservación de párrafos
- **Salida:** Fragmentos individuales en `corpus_procesado/`

#### Paso 3: Vectorización del Corpus
```bash
python 03_vectorizar_corpus.py
```
- **Función:** Genera embeddings para todos los fragmentos
- **Modelo:** Sentence-Transformers multilingüe (384 dimensiones)
- **Proceso:** Lee múltiples formatos (TXT, PDF, DOCX), divide en chunks, genera embeddings
- **Salida:** Embeddings en `corpus_embeddings/embeddings.npz` y metadatos en JSON

#### Paso 4: Creación del Índice FAISS
```bash
python 04_crear_indice_faiss.py
```
- **Función:** Construye índice vectorial para búsqueda eficiente
- **Tipo de índice:** HNSW (balance óptimo velocidad/precisión)
- **Características:** Búsqueda aproximada con 32 vecinos, efSearch=50
- **Salida:** Índice FAISS en `faiss_index/` con metadatos y configuración

#### Paso 5: Sistema RAG Completo
```bash
python 05_rag_ollama.py
```
- **Función:** Sistema interactivo de consultas con recuperación y generación
- **Modelo LLM:** Llama 3.2 via Ollama (temperatura 0.3)
- **Recuperación:** Top 5 documentos más relevantes por similitud coseno
- **Interfaz:** Modo interactivo, pruebas automáticas o solo búsqueda

## 📊 Metodología

### 1. Pipeline RAG Implementado
```
Consulta → Embedding → Búsqueda FAISS → Recuperación → Contexto → Prompt → Ollama → Respuesta
```

### 2. Procesamiento de Documentos
- **Ingestión multi-formato:** TXT, PDF, DOCX, HTML
- **Fragmentación inteligente:** Chunks de 500 palabras con overlap de 50 palabras
- **Preservación de metadatos:** Carpeta temática, archivo origen, número de fragmento
- **Normalización textual:** Limpieza de caracteres especiales, URLs, emails

### 3. Generación de Embeddings
- **Modelo:** `paraphrase-multilingual-MiniLM-L12-v2`
- **Características:** 384 dimensiones, multilingüe (español optimizado)
- **Proceso:** Batch encoding con barra de progreso
- **Almacenamiento:** NPZ comprimido con metadatos JSON asociados

### 4. Indexación Vectorial con FAISS
- **Arquitectura HNSW:** Grafos de navegación de pequeña mundo (Hierarchical Navigable Small World)
- **Parámetros:** M=32 (vecinos), efConstruction=200, efSearch=50
- **Métrica:** Distancia L2 (Euclidiana) convertida a similitud coseno
- **Eficiencia:** Búsqueda sub-lineal en grandes colecciones de documentos

### 5. Sistema de Recuperación
- **Búsqueda semántica:** Similitud entre embedding de consulta y documentos
- **Ranking:** Top-k documentos por similitud coseno (1/(1+distancia))
- **Umbralización:** Resultados filtrados por relevancia
- **Contexto formateado:** Metadatos completos para cada documento recuperado

### 6. Generación con Ollama
- **Modelo local:** Llama 3.2 3B (equilibrio rendimiento/calidad)
- **Prompt engineering:** 
  ```
  Sistema: Asistente académico especializado
  Contexto: {documentos recuperados}
  Instrucciones: Usar solo contexto, citar fuentes, ser preciso
  Pregunta: {consulta del usuario}
  ```
- **Parámetros:** temperature=0.3 (baja creatividad, alta precisión), num_predict=1000 tokens

### 7. Interfaz de Usuario
- **Tres modos de operación:** Interactivo, pruebas automáticas, solo búsqueda
- **Comandos especiales:** `/temas`, `/salir`, `/ayuda`
- **Visualización:** Resultados formateados con documentos de referencia
- **Persistencia:** Opción para guardar consultas y respuestas en JSON

## 🖼️ Evidencias

## Interfaz interactiva
#![prueba1](https://github.com/user-attachments/assets/ed0aa246-8306-4eb8-82b2-09894ef63e81)

![prueba2](https://github.com/user-attachments/assets/4cc7d3d3-b649-44a3-962b-4b8847326801)

### Resultados de búsqueda
![prueba3](https://github.com/user-attachments/assets/e1118b13-18a5-4954-9981-733bc177dcab)

![prueba4](https://github.com/user-attachments/assets/533c97d5-72fc-4756-9f23-34d13ee642ac)
