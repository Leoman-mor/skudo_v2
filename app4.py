# skudo_con_ia.py
# ----------------------------------------------------------------------
# SKUDO – Soluquim IA Suite
# Mockup consolidado + agentes de IA:
#  - Agente Guía (navegación y decisiones)
#  - Agente Informe 3687 (redacción del informe usando datos consolidados)
# ----------------------------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# ----------------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="SKUDO – Soluquim IA Suite",
    layout="wide",
)

st.markdown(
    """
    <style>
    .skudo-title { font-size: 26px; font-weight: 700; margin-bottom: 0.2rem; }
    .skudo-subtitle { font-size: 14px; color: #666; margin-bottom: 0.5rem; }
    .metric-card {
        padding: 0.75rem;
        border-radius: 0.75rem;
        border: 1px solid #e5e5e5;
        background-color: #fafafa;
        margin-bottom: 0.5rem;
    }
    .section-box {
        padding: 0.75rem 1rem;
        border-radius: 0.75rem;
        border: 1px solid #e5e5e5;
        background-color: #fcfcfc;
        margin-bottom: 0.5rem;
    }
    .agent-box {
        padding: 0.75rem 1rem;
        border-radius: 0.75rem;
        border: 1px solid #d0e3ff;
        background-color: #f3f7ff;
        margin-top: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# DATOS DUMMY – MODELO CONSOLIDADO
# ----------------------------------------------------------------------

def load_instalaciones():
    """
    Modelo mínimo de instalación:
      - ID, nombre, lat/lon
      - indicadores de riesgo, PSM, cultura
      - estado PEC, shapefile, acciones, barreras, eventos
    """
    data = [
        {
            "id": 1,
            "nombre": "Estación Jobo",
            "lat": 8.75, "lon": -75.15,
            "riesgo_global": "Alto",
            "indice_psm": 2.8,
            "indice_cultura": 58,
            "pec_actualizado": True,
            "tiene_shp": True,
            "acciones_abiertas": 10,
            "barreras_rojas": 3,
            "tier1_ytd": 0,
            "tier2_ytd": 2,
        },
        {
            "id": 2,
            "nombre": "Tanque TK-17",
            "lat": 7.90, "lon": -72.50,
            "riesgo_global": "Medio",
            "indice_psm": 2.4,
            "indice_cultura": 52,
            "pec_actualizado": False,
            "tiene_shp": False,
            "acciones_abiertas": 7,
            "barreras_rojas": 1,
            "tier1_ytd": 1,
            "tier2_ytd": 1,
        },
        {
            "id": 3,
            "nombre": "Línea G7",
            "lat": 4.65, "lon": -74.10,
            "riesgo_global": "Alto",
            "indice_psm": 2.2,
            "indice_cultura": 49,
            "pec_actualizado": True,
            "tiene_shp": False,
            "acciones_abiertas": 12,
            "barreras_rojas": 2,
            "tier1_ytd": 0,
            "tier2_ytd": 3,
        },
        {
            "id": 4,
            "nombre": "Reactor R-4",
            "lat": 10.40, "lon": -75.50,
            "riesgo_global": "Medio",
            "indice_psm": 2.6,
            "indice_cultura": 56,
            "pec_actualizado": True,
            "tiene_shp": True,
            "acciones_abiertas": 5,
            "barreras_rojas": 0,
            "tier1_ytd": 0,
            "tier2_ytd": 0,
        },
    ]
    return pd.DataFrame(data)


def load_diagnostico_base():
    """Plantilla de diagnóstico PSM/PPAM (se ajusta levemente por instalación)."""
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
    puntajes_base = [55, 50, 60, 65, 58, 52, 62, 57, 59, 61]
    return pd.DataFrame({"Elemento": elementos, "Puntaje_base": puntajes_base})


def get_diagnostico_for_instalacion(inst_id: int, base_df: pd.DataFrame) -> pd.DataFrame:
    """Simula ligeras variaciones por instalación."""
    np.random.seed(inst_id)
    variacion = np.random.randint(-10, 10, size=base_df.shape[0])
    df = base_df.copy()
    df["Puntaje"] = (df["Puntaje_base"] + variacion).clip(30, 95)
    return df[["Elemento", "Puntaje"]]


def get_cultura_for_instalacion(indice_cultura: int) -> pd.DataFrame:
    """Construye un mini perfil de cultura a partir del índice global."""
    base = indice_cultura
    dims = [
        "Percepción del riesgo",
        "Disciplina operativa",
        "Confianza en reportes",
        "Liderazgo visible",
        "Aprendizaje organizacional",
    ]
    np.random.seed(indice_cultura)
    variacion = np.random.randint(-15, 15, size=len(dims))
    puntajes = (base + variacion).clip(30, 95)
    return pd.DataFrame({"Dimensión": dims, "Puntaje": puntajes})


def get_acciones_for_instalacion(inst_id: int, nombre: str) -> pd.DataFrame:
    """Acciones abiertas por instalación (dummy)."""
    np.random.seed(inst_id + 10)
    n = 3 + np.random.randint(0, 4)
    crits = ["Crítica", "Alta", "Media"]
    estados = ["Abierta", "En curso", "Planificada"]
    data = []
    for i in range(n):
        data.append({
            "Id": f"{inst_id}-{i+1}",
            "Instalación": nombre,
            "Descripción": f"Acción {i+1} para {nombre}",
            "Criticidad": crits[i % len(crits)],
            "Días_vencida": int(np.random.randint(0, 20)),
            "Estado": estados[i % len(estados)],
        })
    return pd.DataFrame(data)

# ----------------------------------------------------------------------
# AGENTES IA (MOCKS)
# Aquí es donde luego enchufas tu LLM (OpenAI, etc.)
# ----------------------------------------------------------------------

def agente_guia_respuesta(vista: str, instalacion: str, objetivo: str, pregunta: str, df_inst: pd.DataFrame) -> str:
    """
    Simula un agente guía que:
      - lee la vista actual
      - mira la instalación seleccionada
      - entiende el objetivo
      - contesta con próximos pasos prácticos
    En producción, aquí iría una llamada a la API de IA con un prompt bien armado.
    """
    if vista == "Corporativo":
        foco = "en toda la compañía"
    else:
        foco = f"en la instalación {instalacion}"

    base = f"Estás en la vista **{vista}**, trabajando {foco}. "

    if "priorizar" in objetivo.lower():
        return (
            base
            + "Para priorizar intervenciones:\n"
              "1) Revisa en el tablero las instalaciones con riesgo 'Alto' y más barreras rojas.\n"
              "2) Entra al diagnóstico de esa instalación y ubica los elementos PSM más débiles.\n"
              "3) Desde allí, selecciona las acciones 'Críticas' y 'Altas' para construir el plan trimestral.\n"
              "4) Finalmente, genera el borrador del Informe 3687 para asegurar que las brechas queden registradas."
        )
    if "auditor" in objetivo.lower() or "auditoría" in objetivo.lower():
        return (
            base
            + "Para preparar una auditoría PPAM/PSM:\n"
              "1) Usa la vista de Diagnóstico para exportar el resumen de madurez y cultura.\n"
              "2) Descarga el listado de acciones abiertas y barreras en rojo.\n"
              "3) En la vista del Informe 3687, valida que los capítulos de conocimiento del riesgo, "
              "reducción del riesgo y PEC estén completos.\n"
              "4) Documenta qué evidencias (documentos, registros, simulacros) ya están cargadas en SKUDO "
              "y cuáles faltan por anexar en el repositorio documental."
        )
    if "informe" in objetivo.lower():
        return (
            base
            + "Para generar el Informe de Seguridad:\n"
              "1) Asegúrate de tener seleccionada la instalación correcta.\n"
              "2) Revisa el diagnóstico para confirmar los elementos con menor puntaje y las acciones clave.\n"
              "3) Ve a la vista 'Informe 3687', valida las secciones 1 a 4 y deja marcadas solo las que tengas completas.\n"
              "4) Usa el botón 'Generar borrador' y luego ajusta el texto con información específica de procesos, "
              "sustancias y acuerdos con autoridades."
        )

    # Respuesta genérica si la pregunta no cae en ningún caso
    return (
        base
        + "Te puedo ayudar a navegar SKUDO. Por ejemplo: entra primero al tablero ejecutivo para ver "
          "dónde está el riesgo, luego abre el diagnóstico de la instalación más crítica y finalmente "
          "usa el generador del Informe 3687 para consolidar la información."
    )


def agente_informe_borrador(inst_row, df_diag, df_cultura, acciones_df) -> str:
    """
    Simula el agente que construye un texto de borrador de Informe 3687
    usando la info consolidada de la instalación.
    En producción, aquí se arma un prompt grande con tablas + contexto.
    """
    nombre = inst_row["nombre"]
    riesgo = inst_row["riesgo_global"]
    psm = inst_row["indice_psm"]
    cultura = inst_row["indice_cultura"]
    barr_rojas = inst_row["barreras_rojas"]
    pec = "actualizado" if inst_row["pec_actualizado"] else "pendiente de actualización"
    shp = "disponible" if inst_row["tiene_shp"] else "no disponible"

    elemento_mas_debil = df_diag.sort_values("Puntaje").iloc[0]["Elemento"]
    dim_cultura_mas_baja = df_cultura.sort_values("Puntaje").iloc[0]["Dimensión"]
    acciones_criticas = acciones_df[acciones_df["Criticidad"] == "Crítica"].shape[0]

    texto = f"""
INFORME DE SEGURIDAD – INSTALACIÓN {nombre}

1. RESUMEN EJECUTIVO
La instalación {nombre} se clasifica con un nivel de riesgo global **{riesgo}**. El sistema de gestión
de seguridad de procesos (PSM/PPAM) presenta una madurez estimada de **{psm:.1f}/5** y un índice de
cultura de seguridad del **{cultura} %**.

El elemento de gestión con menor desempeño es **{elemento_mas_debil}**, mientras que en aspectos
culturales la dimensión más débil corresponde a **{dim_cultura_mas_baja}**. Actualmente se
registran **{acciones_criticas}** acciones de criticidad 'Crítica' y un total de {barr_rojas}
barreras críticas en estado rojo.

2. CONOCIMIENTO DEL RIESGO
La identificación de peligros y la evaluación de riesgos se han realizado con metodologías reconocidas
como HAZOP, LOPA y QRA, siguiendo buenas prácticas de ingeniería para instalaciones clasificadas.
Se han definido los escenarios de accidente mayor conforme a la normativa vigente, y se dispone de
modelaciones de consecuencias que permiten estimar la magnitud y gravedad de los impactos
en personas, ambiente e infraestructura.

3. REDUCCIÓN DEL RIESGO
Las medidas de prevención y mitigación incluyen barreras instrumentadas, dispositivos de alivio,
diques de contención, sistemas de detección y procedimientos operativos. La presencia de {barr_rojas}
barreras críticas en rojo indica la necesidad de reforzar la gestión de integridad y la disciplina
operativa, priorizando las acciones asociadas a dichas barreras.

4. MANEJO DEL DESASTRE (PEC)
El Plan de Emergencia y Contingencia (PEC) para {nombre} se encuentra {pec}. Este plan integra
la estructura de mando, los procedimientos de respuesta ante los principales escenarios de accidente
mayor y la estrategia de recuperación posterior al evento, en articulación con el PGRDEPP y los
planes de continuidad del negocio.

5. INFORMACIÓN PARA ORDENAMIENTO TERRITORIAL
La información geoespacial de los isocontornos de riesgo individual global se encuentra {shp}.
Cuando la geodatabase está disponible, se remite a las autoridades territoriales competentes para
apoyar los procesos de ordenamiento y planificación del uso del suelo, proponiendo restricciones
y recomendaciones que limiten la exposición de la población y la infraestructura crítica.

6. PLAN DE MEJORA
Con base en el diagnóstico, se prioriza el fortalecimiento del elemento **{elemento_mas_debil}** y
de la dimensión cultural **{dim_cultura_mas_baja}**, así como el cierre oportuno de las acciones
críticas y la recuperación de las barreras en estado rojo. Estas acciones se integran al plan de
trabajo anual de PSM/PPAM y serán objeto de seguimiento en los próximos ciclos de revisión.
""".strip()

    return texto

# ----------------------------------------------------------------------
# CABECERA COMPARTIDA
# ----------------------------------------------------------------------

def ui_header(df_instalaciones: pd.DataFrame):
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        st.markdown('<div class="skudo-title">🛡️ SKUDO – Soluquim IA Suite</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="skudo-subtitle">'
            'Memoria viva y copiloto de Seguridad de Procesos (PSM/PPAM) para instalaciones clasificadas.'
            '</div>',
            unsafe_allow_html=True,
        )
    with col2:
        rol = st.selectbox(
            "Rol",
            ["Gerente General", "Gerente HSSE", "Gerente de Planta", "Ingeniero de Proceso"],
        )
    with col3:
        st.caption(datetime.now().strftime("Fecha: %Y-%m-%d"))
        vista = st.selectbox("Vista", ["Corporativo", *df_instalaciones["nombre"].tolist()])
    st.divider()
    return rol, vista

# ----------------------------------------------------------------------
# VISIÓN 1 – TABLERO EJECUTIVO
# ----------------------------------------------------------------------

def pantalla_vision_ejecutiva(df_inst: pd.DataFrame, vista: str):
    st.subheader("1️⃣ Visión Ejecutiva Consolidada")

    tier1_total = df_inst["tier1_ytd"].sum()
    tier2_total = df_inst["tier2_ytd"].sum()
    barreras_rojas = df_inst["barreras_rojas"].sum()
    acciones_abiertas = df_inst["acciones_abiertas"].sum()
    madurez_media = df_inst["indice_psm"].mean()
    cultura_media = df_inst["indice_cultura"].mean()

    colk1, colk2, colk3, colk4, colk5, colk6 = st.columns(6)
    with colk1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Eventos Tier 1 – YTD", int(tier1_total))
        st.markdown("</div>", unsafe_allow_html=True)
    with colk2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Eventos Tier 2 – YTD", int(tier2_total))
        st.markdown("</div>", unsafe_allow_html=True)
    with colk3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Barreras críticas en rojo", int(barreras_rojas))
        st.markdown("</div>", unsafe_allow_html=True)
    with colk4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Acciones abiertas", int(acciones_abiertas))
        st.markdown("</div>", unsafe_allow_html=True)
    with colk5:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Madurez PSM corporativa", f"{madurez_media:.1f} / 5")
        st.markdown("</div>", unsafe_allow_html=True)
    with colk6:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Índice de cultura PSM", f"{cultura_media:.0f} %")
        st.markdown("</div>", unsafe_allow_html=True)

    colmap, coldet = st.columns([2, 1])

    with colmap:
        st.markdown("#### Mapa geoespacial de instalaciones clasificadas")
        st.caption("Base para QRA, Informe 3687 y anexos de ordenamiento territorial.")
        st.map(df_inst[["lat", "lon"]], size=40)

        st.markdown("#### Riesgo por instalación (Tier 2 + barreras rojas)")
        df_chart = df_inst.copy()
        df_chart["Eventos_T2"] = df_chart["tier2_ytd"]
        df_chart["Barreras_Rojas"] = df_chart["barreras_rojas"]
        chart = (
            alt.Chart(df_chart)
            .mark_bar()
            .encode(
                x=alt.X("nombre", title="Instalación", sort=None),
                y=alt.Y("Eventos_T2", title="Eventos Tier 2"),
                color="riesgo_global",
                tooltip=["nombre", "riesgo_global", "Eventos_T2", "Barreras_Rojas"],
            )
        )
        st.altair_chart(chart, use_container_width=True)

    with coldet:
        if vista == "Corporativo":
            st.markdown("#### Sin selección: vista corporativa")
            st.info(
                "Selecciona una instalación en el selector de arriba para ver su ficha consolidada "
                "de riesgo, PSM, cultura, PEC e Informe 3687."
            )
        else:
            inst_row = df_inst[df_inst["nombre"] == vista].iloc[0]
            st.markdown(f"#### Ficha consolidada – {inst_row['nombre']}")

            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.markdown(f"**Riesgo global:** {inst_row['riesgo_global']}")
            st.markdown(f"**Índice PSM:** {inst_row['indice_psm']:.1f} / 5")
            st.markdown(f"**Índice cultura:** {inst_row['indice_cultura']} %")
            st.markdown(f"**Barreras críticas en rojo:** {inst_row['barreras_rojas']}")
            st.markdown(f"**Acciones abiertas:** {inst_row['acciones_abiertas']}")
            st.markdown(
                f"**PEC actualizado:** {'Sí ✅' if inst_row['pec_actualizado'] else 'No ❌'}"
            )
            st.markdown(
                f"**Shapefile/isocontornos OT:** {'Sí ✅' if inst_row['tiene_shp'] else 'No ❌'}"
            )
            st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    colb1, colb2 = st.columns(2)
    with colb1:
        st.button("Generar Insight Ejecutivo (IA)")
    with colb2:
        st.button("Ir al Informe 3687 de esta instalación")

# ----------------------------------------------------------------------
# VISIÓN 2 – DIAGNÓSTICO
# ----------------------------------------------------------------------

def pantalla_diagnostico(df_inst: pd.DataFrame, vista: str, df_diag_base: pd.DataFrame):
    st.subheader("2️⃣ Diagnóstico SKUDO – PSM/PPAM + Cultura")

    if vista == "Corporativo":
        st.info("Selecciona una instalación específica para ver su diagnóstico detallado.")
        return

    inst_row = df_inst[df_inst["nombre"] == vista].iloc[0]
    df_diag = get_diagnostico_for_instalacion(inst_row["id"], df_diag_base)
    df_cultura = get_cultura_for_instalacion(int(inst_row["indice_cultura"]))
    acciones_df = get_acciones_for_instalacion(inst_row["id"], inst_row["nombre"])

    coltop1, coltop2, coltop3 = st.columns(3)
    with coltop1:
        st.metric("Madurez PSM/PPAM", f"{inst_row['indice_psm']:.1f} / 5")
    with coltop2:
        st.metric("Índice de cultura PSM", f"{inst_row['indice_cultura']} %")
    with coltop3:
        st.metric("Acciones abiertas", int(inst_row["acciones_abiertas"]))

    tab1, tab2, tab3 = st.tabs(["Resumen ejecutivo", "Mapa de madurez", "Brechas y ruta"])

    with tab1:
        st.markdown(f"### Resumen ejecutivo – {inst_row['nombre']}")
        st.info(
            f"El sistema de seguridad de procesos de **{inst_row['nombre']}** presenta una "
            f"madurez técnica de aproximadamente {inst_row['indice_psm']:.1f}/5 y un índice "
            f"de cultura de {inst_row['indice_cultura']} %. "
            "Los elementos con menor puntaje se consideran brechas prioritarias para los próximos ciclos."
        )

    with tab2:
        st.markdown("### Mapa de madurez PSM/PPAM")
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

        st.markdown("### Perfil de cultura de seguridad de procesos")
        chart_cult = (
            alt.Chart(df_cultura)
            .mark_bar()
            .encode(
                x=alt.X("Dimensión", sort=None),
                y=alt.Y("Puntaje", scale=alt.Scale(domain=[0, 100])),
                tooltip=["Dimensión", "Puntaje"],
            )
        )
        st.altair_chart(chart_cult, use_container_width=True)

    with tab3:
        st.markdown("### Brechas críticas y acciones asociadas")
        st.dataframe(acciones_df, use_container_width=True, hide_index=True)

        st.markdown("### Ruta sugerida (mockup)")
        ruta = [
            "Q1: Integridad mecánica + revisión de barreras en rojo.",
            "Q2: Gestión de cambios + disciplina operativa (cultura).",
            "Q3: Actualizar escenarios Res. 1890 + QRA + shapefiles OT.",
            "Q4: Auditoría PPAM + cierre de brechas clave del Informe 3687.",
        ]
        for item in ruta:
            st.write(f"✅ {item}")

    st.divider()
    st.button("Exportar diagnóstico completo para esta instalación")

# ----------------------------------------------------------------------
# VISIÓN 3 – INFORME DE SEGURIDAD (RES. 3687) + AGENTE INFORME
# ----------------------------------------------------------------------

def pantalla_informe_3687(df_inst: pd.DataFrame, vista: str, df_diag_base: pd.DataFrame):
    st.subheader("3️⃣ Informe de Seguridad – Resolución 3687 de 2025")

    if vista == "Corporativo":
        st.info("Selecciona una instalación específica para ver su borrador de Informe de Seguridad.")
        return

    inst_row = df_inst[df_inst["nombre"] == vista].iloc[0]
    df_diag = get_diagnostico_for_instalacion(inst_row["id"], df_diag_base)
    df_cultura = get_cultura_for_instalacion(int(inst_row["indice_cultura"]))
    acciones_df = get_acciones_for_instalacion(inst_row["id"], inst_row["nombre"])

    st.markdown(f"### Borrador del Informe – {inst_row['nombre']}")

    tab1, tab2, tab3, tab4 = st.tabs([
        "1. Conocimiento del riesgo",
        "2. Reducción del riesgo",
        "3. Manejo del desastre (PEC)",
        "4. Anexos OT + Agente Informe",
    ])

    with tab1:
        st.markdown("#### 1. Proceso de conocimiento del riesgo")
        st.write(
            f"- Instalación: **{inst_row['nombre']}**\n"
            f"- Riesgo global: **{inst_row['riesgo_global']}**\n"
            "- Información de procesos y sustancias sustraída de Soluquim y estudios PHA/QRA.\n"
        )
        st.write(
            "- Inventario de sustancias peligrosas con HDS bajo SGA.\n"
            "- Contexto interno: madurez PSM/PPAM y cultura de seguridad.\n"
            "- Contexto externo: entorno, elementos expuestos y posibles efectos dominó.\n"
        )

    with tab2:
        st.markdown("#### 2. Proceso de reducción del riesgo")
        st.write(
            f"- Número de barreras críticas en rojo: **{inst_row['barreras_rojas']}**.\n"
            "- Medidas preventivas y mitigadoras documentadas en SKUDO.\n"
            "- Integración con sistemas de protección, detección y respuesta.\n"
        )

    with tab3:
        st.markdown("#### 3. Manejo del desastre – PEC")
        st.write(
            f"- Estado del PEC: **{'Actualizado' if inst_row['pec_actualizado'] else 'Pendiente de actualización'}**.\n"
            "- Incluye respuesta ante escenarios de accidente mayor y coordinación con autoridades.\n"
        )

    with tab4:
        st.markdown("#### 4. Anexos para ordenamiento territorial y Agente Informe")
        st.write(
            f"- Información geoespacial (isocontornos): **{'Disponible' if inst_row['tiene_shp'] else 'Pendiente'}**.\n"
            "- Se generarán shapefiles/geodatabase para remisión a autoridades territoriales.\n"
        )

        st.markdown("---")
        st.markdown("### 🧾 Agente Informe 3687 – Borrador automatizado")

        st.caption(
            "Este agente toma la información consolidada de la instalación (riesgo, PSM, cultura, "
            "acciones, PEC y geoespacial) y construye un borrador en lenguaje de informe."
        )

        if st.button("Pedir al agente que genere el borrador"):
            borrador = agente_informe_borrador(inst_row, df_diag, df_cultura, acciones_df)
            st.markdown('<div class="agent-box">', unsafe_allow_html=True)
            st.markdown("**Borrador generado por el agente (mockup):**")
            st.text_area("Texto del borrador", value=borrador, height=400)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        nombre_archivo = st.text_input(
            "Nombre del archivo de Informe",
            value=f"Informe_de_Seguridad_{inst_row['nombre'].replace(' ', '_')}_2025",
        )

        colb1, colb2 = st.columns(2)
        with colb1:
            st.button("Generar PDF/Word (mock)")
        with colb2:
            st.button("Preparar paquete para cargue en herramienta Mintrabajo")

# ----------------------------------------------------------------------
# AGENTE GUÍA (BARRA INFERIOR)
# ----------------------------------------------------------------------

def bloque_agente_guia(vista: str, df_inst: pd.DataFrame):
    st.markdown("---")
    with st.expander("🧭 Agente Guía – Necesito que SKUDO me oriente"):
        col1, col2 = st.columns([1, 2])
        with col1:
            objetivo = st.selectbox(
                "¿Cuál es tu objetivo?",
                [
                    "Quiero priorizar dónde intervenir",
                    "Estoy preparando una auditoría PPAM/PSM",
                    "Necesito generar el Informe 3687",
                    "Solo quiero entender qué mirar primero",
                ],
            )
        with col2:
            pregunta = st.text_input(
                "Pregunta al agente (opcional)",
                value="¿Cuál debería ser mi siguiente paso?",
            )

        if vista == "Corporativo":
            instalacion = "todas"
        else:
            instalacion = vista

        if st.button("Preguntar al agente guía"):
            respuesta = agente_guia_respuesta(vista, instalacion, objetivo, pregunta, df_inst)
            st.markdown('<div class="agent-box">', unsafe_allow_html=True)
            st.markdown(respuesta)
            st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# APP PRINCIPAL
# ----------------------------------------------------------------------

def main():
    df_inst = load_instalaciones()
    df_diag_base = load_diagnostico_base()

    st.sidebar.title("Navegación SKUDO")
    pagina = st.sidebar.radio(
        "Ir a:",
        [
            "1. Visión Ejecutiva",
            "2. Diagnóstico",
            "3. Informe de Seguridad (Res. 3687)",
        ],
    )

    rol, vista = ui_header(df_inst)

    if pagina == "1. Visión Ejecutiva":
        pantalla_vision_ejecutiva(df_inst, vista)
    elif pagina == "2. Diagnóstico":
        pantalla_diagnostico(df_inst, vista, df_diag_base)
    elif pagina == "3. Informe de Seguridad (Res. 3687)":
        pantalla_informe_3687(df_inst, vista, df_diag_base)

    # Agente Guía aparece en todas las vistas
    bloque_agente_guia(vista, df_inst)


if __name__ == "__main__":
    main()
