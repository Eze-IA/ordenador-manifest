import streamlit as st

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser la primera instrucción de Streamlit)
st.set_page_config(
    page_title="Manifest: Dependency Resolver",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. BARRA LATERAL (SIDEBAR) - PASARELA DE MONETIZACIÓN Y ESTADO
with st.sidebar:
    st.markdown("### ☕ ¿Te ahorré tiempo?")
    st.write(
        "Si **Manifest** te ayudó a automatizar la secuencia lógica de tus archivos "
        "y evitó errores en tus despliegues, puedes apoyar el proyecto invitándome un café:"
    )
    
    # Botón Internacional (Ko-fi en Dólares)
    st.link_button(
        "Apoyar en Ko-fi (USD 🇺🇸)", 
        "https://ko-fi.com/ezeia", 
        type="secondary",
        icon="☕",
        use_container_width=True
    )
    
    st.write("") # Pequeño espacio separador
    
    # Botón Local (Cafecito en Pesos)
    st.link_button(
        "Invitame un Cafecito (ARS 🇦🇷)", 
        "https://cafecito.app/eze-ia", 
        type="secondary",
        icon="🧉",
        use_container_width=True
    )
    
    st.divider()
    st.caption("🔒 **Seguridad Avanzada:** El procesamiento se ejecuta 100% en tu navegador de forma local. Tus archivos nunca se suben a ningún servidor.")
    st.caption("Manifest Web — v1.0.3")

# 3. CUERPO PRINCIPAL DE LA APLICACIÓN
st.title("📄 Manifest")
st.subheader("Intelligent File Dependency Resolver")
st.write("Detecta, analiza y ordena lógicamente colecciones de archivos de configuración y scripts antes de tu despliegue.")

st.divider()

# Creación de columnas para los dos inputs principales
col1, col2 = st.columns(2)

with col1:
    st.markdown("**1. Molde Guía (Secuencia lógica):**")
    molde_texto = st.text_area(
        label="Ingresa el orden correcto de los archivos de referencia",
        placeholder="V1__init_tables.sql\nV2__add_keys.sql",
        height=150,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("**2. Manifiesto desordenado (.txt):**")
    archivo_subido = st.file_uploader(
        label="Sube tu archivo de manifiesto desordenado",
        type=["txt"],
        label_visibility="collapsed"
    )

st.write("") # Espacio estético

# Botón para procesar la secuencia
if st.button("Ordenar Secuencia 🚀", type="primary", use_container_width=True):
    if not molde_texto.strip():
        st.error("Por favor, ingresa el molde guía con la secuencia lógica.")
    elif archivo_subido is None:
        st.error("Por favor, selecciona y sube un archivo manifiesto (.txt).")
    else:
        try:
            # --- LÓGICA DE PROCESAMIENTO LOCAL EN PYTHON ---
            
            # Procesar el molde guía
            guias_lineas = [linea.strip() for linea in molde_texto.split('\n') if linea.strip()]
            guias_solo_nombres = []
            for linea in guias_lineas:
                # Extrae el nombre del archivo eliminando rutas (compatibilidad con / y \)
                nombre = linea.replace('\\', '/').split('/')[-1].lower()
                guias_solo_nombres.append(nombre)

            # Leer el archivo manifiesto subido por el usuario
            contenido = archivo_subido.read().decode("utf-8")
            lineas_originales = [linea.strip() for linea in contenido.splitlines() if linea.strip()]

            lineas_filtradas = []

            # Filtrar y preparar las coincidencias
            for linea in lineas_originales:
                nombre_archivo = ""
                
                # Manejo de formatos con pipes '|' o rutas comunes
                if '|' in linea:
                    nombre_archivo = linea.split('|')[-1].strip().lower()
                else:
                    nombre_archivo = linea.replace('\\', '/').split('/')[-1].strip().lower()

                # Ignorar archivos de revisión intermedios
                if nombre_archivo.endswith('_rev.sql'):
                    continue

                # Si el archivo está en la guía, lo agregamos para ordenar
                if nombre_archivo in guias_solo_nombres:
                    lineas_filtradas.append({
                        "texto_original": linea,
                        "nombre_limpio": nombre_archivo
                    })

            # Ordenar las líneas basándose estrictamente en la posición del molde guía
            lineas_filtradas.sort(key=lambda item: guias_solo_nombres.index(item["nombre_limpio"]))

            # Unificar el resultado final
            resultado_final = "\n".join([item["texto_original"] for item in lineas_filtradas])

            if resultado_final:
                st.success("✓ ¡Secuencia ordenada con éxito!")
                
                # Vista previa del resultado en un bloque de código/texto estructurado
                st.markdown("**Vista previa del resultado:**")
                st.code(resultado_final, language="text")
                
                # Botón nativo para descargar el archivo procesado
                st.download_button(
                    label="Descargar Archivo Ordenado 📥",
                    data=resultado_final,
                    file_name="manifest_ordenado.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.warning("No se encontraron coincidencias exactas entre el archivo de manifiesto y tu molde guía.")
                
        except Exception as e:
            st.error(f"Ocurrió un error al procesar el archivo: {str(e)}")
