import streamlit as st
from C1_calculadora.materiales import MATERIALES
from C1_calculadora.validaciones import validar_numero_positivo, validar_seccion_transversal
from C1_calculadora.calculos import calcular_circuito
from C2_servicios.historial import cargar_historial, guardar_calculo
from C2_servicios.reportes import exportar_a_csv
from C2_servicios.logs import obtener_logger, RUTA_LOG
from C3_Utilidades.generadores import leer_lineas_log     

logger = obtener_logger("app")

# Configuración de la página
st.set_page_config(
    page_title="Calculadora Eléctrica DC | UNIMAR",
    page_icon="⚡",
    layout="wide"
)

# Tupla con las secciones obligatorias del menú
SECCIONES = (
    "⚡ Calculadora",
    "📜 Historial",
    "🛠️ Logs Técnicos",
    "📊 Reportes",
    "📘 Fundamentos y Ayuda"
)

# Barra lateral de navegación
st.sidebar.title("⚡ Simulador DC")
st.sidebar.markdown("Proyecto Final - Programación I")
pagina = st.sidebar.radio("Navegación:", SECCIONES)
st.sidebar.divider()
st.sidebar.caption("Simulación didáctica a 20 °C. No usar para instalaciones reales.")


# ==========================================
# 1. CALCULADORA
# ==========================================
if pagina == "⚡ Calculadora":
    st.title("⚡ Calculadora de Corriente y Resistencia DC")
    st.write("Ingresa los parámetros del circuito en serie (fuente, ida, carga y retorno).")

    # Inicializar valores en memoria para poder limpiar el formulario
    for clave in ["v_in", "rc_in", "l_in", "a_in"]:
        if clave not in st.session_state:
            st.session_state[clave] = ""

    def limpiar_formulario():
        st.session_state["v_in"] = ""
        st.session_state["rc_in"] = ""
        st.session_state["l_in"] = ""
        st.session_state["a_in"] = ""

    col1, col2 = st.columns(2)
    with col1:
        voltaje_txt = st.text_input("Tensión de alimentación V (V)", key="v_in", placeholder="Ej: 12")
        rcarga_txt = st.text_input("Resistencia de carga Rcarga (Ω)", key="rc_in", placeholder="Ej: 10")
        material = st.selectbox("Material del conductor", list(MATERIALES.keys()))

    with col2:
        longitud_txt = st.text_input("Longitud de ida L (m)", key="l_in", placeholder="Ej: 5")
        seccion_txt = st.text_input("Sección transversal A (mm²)", key="a_in", placeholder="Ej: 2,5 mm²")
        st.info(f"Resistividad del {material}: **{MATERIALES[material]:.2e} Ω·m**")

    btn_col1, btn_col2, _ = st.columns([1, 1, 4])
    with btn_col1:
        calcular = st.button("🚀 Calcular", type="primary", use_container_width=True)
    with btn_col2:
        st.button("🧹 Limpiar", on_click=limpiar_formulario, use_container_width=True)

    if calcular:
        try:
            # Validaciones
            v = validar_numero_positivo(voltaje_txt, "Tensión (V)")
            r_carga = validar_numero_positivo(rcarga_txt, "Resistencia de carga")
            l_ida = validar_numero_positivo(longitud_txt, "Longitud de ida")
            seccion = validar_seccion_transversal(seccion_txt)

            # Cálculos
            res = calcular_circuito(v, r_carga, material, l_ida, seccion)

            # Guardar en historial JSON
            entradas = {
                "voltaje": v,
                "r_carga": r_carga,
                "material": material,
                "longitud_ida": l_ida,
                "seccion_mm2": seccion
            }
            id_reg = guardar_calculo(entradas, res)

            st.success(f"✅ Cálculo completado y guardado en el historial (ID: {id_reg})")

            # Mostrar resultados con tarjetas métricas
            st.subheader("Resultados del Circuito")
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Resistencia Cable (Rc)", f"{res['r_cable']:.4f} Ω")
            m2.metric("Resistencia Total (Rt)", f"{res['r_total']:.4f} Ω")
            m3.metric("Corriente (I)", f"{res['corriente']:.4f} A")
            m4.metric("Caída de Tensión (Vc)", f"{res['caida_tension']:.4f} V")
            m5.metric("Potencia Cable (Pc)", f"{res['potencia_cable']:.4f} W")

            st.caption(f"Longitud total calculada (ida + retorno): {res['longitud_total']} m | Área: {res['area_m2']:.2e} m²")

        except ValueError as error_val:
            st.error(f"⚠️ Error de validación: {error_val}")
        except Exception as error_gen:
            st.error(f"❌ Ocurrió un error inesperado: {error_gen}")


