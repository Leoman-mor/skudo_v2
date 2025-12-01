import streamlit as st
import math

# ---------------------------------------------------------
# FUNCIÓN PARA CALCULAR MUESTRA CON POBLACIÓN FINITA
# ---------------------------------------------------------
def calcular_muestra(N, nivel_confianza=0.95, margen_error=0.05, p=0.5):
    # Valor Z según el nivel de confianza
    Z_values = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    Z = Z_values[nivel_confianza]

    q = 1 - p

    # Fórmula población finita:
    # n = (Z^2 * p * q * N) / (e^2 * (N - 1) + Z^2 * p * q)
    numerador = (Z**2) * p * q * N
    denominador = (margen_error**2) * (N - 1) + (Z**2) * p * q
    n = numerador / denominador

    return math.ceil(n)


# ---------------------------------------------------------
# INTERFAZ STREAMLIT
# ---------------------------------------------------------
st.title("Calculadora de Muestra Estadística – CCPS")

st.write("Calcula el tamaño de muestra para evaluar cultura en seguridad de procesos.")

N = st.number_input("Número total de trabajadores (opcional excluir a líderes)", min_value=1, step=1)

nivel_confianza = st.selectbox(
    "Nivel de confianza",
    options=[0.90, 0.95, 0.99],
    format_func=lambda x: f"{int(x*100)}%"
)

margen_error = st.slider(
    "Margen de error (e)",
    min_value=0.01,
    max_value=0.10,
    value=0.05,
    step=0.01
)

if st.button("Calcular muestra"):
    n = calcular_muestra(
        N=N,
        nivel_confianza=nivel_confianza,
        margen_error=margen_error,
        p=0.5  # Valor conservador
    )

    st.success(f"**Tamaño de muestra recomendado: {n} trabajadores**")

