import streamlit as st

# Configuración premium de la página web
st.set_page_config(
    page_title="Manifest: Intelligent File Dependency Resolver", 
    page_icon="📝",
    layout="centered"
)

# Título y Posicionamiento de Alto Impacto (Enterprise)
st.title("📝 Manifest")
st.subheader("Intelligent File Dependency Resolver")
st.write("Detecta, analiza y ordena lógicamente colecciones de archivos de configuración y scripts antes de su despliegue en producción.")

# Cuadro de beneficios y casos de uso recomendados
st.info("""
**Diseñado para resolver dependencias y secuencias críticas en:**
✔ SQL Migrations (Oracle, SQL Server, MySQL) | ✔ Flyway & Liquibase | ✔ Kubernetes YAML & Terraform HCL | ✔ Bash & PowerShell Scripts | ✔ Chrome Extension Manifests
""")

# 1. Entrada de la plantilla o molde guía
molde = st.text_area(
    "1. Pega aquí el Molde Guía (Orden topológico o secuencia lógica deseada):", 
    height=160, 
    placeholder="..\\database\\migrations\\V1__init_tables.sql\n..\\database\\migrations\\V2__add_foreign_keys.sql"
)

# 2. Subida del archivo original de entrada
archivo_subido = st.file_uploader("2. Selecciona tu archivo Manifiesto desordenado (.txt)", type=["txt"])

if archivo_subido and molde:
    # --- PROCESAR EL MOLDE ---
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
        
        # Extracción inteligente según formato
        if '|' in linea_limpia:
            nombre_archivo = linea_limpia.split('|')[-1].lower()
        else:
            nombre_archivo = linea_limpia.split('\\')[-1].split('/')[-1].lower()
            
        # Filtro automático corporativo
        if nombre_archivo.endswith('_rev.sql'):
            continue
            
        if nombre_archivo in guias_solo_nombres:
            lineas_filtradas.append((linea_limpia, nombre_archivo))
            
    # --- ORDENAMIENTO TOPOLÓGICO / INTELIGENTE ---
    lineas_ordenadas = sorted(
        lineas_filtradas, 
        key=lambda x: guias_solo_nombres.index(x[1]) if x[1] in guias_solo_nombres else 999
    )
    
    resultado_final = "\n".join([item[0] for item in lineas_ordenadas])
    
    if resultado_final:
        st.success("✓ ¡Dependencias resueltas! Secuencia ordenada con éxito para un despliegue seguro.")
        
        # Vista previa en pantalla
        st.write("**Vista previa del Manifiesto resultante:**")
        st.code(resultado_final, language="text")
        
        # 3. Botón definitivo de descarga
        st.download_button(
            label="3. Descargar Manifiesto Ordenado 📥",
            data=resultado_final,
            file_name="manifest_ordenado.txt",
            mime="text/plain"
        )
    else:
        st.error("No se encontraron coincidencias entre el archivo de entrada y el molde de dependencias. Revisa los nombres internos.")
