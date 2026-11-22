import time
from C2_servicios.logs import obtener_logger

logger = obtener_logger("utilidades.decoradores")

def registrar_operacion(funcion):
    """Decorador que mide el tiempo de ejecución y lo registra en app.log."""
    def envoltura(*args, **kwargs):
        inicio = time.time()
        try:
            resultado = funcion(*args, **kwargs)
            duracion = time.time() - inicio
            logger.info(f"Operación '{funcion.__name__}' completada en {duracion:.4f}s")
            return resultado
        except Exception as error:
            logger.error(f"Error en '{funcion.__name__}': {error}")
            raise error
    return envoltura 