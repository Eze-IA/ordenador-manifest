import streamlit as st

st.set_page_config(page_title="Ordenador Universal de Texto", page_icon="📝")

st.title("📝 Ordenador Universal de Texto")
st.write("Sube cualquier archivo de texto y ordénalo copiando y pegando un modelo o plantilla de guía.")

# 1. El usuario pega el molde con el orden que quiere
molde = st.text_area(
    "1. Pega aquí las líneas en el orden exacto que las necesitas:", 
    height=200, 
    placeholder="Línea A\nLínea B\nLínea C..."
)

# 2. El usuario sube el archivo original desordenado
archivo_subido = st.file_uploader("2. Sube tu archivo original (.txt)", type=["txt"])

if archivo_subido and molde:
    # Limpiamos las líneas del molde que pegó el usuario
    guias = [linea.strip() for linea in molde.split('\n') if linea.strip()]
    
    # Leer el archivo original línea por línea
    lineas_originales = archivo_subido.read().decode("utf-8").splitlines()
    lineas_originales = [linea.strip() for linea in lineas_originales if linea.strip()]
    
    # Filtrar: solo nos quedamos con las líneas del archivo original que aparezcan en la guía
    # (También sirve por si tu manifest original tiene cosas extras que quieres limpiar)
    lineas_filtradas = [linea for linea in lineas_originales if linea in guias]
    
    # ORDENAMIENTO UNIVERSAL:
    # Ordenamos las líneas del archivo basándonos exactamente en la posición que ocupan en la guía
    lineas_ordenadas = sorted(lineas_filtradas, key=lambda l: guias.index(l))
    
    resultado_final = "\n".join(lineas_ordenadas)
    
    st.success("¡Archivo procesado y ordenado con éxito!")
    
    # 3. Botón para descargar el resultado
    st.download_button(
        label="3. Descargar Archivo Ordenado 📥",
        data=resultado_final,
        file_name="texto_ordenado.txt",
        mime="text/plain"
    )
