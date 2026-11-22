import logging
import os

# Creamos la carpeta logs si no existe
os.makedirs("logs", exist_ok=True)

RUTA_LOG = "logs/app.log"

def obtener_logger(nombre_modulo):
    """Configura y devuelve un logger para cada módulo del proyecto."""
    logger = logging.getLogger(nombre_modulo)
    logger.setLevel(logging.INFO)

    # Evitamos duplicar mensajes si el logger ya fue configurado
    if not logger.handlers:
        archivo_handler = logging.FileHandler(RUTA_LOG, encoding="utf-8")
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        archivo_handler.setFormatter(formato)
        logger.addHandler(archivo_handler)

    return logger 