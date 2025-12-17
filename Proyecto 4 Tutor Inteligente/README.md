# Proyecto 4: Tutor Inteligente para Algoritmos con Fine-Tuning LoRA

## 📌 Descripción
Este proyecto implementa un sistema de tutoría inteligente especializado en algoritmos y estructuras de datos, utilizando fine-tuning con LoRA (Low-Rank Adaptation) sobre el modelo Llama 3.2. El sistema es capaz de responder preguntas, generar pseudocódigo, explicar conceptos complejos y corregir errores algorítmicos, todo basado en un dataset especializado de preguntas y respuestas.

## 🎯 Objetivos
- Implementar fine-tuning con LoRA para adaptar un modelo de lenguaje a un dominio específico (algoritmos)
- Crear un dataset especializado de tutoría en algoritmos y estructuras de datos
- Desarrollar un pipeline completo desde el entrenamiento hasta el despliegue con Ollama
- Optimizar el modelo para ejecución local eficiente mediante cuantización GGUF
- Construir un sistema de tutoría interactivo que responda con precisión técnica

## 🛠️ Tecnologías Utilizadas
- **Modelo base:** Llama 3.2 3B Instruct (Meta)
- **Framework:** Hugging Face Transformers, PEFT (LoRA)
- **Entrenamiento:** bitsandbytes (8-bit quantization), PyTorch
- **Dataset:** JSONL personalizado con 200+ pares instrucción-respuesta
- **Conversión:** llama.cpp para formato GGUF cuantizado
- **Despliegue:** Ollama con archivo Modelfile personalizado

## 🚀 Instalación y Ejecución

### Prerrequisitos
```bash
# Instalación de dependencias principales
pip install torch transformers datasets peft bitsandbytes accelerate
pip install sentencepiece protobuf

# Para conversión GGUF
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make

# Ollama (descargar desde ollama.ai)
```

### Estructura del Proyecto
```
tutor_dataset.jsonl           # Dataset de entrenamiento (200+ ejemplos)
train_lora.py                 # Script de entrenamiento con LoRA
convert.py                    # Conversión a formato GGUF
Modelfile                     # Configuración para Ollama (sin extensión)
lora-tutor/                   # Adaptadores LoRA entrenados
llama_lora.gguf              # Modelo fusionado y cuantizado
```

### Flujo de Ejecución Completo:

#### Paso 1: Preparar el Dataset
- **Formato:** JSONL con pares `{"instruction": "...", "response": "..."}`
- **Contenido:** 200+ preguntas y respuestas sobre algoritmos, estructuras de datos, complejidad temporal
- **Ejemplo:**
```json
{"instruction": "Explica la complejidad temporal de la búsqueda binaria.", "response": "La búsqueda binaria tiene una complejidad temporal de O(log n). Esto se debe a que el espacio de búsqueda se reduce a la mitad en cada iteración..."}
```

#### Paso 2: Entrenamiento con LoRA
```bash
python train_lora.py
```
**Parámetros de entrenamiento:**
- **Modelo base:** `meta-llama/Llama-3.2-3B-Instruct`
- **LoRA rank (r):** 8 (bajo para eficiencia)
- **LoRA alpha:** 16 (factor de escalado)
- **Módulos objetivo:** q_proj, k_proj, v_proj, o_proj (attention layers)
- **Batch size efectivo:** 16 (gradient accumulation)
- **Épocas:** 3
- **Quantization:** 8-bit (bitsandbytes)

#### Paso 3: Conversión a GGUF
```bash
python convert.py --base meta-llama/Llama-3.2-3B-Instruct --model ./lora-tutor --out llama_lora.gguf --dtype float16
```
**Proceso de conversión:**
1. Fusiona adaptadores LoRA con modelo base
2. Guarda modelo fusionado temporalmente
3. Convierte a formato GGUF con cuantización Q8_0
4. Genera archivo `llama_lora.gguf` optimizado

#### Paso 4: Crear Modelo Ollama
```bash
ollama create tutor-algoritmos -f Modelfile
```
**Contenido del Modelfile:**
- **FROM:** Modelo base Llama 3.2
- **ADAPTER:** Archivo GGUF fusionado
- **SYSTEM:** Prompt específico para tutoría algorítmica
- **PARAMETERS:** temperature=0.2 (baja creatividad), top_p=0.9

#### Paso 5: Ejecutar el Tutor
```bash
ollama run tutor-algoritmos
```
**Ejemplo de interacción:**
```
Usuario: ¿Cuál es la complejidad de Bubble Sort?
Tutor: Bubble Sort tiene complejidad O(n²) en el peor caso. Esto se debe a que...
```

## 📊 Metodología

### 1. Dataset Especializado
- **200+ ejemplos cuidadosamente elaborados**
- **Temas cubiertos:** Complejidad algorítmica, estructuras de datos, grafos, árboles, búsqueda, ordenamiento
- **Formato estandarizado:** Instrucción clara + respuesta técnica completa
- **Incluye:** Pseudocódigo, fórmulas matemáticas, explicaciones paso a paso

### 2. Fine-Tuning con LoRA
- **Adaptación eficiente:** Solo 0.1% de parámetros entrenados (~8M de 8B)
- **Configuración LoRA:**
  - `r=8`: Dimensión de baja jerarquía (balance calidad/eficiencia)
  - `lora_alpha=16`: Factor de escalado para adaptadores
  - `target_modules`: Capas de atención (q_proj, k_proj, v_proj, o_proj)
  - `lora_dropout=0.1`: Regularización para evitar overfitting
- **Entrenamiento optimizado:**
  - 8-bit quantization para ahorrar memoria
  - Gradient accumulation (batch size efectivo 16)
  - FP16 mixed precision
  - 3 épocas para convergencia adecuada

### 3. Pipeline de Conversión
1. **Fusión LoRA:** Merge adaptadores con modelo base
2. **Serialización segura:** Guardado en formato safetensors
3. **Conversión GGUF:** Optimizado para llama.cpp
4. **Cuantización Q8_0:** 8-bit quantization (balance precisión/velocidad)

### 4. Sistema de Prompt Engineering
- **System prompt especializado:** Define rol de tutor algorítmico
- **Parámetros de inferencia:**
  - `temperature=0.2`: Respuestas consistentes y técnicas
  - `top_p=0.9`: Balance entre creatividad y precisión
- **Contexto restringido:** Solo utiliza conocimiento del dataset

### 5. Optimizaciones de Rendimiento
- **Memoria eficiente:** 8-bit quantization durante entrenamiento
- **Inferencia rápida:** Formato GGUF optimizado para CPU/GPU
- **Modelo liviano:** ~3.5GB (vs 12GB del modelo original)
- **Respuesta en tiempo real:** Latencia baja para interacción fluida

## 🖼️ Evidencias

### Interacción con el tutor
![prueba1](https://github.com/user-attachments/assets/ba2abab9-1df3-43ce-958e-719f35dd3521)

![prueba2](https://github.com/user-attachments/assets/417624c8-e345-4486-96c4-04b825516e47)

![prueba3](https://github.com/user-attachments/assets/e30c4d43-2c61-4c3d-8a52-34091cccda80)

