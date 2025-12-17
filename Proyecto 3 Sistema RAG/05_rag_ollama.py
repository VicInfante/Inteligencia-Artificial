# rag_ollama_simple.py
import os
import pickle
import json
import faiss
import numpy as np
from typing import List, Dict, Any
from datetime import datetime
import ollama
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------
FAISS_INDEX_PATH = "faiss_index"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
OLLAMA_MODEL = "llama3.2:latest"
SYSTEM_PROMPT = """Eres un asistente académico especializado en filosofía de la tecnología, 
psicología digital y estudios sociales de la IA. Responde basándote en el contexto proporcionado.

CONTEXTO:
{context}

INSTRUCCIONES:
1. Usa SOLO la información del contexto proporcionado
2. Si no hay información suficiente, di "No encontré información en los documentos"
3. Cita las fuentes mencionando la carpeta temática
4. Sé preciso y académico en tus respuestas

PREGUNTA: {question}

RESPUESTA:"""

# ---------------------------------------------------------
# 1. CLASE PRINCIPAL DEL SISTEMA RAG (SIMPLIFICADA)
# ---------------------------------------------------------
class RAGSystemOllama:
    def __init__(self, faiss_index_path: str = FAISS_INDEX_PATH):
        """Inicializa el sistema RAG con Ollama (sin verificación de modelos)."""
        print("🚀 Inicializando sistema RAG con Ollama...")
        
        # Cargar índice FAISS
        self.index, self.metadatos, self.config = self._cargar_indice(faiss_index_path)
        print(f"   ✓ Índice cargado: {self.index.ntotal} documentos")
        
        # Inicializar modelos
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        print(f"   ✓ Modelo de embeddings cargado: {EMBEDDING_MODEL}")
        
        # Asumir que Ollama está disponible (sin verificar lista de modelos)
        print(f"   ✓ Usando modelo Ollama: {OLLAMA_MODEL}")
        self.ollama_disponible = True  # Asumimos que está disponible
        
        # Estadísticas
        self._mostrar_estadisticas()
    
    def _cargar_indice(self, path: str):
        """Carga el índice FAISS y metadatos."""
        # Buscar archivo de índice
        archivos_faiss = [f for f in os.listdir(path) if f.endswith('.faiss')]
        if not archivos_faiss:
            raise FileNotFoundError(f"No se encontró índice FAISS en {path}")
        
        index_file = os.path.join(path, archivos_faiss[0])
        metadata_file = os.path.join(path, "index_metadata.pkl")
        config_file = os.path.join(path, "config.json")
        
        # Cargar
        index = faiss.read_index(index_file)
        
        with open(metadata_file, 'rb') as f:
            metadatos = pickle.load(f)
            
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        return index, metadatos, config
    
    def _mostrar_estadisticas(self):
        """Muestra estadísticas del corpus cargado."""
        temas = set(doc['carpeta'] for doc in self.metadatos)
        print(f"   📚 Temas cargados: {len(temas)}")
        print(f"   📄 Documentos totales: {len(self.metadatos)}")
        
        # Mostrar algunos temas como ejemplo
        print("   🏷️  Algunos temas disponibles:")
        for i, tema in enumerate(list(temas)[:5]):
            print(f"      {i+1}. {tema}")
        if len(temas) > 5:
            print(f"      ... y {len(temas)-5} más")
    
    # ---------------------------------------------------------
    # 2. BÚSQUEDA Y RECUPERACIÓN
    # ---------------------------------------------------------
    def buscar_documentos(self, consulta: str, k: int = 5) -> List[Dict[str, Any]]:
        """Busca documentos relevantes para una consulta."""
        # Convertir consulta a embedding
        query_embedding = self.embedding_model.encode([consulta], convert_to_numpy=True)
        
        # Buscar en índice FAISS
        distancias, indices = self.index.search(query_embedding, k)
        
        # Preparar resultados
        resultados = []
        for distancia, idx in zip(distancias[0], indices[0]):
            if idx != -1:  # -1 significa no encontrado
                doc = self.metadatos[idx].copy()
                doc['similitud'] = float(1 / (1 + distancia))  # Convertir distancia a similitud
                doc['distancia'] = float(distancia)
                resultados.append(doc)
        
        return resultados
    
    def formatear_contexto(self, documentos: List[Dict[str, Any]]) -> str:
        """Formatea los documentos como contexto para el LLM."""
        contexto = ""
        for i, doc in enumerate(documentos, 1):
            contexto += f"[Documento {i} - {doc['carpeta']}]\n"
            contexto += f"Archivo: {doc['archivo']} (Fragmento {doc['chunk_num']+1}/{doc['total_chunks']})\n"
            contexto += f"Contenido: {doc['texto']}\n\n"
        
        return contexto.strip()
    
    # ---------------------------------------------------------
    # 3. GENERACIÓN CON OLLAMA (SIMPLIFICADA)
    # ---------------------------------------------------------
    def generar_respuesta(self, consulta: str, contexto: str) -> str:
        """Genera una respuesta usando Ollama con el contexto proporcionado."""
        try:
            # Crear prompt con contexto
            prompt = SYSTEM_PROMPT.format(context=contexto, question=consulta)
            
            # Llamar a Ollama directamente
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[
                    {'role': 'system', 'content': 'Eres un asistente académico preciso.'},
                    {'role': 'user', 'content': prompt}
                ],
                options={
                    'temperature': 0.3,
                    'num_predict': 1000
                }
            )
            
            return response['message']['content']
            
        except Exception as e:
            return f"❌ Error generando respuesta: {str(e)}"
    
    # ---------------------------------------------------------
    # 4. PROCESAMIENTO COMPLETO RAG
    # ---------------------------------------------------------
    def preguntar(self, consulta: str, k: int = 5) -> Dict[str, Any]:
        """Procesa una consulta completa: búsqueda + generación."""
        print(f"\n🔍 Procesando: '{consulta}'")
        
        # Paso 1: Buscar documentos relevantes
        print("   📂 Buscando documentos...")
        documentos = self.buscar_documentos(consulta, k)
        
        if not documentos:
            return {
                'consulta': consulta,
                'respuesta': "No encontré documentos relevantes para tu consulta.",
                'documentos': [],
                'contexto': ""
            }
        
        print(f"   ✓ Encontrados {len(documentos)} documentos relevantes")
        
        # Paso 2: Formatear contexto
        contexto = self.formatear_contexto(documentos)
        
        # Paso 3: Generar respuesta
        print(f"   🤖 Generando respuesta con {OLLAMA_MODEL}...")
        respuesta = self.generar_respuesta(consulta, contexto)
        
        # Paso 4: Preparar resultado
        resultado = {
            'consulta': consulta,
            'respuesta': respuesta,
            'documentos': documentos,
            'contexto': contexto[:500] + "..." if len(contexto) > 500 else contexto,
            'timestamp': datetime.now().isoformat(),
            'modelo_usado': OLLAMA_MODEL
        }
        
        return resultado
    
    # ---------------------------------------------------------
    # 5. FUNCIONES DE VISUALIZACIÓN
    # ---------------------------------------------------------
    def mostrar_resultado(self, resultado: Dict[str, Any]):
        """Muestra un resultado de forma formateada."""
        print(f"\n{'='*60}")
        print(f"📝 CONSULTA: {resultado['consulta']}")
        print(f"{'='*60}")
        
        print(f"\n🤖 RESPUESTA ({resultado['modelo_usado']}):")
        print(f"{'-'*40}")
        print(resultado['respuesta'])
        print(f"{'-'*40}")
        
        if resultado['documentos']:
            print(f"\n📚 DOCUMENTOS DE REFERENCIA ({len(resultado['documentos'])}):")
            for i, doc in enumerate(resultado['documentos'], 1):
                print(f"\n{i}. 📁 {doc['carpeta']}")
                print(f"   📄 {doc['archivo']} (Fragmento {doc['chunk_num']+1})")
                print(f"   📊 Similitud: {doc['similitud']:.2%}")
                print(f"   📝 {doc['texto'][:150]}...")
    
    def listar_temas(self) -> List[str]:
        """Lista todos los temas disponibles en el corpus."""
        temas = sorted(set(doc['carpeta'] for doc in self.metadatos))
        return temas

