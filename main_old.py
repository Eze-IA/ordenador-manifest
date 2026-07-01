import streamlit as st

st.title("Procesador y Ordenador de Manifest")

# 1. El usuario pega el orden que quiere
molde = st.text_area("1. Pega aquí el orden de rutas deseado:", height=150)

# 2. El usuario sube el archivo manifest.txt
archivo_subido = st.file_uploader("2. Sube tu archivo manifest.txt original", type=["txt"])

if archivo_subido and molde:
    # Procesar las líneas de la guía
    guias = [linea.strip().split('\\')[-1].lower() for linea in molde.split('\n') if linea.strip()]
    
    # Leer el manifest original
    lineas_originales = archivo_subido.read().decode("utf-8").splitlines()
    
    # Filtrar e ignorar _rev.sql
    lineas_filtradas = []
    for linea in lineas_originales:
        if not linea.strip(): continue
        partes = linea.split('|')
        if len(partes) >= 4:
            archivo_nombre = partes[3]
            if archivo_nombre.lower() in guias and not archivo_nombre.endswith('_rev.sql'):
                lineas_filtradas.append(linea)
                
    # Ordenar según la guía
    lineas_ordenadas = sorted(lineas_filtradas, key=lambda l: guias.index(l.split('|')[3].lower()) if l.split('|')[3].lower() in guias else 999)
    
    resultado_final = "\n".join(lineas_ordenadas)
    
    # 3. Botón para descargar el resultado
    st.download_button(
        label="3. Descargar Manifest Ordenado",
        data=resultado_final,
        file_name="manifest_ordenado.txt",
        mime="text/plain"
    )
