import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer
import faiss
import pickle

# ---------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------
EMBEDDINGS_PATH = "corpus_embeddings/embeddings.npz"
METADATA_PATH = "corpus_embeddings/metadatos.json"
FAISS_INDEX_PATH = "faiss_index"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2" 

# ---------------------------------------------------------
# 1. CARGAR DATOS PREPROCESADOS
# ---------------------------------------------------------
def cargar_datos_preprocesados():
    """Carga embeddings y metadatos guardados previamente."""
    print("📂 Cargando embeddings y metadatos...")
    
    # Cargar embeddings
    datos = np.load(EMBEDDINGS_PATH)
    embeddings = datos['embeddings']
    print(f"  ✓ Embeddings cargados: {embeddings.shape}")
    
    # Cargar metadatos
    with open(METADATA_PATH, 'r', encoding='utf-8') as f:
        metadatos = json.load(f)
    print(f"  ✓ Metadatos cargados: {len(metadatos)} documentos")
    
    return embeddings, metadatos

# ---------------------------------------------------------
# 2. CREAR ÍNDICE FAISS
# ---------------------------------------------------------
def crear_indice_faiss(embeddings, tipo_indice="flat"):
    """
    Crea un índice FAISS para búsqueda vectorial.
    
    Tipos de índice:
    - "flat": Exacto pero más lento para muchos vectores (L2 o Inner Product)
    - "ivf": Más rápido, aproximado (requiere entrenamiento)
    - "hnsw": Balance entre velocidad y precisión (recomendado)
    """
    dimension = embeddings.shape[1]
    print(f"\n🔧 Creando índice FAISS (dimensión: {dimension})...")
    
    if tipo_indice == "flat":
        # Índice plano - búsqueda exacta
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        print("  ✓ Índice FlatL2 creado (búsqueda exacta)")
    
    elif tipo_indice == "ivf":
        # Índice IVF (Inverted File) - más rápido, aproximado
        nlist = 100  # Número de clusters
        quantizer = faiss.IndexFlatL2(dimension)
        index = faiss.IndexIVFFlat(quantizer, dimension, nlist, faiss.METRIC_L2)
        
        # Entrenar el índice
        print("  Entrenando índice IVF...")
        index.train(embeddings)
        index.add(embeddings)
        index.nprobe = 10  # Número de clusters a revisar
        print("  ✓ Índice IVF creado (búsqueda aproximada)")
    
    elif tipo_indice == "hnsw":
        # Índice HNSW - buen balance velocidad/precisión
        index = faiss.IndexHNSWFlat(dimension, 32)  # 32 es el número de vecinos
        index.hnsw.efConstruction = 200  # Controla la construcción
        index.hnsw.efSearch = 50  # Controla la búsqueda
        index.add(embeddings)
        print("  ✓ Índice HNSW creado (balance velocidad/precisión)")
    
    else:
        raise ValueError(f"Tipo de índice no válido: {tipo_indice}")
    
    return index

# ---------------------------------------------------------
# 3. GUARDAR ÍNDICE Y METADATOS
# ---------------------------------------------------------
def guardar_indice(index, metadatos, tipo_indice):
    """Guarda el índice FAISS y los metadatos asociados."""
    os.makedirs(FAISS_INDEX_PATH, exist_ok=True)
    
    # Guardar índice FAISS
    index_file = os.path.join(FAISS_INDEX_PATH, f"index_{tipo_indice}.faiss")
    faiss.write_index(index, index_file)
    print(f"  ✓ Índice guardado: {index_file}")
    
    # Guardar metadatos asociados
    metadata_file = os.path.join(FAISS_INDEX_PATH, "index_metadata.pkl")
    with open(metadata_file, 'wb') as f:
        pickle.dump(metadatos, f)
    print(f"  ✓ Metadatos guardados: {metadata_file}")
    
    # Guardar información de configuración
    config = {
        "tipo_indice": tipo_indice,
        "dimension": index.d,
        "total_vectores": index.ntotal,
        "modelo_embeddings": MODEL_NAME
    }
    
    config_file = os.path.join(FAISS_INDEX_PATH, "config.json")
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"  ✓ Configuración guardada: {config_file}")
    
    return index_file, metadata_file

