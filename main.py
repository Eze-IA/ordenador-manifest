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

# --- SISTEMA DE DATOS DE EJEMPLO CORPORATIVO AMPLIADO ---
ejemplo_molde = (
    "01_env_setup.sh\n"
    "V1__create_tables.sql\n"
    "V2__add_foreign_keys.sql\n"
    "sp_upsert_customer.sp\n"
    "sp_process_billing.sp\n"
    "rpt_monthly_invoice.sqr\n"
    "V3__insert_seed_data.sql"
)

ejemplo_manifiesto_simulado = (
    "C:\\deploy\\src\\sp_process_billing.sp\n"
    "C:\\deploy\\src\\V2__add_foreign_keys.sql\n"
    "C:\\deploy\\src\\01_env_setup.sh\n"
    "C:\\deploy\\src\\rpt_monthly_invoice.sqr\n"
    "C:\\deploy\\src\\V3__insert_seed_data.sql\n"
    "C:\\deploy\\src\\sp_upsert_customer.sp\n"
    "C:\\deploy\\src\\V1__create_tables.sql"
)

# Inicializar estados de persistencia en la sesión
if "molde_val" not in st.session_state:
    st.session_state.molde_val = ""
if "resultado_ejemplo" not in st.session_state:
    st.session_state.resultado_ejemplo = ""
if "modo_ejemplo" not in st.session_state:
    st.session_state.modo_ejemplo = False

# Fila superior con el botón de ejemplo automático
col_ej, _ = st.columns([1, 3])
with col_ej:
    if st.button("💡 Cargar Ejemplo", use_container_width=True):
        st.session_state.molde_val = ejemplo_molde
        st.session_state.resultado_ejemplo = ejemplo_manifiesto_simulado
        st.session_state.modo_ejemplo = True
        st.toast("¡Ejemplo empresarial cargado y procesado automáticamente!")

st.divider()

# Columnas para los dos inputs principales
col1, col2 = st.columns(2)

with col1:
    st.markdown("**1. Molde Guía (Secuencia lógica):**")
    molde_texto = st.text_area(
        label="Ingresa el orden correcto de los archivos de referencia",
        value=st.session_state.molde_val,
        placeholder="V1__init_tables.sql\nV2__add_keys.sql",
        height=180,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("**2. Manifiesto desordenado (.txt):**")
    
    # Si estamos en modo ejemplo, mostramos visualmente que el archivo ya está precargado
    if st.session_state.modo_ejemplo:
        st.info("📄 manifest_ejemplo_corporativo.txt")
        if st.button("❌ Quitar ejemplo", use_container_width=True):
            st.session_state.molde_val = ""
            st.session_state.resultado_ejemplo = ""
            st.session_state.modo_ejemplo = False
            st.rerun()
    else:
        archivo_subido = st.file_uploader(
            label="Sube tu archivo de manifiesto desordenado",
            type=["txt"],
            label_visibility="collapsed"
        )

st.write("") 

# Variable para acumular el texto a procesar
texto_manifiesto = ""
procesar_ahora = False

# Determinar de dónde viene la información
if st.session_state.modo_ejemplo:
    texto_manifiesto = st.session_state.resultado_ejemplo
    procesar_ahora = True
elif st.button("Ordenar Secuencia 🚀", type="primary", use_container_width=True):
    if not molde_texto.strip():
        st.error("Por favor, ingresa el molde guía con la secuencia lógica.")
    elif archivo_subido is None:
        st.error("Por favor, selecciona y sube un archivo manifiesto (.txt).")
    else:
        texto_manifiesto = archivo_subido.read().decode("utf-8")
        procesar_ahora = True

# --- LÓGICA DE PROCESAMIENTO ---
if procesar_ahora and molde_texto.strip():
    try:
        # Procesar el molde guía
        guias_lineas = [linea.strip() for linea in molde_texto.split('\n') if linea.strip()]
        guias_solo_nombres = []
        for linea in guias_lineas:
            nombre = linea.replace('\\', '/').split('/')[-1].lower()
            guias_solo_nombres.append(nombre)

        # Procesar las líneas del manifiesto
        lineas_originales = [linea.strip() for linea in texto_manifiesto.splitlines() if linea.strip()]
        lineas_filtradas = []

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

        # Ordenar estrictamente por la posición en el molde guía
        lineas_filtradas.sort(key=lambda item: guias_solo_nombres.index(item["nombre_limpio"]))

        # Unificar resultado
        resultado_final = "\n".join([item["texto_original"] for item in lineas_filtradas])

        if resultado_final:
            st.success("✓ ¡Secuencia ordenada con éxito!")
            st.markdown("**Vista previa del resultado ordenado:**")
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
with st.expander("ℹ️ Más información y Extensiones soportadas"):
    st.markdown("""
    ### ¿Qué es Manifest?
    Es una herramienta para desarrolladores, DBAs y DevOps diseñada para secuenciar, estructurar y ordenar colecciones complejas de scripts de despliegue basándose en dependencias jerárquicas estrictas.
    
    ### Ideal para entornos empresariales:
    * **Migraciones SQL Avanzadas (`.sql`, `.sp`):** Ordena tablas, Foreign Keys y Procedimientos Almacenados evitando fallos de compilación cruzada. Compatible con frameworks como Flyway o parches manuales.
    * **Reportes de Sistemas Centrales (`.sqr`, `.cfg`):** Secuencia archivos legados de reportes estructurados antes de empaquetar compilaciones a producción.
    * **Scripts de Automatización y Servidores (`.sh`, `.bat`, `.py`):** Configura el orden de ejecución de tareas de infraestructura en pipelines de despliegue.
    """)

# --- ☕ PIE DE PÁGINA: SECCIÓN DE MONETIZACIÓN AL FINAL ---
st.divider()

st.markdown("##### ☕ ¿Te ahorré tiempo?")
st.write("Si **Manifest** te ayudó a automatizar tus procesos y evitar fallos de despliegue, puedes apoyar el proyecto invitándome un café:")

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
col_sec, col_ver = st.columns([3, 1])
with col_sec:
    st.caption("🔒 **Seguridad Avanzada:** El procesamiento se ejecuta 100% en tu navegador de forma local. Tus archivos nunca se suben a ningún servidor.")
with col_ver:
    st.caption("Manifest Web — v1.0.3")
