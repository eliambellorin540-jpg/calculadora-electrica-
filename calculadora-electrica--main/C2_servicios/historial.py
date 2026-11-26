import json
import os
from datetime import datetime
from C2_servicios.logs import obtener_logger

logger = obtener_logger("servicios.historial")

os.makedirs("data", exist_ok=True)
RUTA_HISTORIAL = "data/historial.json"

def cargar_historial():
    """Carga la lista de cálculos desde JSON. Si no existe o falla, devuelve lista vacía."""
    if not os.path.exists(RUTA_HISTORIAL):
        logger.warning("historial.json no existe. Se inicializará uno nuevo.")
        return []

    try:
        with open(RUTA_HISTORIAL, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return datos if isinstance(datos, list) else []
    except json.JSONDecodeError:
        logger.error("El archivo historial.json está corrupto o ilegible.")
        return []
    except Exception as error:
        logger.error(f"Error al leer historial.json: {error}")
        return []


def guardar_calculo(entradas, resultados):
    """Agrega un nuevo registro al historial JSON y devuelve su ID."""
    historial = cargar_historial()
    nuevo_id = f"{len(historial) + 1:04d}"

    registro = {
        "id": nuevo_id,
        "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entradas": entradas,
        "resultados": resultados
    }

    historial.append(registro)

    try:
        with open(RUTA_HISTORIAL, "w", encoding="utf-8") as archivo:
            json.dump(historial, archivo, indent=4, ensure_ascii=False)
        logger.info(f"Cálculo guardado correctamente | id={nuevo_id}")
        return nuevo_id
    except Exception as error:
        logger.error(f"No se pudo escribir en historial.json: {error}")
        raise error