# ---------------------------------------------------------
# 4. PROBAR EL ÍNDICE CON CONSULTAS DE EJEMPLO
# ---------------------------------------------------------
def probar_indice(index, metadatos, modelo_embeddings, consultas_prueba=None):
    """Prueba el índice con algunas consultas de ejemplo."""
    if consultas_prueba is None:
        consultas_prueba = [
            "¿Qué son los algoritmos deshumanizantes?",
            "Cómo afecta la ansiedad a la generación Z?",
            "Qué es el filtro burbuja en redes sociales?",
            "Habermas y la razón en el espacio público",
            "Narcisismo en TikTok"
        ]
    
    print(f"\n🧪 Probando índice con {len(consultas_prueba)} consultas...")
    
    for i, consulta in enumerate(consultas_prueba):
        print(f"\nConsulta {i+1}: '{consulta}'")
        
        # Convertir consulta a embedding
        embedding_consulta = modelo_embeddings.encode([consulta], convert_to_numpy=True)
        
        # Buscar los k documentos más similares
        k = 3  # Número de resultados a retornar
        distancias, indices = index.search(embedding_consulta, k)
        
        # Mostrar resultados
        for j, (distancia, idx) in enumerate(zip(distancias[0], indices[0])):
            if idx != -1:  # -1 significa no encontrado
                doc = metadatos[idx]
                print(f"  {j+1}. [Distancia: {distancia:.4f}]")
                print(f"     📁 Tema: {doc['carpeta']}")
                print(f"     📄 Archivo: {doc['archivo']}")
                print(f"     📝 Fragmento: {doc['texto'][:150]}...")
                print()

# ---------------------------------------------------------
# 5. FUNCIÓN PRINCIPAL
# ---------------------------------------------------------
def main():
    print("=" * 60)
    print("CREACIÓN DE ÍNDICE VECTORIAL FAISS")
    print("=" * 60)
    
    # Paso 1: Cargar datos
    embeddings, metadatos = cargar_datos_preprocesados()
    
    # Paso 2: Crear índice (elige el tipo que prefieras)
    # Opciones: "flat" (exacto), "ivf" (rápido), "hnsw" (recomendado)
    TIPO_INDICE = "hnsw"
    index = crear_indice_faiss(embeddings, tipo_indice=TIPO_INDICE)
    
    # Paso 3: Guardar índice
    guardar_indice(index, metadatos, TIPO_INDICE)
    
    # Paso 4: Cargar modelo de embeddings para pruebas
    print("\n🤖 Cargando modelo para generar embeddings de consultas...")
    modelo = SentenceTransformer(MODEL_NAME)
    
    # Paso 5: Probar el índice
    probar_indice(index, metadatos, modelo)
    
    # Información de rendimiento
    print("\n" + "=" * 60)
    print("INFORMACIÓN DEL ÍNDICE CREADO")
    print("=" * 60)
    print(f"• Tipo de índice: {TIPO_INDICE}")
    print(f"• Dimensión: {index.d}")
    print(f"• Total de vectores: {index.ntotal}")
    print(f"• Ruta del índice: {FAISS_INDEX_PATH}/")
    
    # Mostrar estructura de archivos creados
    print(f"\n📁 Archivos creados en '{FAISS_INDEX_PATH}/':")
    for archivo in os.listdir(FAISS_INDEX_PATH):
        tamaño = os.path.getsize(os.path.join(FAISS_INDEX_PATH, archivo))
        print(f"  - {archivo} ({tamaño:,} bytes)")

# ---------------------------------------------------------
# 6. FUNCIÓN PARA CARGAR ÍNDICE (para uso futuro)
# ---------------------------------------------------------
def cargar_indice_existente():
    """Carga un índice FAISS previamente guardado."""
    # Buscar el archivo de índice
    archivos_faiss = [f for f in os.listdir(FAISS_INDEX_PATH) if f.endswith('.faiss')]
    
    if not archivos_faiss:
        raise FileNotFoundError(f"No se encontró índice FAISS en {FAISS_INDEX_PATH}")
    
    # Cargar el primer índice encontrado
    index_file = os.path.join(FAISS_INDEX_PATH, archivos_faiss[0])
    print(f"📂 Cargando índice: {index_file}")
    index = faiss.read_index(index_file)
    
    # Cargar metadatos
    metadata_file = os.path.join(FAISS_INDEX_PATH, "index_metadata.pkl")
    with open(metadata_file, 'rb') as f:
        metadatos = pickle.load(f)
    
    # Cargar configuración
    config_file = os.path.join(FAISS_INDEX_PATH, "config.json")
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    print(f"✓ Índice cargado: {config['tipo_indice']} con {index.ntotal} vectores")
    
    return index, metadatos, config

# ---------------------------------------------------------
# EJECUCIÓN
# ---------------------------------------------------------
if __name__ == "__main__":
    # Instalar FAISS si no lo tienes:
    # pip install faiss-cpu  # Para CPU
    # pip install faiss-gpu  # Para GPU (opcional)
    
    try:
        import faiss
        main()
    except ImportError:
        print("❌ FAISS no está instalado. Instálalo con:")
        print("   pip install faiss-cpu  # Para CPU")
        print("   # o")
        print("   pip install faiss-gpu  # Para GPU (opcional)")