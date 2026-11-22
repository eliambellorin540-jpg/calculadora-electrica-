# Diccionario con resistividades en Ohm*m a 20 °C
MATERIALES = {
    "Cobre": 1.68e-8,
    "Aluminio": 2.65e-8,
    "Plata": 1.59e-8,
    "Oro": 2.44e-8,
    "Hierro": 9.71e-8
}

def obtener_resistividad(nombre_material):
    """Devuelve la resistividad del material seleccionado."""
    if nombre_material in MATERIALES:
        return MATERIALES[nombre_material]
    raise ValueError(f"El material '{nombre_material}' no está disponible.") 