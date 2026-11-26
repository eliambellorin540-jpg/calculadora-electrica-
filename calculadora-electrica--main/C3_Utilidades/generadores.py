import os
from C2_servicios.logs import obtener_logger

logger = obtener_logger("utilidades.generadores")

def leer_lineas_log(ruta_archivo):
    """Generador que devuelve cada línea del archivo app.log una por una."""
    if not os.path.exists(ruta_archivo):
        logger.warning(f"El archivo {ruta_archivo} aún no existe.")
        return

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            yield linea.strip() 