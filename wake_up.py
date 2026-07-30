import urllib.request
import ssl

# URL exacta de tu aplicación
URL = "https://ordenador-manifest-v2.streamlit.app/"

try:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Hacemos una petición al endpoint interno de salud de Streamlit
    req = urllib.request.Request(
        f"{URL}_stcore/health", 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    response = urllib.request.urlopen(req, context=ctx)
    print("Petición de reactivación enviada. Código de respuesta:", response.getcode())
except Exception as e:
    print("Ocurrió un error al intentar despertar la app:", e)
