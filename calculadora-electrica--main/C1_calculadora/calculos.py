from C1_calculadora.materiales  import obtener_resistividad
from C3_Utilidades.decoradores import registrar_operacion 

@registrar_operacion
def calcular_circuito(voltaje, r_carga, material, longitud_ida, seccion_mm2):
    """Calcula todas las magnitudes del circuito DC en serie sin redondear."""
    rho = obtener_resistividad(material)

    # 1. Conversión de área de mm² a m²
    area_m2 = seccion_mm2 * 1e-6

    # 2. Longitud total (ida y retorno)
    longitud_total = 2 * longitud_ida

    # 3. Resistencia del cable (Rc)
    r_cable = (rho * longitud_total) / area_m2

    # 4. Resistencia total (Rt)
    r_total = r_carga + r_cable

    # 5. Corriente estimada (Ley de Ohm)
    corriente = voltaje / r_total

    # 6. Caída de tensión en el cable (Vc)
    caida_tension = corriente * r_cable

    # 7. Potencia disipada en el cable (Pc)
    potencia_cable = (corriente ** 2) * r_cable

    return {
        "area_m2": area_m2,
        "longitud_total": longitud_total,
        "r_cable": r_cable,
        "r_total": r_total,
        "corriente": corriente,
        "caida_tension": caida_tension,
        "potencia_cable": potencia_cable
    }