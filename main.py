import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Manifest: Intelligent File Sorter", 
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# INYECCIÓN DE LA ETIQUETA META DE GOOGLE (Oculta en el head de la web)
st.html(f'<meta name="google-site-verification" content="KzHB3sz8GprCF3Zd-eR38c94JzDGFBh_MedxFRlmirw" />')

# 2. DISEÑO DE INTERFAZ Y ESTILOS (CSS)
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    
    .enterprise-card {
        background-color: var(--background-secondary);
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    
    .main-title {
        font-family: 'Segoe UI', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1976D2 0%, #00D4FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        letter-spacing: -2px;
    }
    
    .slogan {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1976D2;
        margin-bottom: 1rem;
    }

    .feature-box {
        background: rgba(25, 118, 210, 0.04);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1976D2;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- CUERPO PRINCIPAL (DISEÑO SaaS) ---
st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Manifest</h1>', unsafe_allow_html=True)
st.markdown('<p class="slogan">The smart way to organize deployment files.</p>', unsafe_allow_html=True)

st.write("**Organiza automáticamente archivos de despliegue y manifests de bases de datos en segundos.**")

# Características destacadas (Grid visual)
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="feature-box">🧠 <b>Ordenamiento inteligente</b> basado en guías de referencia.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-box">⚙️ <b>Filtros configurables</b> para scripts de reversión (*_rev).</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="feature-box">📂 <b>Extracción automática</b> ignorando rutas complejas.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-box">🔒 <b>Privacidad Total:</b> Ejecución 100% local en tu navegador.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- BOTÓN DESPLEGABLE NATIVO (DOCUMENTACIÓN) ---
with st.expander("📖 Conoce más sobre Manifest (Problema que resuelve e Impacto DevOps)"):
    st.markdown("""
    ### 💻 ¿Para quién es?
    **Manifest** es una solución ligera y potente diseñada para desarrolladores, DBAs y equipos DevOps que necesitan preparar despliegues de forma rápida, segura y sin errores.
    
    ### ⚠️ ¿Qué problema resuelve?
    Evita tareas repetitivas y catastróficas al preparar despliegues complejos. Olvídate de errores humanos en producción como:
    - *'La tabla se creó después del índice.'*
    - *'La foreign key apunta a una tabla que todavía no existe.'*
    
    ### 🚀 Ideal para secuenciar dependencias en:
    - **Bases de datos:** Oracle, SQL Server, PostgreSQL, MySQL.
    - **Automatizadores:** Flyway, Liquibase, scripts SQL personalizados.
    - **Estructuras:** Kubernetes YAML, Terraform HCL, Bash o PowerShell.
    """)

st.write("---")

# --- VARIABLES PARA LA SIMULACIÓN ---
ejemplo_molde = (
    "..\\database\\schema\\01_tables.sql\n"
    "..\\database\\schema\\02_indexes.sql\n"
    "..\\database\\schema\\03_foreign_keys.sql\n"
    "..\\database\\data\\04_initial_seed.sql"
)

ejemplo_archivo = (
    "..\\all_scripts\\03_foreign_keys.sql\n"
    "..\\all_scripts\\01_tables.sql\n"
    "..\\all_scripts\\01_tables_rev.sql\n"
    "..\\all_scripts\\04_initial_seed.sql\n"
    "..\\all_scripts\\02_indexes.sql"
)

if "molde_val" not in st.session_state:
    st.session_state.molde_val = ""
if "archivo_val" not in st.session_state:
    st.session_state.archivo_val = ""
if "mostrar_resultado_demo" not in st.session_state:
    st.session_state.mostrar_resultado_demo = False

# --- HERRAMIENTA DE TRABAJO ---
st.markdown("### 🛠 Herramienta de Secuenciación")

if st.button("🚀 Cargar ejemplo de prueba (Demo Rápida)"):
    st.session_state.molde_val = ejemplo_molde
    st.session_state.archivo_val = ejemplo_archivo
    st.session_state.mostrar_resultado_demo = True

molde = st.text_area(
    "1. Pega aquí el Molde Guía (Orden topológico deseado):", 
    value=st.session_state.molde_val,
    height=150, 
    placeholder="..\\database\\migrations\\V1__init_tables.sql\n..\\database\\migrations\\V2__add_foreign_keys.sql"
)

contenido_archivo = ""
if st.session_state.mostrar_resultado_demo:
    st.info("💡 Modo Demo activado: Se cargó un manifiesto de producción desordenado simulado (incluye un script de reversión '_rev.sql' que será ignorado automáticamente).")
    archivo_texto_demo = st.text_area("2. Contenido del Manifiesto original desordenado:", value=st.session_state.archivo_val, height=130)
    contenido_archivo = archivo_texto_demo
else:
    archivo_subido = st.file_uploader("2. Selecciona tu archivo Manifiesto desordenado (.txt)", type=["txt"])
    if archivo_subido:
        contenido_archivo = archivo_subido.read().decode("utf-8")

if st.session_state.mostrar_resultado_demo:
    if st.button("❌ Limpiar demostración"):
        st.session_state.molde_val = ""
        st.session_state.archivo_val = ""
        st.session_state.mostrar_resultado_demo = False
        st.rerun()

# --- LÓGICA DE PROCESAMIENTO ---
if contenido_archivo and molde:
    guias_originales = [linea.strip() for linea in molde.split('\n') if linea.strip()]
    guias_solo_nombres = [linea.split('\\')[-1].split('/')[-1].lower() for linea in guias_originales]
    
    lineas_originales = [linea.strip() for linea in contenido_archivo.split('\n') if linea.strip()]
    
    lineas_filtradas = []
    for linea in lineas_originales:
        if not linea: continue
        
        nombre_archivo = linea.split('|')[-1].lower() if '|' in linea else linea.split('\\')[-1].split('/')[-1].lower()
            
        if nombre_archivo.endswith('_rev.sql'): continue
            
        if nombre_archivo in guias_solo_nombres:
            lineas_filtradas.append((linea, nombre_archivo))
            
    lineas_ordenadas = sorted(
        lineas_filtradas, 
        key=lambda x: guias_solo_nombres.index(x[1]) if x[1] in guias_solo_nombres else 999
    )
    
    resultado_final = "\n".join([item[0] for item in lineas_ordenadas])
    
    if resultado_final:
        st.markdown("---")
        st.success("✓ **Dependencias resueltas.** Secuencia lista para un despliegue seguro.")
        st.write("Vista previa del resultado ordenado por Manifest:")
        st.code(resultado_final, language="text")
        
        st.download_button(
            label="Descargar Manifiesto Ordenado 📥",
            data=resultado_final,
            file_name="manifest_ordenado.txt",
            mime="text/plain"
        )
    else:
        st.error("No se encontraron coincidencias entre el archivo de entrada y el molde de dependencias.")
