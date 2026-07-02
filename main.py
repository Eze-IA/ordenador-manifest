import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Manifest: Intelligent File Sorter", 
    page_icon="📝",
    layout="centered"
)

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

    .tech-badge {
        display: inline-block;
        padding: 4px 12px;
        background: #e2e8f0;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        color: #475569;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (DOCUMENTACIÓN Y VALOR) ---
with st.sidebar:
    st.markdown("## 🧠 Acerca de Manifest")
    st.write("""
    **Manifest** es una solución ligera y potente diseñada para eliminar el riesgo de errores en despliegues.
    
    A partir de una lista guía, reorganiza automáticamente colecciones de scripts, eliminando el trabajo manual propenso a fallos.
    """)
    
    st.markdown("### 🔒 Privacidad Corporativa")
    st.info("Procesamiento 100% local. Los archivos nunca salen de tu navegador, cumpliendo con los estándares de seguridad bancarios.")
    
    st.markdown("### 🚀 Ideal para:")
    st.markdown("""
    - **Databases:** Oracle, SQL Server, PostgreSQL, MySQL.
    - **Frameworks:** Flyway, Liquibase.
    - **DevOps:** Kubernetes YAML, Terraform, Bash.
    """)

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
    st.markdown('<div class="feature-box">🔒 <b>Privacidad Total:</b> Ejecución 100% local.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- HERRAMIENTA DE TRABAJO ---
st.markdown("### 🛠 Herramienta de Secuenciación")

molde = st.text_area(
    "1. Pega aquí el Molde Guía (Orden topológico deseado):", 
    height=150, 
    placeholder="..\\database\\migrations\\V1__init_tables.sql\n..\\database\\migrations\\V2__add_foreign_keys.sql"
)

archivo_subido = st.file_uploader("2. Selecciona tu archivo Manifiesto desordenado (.txt)", type=["txt"])

# --- LÓGICA DE PROCESAMIENTO ---
if archivo_subido and molde:
    guias_originales = [linea.strip() for linea in molde.split('\n') if linea.strip()]
    guias_solo_nombres = [linea.split('\\')[-1].split('/')[-1].lower() for linea in guias_originales]
    
    lineas_originales = archivo_subido.read().decode("utf-8").splitlines()
    
    lineas_filtradas = []
    for linea in lineas_originales:
        linea_limpia = linea.strip()
        if not linea_limpia: continue
        
        nombre_archivo = linea_limpia.split('|')[-1].lower() if '|' in linea_limpia else linea_limpia.split('\\')[-1].split('/')[-1].lower()
            
        if nombre_archivo.endswith('_rev.sql'): continue
            
        if nombre_archivo in guias_solo_nombres:
            lineas_filtradas.append((linea_limpia, nombre_archivo))
            
    lineas_ordenadas = sorted(
        lineas_filtradas, 
        key=lambda x: guias_solo_nombres.index(x[1]) if x[1] in guias_solo_nombres else 999
    )
    
    resultado_final = "\n".join([item[0] for item in lineas_ordenadas])
    
    if resultado_final:
        st.markdown("---")
        st.success("✓ **Dependencias resueltas.** Secuencia lista para un despliegue seguro.")
        
        st.write("Vista previa:")
        st.code(resultado_final, language="text")
        
        st.download_button(
            label="Descargar Manifiesto Ordenado 📥",
            data=resultado_final,
            file_name="manifest_ordenado.txt",
            mime="text/plain"
        )
