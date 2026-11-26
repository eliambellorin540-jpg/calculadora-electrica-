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
