import os
import glob
from typing import List, Dict, Any
import PyPDF2  
from sentence_transformers import SentenceTransformer
import numpy as np

# ---------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------
CORPUS_PATH = "corpus_procesado"  
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2" 

CHUNK_SIZE = 500  
OVERLAP = 50     

# ---------------------------------------------------------
# 1. FUNCIÓN PARA LEER DIFERENTES FORMATOS DE ARCHIVO
# ---------------------------------------------------------
def leer_archivo(ruta_archivo: str) -> str:
    """Lee el contenido de un archivo según su extensión."""
    texto = ""
    
    if ruta_archivo.endswith('.txt'):
        with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as f:
            texto = f.read()
    
    elif ruta_archivo.endswith('.pdf'):
        try:
            with open(ruta_archivo, 'rb') as f:
                lector = PyPDF2.PdfReader(f)
                for pagina in lector.pages:
                    texto += pagina.extract_text() + "\n"
        except Exception as e:
            print(f"Error leyendo PDF {ruta_archivo}: {e}")
    
    elif ruta_archivo.endswith(('.docx', '.doc')):
        try:
            import docx
            doc = docx.Document(ruta_archivo)
            texto = "\n".join([para.text for para in doc.paragraphs])
        except ImportError:
            print("Instala python-docx para leer .docx: pip install python-docx")
        except Exception as e:
            print(f"Error leyendo Word {ruta_archivo}: {e}")
    
    return texto.strip()

