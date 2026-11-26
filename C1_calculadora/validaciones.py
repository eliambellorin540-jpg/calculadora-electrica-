import math
import re
from C2_servicios.logs import obtener_logger

logger = obtener_logger("calculadora.validaciones")

def validar_numero_positivo(texto, nombre_campo):
    """Valida que un texto sea un número finito mayor que cero."""
    texto_limpio = str(texto).strip().replace(",", ".")
    
    if not texto_limpio:
        logger.warning(f"Campo vacío en {nombre_campo}")
        raise ValueError(f"El campo '{nombre_campo}' no puede estar vacío.")

    try:
        valor = float(texto_limpio)
    except ValueError:
        logger.warning(f"Formato no numérico en {nombre_campo}: '{texto}'")
        raise ValueError(f"'{nombre_campo}' debe ser un número válido.")

    if math.isnan(valor) or math.isinf(valor):
        logger.warning(f"Valor NaN o infinito en {nombre_campo}")
        raise ValueError(f"'{nombre_campo}' debe ser un número finito.")

    if valor <= 0:
        logger.warning(f"Valor menor o igual a cero en {nombre_campo}: {valor}")
        raise ValueError(f"'{nombre_campo}' debe ser mayor que cero.")

    return valor


def validar_seccion_transversal(texto):
    """
    Valida y extrae el área en mm² usando expresiones regulares.
    Formatos admitidos: '2.5', '2,5', '2.5 mm2', '2,5 mm²'.
    Formatos rechazados: letras sueltas, unidades distintas (cm, m), negativos.
    """
    texto_limpio = str(texto).strip()
    
    # Patrón regex: número entero o decimal (con . o ,) y unidad opcional mm2 o mm²
    patron = r"^(\d+(?:[.,]\d+)?)\s*(mm2|mm²)?$"
    coincidencia = re.match(patron, texto_limpio, re.IGNORECASE)

    if not coincidencia:
        logger.warning(f"Sección transversal con formato inválido: '{texto}'")
        raise ValueError(
            "-Sección inválida. Usa formatos como: 2.5, 2,5, 2.5 mm2 o 2,5 mm²."
        )

    numero_texto = coincidencia.group(1)
    return validar_numero_positivo(numero_texto, "Sección transversal")