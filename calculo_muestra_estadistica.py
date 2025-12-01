import streamlit as st
import math

# ---------------------------------------------------------
# FUNCIÓN PARA CALCULAR MUESTRA CON POBLACIÓN FINITA
# ---------------------------------------------------------
def calcular_muestra(N, nivel_confianza=0.95, margen_error=0.05, p=0.5):
    if N <= 0:
        return 0
    
    Z_values = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    Z = Z_values[nivel_confianza]

    q = 1 - p

    numerador = (Z**2) * p * q * N
    denominador = (margen_error**2) * (N - 1) + (Z**2) * p * q
    n = numerador / denominador

    return math.ceil(n)


# ---------------------------------------------------------
# INTERFAZ STREAMLIT
# ---------------------------------------------------------
st.title("Calculadora de Muestra Estadística – CCPS")

st.write("Calcula el tamaño de muestra para trabajadores directos y contratistas.")

# ------------------------
# Entradas de población
# ------------------------
col1, col2 = st.columns(2)

with col1:
    N_directos = st.number_input(
        "Número de trabajadores directos (opcional excluir líderes)",
        min_value=0,
        step=1,
        value=0
    )

with col2:
    N_contratistas = st.number_input(
        "Número de contratistas",
        min_value=0,
        step=1,
        value=0
    )

# ------------------------
# Parámetros estadísticos
# ------------------------
nivel_confianza = st.selectbox(
    "Nivel de confianza",
    options=[0.90, 0.95, 0.99],
    format_func=lambda x: f"{int(x*100)}%"
)

margen_error = st.number_input(
    "Margen de error (opcional)",
    min_value=0.01,
    max_value=0.10,
    step=0.01,
    value=0.05
)

# ------------------------
# Cálculo de muestras
# ------------------------
if st.button("Calcular muestras"):
    
    muestra_directos = calcular_muestra(
        N=N_directos,
        nivel_confianza=nivel_confianza,
        margen_error=margen_error
    )

    muestra_contratistas = calcular_muestra(
        N=N_contratistas,
        nivel_confianza=nivel_confianza,
        margen_error=margen_error
    )

    st.subheader("Resultados del cálculo muestral")

    nivel_conf_pct = int(nivel_confianza * 100)
    margen_error_pct = int(margen_error * 100)

    colA, colB = st.columns(2)

    # -------------------------------
    # Bloque trabajadores directos
    # -------------------------------
    with colA:
        st.markdown("### Trabajadores directos")

        if N_directos > 0 and muestra_directos > 0:
            st.markdown(
                f"""
                Con una población de **{N_directos}** trabajadores directos, un nivel de confianza de  
                **{nivel_conf_pct}%** y un margen de error máximo de **±{margen_error_pct}%**,  
                el **tamaño mínimo de muestra recomendado es de {muestra_directos} personas**.

                En términos estadísticos, esto significa que si seleccionas de forma aleatoria al menos  
                **{muestra_directos}** trabajadores directos para responder la encuesta, las estimaciones
                de proporciones (por ejemplo, el porcentaje que percibe adecuada la cultura de seguridad)
                tendrán una diferencia esperada no mayor a **±{margen_error_pct} puntos porcentuales**
                respecto al valor real de toda la población de trabajadores directos, con un nivel de
                confianza de **{nivel_conf_pct}%**.
                """
            )
        else:
            st.info("No se ingresó un número válido de trabajadores directos.")

    # -------------------------------
    # Bloque contratistas
    # -------------------------------
    with colB:
        st.markdown("### Contratistas")

        if N_contratistas > 0 and muestra_contratistas > 0:
            st.markdown(
                f"""
                Con una población de **{N_contratistas}** contratistas, un nivel de confianza de  
                **{nivel_conf_pct}%** y un margen de error máximo de **±{margen_error_pct}%**,  
                el **tamaño mínimo de muestra recomendado es de {muestra_contratistas} personas**.

                Desde el punto de vista estadístico, encuestar al menos a **{muestra_contratistas}**
                contratistas permite que las proporciones estimadas para este grupo (por ejemplo,
                el porcentaje que considera que los controles de proceso son claros) se desvíen como máximo
                **±{margen_error_pct} puntos porcentuales** del valor real en toda la población de
                contratistas, con un nivel de confianza de **{nivel_conf_pct}%**.
                """
            )
        else:
            st.info("No se ingresó un número válido de contratistas.")

