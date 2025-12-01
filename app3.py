# skudo_app.py
# -----------------------------------------------------------------------------
# SKUDO – Soluquim IA Suite (Mockup mejorado)
# -----------------------------------------------------------------------------
# Este mockup representa la visión completa:
# 1. Tablero ejecutivo corporativo con mapa geoespacial.
# 2. Diagnóstico de PSM/PPAM + cultura + brechas.
# 3. Generador del Informe de Seguridad (Res. 3687 de 2025).
# 4. Módulos de soporte: barreras, PEC, copiloto IA, admin.
#
# NOTA:
# - Todo usa datos dummy.
# - El objetivo es tener la estructura y el flujo.
# - Luego se conectan fuentes reales: Soluquim, QRA, Excel CCPS, etc.
# -----------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# -----------------------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SKUDO – Soluquim IA Suite",
    layout="wide",
)

# Mini tema visual (simple) para diferenciar secciones
st.markdown(
    """
    <style>
    .skudo-title { font-size: 26px; font-weight: 700; }
    .skudo-subtitle { font-size: 16px; color: #666; }
    .metric-card {
        padding: 0.75rem;
        border-radius: 0.75rem;
        border: 1px solid #e5e5e5;
        background-color: #fafafa;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# DATOS DUMMY – AQUÍ LUEGO SE ENCHUFAN DATOS REALES
# -----------------------------------------------------------------------------

def dummy_instalaciones():
    """Instalaciones clasificadas con coordenadas y riesgo global."""
    data = [
        {
            "Instalación": "Estación Jobo",
            "lat": 8.75, "lon": -75.15,
            "Riesgo_Global": "Alto",
            "Tier1_YTD": 0, "Tier2_YTD": 2,
            "Barreras_Rojas": 3,
        },
        {
            "Instalación": "Tanque TK-17",
            "lat": 7.90, "lon": -72.50,
            "Riesgo_Global": "Medio",
            "Tier1_YTD": 1, "Tier2_YTD": 1,
            "Barreras_Rojas": 1,
        },
        {
            "Instalación": "Línea G7",
            "lat": 4.65, "lon": -74.10,
            "Riesgo_Global": "Alto",
            "Tier1_YTD": 0, "Tier2_YTD": 3,
            "Barreras_Rojas": 2,
        },
        {
            "Instalación": "Reactor R-4",
            "lat": 10.40, "lon": -75.50,
            "Riesgo_Global": "Medio",
            "Tier1_YTD": 0, "Tier2_YTD": 0,
            "Barreras_Rojas": 0,
        },
    ]
    return pd.DataFrame(data)


def dummy_kpis_corporativos():
    """KPIs corporativos clave de PSM."""
    return {
        "tier1_ytd": 1,
        "tier2_ytd": 6,
        "horas_trabajo_mm": 1.8,
        "salud_barreras": 68,   # %
        "madurez_actual": 2.6,
        "madurez_objetivo": 3.5,
        "indice_cultura": 54,
    }


def dummy_activos_criticos():
    """Top activos críticos según riesgo."""
    data = [
        {"Activo": "Estación Jobo", "Riesgo": "Alto",
         "Comentario": "3 barreras críticas vencidas; QRA > 1E-5"},
        {"Activo": "Línea G7", "Riesgo": "Alto",
         "Comentario": "Historial de fugas; alta frecuencia"},
        {"Activo": "Tanque TK-17", "Riesgo": "Medio",
         "Comentario": "LOPA pendiente de actualización"},
        {"Activo": "Reactor R-4", "Riesgo": "Medio",
         "Comentario": "Hallazgos en integridad mecánica"},
        {"Activo": "Rack de válvulas 9", "Riesgo": "Bajo",
         "Comentario": "Sin hallazgos críticos"},
    ]
    return pd.DataFrame(data)


def dummy_diagnostico_psm():
    """Resultado de diagnóstico por elementos PSM/PPAM."""
    elementos = [
        "Gestión de Cambios",
        "Integridad Mecánica",
        "Competencias y Formación",
        "Investigación de Incidentes",
        "Gestión de Riesgos de Proceso",
        "Cultura de Seguridad",
        "Operación y Procedimientos",
        "Gestión de Contratistas",
        "Gestión de Información Técnica",
        "Preparación y Respuesta a Emergencias",
    ]
    np.random.seed(42)
    puntaje = np.random.randint(40, 90, size=len(elementos))
    return pd.DataFrame({"Elemento": elementos, "Puntaje": puntaje})


def dummy_cultura():
    """Indicadores de cultura de seguridad de procesos."""
    items = [
        "Percepción del riesgo",
        "Disciplina operativa",
        "Confianza en reportes",
        "Liderazgo visible",
        "Aprendizaje organizacional",
    ]
    valor = [45, 60, 78, 52, 55]
    return pd.DataFrame({"Dimensión": items, "Puntaje": valor})


def dummy_salud_barreras():
    """Distribución global de barreras."""
    return pd.DataFrame({
        "Estado": ["Verde", "Amarillo", "Rojo"],
        "Cantidad": [122, 18, 8],
    })


def dummy_acciones():
    """Acciones derivadas de estudios de riesgo."""
    data = [
        {"Id": 1, "Instalación": "Estación Jobo",
         "Descripción": "Revisar válvula PSV-14",
         "Criticidad": "Crítica", "Días_vencida": 12, "Estado": "Abierta"},
        {"Id": 2, "Instalación": "Tanque TK-17",
         "Descripción": "Actualizar LOPA del tanque",
         "Criticidad": "Alta", "Días_vencida": 5, "Estado": "En curso"},
        {"Id": 3, "Instalación": "Línea G7",
         "Descripción": "Inspección línea por corrosión",
         "Criticidad": "Alta", "Días_vencida": 0, "Estado": "Planificada"},
        {"Id": 4, "Instalación": "Reactor R-4",
         "Descripción": "Capacitación operadores",
         "Criticidad": "Media", "Días_vencida": 0, "Estado": "Abierta"},
    ]
    return pd.DataFrame(data)


def dummy_simulacros():
    """Registro simple de simulacros PEC."""
    return pd.DataFrame({
        "Fecha": ["2025-03-21", "2025-06-10"],
        "Instalación": ["Línea G7", "Tanque TK-17"],
        "Escenario": ["Derrame tóxico G7", "Explosión TK-17"],
        "Tipo": ["Simulacro", "Simulación de escritorio"],
        "Hallazgos_críticos": [2, 1],
    })

# -----------------------------------------------------------------------------
# CABECERA COMÚN
# -----------------------------------------------------------------------------

def ui_header():
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown('<div class="skudo-title">🛡️ SKUDO – Soluquim IA Suite</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="skudo-subtitle">'
            'Centro de inteligencia para Seguridad de Procesos (PSM/PPAM) y PPAM – alineado con Decreto 1347 y Res. 3687.'
            '</div>',
            unsafe_allow_html=True,
        )
    with col2:
        rol = st.selectbox("Rol", [
            "Gerente General",
            "Gerente HSSE",
            "Gerente de Planta",
            "Ingeniero de Proceso",
            "Coordinador de Emergencias",
        ])
    with col3:
        periodo = st.selectbox("Periodo", ["Últimos 30 días", "YTD", "Últimos 12 meses"])
        st.caption(datetime.now().strftime("Fecha: %Y-%m-%d"))
    st.divider()
    return rol, periodo

# -----------------------------------------------------------------------------
# PANTALLA 1 – TABLERO EJECUTIVO (MAPA GEOESPACIAL + KPIs)
# -----------------------------------------------------------------------------

def pantalla_tablero_ejecutivo():
    rol, periodo = ui_header()

    kpis = dummy_kpis_corporativos()
    df_inst = dummy_instalaciones()
    df_activos = dummy_activos_criticos()

    # FILA DE KPIs EJECUTIVOS
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Eventos Tier 1 – YTD", kpis["tier1_ytd"])
            st.caption("API RP 754 – Accidentes de proceso con mayor severidad.")
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Eventos Tier 2 – YTD", kpis["tier2_ytd"])
            st.caption("Severidad moderada de seguridad de procesos.")
            st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        tasa = kpis["tier1_ytd"] / max(kpis["horas_trabajo_mm"], 0.1)
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Tasa Tier 1 (por MM h)", f"{tasa:.2f}")
            st.caption("Normalización por exposición (millones de horas).")
            st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Salud Global de Barreras (%)", f"{kpis['salud_barreras']}")
            st.caption("Barreras críticas disponibles vs diseñadas.")
            st.markdown("</div>", unsafe_allow_html=True)

    with col5:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Índice de Cultura PSM", f"{kpis['indice_cultura']} %")
            st.caption("Resultado global de encuestas de cultura.")
            st.markdown("</div>", unsafe_allow_html=True)

    # MAPA + RIESGO / TOP ACTIVOS
    col_map, col_right = st.columns([2, 1])

    with col_map:
        st.subheader("🗺️ Mapa Corporativo de Riesgo de Proceso")
        st.caption(
            "Instalaciones clasificadas (Decreto 1347) con nivel de riesgo global, "
            "basado en QRA, barreras y eventos (Tier1/2)."
        )
        st.map(df_inst[["lat", "lon"]], size=40)

        # Distribución de riesgo por instalación
        st.markdown("**Distribución de riesgo por instalación**")
        fig_risk = (
            alt.Chart(df_inst)
            .mark_bar()
            .encode(
                x=alt.X("Instalación", sort=None),
                y=alt.Y("Tier2_YTD", title="Eventos Tier 2"),
                color="Riesgo_Global",
                tooltip=["Instalación", "Riesgo_Global", "Tier1_YTD", "Tier2_YTD", "Barreras_Rojas"],
            )
        )
        st.altair_chart(fig_risk, use_container_width=True)

    with col_right:
        st.subheader("Top 5 Activos Críticos")
        st.dataframe(df_activos, use_container_width=True, hide_index=True)

        st.subheader("Madurez PSM/PPAM Corporativa")
        madurez_df = pd.DataFrame({
            "Tipo": ["Actual", "Objetivo"],
            "Nivel": [kpis["madurez_actual"], kpis["madurez_objetivo"]],
        })
        chart = (
            alt.Chart(madurez_df)
            .mark_bar()
            .encode(
                x=alt.X("Tipo", sort=None),
                y=alt.Y("Nivel", scale=alt.Scale(domain=[0, 5])),
                tooltip=["Tipo", "Nivel"]
            )
        )
        st.altair_chart(chart, use_container_width=True)

    # INSIGHT EJECUTIVO IA
    st.subheader("Executive AI Insight")
    st.info(
        "La Estación Jobo y la Línea G7 concentran el mayor riesgo corporativo, con 5 barreras críticas "
        "en estado rojo y la mayor frecuencia de eventos Tier 2. "
        "Recomendación: priorizar inspecciones, revisión LOPA y refuerzo de competencias en operación "
        "antes del cierre del trimestre."
    )

    st.divider()
    col_inf1, col_inf2, col_inf3 = st.columns(3)
    with col_inf1:
        st.button("Generar Informe Ejecutivo (IA)")
    with col_inf2:
        st.button("Preparar Informe de Seguridad – Res. 3687 (Borrador)")
    with col_inf3:
        st.button("Ver Mapa de Isocontornos (QRA)")

# -----------------------------------------------------------------------------
# PANTALLA 2 – DIAGNÓSTICO SKUDO (NOTA + MAPA DE CALOR)
# -----------------------------------------------------------------------------

def pantalla_diagnostico():
    ui_header()

    st.subheader("🧭 Diagnóstico Global SKUDO – PSM, PPAM y Cultura")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cumplimiento técnico PSM/PPAM", "63 %")
    with col2:
        st.metric("Madurez cultural", "54 %")
    with col3:
        st.metric("Gobernanza y roles", "71 %")

    tabs = st.tabs(["Resumen ejecutivo", "Mapa de madurez", "Detalle por elemento"])

    df_diag = dummy_diagnostico_psm()
    df_cultura = dummy_cultura()

    with tabs[0]:
        st.markdown("### Foto general (IA)")
        st.info(
            "El sistema de PSM se encuentra en una fase intermedia de madurez. "
            "Los puntos más débiles son: Gestión de Cambios, Integridad Mecánica y Cultura de Seguridad. "
            "Se recomienda enfocar el plan de 12–18 meses en estos elementos, "
            "alineando recursos, competencias y gobernanza."
        )
        st.markdown("### Brechas críticas detectadas")
        st.warning(
            "- 24 recomendaciones abiertas de HAZOP/LOPA.\n"
            "- 8 barreras críticas degradadas en activos de proceso.\n"
            "- Falta evidencia formal de PEC actualizado en 2 instalaciones.\n"
            "- 2 instalaciones sin shapefile para ordenamiento territorial (Res. 3687 – Anexo OT)."
        )

    with tabs[1]:
        st.markdown("### Mapa de madurez por elemento PSM/PPAM")
        chart_diag = (
            alt.Chart(df_diag)
            .mark_bar()
            .encode(
                x=alt.X("Elemento", sort=None),
                y=alt.Y("Puntaje", scale=alt.Scale(domain=[0, 100])),
                tooltip=["Elemento", "Puntaje"],
            )
        )
        st.altair_chart(chart_diag, use_container_width=True)

        st.markdown("### Cultura de Seguridad de Procesos")
        cultura_chart = (
            alt.Chart(df_cultura)
            .mark_bar()
            .encode(
                x=alt.X("Dimensión", sort=None),
                y=alt.Y("Puntaje", scale=alt.Scale(domain=[0, 100])),
                tooltip=["Dimensión", "Puntaje"],
            )
        )
        st.altair_chart(cultura_chart, use_container_width=True)

    with tabs[2]:
        st.markdown("### Detalle de resultados por elemento")
        st.dataframe(df_diag.sort_values("Puntaje", ascending=True), use_container_width=True, hide_index=True)

        st.markdown("### Ruta SKUDO de Implementación (sugerida por IA)")
        timeline = [
            "Q1: Integridad mecánica + revisión LOPA + PEC",
            "Q2: Gestión de cambios + cultura de disciplina operativa",
            "Q3: Modelaje escenarios Res. 1890 + QRA actualizado",
            "Q4: Auditoría PPAM + Informe de Seguridad para Mintrabajo",
        ]
        for item in timeline:
            st.write(f"✅ {item}")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.button("Ejecutar nuevo diagnóstico")
    with col_b:
        st.button("Comparar contra ciclo anterior")

# -----------------------------------------------------------------------------
# PANTALLA 3 – GENERADOR INFORME DE SEGURIDAD (RES. 3687)
# -----------------------------------------------------------------------------

def pantalla_informe_seguridad():
    ui_header()

    st.subheader("📄 Generador de Informe de Seguridad – Resolución 3687 de 2025")

    st.caption(
        "Estructura alineada con: Proceso de conocimiento del riesgo, "
        "reducción del riesgo, manejo del desastre y anexos de ordenamiento territorial."
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "1. Conocimiento del riesgo",
        "2. Reducción del riesgo",
        "3. Manejo del desastre (PEC)",
        "4. Anexos OT y exportación",
    ])

    with tab1:
        st.markdown("### 1. Proceso de conocimiento del riesgo")

        st.checkbox("1.1 Información general del establecimiento y procesos", value=True)
        st.checkbox("1.2 Inventario de sustancias peligrosas (SGA) y HDS", value=True)
        st.checkbox("1.3 Contexto externo y elementos expuestos", value=True)
        st.checkbox("1.4 Contexto interno y sistema de gestión PPAM", value=True)
        st.checkbox("1.5 Identificación de peligros y escenarios (Res. 1890)", value=True)
        st.checkbox("1.6 Evaluación cuantitativa del riesgo (QRA + isocontornos)", value=True)

        st.text_area(
            "Notas / comentarios adicionales (conocimiento del riesgo)",
            value="Ejemplo: Se usa CCPS + ISO 31000 + ISO 31010 como RAGAGEP para evaluación de riesgos.",
            height=120,
        )

    with tab2:
        st.markdown("### 2. Proceso de reducción del riesgo")
        st.checkbox("2.1 Medidas de prevención y mitigación (barreras, salvaguardas)", value=True)
        st.checkbox("2.2 Sistemas de protección, detección, control y alivio", value=True)
        st.checkbox("2.3 Medios internos y externos de respuesta", value=True)
        st.checkbox("2.4 Mecanismos de protección financiera", value=True)

        st.text_area(
            "Resumen de medidas clave",
            value="Ejemplo: Se han implementado barreras instrumentadas (SIS), PSV, diques de contención, "
                  "y se cuenta con pólizas de responsabilidad civil y ambiental asociadas a los escenarios de "
                  "accidente mayor identificados.",
            height=120,
        )

    with tab3:
        st.markdown("### 3. Manejo del desastre – PEC")
        st.checkbox("3.1 Plan estratégico de emergencias", value=True)
        st.checkbox("3.2 Plan operativo de respuesta", value=True)
        st.checkbox("3.3 Plan de recuperación post-evento", value=True)
        st.checkbox("3.4 Coordinación institucional y simulacros", value=True)

        st.text_area(
            "Descripción breve del PEC (versión sin anexos)",
            value="Ejemplo: El PEC integra roles, cadena de mando, procedimientos de activación, "
                  "medios de comunicación, coordinación con autoridades y cronograma de simulacros "
                  "de accidentes mayores.",
            height=140,
        )

    with tab4:
        st.markdown("### 4. Anexos para Ordenamiento Territorial")
        st.checkbox("4.1 Shapefiles/geodatabase de isocontornos de riesgo individual global", value=True)
        st.checkbox("4.2 Mapas de zonas susceptibles de afectación", value=True)
        st.checkbox("4.3 Resumen de magnitud y gravedad de consecuencias", value=True)
        st.checkbox("4.4 Recomendaciones para limitar consecuencias en OT", value=True)

        st.text_input("Nombre del archivo shapefile/geodatabase", value="isocontornos_instalacion_xx.shp")
        st.text_input("Nombre del Informe", value="Informe_de_Seguridad_Instalacion_Clasificada_2025")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.button("Generar borrador de Informe (PDF/Word)")
        with col2:
            st.button("Preparar paquete para cargue en herramienta Mintrabajo")

# -----------------------------------------------------------------------------
# PANTALLA 4 – BARRERAS Y ACCIONES
# -----------------------------------------------------------------------------

def pantalla_barreras_acciones():
    ui_header()

    st.subheader("🛡️ Gestión de Barreras Críticas y Acciones")

    df_salud = dummy_salud_barreras()
    df_acc = dummy_acciones()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Salud de Barreras (global)")
        chart_barreras = (
            alt.Chart(df_salud)
            .mark_arc()
            .encode(
                theta="Cantidad",
                color="Estado",
                tooltip=["Estado", "Cantidad"],
            )
        )
        st.altair_chart(chart_barreras, use_container_width=True)
        st.caption("Verde: disponible – Amarillo: degradada – Rojo: no disponible")

    with col2:
        st.markdown("### Acciones priorizadas por criticidad")
        st.dataframe(df_acc, use_container_width=True, hide_index=True)

    st.divider()
    st.button("Exportar resumen para auditoría PPAM/PSM")

# -----------------------------------------------------------------------------
# PANTALLA 5 – PEC + EMERGENCIAS + PGRDEPP
# -----------------------------------------------------------------------------

def pantalla_pec():
    ui_header()

    st.subheader("🚨 PEC, Emergencias y PGRDEPP")
    st.caption("Estructura alineada con Decreto 2157, 1868 y Resolución 3687 de 2025.")

    tabs = st.tabs(["Plan Estratégico", "Plan Operativo", "Plan de Recuperación", "Simulacros"])

    with tabs[0]:
        st.markdown("### Plan Estratégico de Emergencias")
        st.text_area(
            "Descripción estratégica",
            value=(
                "Define el marco general de actuación ante accidentes mayores de proceso, "
                "roles de alta dirección, relación con el PGRDEPP y coordinación institucional."
            ),
            height=200
        )

    with tabs[1]:
        st.markdown("### Plan Operativo de Respuesta")
        st.text_area(
            "Procedimientos operativos",
            value=(
                "Procedimientos específicos para derrames, incendios, explosiones y liberaciones tóxicas, "
                "incluyendo activación de alarmas, rutas de evacuación, puntos de encuentro y comunicación "
                "con autoridades."
            ),
            height=200
        )

    with tabs[2]:
        st.markdown("### Plan de Recuperación")
        st.text_area(
            "Estrategia de recuperación",
            value=(
                "Definición de acciones de recuperación técnica, ambiental, social y de negocio después "
                "de un accidente mayor, coordinación con planes de continuidad y gestión de crisis."
            ),
            height=200
        )

    with tabs[3]:
        st.markdown("### Simulacros y ejercicios")
        df_sim = dummy_simulacros()
        st.dataframe(df_sim, use_container_width=True, hide_index=True)
        st.button("Registrar nuevo simulacro")

    st.divider()
    st.button("Marcar PEC como actualizado para Informe de Seguridad")

# -----------------------------------------------------------------------------
# PANTALLA 6 – COPILOTO DE ANÁLISIS DE RIESGO (IA)
# -----------------------------------------------------------------------------

def pantalla_copiloto_riesgos():
    ui_header()

    st.subheader("🤖 Copiloto de Análisis de Riesgo de Proceso")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Configuración del estudio")
        tipo_estudio = st.radio(
            "Tipo de estudio",
            ["HAZOP", "LOPA", "What-If", "BowTie", "QRA", "Checklist PPAM"],
            index=0
        )
        instalacion = st.selectbox(
            "Instalación / Unidad",
            ["Estación Jobo", "Tanque TK-17", "Línea G7", "Reactor R-4"]
        )
        st.text_input("Objetivo del estudio", value="Evaluar escenarios de sobrepresión y fugas tóxicas")

    with col2:
        st.markdown("### Pre-estudio sugerido por IA (mockup)")
        st.code(
f"""
Estudio: {tipo_estudio} – {instalacion}

Nodos sugeridos:
  - Nodo 1: Entrada de la línea principal
  - Nodo 2: Tanque intermedio
  - Nodo 3: Descarga a antorcha

Desviaciones iniciales:
  - No flujo
  - Más flujo
  - Menos presión
  - Más temperatura
  - Fuga a atmósfera

Causas típicas (IA):
  - Obstrucción parcial de válvula
  - Falla de sello mecánico
  - Error de setpoint en controlador
  - Sobrellenado por fallo en lazo de nivel

Salvaguardas existentes:
  - Válvula de alivio PSV-14
  - Sistema de parada de emergencia (ESD)
  - Detección de gas inflamable y tóxico
  - Dique de contención en TK-17

Historial asociado:
  - 2 eventos menores (Tier 3) en últimos 3 años
  - 1 recomendación HAZOP pendiente de cierre
""",
            language="markdown",
        )

    st.markdown("### Durante el estudio – Sugerencias en vivo")
    st.info(
        "💡 *IA SKUDO*: En el HAZOP de 2021 en la Estación Jobo se documentó una causa similar "
        "con sobrellenado del tanque. ¿Deseas importar las causas y salvaguardas asociadas?"
    )

    st.markdown("### Publicación del estudio")
    st.button("Publicar estudio y generar acciones, barreras, evidencias y anexos Res. 3687")

# -----------------------------------------------------------------------------
# PANTALLA 7 – COPILOTO OPERACIONAL (CHAT)
# -----------------------------------------------------------------------------

def pantalla_copiloto_operacional():
    ui_header()
    st.subheader("💬 Copiloto Operacional de Seguridad de Procesos")

    st.caption("En producción aquí se conecta el LLM entrenado con documentos del cliente, CCPS, PPAM, etc.")

    pregunta = st.text_input(
        "Tu pregunta",
        value="¿Qué barreras críticas están vencidas esta semana?"
    )

    if st.button("Consultar IA SKUDO"):
        st.markdown("**Respuesta simulada (mockup):**")
        st.info(
            "Se identifican 3 barreras críticas vencidas esta semana:\n"
            "- PSV-14 en Estación Jobo (12 días vencida).\n"
            "- Detector de gas tóxico G7-03 fuera de servicio.\n"
            "- Sistema de rociadores en TK-17 en mantenimiento prolongado.\n\n"
            "Recomendación: coordinar con mantenimiento para cierre inmediato de OT "
            "y evaluar necesidad de paro preventivo en Estación Jobo."
        )

# -----------------------------------------------------------------------------
# PANTALLA 8 – ADMIN / CONFIGURACIÓN
# -----------------------------------------------------------------------------

def pantalla_admin():
    ui_header()
    st.subheader("⚙️ Administración y Configuración SKUDO")

    tabs = st.tabs([
        "Organización y roles",
        "Matriz PSM/PPAM por cargo",
        "KPIs corporativos",
        "Integraciones",
        "Geoespacial y regulatorio",
    ])

    with tabs[0]:
        st.markdown("### Organización y roles")
        st.text_area(
            "Estructura organizacional",
            value="Gerente General > Gerente HSSE > Jefes de Planta > Ingenieros de Proceso > Operadores",
            height=120
        )

    with tabs[1]:
        st.markdown("### Matriz PSM/PPAM por cargo (simplificada)")
        df_mat = pd.DataFrame({
            "Cargo": ["Gerente HSSE", "Jefe de Planta", "Ingeniero de Proceso", "Operador"],
            "Elementos_PSM_clave": [
                "Gobernanza, KPIs, Gestión de Riesgos",
                "Integridad, Operación, Contratistas",
                "Riesgos, MoC, Integridad",
                "Disciplina operativa, Procedimientos",
            ],
        })
        st.dataframe(df_mat, use_container_width=True, hide_index=True)

    with tabs[2]:
        st.markdown("### KPIs corporativos de PSM")
        st.text_area(
            "Lista de KPIs",
            value=(
                "- Tasa Tier 1 / MM h\n"
                "- Tasa Tier 2 / MM h\n"
                "- % barreras críticas disponibles\n"
                "- % cierre de recomendaciones HAZOP/LOPA\n"
                "- Índice de madurez PSM\n"
                "- Índice de cultura de seguridad\n"
            ),
            height=150
        )

    with tabs[3]:
        st.markdown("### Integraciones (ERP/CMMS/SCADA)")
        st.checkbox("SAP / ERP", value=True)
        st.checkbox("Maximo / CMMS", value=False)
        st.checkbox("PI / Historiador de procesos", value=False)
        st.checkbox("Herramienta SIG (QGIS/ArcGIS)", value=True)

    with tabs[4]:
        st.markdown("### Datos geoespaciales y parámetros regulatorios")
        st.text_input("Sistema de referencia geodésico oficial", value="MAGNA-SIRGAS / EPSG:3116")
        st.number_input("Periodo de actualización del Informe de Seguridad (años)", min_value=1, max_value=10, value=5)
        st.number_input("Ventana para instalaciones existentes (años)", min_value=1, max_value=5, value=2)
        st.caption("Parámetros alineados con Decreto 1347 de 2021 y Resolución 3687 de 2025.")

# -----------------------------------------------------------------------------
# APP PRINCIPAL
# -----------------------------------------------------------------------------

def main():
    st.sidebar.title("Navegación SKUDO")
    opcion = st.sidebar.radio(
        "Ir a:",
        [
            "1. Tablero Ejecutivo",
            "2. Diagnóstico SKUDO",
            "3. Informe de Seguridad (Res. 3687)",
            "4. Barreras y Acciones",
            "5. PEC y Emergencias",
            "6. Copiloto Análisis de Riesgo",
            "7. Copiloto Operacional",
            "8. Admin / Configuración",
        ]
    )

    if opcion == "1. Tablero Ejecutivo":
        pantalla_tablero_ejecutivo()
    elif opcion == "2. Diagnóstico SKUDO":
        pantalla_diagnostico()
    elif opcion == "3. Informe de Seguridad (Res. 3687)":
        pantalla_informe_seguridad()
    elif opcion == "4. Barreras y Acciones":
        pantalla_barreras_acciones()
    elif opcion == "5. PEC y Emergencias":
        pantalla_pec()
    elif opcion == "6. Copiloto Análisis de Riesgo":
        pantalla_copiloto_riesgos()
    elif opcion == "7. Copiloto Operacional":
        pantalla_copiloto_operacional()
    elif opcion == "8. Admin / Configuración":
        pantalla_admin()


if __name__ == "__main__":
    main()