# ==========================================
# 2. HISTORIAL
# ==========================================
elif pagina == "📜 Historial":
    st.title("📜 Historial de Cálculos")
    historial = cargar_historial()

    if not historial:
        st.info("Aún no hay cálculos guardados en data/historial.json.")
    else:
        # Filtros por material y fecha
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filtro_mat = st.selectbox("Filtrar por material:", ["Todos"] + list(MATERIALES.keys()))
        with col_f2:
            filtro_fecha = st.text_input("Filtrar por fecha (AAAA-MM-DD):", placeholder="Ej: 2026-11-20")

        # Lista de comprensión para filtrar
        filtrados = [
            reg for reg in historial
            if (filtro_mat == "Todos" or reg["entradas"]["material"] == filtro_mat)
            and (filtro_fecha.strip() in reg["fecha_hora"])
        ]

        if not filtrados:
            logger.warning("Filtro de historial sin coincidencias.")
            st.warning("No se encontraron registros con esos filtros.")
        else:
            tabla = []
            for r in filtrados:
                tabla.append({
                    "ID": r["id"],
                    "Fecha": r["fecha_hora"],
                    "Material": r["entradas"]["material"],
                    "V (V)": r["entradas"]["voltaje"],
                    "Rcarga (Ω)": r["entradas"]["r_carga"],
                    "L ida (m)": r["entradas"]["longitud_ida"],
                    "A (mm²)": r["entradas"]["seccion_mm2"],
                    "Rc (Ω)": round(r["resultados"]["r_cable"], 4),
                    "I (A)": round(r["resultados"]["corriente"], 4),
                    "Vc (V)": round(r["resultados"]["caida_tension"], 4),
                    "Pc (W)": round(r["resultados"]["potencia_cable"], 4)
                })
            st.dataframe(tabla, use_container_width=True)


# ==========================================
# 3. LOGS TÉCNICOS
# ==========================================
elif pagina == "🛠️ Logs Técnicos":
    st.title("🛠️ Registro de Eventos Técnicos (app.log)")
    st.write("Lectura iterativa en tiempo real usando un generador (`yield`).")

    # Consumimos el generador en una lista para mostrar los más recientes primero
    lineas = list(leer_lineas_log(RUTA_LOG))

    if not lineas:
        st.info("No hay eventos registrados todavía.")
    else:
        cantidad = st.slider("Mostrar últimas líneas:", 5, max(10, len(lineas)), min(20, len(lineas)))
        recientes = lineas[-cantidad:]
        recientes.reverse()
        st.code("\n".join(recientes), language="text")


# ==========================================
# 4. REPORTES
# ==========================================
elif pagina == "📊 Reportes":
    st.title("📊 Exportación de Reportes CSV")
    historial = cargar_historial()

    if not historial:
        st.warning("Realiza al menos un cálculo para poder generar un reporte.")
    else:
        st.write(f"Actualmente hay **{len(historial)}** cálculos listos para exportar.")
        if st.button("📄 Generar archivo CSV"):
            contenido_csv = exportar_a_csv(historial)
            st.success("Archivo guardado en `reportes/reporte_calculos.csv`.")
            st.download_button(
                label="⬇️ Descargar reporte_calculos.csv",
                data=contenido_csv,
                file_name="reporte_calculos.csv",
                mime="text/csv"
            )


# ==========================================
# 5. FUNDAMENTOS Y AYUDA
# ==========================================
elif pagina == "📘 Fundamentos y Ayuda":
    st.title("📘 Fundamentos Teóricos y Ayuda")

    st.subheader("1. Modelo Matemático (Circuito DC en Serie)")
    st.markdown("""
    El simulador modela una fuente DC conectada a una carga mediante un conductor de ida y retorno del mismo material y sección:
    1. **Conversión de área:** $A(m^2) = A(mm^2) \\times 10^{-6}$
    2. **Longitud total:** $L_{total} = 2 \\times L$
    3. **Resistencia del cable:** $R_c = \\rho \\times \\frac{L_{total}}{A(m^2)}$
    4. **Resistencia total:** $R_t = R_{carga} + R_c$
    5. **Corriente estimada (Ley de Ohm):** $I = \\frac{V}{R_t}$
    6. **Caída de tensión en el cable:** $V_c = I \\times R_c$
    7. **Potencia disipada en el cable:** $P_c = I^2 \\times R_c$
    """)

    st.subheader("2. Caso de Comprobación")
    st.info("Entradas: **12 V** | **10 Ω** | **Cobre** | **5 m** | **2,5 mm²** → Resultados esperados: **Rc ≈ 0.0672 Ω**, **Rt ≈ 10.0672 Ω**, **I ≈ 1.1920 A**, **Vc ≈ 0.0801 V**, **Pc ≈ 0.0955 W**.")

    st.subheader("3. Alcance y Limitaciones")
    st.warning("Esta es una simulación didáctica a 20 °C. No calcula ampacidad, calentamiento del conductor ni resistencia de contactos. No debe utilizarse para dimensionar instalaciones eléctricas reales.")