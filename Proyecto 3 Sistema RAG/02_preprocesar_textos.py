import os
import re

def limpiar_texto(texto):
    """Limpia el texto de caracteres no deseados"""
    # Eliminar múltiples espacios y saltos
    texto = re.sub(r'\n\s*\n', '\n\n', texto)  # Preservar párrafos
    texto = re.sub(r'[ \t]+', ' ', texto)      # Espacios múltiples
    # Eliminar URLs
    texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
    # Eliminar correos
    texto = re.sub(r'\S+@\S+', '', texto)
    # Eliminar caracteres especiales excepto puntuación básica
    texto = re.sub(r'[^\w\s.,;:¡!¿?áéíóúüñÁÉÍÓÚÜÑ\-]', '', texto)
    return texto.strip()

def dividir_en_fragmentos(texto, palabras_por_fragmento=500):
    """Divide el texto en fragmentos de ~N palabras"""
    palabras = texto.split()
    if len(palabras) <= palabras_por_fragmento:
        return [texto]
    
    fragmentos = []
    for i in range(0, len(palabras), palabras_por_fragmento):
        fragmento = ' '.join(palabras[i:i+palabras_por_fragmento])
        fragmentos.append(fragmento)
    return fragmentos

def procesar_corpus():
    """Procesa todos los textos de la carpeta corpus/"""
    if not os.path.exists("corpus"):
        print("❌ No existe la carpeta 'corpus/'. Ejecuta primero 01_recolectar_corpus.py")
        return
    
    # Crear carpeta para resultados
    if not os.path.exists("corpus_procesado"):
        os.makedirs("corpus_procesado")
    
    archivos_txt = [f for f in os.listdir("corpus") if f.endswith(".txt")]
    
    if not archivos_txt:
        print("❌ No hay archivos .txt en la carpeta 'corpus/'")
        return
    
    print(f"📚 Procesando {len(archivos_txt)} archivos...")
    
    todos_fragmentos = []
    metadata = []
    
    for archivo in archivos_txt:
        try:
            with open(f"corpus/{archivo}", "r", encoding="utf-8") as f:
                contenido = f.read()
            
            if not contenido.strip():
                print(f"⚠️ Archivo vacío: {archivo}")
                continue
            
            # Limpiar
            contenido_limpio = limpiar_texto(contenido)
            
            # Dividir
            fragmentos = dividir_en_fragmentos(contenido_limpio, palabras_por_fragmento=400)
            
            # Guardar cada fragmento individualmente
            for i, fragmento in enumerate(fragmentos):
                if fragmento.strip():
                    nombre_fragmento = f"{archivo[:-4]}_frag{i+1:03d}.txt"
                    ruta_fragmento = f"corpus_procesado/{nombre_fragmento}"
                    
                    with open(ruta_fragmento, "w", encoding="utf-8") as f:
                        f.write(fragmento)
                    
                    todos_fragmentos.append(fragmento)
                    metadata.append({
                        "archivo_original": archivo,
                        "fragmento": nombre_fragmento,
                        "palabras": len(fragmento.split())
                    })
            
            print(f"✅ {archivo}: {len(fragmentos)} fragmentos")
            
        except Exception as e:
            print(f"❌ Error procesando {archivo}: {e}")
    
    # Guardar lista completa de fragmentos
    if todos_fragmentos:
        with open("corpus_procesado/!todos_fragmentos.txt", "w", encoding="utf-8") as f:
            for frag in todos_fragmentos:
                f.write(f"--- FRAGMENTO ---\n{frag}\n\n")
        
        print(f"\n🎉 Procesamiento completo:")
        print(f"   • Fragmentos totales: {len(todos_fragmentos)}")
        print(f"   • Carpeta 'corpus_procesado/' creada con resultados")
        print(f"   • Archivo consolidado: '!todos_fragmentos.txt'")
    else:
        print("\n⚠️ No se generaron fragmentos. Revisa los archivos fuente.")

if __name__ == "__main__":
    print("="*60)
    print("🧹 PREPROCESADOR DE TEXTOS")
    print("="*60)
    procesar_corpus()