import os
import requests
from bs4 import BeautifulSoup
import pdfplumber
import time

if not os.path.exists("corpus"):
    os.makedirs("corpus")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def descargar_texto_url(url, nombre_archivo):
    """Descarga texto de una página web y lo guarda como .txt"""
    try:
        print(f"🌐 Descargando: {nombre_archivo}...")
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        texto = soup.get_text(separator='\n', strip=True)
        
        # Guardar
        ruta = f"corpus/{nombre_archivo}.txt"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"✅ Texto guardado: {ruta}")
        return True
    except Exception as e:
        print(f"❌ Error descargando {nombre_archivo}: {e}")
        return False

def descargar_pdf(url, nombre_archivo):
    """Descarga un PDF y extrae su texto"""
    try:
        print(f"📥 Descargando PDF: {nombre_archivo}...")
        response = requests.get(url, headers=headers, timeout=15, stream=True)
        
        pdf_path = f"corpus/temp_{nombre_archivo}.pdf"
        with open(pdf_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Extraer texto del PDF
        texto_completo = ""
        with pdfplumber.open(pdf_path) as pdf:
            for pagina in pdf.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto_completo += texto_pagina + "\n\n"
        
        # Guardar texto extraído
        if texto_completo.strip():
            txt_path = f"corpus/{nombre_archivo}.txt"
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(texto_completo)
            print(f"✅ PDF procesado y guardado como texto: {txt_path}")
            
            # Opcional: eliminar PDF temporal
            os.remove(pdf_path)
            return True
        else:
            print(f"⚠️ PDF sin texto extraíble: {nombre_archivo}")
            return False
            
    except Exception as e:
        print(f"❌ Error procesando PDF {nombre_archivo}: {e}")
        return False

def extraer_texto_de_pdf_local(ruta_pdf, nombre_archivo):
    """Extrae texto de un PDF ya descargado localmente"""
    try:
        print(f"📄 Extrayendo texto de PDF local: {ruta_pdf}...")
        texto_completo = ""
        with pdfplumber.open(ruta_pdf) as pdf:
            for i, pagina in enumerate(pdf.pages):
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto_completo += f"--- Página {i+1} ---\n{texto_pagina}\n\n"
        
        if texto_completo.strip():
            txt_path = f"corpus/{nombre_archivo}.txt"
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(texto_completo)
            print(f"✅ Texto extraído y guardado: {txt_path}")
            return True
        else:
            print(f"⚠️ No se pudo extraer texto del PDF: {ruta_pdf}")
            return False
    except Exception as e:
        print(f"❌ Error extrayendo PDF local: {e}")
        return False

# --- EJEMPLOS DE FUENTES (REEMPLAZA CON TUS URLS REALES) ---
def descargar_ejemplos():
    """Ejemplos de URLs - REEMPLAZA ESTOS CON TUS FUENTES REALES"""
    
    # LISTA DE FUENTES DE PRUEBA (modifica estas URLs)
    fuentes = [
        # 1. Artículos web (HTML)
        {
            "url": "https://ctxt.es/es/20230101/Firmas/41641/",
            "nombre": "tecnologia_autonomia_ctxt",
            "tipo": "web"
        },
        {
            "url": "https://www.letraslibres.com/mexico/revista/generacion-z-la-generacion-mas-infeliz",
            "nombre": "generacion_z_infeliz_letraslibres",
            "tipo": "web"
        },
        
        # 2. PDFs académicos (asegúrate de que sean de acceso público)
        {
            "url": "https://www.scielo.org.mx/pdf/peredu/v46n184/0185-2698-peredu-46-184-111.pdf",
            "nombre": "redes_sociales_identidad_scielo",
            "tipo": "pdf"
        },
        # Agrega más URLs aquí...
    ]
    
    for fuente in fuentes:
        if fuente["tipo"] == "web":
            descargar_texto_url(fuente["url"], fuente["nombre"])
        elif fuente["tipo"] == "pdf":
            descargar_pdf(fuente["url"], fuente["nombre"])
        time.sleep(2)  # Pausa para no saturar servidores

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    print("="*60)
    print("🔍 RECOLECTOR DE CORPUS PARA PROYECTO RAG")
    print("="*60)
    
    # Opción 1: Descargar ejemplos (reemplaza las URLs primero)
    # descargar_ejemplos()
    
    # Opción 2: Descargar manualmente URL específica
    print("\n📝 Opciones:")
    print("1. Descargar de URL web")
    print("2. Descargar y extraer PDF de URL")
    print("3. Extraer texto de PDF local")
    
    opcion = input("\nSelecciona opción (1-3): ").strip()
    
    if opcion == "1":
        url = input("URL de la página web: ").strip()
        nombre = input("Nombre para guardar (sin extensión): ").strip()
        descargar_texto_url(url, nombre)
        
    elif opcion == "2":
        url = input("URL del PDF: ").strip()
        nombre = input("Nombre para guardar (sin extensión): ").strip()
        descargar_pdf(url, nombre)
        
    elif opcion == "3":
        ruta = input("Ruta del PDF local (ej: C:/Users/.../documento.pdf): ").strip()
        nombre = input("Nombre para guardar (sin extensión): ").strip()
        extraer_texto_de_pdf_local(ruta, nombre)
    
    else:
        print("❌ Opción no válida")
    
    print("\n🎯 Proceso completado. Revisa la carpeta 'corpus/'")