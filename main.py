import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA (Pestaña del navegador)
st.set_page_config(
    page_title="Manifest: Intelligent File Dependency Resolver", 
    page_icon="📝",
    layout="centered"
)

# 2. INYECCIÓN DE ESTILOS CSS AVANZADOS (CORREGIDO)
st.markdown("""
    <style>
    /* Ocultar elementos por defecto de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Contenedor Principal estilo Tarjeta Enterprise */
    .enterprise-card {
        background-color: var(--background-secondary);
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }
    
    /* Maquetado de Cabecera con Logo Flotante */
    .brand-container {
        display: flex;
        align-items: center;
        gap: 25px;
        margin-bottom: 20px;
    }
    
    .brand-logo {
        width: 110px;
        height: auto;
        border-radius: 12px;
    }
    
    .brand-text-group {
        display: flex;
        flex-direction: column;
    }
    
    .main-title {
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1976D2 0%, #00D4FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -1.5px;
        line-height: 1.1;
    }
    
    .subtitle {
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 5px;
    }
    
    .tagline {
        font-size: 1.05rem;
        line-height: 1.6;
        color: var(--text-color);
        opacity: 0.85;
        margin-bottom: 2rem;
    }
    
    /* Grilla Corporativa SaaS */
    .tech-header {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748b;
        margin-bottom: 0.8rem;
    }
    
    .tech-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-bottom: 1rem;
    }
    
    .tech-item {
        background: rgba(25, 118, 210, 0.06);
        border: 1px solid rgba(25, 118, 210, 0.15);
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .tech-icon {
        color: #10b981;
    }
    
    /* Inputs */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }
    
    label p {
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    
    .stTextArea textarea {
        font-family: 'Consolas', 'Courier New', monospace !important;
        font-size: 0.85rem !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. INTERFAZ VISUAL (REESTRUCTURADA CON LOGO ENTERPRISE)
st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)

st.markdown("""
<div class="brand-container">
    <img class="brand-logo" src="https://i.postimg.co/Rh0g3Nfc/manifest-logo.png" alt="Manifest Logo">
    <div class="brand-text-group">
        <h1 class="main-title">Manifest</h1>
        <div class="subtitle">Intelligent File Dependency Resolver</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="tagline">Detecta, analiza y ordena lógicamente colecciones de archivos de configuración y scripts antes de su despliegue en producción.</p>', unsafe_allow_html=True)
st.markdown('<div class="tech-header">Diseñado para resolver secuencias complejas en:</div>', unsafe_allow_html=True)

st.markdown("""
<div class="tech-grid">
    <div class="tech-item"><span class="tech-icon">✔</span> SQL (Oracle / MS SQL)</div>
    <div class="tech-item"><span class="tech-icon">✔</span> Flyway & Liquibase</div>
    <div class="tech-item"><span class="tech-icon">✔</span> Kubernetes YAML</div>
    <div class="tech-item"><span class="tech-icon">✔</span> Terraform HCL</div>
    <div class="tech-item"><span class="tech-icon">✔</span> Bash / PowerShell</div>
    <div class="tech-item"><span class="tech-icon">✔</span> Chrome Manifests</div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 4. ENTRADA DE DATOS NATIVA OPTIMIZADA
molde = st.text_area(
    "1. Pega aquí el Molde Guía (Orden topológico o secuencia lógica deseada):", 
    height=160, 
    placeholder="..\\database\\migrations\\V1__init_tables.sql\n..\\database\\migrations\\V2__add_foreign_keys.sql"
)

archivo_subido = st.file_uploader("2. Selecciona tu archivo Manifiesto desordenado (.txt)", type=["txt"])

# 5. ALGORITMO DE ORDENAMIENTO
if archivo_subido and molde:
    guias_originales = [linea.strip() for linea in molde.split('\n') if linea.strip()]
    guias_solo_nombres = [linea.split('\\')[-1].split('/')[-1].lower() for linea in guias_originales]
    
    lineas_originales = archivo_subido.read().decode("utf-8").splitlines()
    
    lineas_filtradas = []
    for linea in lineas_originales:
        linea_limpia = linea.strip()
        if not linea_limpia: 
            continue
        
        nombre_archivo = linea_limpia.split('|')[-1].lower() if '|' in linea_limpia else linea_limpia.split('\\')[-1].split('/')[-1].lower()
            
        if nombre_archivo.endswith('_rev.sql'):
            continue
            
        if nombre_archivo in guias_solo_nombres:
            lineas_filtradas.append((linea_limpia, nombre_archivo))
            
    lineas_ordenadas = sorted(
        lineas_filtradas, 
        key=lambda x: guias_solo_nombres.index(x[1]) if x[1] in guias_solo_nombres else 999
    )
    
    resultado_final = "\n".join([item[0] for item in lineas_ordenadas])
    
    # 6. PANEL DE RESULTADOS
    if resultado_final:
        st.markdown("---")
        st.success("✓ ¡Dependencias resueltas! Secuencia ordenada con éxito para un despliegue seguro.")
        st.write("**Vista previa del Manifiesto resultante:**")
        st.code(resultado_final, language="text")
        
        st.download_button(
            label="Descargar Manifiesto Ordenado 📥",
            data=resultado_final,
            file_name="manifest_ordenado.txt",
            mime="text/plain"
        )
    else:
        st.error("No se encontraron coincidencias entre el archivo de entrada y el molde de dependencias.")