# ---------------------------------------------------------
# 2. FUNCIÓN PARA DIVIDIR TEXTO EN CHUNKS
# ---------------------------------------------------------
def dividir_en_chunks(texto: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> List[str]:
    """Divide un texto en chunks con superposición."""
    palabras = texto.split()
    chunks = []
    
    if len(palabras) <= chunk_size:
        return [" ".join(palabras)]
    
    i = 0
    while i < len(palabras):
        chunk = palabras[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    
    return chunks

# ---------------------------------------------------------
# 3. FUNCIÓN PRINCIPAL PARA PROCESAR EL CORPUS
# ---------------------------------------------------------
def procesar_corpus(corpus_path: str) -> List[Dict[str, Any]]:
    """Recorre todas las carpetas, lee archivos y prepara chunks con metadatos."""
    documentos = []
    
    # Recorrer cada carpeta temática
    for carpeta in os.listdir(corpus_path):
        ruta_carpeta = os.path.join(corpus_path, carpeta)
        
        if not os.path.isdir(ruta_carpeta):
            continue
        
        print(f"Procesando carpeta: {carpeta}")
        
        # Buscar todos los archivos de texto en la carpeta
        patrones = ['*.txt', '*.pdf', '*.docx', '*.doc']
        archivos = []
        for patron in patrones:
            archivos.extend(glob.glob(os.path.join(ruta_carpeta, patron)))
        
        # Procesar cada archivo
        for archivo in archivos:
            print(f"  Leyendo: {os.path.basename(archivo)}")
            
            # Leer contenido
            texto = leer_archivo(archivo)
            if not texto:
                print(f"    ⚠️  Archivo vacío o no legible: {archivo}")
                continue
            
            # Dividir en chunks
            chunks = dividir_en_chunks(texto)
            
            # Crear registro para cada chunk
            for i, chunk in enumerate(chunks):
                documento = {
                    'id': f"{carpeta}_{os.path.basename(archivo)}_{i}",
                    'texto': chunk,
                    'carpeta': carpeta,
                    'archivo': os.path.basename(archivo),
                    'chunk_num': i,
                    'total_chunks': len(chunks),
                    'palabras': len(chunk.split())
                }
                documentos.append(documento)
    
    return documentos

# ---------------------------------------------------------
# 4. FUNCIÓN PARA GENERAR EMBEDDINGS
# ---------------------------------------------------------
def generar_embeddings(documentos: List[Dict[str, Any]], model_name: str = MODEL_NAME):
    """Genera embeddings para todos los documentos."""
    print(f"\nCargando modelo de embeddings: {model_name}")
    modelo = SentenceTransformer(model_name)
    
    textos = [doc['texto'] for doc in documentos]
    
    print(f"Generando embeddings para {len(textos)} chunks...")
    embeddings = modelo.encode(textos, show_progress_bar=True, convert_to_numpy=True)
    
    # Añadir embeddings a cada documento
    for i, doc in enumerate(documentos):
        doc['embedding'] = embeddings[i]
    
    print(f"✓ Embeddings generados. Dimensión: {embeddings.shape}")
    return documentos, embeddings

# ---------------------------------------------------------
# 5. GUARDAR LOS RESULTADOS
# ---------------------------------------------------------
def guardar_resultados(documentos: List[Dict[str, Any]], ruta_salida: str = "corpus_embeddings"):
    """Guarda los documentos con embeddings en archivos NPZ y JSON."""
    import json
    import numpy as np
    
    # Crear carpeta si no existe
    os.makedirs(ruta_salida, exist_ok=True)
    
    # Separar embeddings y metadatos
    embeddings = np.array([doc.pop('embedding') for doc in documentos])  # Removemos embedding del dict
    
    # Guardar embeddings como numpy array
    np.savez_compressed(
        os.path.join(ruta_salida, "embeddings.npz"),
        embeddings=embeddings
    )
    
    # Guardar metadatos como JSON
    with open(os.path.join(ruta_salida, "metadatos.json"), 'w', encoding='utf-8') as f:
        json.dump(documentos, f, ensure_ascii=False, indent=2)
    
    # Guardar también los textos planos (útil para debugging)
    with open(os.path.join(ruta_salida, "textos.txt"), 'w', encoding='utf-8') as f:
        for doc in documentos:
            f.write(f"=== {doc['id']} ===\n")
            f.write(doc['texto'][:500] + "...\n\n")
    
    print(f"\n✓ Resultados guardados en: {ruta_salida}/")
    print(f"  - embeddings.npz: {embeddings.shape[0]} embeddings de dimensión {embeddings.shape[1]}")
    print(f"  - metadatos.json: {len(documentos)} documentos con metadatos")
    print(f"  - textos.txt: muestra de los textos")

# ---------------------------------------------------------
# 6. EJECUCIÓN PRINCIPAL
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("PROCESAMIENTO DE CORPUS PARA SISTEMA RAG")
    print("=" * 60)
    
    # Paso 1: Procesar corpus y crear chunks
    print("\n📂 1. Procesando estructura de carpetas...")
    documentos = procesar_corpus(CORPUS_PATH)
    
    if not documentos:
        print("❌ No se encontraron documentos para procesar.")
        exit()
    
    print(f"✓ {len(documentos)} chunks creados de {len(set(d['carpeta'] for d in documentos))} temas")
    
    # Paso 2: Generar embeddings
    print("\n🔤 2. Generando embeddings...")
    documentos_con_embeddings, embeddings = generar_embeddings(documentos)
    
    # Paso 3: Guardar resultados
    print("\n💾 3. Guardando resultados...")
    guardar_resultados(documentos_con_embeddings)
    
    # Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    print(f"• Carpetas procesadas: {len(os.listdir(CORPUS_PATH))}")
    print(f"• Total de chunks/textos: {len(documentos_con_embeddings)}")
    print(f"• Dimensión de embeddings: {embeddings.shape[1]}")
    print(f"• Tamaño total del corpus: {sum(len(d['texto']) for d in documentos_con_embeddings):,} caracteres")
    
    # Mostrar algunos ejemplos
    print("\n📄 Muestra de chunks creados:")
    for i, doc in enumerate(documentos_con_embeddings[:3]):
        print(f"  {i+1}. [{doc['carpeta']}] {doc['texto'][:100]}...")
    
    print("\n✅ ¡Paso 1 completado!")