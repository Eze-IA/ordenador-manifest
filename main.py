import streamlit as st

# 1. CONFIGURACIÓN DE LA PÁGINA (Limpia y centrada)
st.set_page_config(
    page_title="Manifest: Dependency Resolver",
    page_icon="📄",
    layout="centered"
)

# 2. CUERPO PRINCIPAL DE LA APLICACIÓN
st.title("📄 Manifest")
st.subheader("Intelligent File Dependency Resolver")
st.write("Detecta, analiza y ordena lógicamente colecciones de archivos de configuración y scripts antes de tu despliegue.")

# --- SISTEMA DE DATOS DE EJEMPLO ---
ejemplo_molde = "V1__init_tables.sql\nV2__add_keys.sql\nV3__insert_defaults.sql"

# Inicializar estados de persistencia si no existen
if "molde_val" not in st.session_state:
    st.session_state.molde_val = ""

# Fila de botones de soporte superior
col_ej, _ = st.columns([1, 3])
with col_ej:
    if st.button("💡 Cargar Ejemplo", use_container_width=True):
        st.session_state.molde_val = ejemplo_molde
        st.toast("Ejemplo cargado. ¡Ahora sube un archivo con las mismas líneas desordenadas!")

st.divider()

# Columnas para los dos inputs principales
col1, col2 = st.columns(2)

with col1:
    st.markdown("**1. Molde Guía (Secuencia lógica):**")
    molde_texto = st.text_area(
        label="Ingresa el orden correcto de los archivos de referencia",
        value=st.session_state.molde_val,
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
    if st.session_state.molde_val and archivo_subido is None:
        st.info("💡 Para probar el ejemplo, crea un archivo `.txt` con las líneas desordenadas y subirlo acá.")

st.write("") 

# Botón para procesar la secuencia
if st.button("Ordenar Secuencia 🚀", type="primary", use_container_width=True):
    if not molde_texto.strip():
        st.error("Por favor, ingresa el molde guía con la secuencia lógica.")
    elif archivo_subido is None:
        st.error("Por favor, selecciona y sube un archivo manifiesto (.txt).")
    else:
        try:
            # Procesar el molde guía
            guias_lineas = [linea.strip() for linea in molde_texto.split('\n') if linea.strip()]
            guias_solo_nombres = []
            for linea in guias_lineas:
                nombre = linea.replace('\\', '/').split('/')[-1].lower()
                guias_solo_nombres.append(nombre)

            # Leer el archivo manifiesto subido
            contenido = archivo_subido.read().decode("utf-8")
            lineas_originales = [linea.strip() for linea in contenido.splitlines() if linea.strip()]

            lineas_filtradas = []

            # Filtrar y preparar las coincidencias
            for linea in lineas_originales:
                nombre_archivo = ""
                if '|' in linea:
                    nombre_archivo = linea.split('|')[-1].strip().lower()
                else:
                    nombre_archivo = linea.replace('\\', '/').split('/')[-1].strip().lower()

                if nombre_archivo.endswith('_rev.sql'):
                    continue

                if nombre_archivo in guias_solo_nombres:
                    lineas_filtradas.append({
                        "texto_original": linea,
                        "nombre_limpio": nombre_archivo
                    })

            # Ordenar las líneas basándose estrictamente en el molde guía
            lineas_filtradas.sort(key=lambda item: guias_solo_nombres.index(item["nombre_limpio"]))

            # Unificar el resultado final
            resultado_final = "\n".join([item["texto_original"] for item in lineas_filtradas])

            if resultado_final:
                st.success("✓ ¡Secuencia ordenada con éxito!")
                st.markdown("**Vista previa del resultado:**")
                st.code(resultado_final, language="text")
                
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

# --- SECCIÓN DESPLEGABLE DE MÁS INFORMACIÓN ---
st.write("")
with st.expander("ℹ️ Más información y Arquitecturas soportadas"):
    st.markdown("""
    ### ¿Qué es Manifest?
    Es una herramienta para desarrolladores y administradores de bases de datos diseñada para secuenciar y ordenar archivos de despliegue de infraestructura basados en dependencias lógicas estrictas.
    
    ### Ideal para resolver dependencias en:
    * **SQL / Migraciones de bases de datos:** Flyway, Liquibase, parches manuales de Oracle, PostgreSQL o SQL Server (evita errores de Foreign Keys faltantes).
    * **Orquestación de Infraestructura:** Manifiestos de Kubernetes (K8s), plantillas ordenadas de Terraform o configuraciones modulares en entornos Cloud.
    * **Limpieza de Historiales:** Filtra y remueve automáticamente archivos temporales o de revisión intermedia (como sufijos `_rev.sql`).
    """)

# --- ☕ PIE DE PÁGINA: SECCIÓN DE MONETIZACIÓN AL FINAL ---
st.divider() # Línea sutil de separación

st.markdown("##### ☕ ¿Te ahorré tiempo?")
st.write("Si **Manifest** te ayudó a automatizar tus procesos, puedes apoyar el proyecto invitándome un café:")

# Creamos columnas para que los botones queden perfectamente alineados uno al lado del otro
col_kofi, col_cafecito, _ = st.columns([1.2, 1.5, 2])

with col_kofi:
    st.link_button(
        "Apoyar en Ko-fi ($ USD)", 
        "https://ko-fi.com/ezeia", 
        icon="☕", 
        use_container_width=True
    )

with col_cafecito:
    st.link_button(
        "Invitame un Cafecito (ARS)", 
        "https://cafecito.app/eze-ia", 
        icon="🧉", 
        use_container_width=True
    )

st.write("")
# Créditos y notas de seguridad al final absoluto
col_sec, col_ver = st.columns([3, 1])
with col_sec:
    st.caption("🔒 **Seguridad Avanzada:** El procesamiento se ejecuta 100% en tu navegador de forma local. Tus archivos nunca se suben a ningún servidor.")
with col_ver:
    st.caption("Manifest Web — v1.0.3")
