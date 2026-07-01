import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Manifest: Intelligent File Dependency Resolver", 
    page_icon="📝",
    layout="centered"
)

# 2. INYECCIÓN DE ESTILOS CSS AVANZADOS (BRANDING ENTERPRISE)
st.markdown("""
    <style>
    /* Ocultar elementos por defecto de Streamlit para limpieza visual */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Contenedor Principal estilo Tarjeta Premium */
    .enterprise-card {
        background-color: var(--background-secondary);
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }
    
    /* Tipografía y Encabezados */
    .main-title {
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1976D2 0%, #00D4FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }
    
    .subtitle {
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 1.05rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 1rem;
    }
    
    .tagline {
        font-size: 1.05rem;
        line-height: 1.6;
        color: var(--text-color);
        opacity: 0.85;
        margin-bottom: 2rem;
    }
    
    /* Grilla de Características / Compatibilidad */
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
        margin-bottom: 2.5rem;
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
    
    /* Ajustes sobre los bloques nativos de Streamlit */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }
    
    label p {
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        color: var(--text-color) !important;
    }
    
    .stTextArea textarea {
        font-family: 'Consolas', 'Courier New', monospace !important;
        font-size: 0.85rem !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_index=True)

# 3. INTERFAZ VISUAL MAQUETADA CON HTML PREMIUM
st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Manifest</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Intelligent File Dependency Resolver</div>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Detecta, analiza y ordena lógicamente colecciones de archivos de configuración y scripts antes de su despliegue en producción.</p>', unsafe_allow_html=True)

st.markdown('<div class="tech-header">Diseñado para resolver secuencias complejas en:</div>', unsafe_allow_html=True)

# Grilla corporativa moderna de compatibilidad
st.markdown("""
<div class="tech-grid">
    <div class="tech-item"><span class="tech-icon">✔</span> SQL (Oracle / SQL Server)</div>
    <div class="tech-item"><span class="tech-icon">✔</span> Flyway & Liquibase</div>
    <div class="tech-item"><span class="tech-icon">✔</span> Kubernetes YAML</div>
    <div class="tech-item"><span class="tech-icon">✔</span> Terraform HCL</div>
    <div class="tech-item"><span class="tech-icon">✔</span> Bash / PowerShell</div>
    <div class="tech-item"><span class="tech-icon">✔</span> Chrome Manifests</div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Cierre de la tarjeta de presentación

# 4. FORMULARIO Y ENTRADA DE DATOS (NATIVO OPTIMIZADO)
molde = st.text_area(
    "1. Pega aquí el Molde Guía (Orden topológico o secuencia lógica deseada):", 
    height=160, 
    placeholder="..\\database\\migrations\\V1__init_tables.sql\n..\\database\\migrations\\V2__add_foreign_keys.sql"
)

archivo_subido = st.file_uploader("2. Selecciona tu archivo Manifiesto desordenado (.txt)", type=["txt"])

# 5. MOTOR DE PROCESAMIENTO LOGÍSTICO
if archivo_subido and molde:
    guias_originales = [linea.strip() for linea in molde.split('\n') if linea.strip()]
    
    guias_solo_nombres = []
    for linea in guias_originales:
        nombre = linea.split('\\')[-1].split('/')[-1].lower()
        guias_solo_nombres.append(nombre)
    
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
            
    lineas_ordenadas = sorted(
        lineas_filtradas, 
        key=lambda x: guias_solo_nombres.index(x[1]) if x[1] in guias_solo_nombres else 999
    )
    
    resultado_final = "\n".join([item[0] for item in lineas_ordenadas])
    
    # 6. SECCIÓN DE RESULTADO ESTILIZADA
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
