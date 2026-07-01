import streamlit as st
import os

st.set_page_config(page_title="Manifesto - Ordenador Universal de Texto -", page_icon="📝")

st.title("📝 Ordenador Universal Inteligente")
st.write("Sube cualquier archivo de texto y ordénalo copiando y pegando una plantilla de guía.")

# 1. Entrada de la plantilla guía
molde = st.text_area(
    "1. Pega aquí las líneas o rutas en el orden exacto que las necesitas:", 
    height=200, 
    placeholder="..\\Ruta\\archivo1.sql\n..\\Ruta\\archivo2.sp"
)

# 2. Subida del archivo original
archivo_subido = st.file_uploader("2. Sube tu archivo original (.txt)", type=["txt"])

if archivo_subido and molde:
    # --- PROCESAR LA GUÍA ---
    guias_originales = [linea.strip() for linea in molde.split('\n') if linea.strip()]
    
    guias_solo_nombres = []
    for linea in guias_originales:
        nombre = linea.split('\\')[-1].split('/')[-1].lower()
        guias_solo_nombres.append(nombre)
    
    # --- PROCESAR EL ARCHIVO SUBIDO ---
    lineas_originales = archivo_subido.read().decode("utf-8").splitlines()
    
    lineas_filtradas = []
    for linea in lineas_originales:
        linea_limpia = linea.strip()
        if not linea_limpia: 
            continue
        
        if '|' in linea_limpia:
            nombre_archivo = linea_limpia.split('|')[-1].lower()
        else:
            nombre_archivo = linea_limpia.split('\\')[-1].split('/')[-1].lower()
            
        if nombre_archivo.endswith('_rev.sql'):
            continue
            
        if nombre_archivo in guias_solo_nombres:
            lineas_filtradas.append((linea_limpia, nombre_archivo))
            
    # --- ORDENAMIENTO INTELIGENTE ---
    lineas_ordenadas = sorted(
        lineas_filtradas, 
        key=lambda x: guias_solo_nombres.index(x[1]) if x[1] in guias_solo_nombres else 999
    )
    
    resultado_final = "\n".join([item[0] for item in lineas_ordenadas])
    
    if resultado_final:
        st.success("¡Archivo procesado y ordenado con éxito!")
        
        # --- NUEVA FUNCIÓN: MOSTRAR EN CUADRO ---
        st.write("### Vista previa del resultado:")
        st.code(resultado_final, language="text")
        
        # 3. Botón para descargar el resultado
        st.download_button(
            label="3. Descargar Archivo Ordenado 📥",
            data=resultado_final,
            file_name="texto_ordenado.txt",
            mime="text/plain"
        )
    else:
        st.error("No se encontraron coincidencias entre el archivo subido y la guía pegada. Revisa los nombres de los archivos.")