# ---------------------------------------------------------
# 6. INTERFAZ INTERACTIVA SIMPLIFICADA
# ---------------------------------------------------------
def interfaz_interactiva():
    """Interfaz interactiva simplificada para el sistema RAG."""
    # Inicializar sistema
    print("="*60)
    print("🧠 SISTEMA RAG ACADÉMICO CON OLLAMA")
    print("="*60)
    
    try:
        rag = RAGSystemOllama()
    except Exception as e:
        print(f"❌ Error inicializando sistema: {e}")
        return
    
    # Comandos disponibles
    print("\n📋 COMANDOS:")
    print("  /temas  - Listar temas del corpus")
    print("  /salir  - Terminar la sesión")
    print("  /ayuda  - Mostrar esta ayuda")
    print("\n💬 Escribe tu pregunta o comando:")
    
    while True:
        try:
            entrada = input("\n❓ > ").strip()
            
            if not entrada:
                continue
            
            # Comandos especiales
            if entrada.lower() == "/salir":
                print("👋 ¡Hasta luego!")
                break
            
            elif entrada.lower() == "/temas":
                temas = rag.listar_temas()
                print(f"\n📚 TEMAS DISPONIBLES ({len(temas)}):")
                print("-" * 40)
                for i, tema in enumerate(temas, 1):
                    print(f"{i:3}. {tema}")
                continue
            
            elif entrada.lower() == "/ayuda":
                print("\n📋 COMANDOS:")
                print("  /temas  - Listar temas del corpus")
                print("  /salir  - Terminar la sesión")
                print("  /ayuda  - Mostrar esta ayuda")
                continue
            
            # Consulta normal
            resultado = rag.preguntar(entrada)
            rag.mostrar_resultado(resultado)
            
            # Opción para guardar la consulta
            guardar = input("\n💾 ¿Guardar esta consulta? (s/n): ").lower()
            if guardar == 's':
                guardar_consulta(resultado)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Sesión interrumpida")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def guardar_consulta(resultado: Dict[str, Any]):
    """Guarda una consulta y su respuesta en un archivo JSON."""
    os.makedirs("consultas_guardadas", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"consultas_guardadas/consulta_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Consulta guardada en: {filename}")

