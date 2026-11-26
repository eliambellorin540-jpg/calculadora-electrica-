import csv
import io
import os
from C2_servicios.logs import obtener_logger

logger = obtener_logger("servicios.reportes")

os.makedirs("reportes", exist_ok=True)

# Tupla inmutable con los encabezados del reporte
ENCABEZADOS_CSV = (
    "ID", "Fecha y Hora", "Voltaje (V)", "R_carga (Ohm)", "Material",
    "Longitud ida (m)", "Sección (mm²)", "Rc (Ohm)", "Rt (Ohm)",
    "Corriente (A)", "Vc (V)", "Pc (W)"
)

def exportar_a_csv(registros, nombre_archivo="reporte_calculos.csv"):
    """Guarda los registros en un archivo CSV y devuelve su contenido en texto."""
    ruta_completa = os.path.join("reportes", nombre_archivo)
    salida_memoria = io.StringIO()

    try:
        with open(ruta_completa, "w", newline="", encoding="utf-8") as archivo_disco:
            escritor_disco = csv.writer(archivo_disco)
            escritor_memoria = csv.writer(salida_memoria)

            escritor_disco.writerow(ENCABEZADOS_CSV)
            escritor_memoria.writerow(ENCABEZADOS_CSV)

            for reg in registros:
                ent = reg["entradas"]
                res = reg["resultados"]
                fila = [
                    reg["id"], reg["fecha_hora"], ent["voltaje"], ent["r_carga"],
                    ent["material"], ent["longitud_ida"], ent["seccion_mm2"],
                    round(res["r_cable"], 4), round(res["r_total"], 4),
                    round(res["corriente"], 4), round(res["caida_tension"], 4),
                    round(res["potencia_cable"], 4)
                ]
                escritor_disco.writerow(fila)
                escritor_memoria.writerow(fila)

        logger.info(f"Reporte CSV exportado con {len(registros)} registros.")
        return salida_memoria.getvalue()
    except Exception as error:
        logger.error(f"Error al exportar CSV: {error}")
        raise error 