# ---------------------------------------------------------
# 7. FUNCIÓN PARA PRUEBAS RÁPIDAS
# ---------------------------------------------------------
def ejecutar_pruebas():
    """Ejecuta pruebas automáticas con consultas predefinidas."""
    print("🧪 Ejecutando pruebas automáticas...")
    
    try:
        rag = RAGSystemOllama()
        
        pruebas = [
            "¿Qué son los algoritmos deshumanizantes?",
            "Explica la ansiedad en la generación Z",
            "¿Qué es el filtro burbuja?",
            "Habla sobre Habermas y el espacio público"
        ]
        
        for i, prueba in enumerate(pruebas, 1):
            print(f"\n{'='*60}")
            print(f"PRUEBA {i}: {prueba}")
            print(f"{'='*60}")
            
            resultado = rag.preguntar(prueba)
            
            print(f"\n📝 RESPUESTA:")
            print("-" * 40)
            print(resultado['respuesta'][:500] + "..." if len(resultado['respuesta']) > 500 else resultado['respuesta'])
            print("-" * 40)
            
            if i < len(pruebas):
                input("\n⏎ Presiona Enter para continuar...")
    
    except Exception as e:
        print(f"❌ Error en pruebas: {e}")

# ---------------------------------------------------------
# EJECUCIÓN PRINCIPAL SIMPLIFICADA
# ---------------------------------------------------------
if __name__ == "__main__":
    print("="*60)
    print("🧠 SISTEMA RAG SIMPLIFICADO - OLLAMA")
    print("="*60)
    print("\nOpciones:")
    print("  1. Interfaz interactiva de consultas")
    print("  2. Ejecutar pruebas automáticas")
    print("  3. Solo buscar documentos (sin generar respuesta)")
    
    opcion = input("\nSelecciona una opción (1-3): ").strip()
    
    try:
        # Inicializar sistema
        rag = RAGSystemOllama()
        
        if opcion == "1":
            # Interfaz interactiva
            interfaz_interactiva()
        
        elif opcion == "2":
            # Pruebas automáticas
            ejecutar_pruebas()
        
        elif opcion == "3":
            # Solo búsqueda
            print("\n🔍 MODO SOLO BÚSQUEDA")
            print("Escribe tus consultas para ver documentos relevantes")
            print("Escribe 'salir' para terminar\n")
            
            while True:
                consulta = input("Buscar: ").strip()
                if consulta.lower() == 'salir':
                    break
                
                documentos = rag.buscar_documentos(consulta, 5)
                
                if documentos:
                    print(f"\n📄 Documentos encontrados ({len(documentos)}):")
                    for i, doc in enumerate(documentos, 1):
                        print(f"\n{i}. 📁 {doc['carpeta']}")
                        print(f"   📄 {doc['archivo']}")
                        print(f"   📊 Similitud: {doc['similitud']:.2%}")
                        print(f"   📝 {doc['texto'][:200]}...")
                else:
                    print("❌ No se encontraron documentos.")
        
        else:
            print("❌ Opción no válida")
    
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\n📋 Asegúrate de que:")
        print("   1. El índice FAISS esté en la carpeta 'faiss_index/'")
        print("   2. Los archivos index_hnsw.faiss e index_metadata.pkl existan")
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")