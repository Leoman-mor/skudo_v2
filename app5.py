import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

import matplotlib.pyplot as plt
import networkx as nx  # pip install networkx

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
IMG_DIR = BASE_DIR / "imagenes"


# =========================================================
# CONFIG GENERAL
# =========================================================
st.set_page_config(
    page_title="SKUDO – Soluquim",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# ESTILO PERSONALIZADO
# ---------------------------------------------------------
PRIMARY = "#005F73"
SECONDARY = "#0A9396"
ACCENT = "#EE9B00"
BG = "#F5F7FB"

st.markdown(
    f"""
    <style>
    .main {{
        background-color: {BG};
    }}
    .block-container {{
        padding-top: 3.5rem !important;   /* antes 0.5rem */
        padding-bottom: 2rem;
        max-width: 1400px;
    }}
    .hero-card {{
        background: radial-gradient(circle at top left, {SECONDARY} 0, {PRIMARY} 60%);
        color: white;
        border-radius: 1rem;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    }}
    .hero-title {{
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }}
    .hero-sub {{
        font-size: 0.95rem;
        opacity: 0.9;
        margin-bottom: 0.8rem;
    }}
    .badge-pill {{
        display: inline-block;
        background: rgba(255,255,255,0.18);
        border-radius: 999px;
        padding: 0.15rem 0.7rem;
        font-size: 0.75rem;
        margin-right: 0.25rem;
    }}
    .metric-card {{
        background-color: white;
        padding: 1rem 1.2rem;
        border-radius: 0.8rem;
        border: 1px solid #E3E7EF;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
    }}
    .metric-title {{
        font-size: 0.9rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.1rem;
    }}
    .metric-value {{
        font-size: 1.4rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.1rem;
    }}
    .metric-sub {{
        font-size: 0.75rem;
        color: #6B7280;
    }}
    .panel-card {{
        background-color: #FFFFFF;
        padding: 1.2rem 1.4rem;
        border-radius: 1rem;
        border: 1px solid #E3E7EF;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
        margin-bottom: 1.2rem;
    }}
    .panel-header {{
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 0.7rem;
    }}
    .panel-header-title {{
        font-size: 1.05rem;
        font-weight: 600;
        color: #111827;
    }}
    .panel-header-sub {{
        font-size: 0.8rem;
        color: #6B7280;
    }}
    .section-title {{
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
        color: #1F2933;
    }}
    .section-sub {{
        font-size: 0.8rem;
        color: #6B7280;
        margin-bottom: 0.5rem;
    }}
    .chip {{
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        font-size: 0.75rem;
        background-color: #E5E7EB;
        margin-right: 0.25rem;
        margin-bottom: 0.15rem;
    }}
    .agent-card {{
        background-color: white;
        border-radius: 0.8rem;
        border: 1px solid #E5E7EB;
        padding: 0.9rem 1rem;
        margin-bottom: 0.6rem;
    }}
    .agent-header {{
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.2rem;
    }}
    .agent-text {{
        font-size: 0.85rem;
        color: #374151;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# DATOS DUMMY (reemplazables por tus datos reales)
# =========================================================
def calificacion_to_score(calif: str) -> int:
    mapping = {
        "Muy bajo": 20,
        "Bajo": 40,
        "Medio": 60,
        "Alto": 80,
        "Muy alto": 95
    }
    return mapping.get(calif, 50)

def load_dummy_data():
    df_sites = pd.DataFrame([
        {
            "sitio": "Planta Mezclas Norte",
            "lat": 6.2518,
            "lon": -75.5636,
            "riesgo_global": "ALTO",
            "madurez_ccps": 58
        },
        {
            "sitio": "Terminal Almacenamiento Sur",
            "lat": 4.7110,
            "lon": -74.0721,
            "riesgo_global": "MEDIO",
            "madurez_ccps": 72
        },
        {
            "sitio": "Planta Reactores Oriente",
            "lat": 7.1193,
            "lon": -73.1227,
            "riesgo_global": "ALTO",
            "madurez_ccps": 63
        },
    ])

    elementos = [
        "Cultura de Seguridad de Procesos",
        "Gestión de riesgos de proceso",
        "Gestión de contratistas",
        "Gestión del cambio",
        "Integridad mecánica",
        "Preparación y respuesta a emergencias",
    ]
    pilares = ["Compromiso", "Comprender el riesgo", "Gestionar el riesgo", "Aprender"]
    sitios = df_sites["sitio"].tolist()

    np.random.seed(42)

    data_heat = []
    for el in elementos:
        for s in sitios:
            cal = np.random.randint(40, 90)
            data_heat.append({
                "Elemento": el,
                "Sitio": s,
                "Calificación": cal
            })
    df_heat = pd.DataFrame(data_heat)

    # Diagnóstico CCPS
    diag_rows = []
    califs = ["Muy bajo", "Bajo", "Medio", "Alto", "Muy alto"]
    for i in range(1, 40):
        diag_rows.append({
            "id": f"D-{i:03d}",
            "pilar": np.random.choice(pilares),
            "elemento": np.random.choice(elementos),
            "instalacion": np.random.choice(sitios),
            "descripcion": f"Ítem de evaluación CCPS #{i}",
            "calificacion": np.random.choice(califs, p=[0.1, 0.2, 0.3, 0.25, 0.15]),
            "evidencia": "Documento / Registros / Entrevistas",
            "estado_plan": np.random.choice(["Sin plan", "En diseño", "En ejecución", "Cerrado"])
        })
    df_diag = pd.DataFrame(diag_rows)

    # Nodos (escenarios / acciones / requisitos)
    df_nodos = pd.DataFrame([
        {
            "id": "N-001",
            "tipo": "Escenario de riesgo",
            "instalacion": "Planta Mezclas Norte",
            "unidad": "Reactor 1",
            "equipo": "R-101",
            "descripcion": "Fuga de solvente inflamable en área de carga y posible sobrepresión en R-101.",
            "riesgo": "ALTO",
            "pilar": "Gestionar el riesgo",
            "relacionados": "D-001 | A-003 | Req-3687-9"
        },
        {
            "id": "N-002",
            "tipo": "Acción / Plan",
            "instalacion": "Terminal Almacenamiento Sur",
            "unidad": "Tanques esféricos",
            "equipo": "TK-201-ESF",
            "descripcion": "Instalar sistema de detección de gas en tanques esféricos.",
            "riesgo": "ALTO",
            "pilar": "Prevenir",
            "relacionados": "N-001 | D-011"
        },
        {
            "id": "N-003",
            "tipo": "Requisito normativo",
            "instalacion": "Planta Reactores Oriente",
            "unidad": "Reactor 2",
            "equipo": "R-202",
            "descripcion": "Actualizar Informe de Seguridad según nueva revisión de la norma.",
            "riesgo": "MEDIO",
            "pilar": "Gestionar el riesgo",
            "relacionados": "D-020 | D-021"
        },
    ])

    # Estudios históricos (HAZOP, What-if, QRA, etc.)
    df_estudios = pd.DataFrame([
        {
            "id_estudio": "E-001",
            "tipo": "HAZOP",
            "anio": 2019,
            "instalacion": "Planta Mezclas Norte",
            "unidad": "Reactor 1",
            "equipo": "R-101",
            "cobertura": "Alta",
            "estado": "Vigente",
            "accion_sugerida": "Revalidar enfocado en escenarios de sobrepresión.",
            "comentario": "HAZOP de detalle para operación normal y arranque."
        },
        {
            "id_estudio": "E-002",
            "tipo": "LOPA",
            "anio": 2020,
            "instalacion": "Planta Mezclas Norte",
            "unidad": "Reactor 1",
            "equipo": "R-101",
            "cobertura": "Media",
            "estado": "Vigente",
            "accion_sugerida": "Revisar supuestos de frecuencias y fallas de PSV.",
            "comentario": "LOPA para escenarios de sobrepresión y fallo de SIS."
        },
        {
            "id_estudio": "E-003",
            "tipo": "What-if",
            "anio": 2017,
            "instalacion": "Terminal Almacenamiento Sur",
            "unidad": "Área de tanques",
            "equipo": "TK-201-ESF",
            "cobertura": "Baja",
            "estado": "Obsoleto",
            "accion_sugerida": "No repetir completo, documentar decisiones previas.",
            "comentario": "What-if de arranque inicial del terminal."
        },
        {
            "id_estudio": "E-004",
            "tipo": "QRA",
            "anio": 2021,
            "instalacion": "Planta Reactores Oriente",
            "unidad": "Complejo de reactores",
            "equipo": "",
            "cobertura": "Alta",
            "estado": "Vigente",
            "accion_sugerida": "Usar como base para ordenamiento territorial y PEC.",
            "comentario": "Análisis cuantitativo de riesgo para toda la planta."
        },
    ])

    return df_sites, df_heat, df_diag, df_nodos, df_estudios


df_sites, df_heat, df_diag, df_nodos, df_estudios = load_dummy_data()

# =========================================================
# ESTADO GLOBAL BÁSICO
# =========================================================
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Campos del informe que vamos a usar para el % de avance
INF_FIELDS = [
    "inf_1_desc_instalacion",
    "inf_1_contexto_ext",
    "inf_1_contexto_int",
    "inf_1_peligros",
    "inf_2_medidas_prev",
    "inf_2_proteccion_fin",
    "inf_3_manejo_desastre",
    "inf_4_ot",
    "inf_4_pec",
    "inf_4_adicional",
]

# Helpers para leer/guardar campos del informe
def get_inf(name: str) -> str:
    return str(st.session_state.get(name, ""))

def set_inf(name: str, value: str):
    st.session_state[name] = value

def build_resumen_elementos(df_diag_filtrado: pd.DataFrame) -> pd.DataFrame:
    """
    Construye un resumen por elemento similar al de tu screenshot:
    - Promedio (0–100) usando calificacion_to_score
    - Porcentaje aproximado de:
        Implementación completa        -> Muy alto
        Impl. parcial en toda la comp. -> Alto
        Impl. parcial en algunas pl.   -> Medio
        No implementado                -> Bajo + Muy bajo
        No aplica                      -> 0 (demo)
    """
    if df_diag_filtrado.empty:
        return pd.DataFrame(
            columns=[
                "Elemento",
                "Promedio",
                "Impl. completa",
                "Impl. parcial (toda)",
                "Impl. parcial (algunas)",
                "No implementado",
                "No aplica",
            ]
        )

    df = df_diag_filtrado.copy()
    df["score"] = df["calificacion"].apply(calificacion_to_score)

    resumen = []
    for elemento, grp in df.groupby("elemento"):
        total = len(grp)
        if total == 0:
            continue

        prom = grp["score"].mean()

        pct_muy_alto = 100 * (grp["calificacion"] == "Muy alto").sum() / total
        pct_alto = 100 * (grp["calificacion"] == "Alto").sum() / total
        pct_medio = 100 * (grp["calificacion"] == "Medio").sum() / total
        pct_bajo = 100 * (
            (grp["calificacion"] == "Bajo") | (grp["calificacion"] == "Muy bajo")
        ).sum() / total
        pct_no_aplica = 0.0  # demo, si tuvieras 'No aplica' real se calcula acá

        resumen.append(
            {
                "Elemento": elemento,
                "Promedio": round(prom, 2),
                "Impl. completa": round(pct_muy_alto, 2),
                "Impl. parcial (toda)": round(pct_alto, 2),
                "Impl. parcial (algunas)": round(pct_medio, 2),
                "No implementado": round(pct_bajo, 2),
                "No aplica": round(pct_no_aplica, 2),
            }
        )

    df_res = pd.DataFrame(resumen)
    df_res = df_res.sort_values("Promedio", ascending=False).reset_index(drop=True)
    return df_res


# =========================================================
# FUNCIONES DE APOYO
# =========================================================
def resumen_calificaciones(df_diag_filtrado: pd.DataFrame) -> pd.DataFrame:
    if df_diag_filtrado.empty:
        return pd.DataFrame(columns=["Calificación", "Cantidad"])
    return (
        df_diag_filtrado["calificacion"]
        .value_counts()
        .rename_axis("Calificación")
        .reset_index(name="Cantidad")
    )


def calcular_madurez_global(df_diag_filtrado: pd.DataFrame) -> float:
    if df_diag_filtrado.empty:
        return 0.0
    scores = df_diag_filtrado["calificacion"].apply(calificacion_to_score)
    return round(scores.mean(), 1)


def prioridades_desde_diag(df_diag_filtrado: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    if df_diag_filtrado.empty:
        return pd.DataFrame(columns=["Nodo / Tema", "Nivel", "Pilar", "Instalación", "Impacto", "Plazo sugerido"])
    df = df_diag_filtrado.copy()
    df["score"] = df["calificacion"].apply(calificacion_to_score)
    df = df.sort_values("score").head(top_n)  # más bajo = peor

    prioridades = []
    for _, row in df.iterrows():
        s = row["score"]
        if s <= 40:
            nivel = "Crítico"
            plazo = "0–3 meses"
            impacto = "Muy alto"
        elif s <= 60:
            nivel = "Importante"
            plazo = "3–6 meses"
            impacto = "Alto"
        else:
            nivel = "Mejorable"
            plazo = "6–12 meses"
            impacto = "Medio"
        prioridades.append({
            "Nodo / Tema": row["descripcion"],
            "Nivel": nivel,
            "Pilar": row["pilar"],
            "Instalación": row["instalacion"],
            "Impacto": impacto,
            "Plazo sugerido": plazo
        })
    return pd.DataFrame(prioridades)


def get_dummy_condiciones_para_estudio(id_estudio: str) -> pd.DataFrame:
    """
    DEMO: condiciones/escenarios, causas, consecuencias, salvaguardas y acciones
    asociadas a cada estudio.
    En producción esto vendría de tus PHA/HAZOP/LOPA reales.
    """
    base = [
        # Estudio E-001 – HAZOP Reactor 1
        {
            "id_estudio": "E-001",
            "id_condicion": "C-001",
            "condicion": "Sobrepresión en R-101 por bloqueo aguas abajo.",
            "causa": "Cierre inadvertido de válvula de salida / fallo del control de caudal.",
            "consecuencia": "Disparo de PSV, posible descarga a antorcha y liberación a la atmósfera.",
            "salvaguardas": "PSV en R-101, alarmas de alta presión, procedimiento de arranque.",
            "accion_sugerida": "Reforzar entrenamiento en arranque/parada y actualizar procedimiento operativo.",
            "tipo_accion": "General (procedimiento / entrenamiento)",
            "criticidad": "Alta",
            "estado_accion": "Pendiente"
        },
        {
            "id_estudio": "E-001",
            "id_condicion": "C-002",
            "condicion": "Sobrepresión en R-101 por reacción fuera de control.",
            "causa": "Sobredosis de reactivo / fallo de control de temperatura.",
            "consecuencia": "Liberación de energía, posible daño al reactor y fuga de producto.",
            "salvaguardas": "Control de temperatura, interlock de parada de alimentación.",
            "accion_sugerida": "Evaluar necesidad de interlock independiente de alta temperatura (SIS).",
            "tipo_accion": "Trabajo en equipo (diseño / inversión)",
            "criticidad": "Muy alta",
            "estado_accion": "En análisis"
        },
        {
            "id_estudio": "E-001",
            "id_condicion": "C-003",
            "condicion": "Pérdida de contención en bridas de R-101.",
            "causa": "Ajuste deficiente / corrosión.",
            "consecuencia": "Fuga de solvente inflamable al área de reactor.",
            "salvaguardas": "Programas de inspección, bandejas de contención, detectores de gas.",
            "accion_sugerida": "Reforzar programa de inspección visual y torqueado de bridas críticas.",
            "tipo_accion": "General (mantenimiento / rutina)",
            "criticidad": "Media",
            "estado_accion": "En ejecución"
        },

        # Estudio E-002 – LOPA PSV R-101
        {
            "id_estudio": "E-002",
            "id_condicion": "C-004",
            "condicion": "Demanda frecuente al PSV de R-101.",
            "causa": "Operación cercana al límite de capacidad / ajustes de control.",
            "consecuencia": "Desgaste acelerado del PSV y mayor probabilidad de fallo.",
            "salvaguardas": "PSV dimensionado, monitoreo de disparos.",
            "accion_sugerida": "Analizar datos históricos de disparos y optimizar puntos de operación.",
            "tipo_accion": "Trabajo en equipo (operación / proceso)",
            "criticidad": "Alta",
            "estado_accion": "Sin iniciar"
        },
        {
            "id_estudio": "E-002",
            "id_condicion": "C-005",
            "condicion": "PSV descargando hacia sistema de antorcha en mantenimiento.",
            "causa": "Mantenimiento simultáneo de antorcha y operación del reactor.",
            "consecuencia": "Riesgo de liberación directa a atmósfera.",
            "salvaguardas": "Procedimiento de bloqueo de operación durante mantenimiento de antorcha.",
            "accion_sugerida": "Reforzar cumplimiento del procedimiento y validación en permisos de trabajo.",
            "tipo_accion": "General (permisos de trabajo / coordinación)",
            "criticidad": "Alta",
            "estado_accion": "Pendiente"
        },

        # Estudio E-003 – What-if tanques
        {
            "id_estudio": "E-003",
            "id_condicion": "C-006",
            "condicion": "Sobrellenado de TK-201-ESF durante recepción.",
            "causa": "Fallo de medición de nivel / error de comunicación operador-bombero.",
            "consecuencia": "Derrame de producto inflamable en dique.",
            "salvaguardas": "Alarmas de alto nivel, procedimientos de recepción.",
            "accion_sugerida": "Estandarizar checklist de recepción y entrenamiento de contratistas.",
            "tipo_accion": "General (procedimiento / contratistas)",
            "criticidad": "Alta",
            "estado_accion": "Pendiente"
        },

        # Estudio E-004 – QRA planta reactores
        {
            "id_estudio": "E-004",
            "id_condicion": "C-007",
            "condicion": "Explosión en reactor con afectación a oficinas administrativas.",
            "causa": "Falla múltiple en sistemas de protección / ubicación de personas expuestas.",
            "consecuencia": "Daño estructural y afectación a personas en edificios cercanos.",
            "salvaguardas": "Diseño de reactor, barreras físicas, rutas de evacuación.",
            "accion_sugerida": "Revisar ubicación de oficinas y aplicar criterios de facility siting.",
            "tipo_accion": "Trabajo en equipo (layout / facility siting)",
            "criticidad": "Muy alta",
            "estado_accion": "Pendiente"
        },
    ]

    df = pd.DataFrame(base)
    df_sel = df[df["id_estudio"] == id_estudio].copy()
    return df_sel.reset_index(drop=True)


def clasificar_acciones_riesgos(df_condiciones: pd.DataFrame):
    """
    Clasifica acciones en:
    - Generales (estandarizables / de aplicación amplia)
    - Trabajo en equipo (requieren análisis conjunto, diseño, inversión, etc.)
    y arma un texto "tipo agente".
    """
    if df_condiciones.empty:
        return "[DEMO SKUDO] No hay condiciones cargadas para este estudio.", pd.DataFrame(), pd.DataFrame()

    df_gen = df_condiciones[df_condiciones["tipo_accion"].str.contains("General", case=False, na=False)].copy()
    df_team = df_condiciones[df_condiciones["tipo_accion"].str.contains("Trabajo en equipo", case=False, na=False)].copy()

    texto = "🔍 **[DEMO SKUDO] Análisis de acciones del estudio seleccionado**\n\n"

    texto += f"- Condiciones totales analizadas: **{len(df_condiciones)}**\n"
    texto += f"- Acciones típicas / generales: **{len(df_gen)}**\n"
    texto += f"- Acciones que requieren trabajo en equipo: **{len(df_team)}**\n\n"

    if not df_gen.empty:
        texto += "**Acciones generales que podrían estandarizarse (procedimientos, entrenamiento, mantenimiento):**\n"
        for _, r in df_gen.head(4).iterrows():
            texto += f"- {r['accion_sugerida']}  \n"
        texto += "\n"

    if not df_team.empty:
        texto += "**Acciones que conviene trabajar en equipo (proceso, operación, ingeniería, HSE):**\n"
        for _, r in df_team.head(4).iterrows():
            texto += f"- {r['accion_sugerida']}  \n"
        texto += "\n"

    texto += (
        "_En la versión completa, SKUDO agruparía automáticamente patrones de causas, "
        "consecuencias y acciones para proponer estándares corporativos y agendas de "
        "reunión de riesgo específicas._"
    )

    return texto, df_gen, df_team


def sugerir_estudio_y_estudios(contexto: dict, df_estudios_base: pd.DataFrame, df_nodos_base: pd.DataFrame):
    """
    Dado el contexto del problema (instalación, unidad, equipo, descripción, tipo_situacion, fase),
    sugiere el tipo de estudio y busca estudios/nodos relacionados (DEMO).
    """

    instalacion = contexto.get("instalacion", "Todas")
    unidad = (contexto.get("unidad") or "").strip()
    equipo = (contexto.get("equipo") or "").strip()
    tipo_situacion = contexto.get("tipo_situacion", "")
    fase = contexto.get("fase", "")
    desc = (contexto.get("descripcion") or "").strip()

    # -------------------------
    # 1) Selección de metodología (DEMO simple)
    # -------------------------
    if tipo_situacion == "Nuevo proyecto / diseño":
        if "conceptual" in fase.lower():
            metodo = "What-if + checklist"
            motivo = (
                "Estás en fase conceptual, donde un **What-if** ampliado ayuda a "
                "explorar escenarios sin entrar al nivel de detalle de un HAZOP completo."
            )
        else:
            metodo = "HAZOP completo"
            motivo = (
                "Para proyectos en detalle, un **HAZOP** completo es el estándar para "
                "identificar desviaciones sistemáticamente."
            )
    elif tipo_situacion == "Cambio (MOC)":
        metodo = "Revalidación de HAZOP / PHA focalizada"
        motivo = (
            "Para cambios, es más eficiente **revalidar el HAZOP/PHA existente** en los nodos "
            "impactados que iniciar un estudio desde cero."
        )
    elif tipo_situacion == "Problema recurrente / desviación operacional":
        metodo = "Revisión focalizada de HAZOP + What-if puntual"
        motivo = (
            "Un problema recurrente suele estar asociado a uno o pocos escenarios; conviene "
            "revisar el HAZOP previo y complementarlo con un **What-if** focalizado."
        )
    elif tipo_situacion == "Incidente / casi incidente":
        metodo = "Investigación de incidentes + actualización de HAZOP/PHA"
        motivo = (
            "Un incidente requiere una **investigación formal** y luego actualizar los estudios "
            "de riesgo para capturar las causas y salvaguardas."
        )
    else:
        metodo = "Revisión de estudios existentes y definición de alcance"
        motivo = (
            "Primero es clave revisar qué estudios históricos existen y su alcance antes de "
            "definir una metodología nueva."
        )

    # -------------------------
    # 2) Búsqueda de estudios relacionados (DEMO)
    # -------------------------
    df_est = df_estudios_base.copy()

    # Filtros suaves por instalación, unidad, equipo
    mask = pd.Series(True, index=df_est.index)
    if instalacion != "Todas":
        mask &= df_est["instalacion"] == instalacion

    if unidad:
        mask &= df_est["unidad"].str.contains(unidad, case=False, na=False)

    if equipo:
        mask &= df_est["equipo"].str.contains(equipo, case=False, na=False)

    df_rel = df_est[mask].copy()

    # Si no encuentra nada, mostrar algunos de la instalación o generales
    if df_rel.empty:
        if instalacion != "Todas":
            df_rel = df_est[df_est["instalacion"] == instalacion].copy()
        if df_rel.empty:
            df_rel = df_est.copy()
        df_rel = df_rel.head(3)

    # -------------------------
    # 3) Búsqueda de nodos relacionados (DEMO)
    # -------------------------
    df_n = df_nodos_base.copy()
    mask_n = pd.Series(True, index=df_n.index)

    if instalacion != "Todas":
        mask_n &= df_n["instalacion"] == instalacion

    desc_lower = desc.lower()
    unidad_lower = unidad.lower()
    equipo_lower = equipo.lower()

    def es_relacionado(row):
        texto = str(row["descripcion"]).lower()
        score = 0
        if equipo_lower and equipo_lower in texto:
            score += 2
        if unidad_lower and unidad_lower in texto:
            score += 1
        # Palabras clave de la descripción larga
        for palabra in desc_lower.split():
            if len(palabra) >= 5 and palabra in texto:
                score += 1
        return score >= 2  # umbral simple para DEMO

    if desc or unidad or equipo:
        rel_mask = df_n.apply(es_relacionado, axis=1)
        mask_n &= rel_mask

    df_n_rel = df_n[mask_n].copy()
    if df_n_rel.empty:
        df_n_rel = df_n.head(3).copy()

    nodos_rel_ids = df_n_rel["id"].tolist()

    # -------------------------
    # 4) Texto tipo "agente" (DEMO)
    # -------------------------
    texto = f"""
[DEMO SKUDO] Para el problema descrito, la metodología sugerida es:

- **{metodo}**

**¿Por qué?**  
{motivo}

He encontrado **{len(df_rel)} estudio(s)** histórico(s) potencialmente relevantes:

"""  # noqa: W291

    for _, r in df_rel.head(5).iterrows():
        texto += (
            f"- `{r['id_estudio']}` – {r['tipo']} ({r['anio']}) en **{r['instalacion']} – {r['unidad']}** "
            f"[Cobertura: {r['cobertura']}, Estado: {r['estado']}]  \n"
        )

    texto += (
        "\nEn la versión completa, SKUDO analizaría el contenido detallado de estos estudios "
        "para evitar repetir análisis y priorizar revalidaciones y acciones de mayor impacto."
    )

    return texto, df_rel, nodos_rel_ids


def get_dummy_riesgos_por_estudios(estudios_ids: list[str]) -> pd.DataFrame:
    """
    DEMO: Escenarios de riesgo de proceso consolidados por estudio.
    En producción esto vendría de tus hojas PHA/HAZOP/LOPA/QRA.
    """

    base = [
        # E-001 – HAZOP Reactor 1
        {
            "id_estudio": "E-001",
            "id_escenario": "RP-001",
            "instalacion": "Planta Mezclas Norte",
            "unidad": "Reactor 1",
            "equipo": "R-101",
            "descripcion_escenario": "Sobrepresión en R-101 por bloqueo aguas abajo.",
            "tipo_peligro": "Presión / Integridad mecánica",
            "fase_operativa": "Operación normal",
            "causa_principal": "Cierre inadvertido de válvula de salida o fallo del control de caudal.",
            "consecuencia_principal": "Disparo frecuente del PSV y posible descarga a antorcha / atmósfera.",
            "salvaguardas_clave": "PSV en R-101, alarmas de alta presión, procedimiento de operación.",
            "severidad": 4,
            "frecuencia": 3,
            "riesgo_residual": 12,
            "nivel_riesgo": "Alto",
            "accion_sugerida": "Reforzar entrenamiento en arranque/parada y actualizar procedimiento operativo.",
            "tipo_accion": "General",
            "clase_accion": "Procedimientos / Entrenamiento",
            "estado_accion": "Pendiente"
        },
        {
            "id_estudio": "E-001",
            "id_escenario": "RP-002",
            "instalacion": "Planta Mezclas Norte",
            "unidad": "Reactor 1",
            "equipo": "R-101",
            "descripcion_escenario": "Reacción fuera de control en R-101 con aumento de presión y temperatura.",
            "tipo_peligro": "Reacción fuera de control",
            "fase_operativa": "Operación / Upset",
            "causa_principal": "Sobredosis de reactivo o fallo del control de temperatura.",
            "consecuencia_principal": "Liberación de energía, posible fallo de contención y fuga de producto.",
            "salvaguardas_clave": "Control de temperatura, interlock de parada de alimentación, PSV.",
            "severidad": 5,
            "frecuencia": 2,
            "riesgo_residual": 10,
            "nivel_riesgo": "Alto",
            "accion_sugerida": "Evaluar necesidad de interlock independiente de alta temperatura (SIS) y revisión de diseño.",
            "tipo_accion": "Trabajo en equipo",
            "clase_accion": "Ingeniería / Diseño / SIS",
            "estado_accion": "En análisis"
        },
        {
            "id_estudio": "E-001",
            "id_escenario": "RP-003",
            "instalacion": "Planta Mezclas Norte",
            "unidad": "Reactor 1",
            "equipo": "R-101 / Bridas",
            "descripcion_escenario": "Fuga en bridas de R-101 por corrosión o torque inadecuado.",
            "tipo_peligro": "Fuga inflamable",
            "fase_operativa": "Operación",
            "causa_principal": "Corrosión, malas prácticas de montaje, ausencia de torqueado controlado.",
            "consecuencia_principal": "Fuga de solvente inflamable en área de reactor.",
            "salvaguardas_clave": "Programa de inspección, detectores de gas, bandejas de contención.",
            "severidad": 3,
            "frecuencia": 3,
            "riesgo_residual": 9,
            "nivel_riesgo": "Medio",
            "accion_sugerida": "Reforzar programa de inspección y torqueado de bridas críticas.",
            "tipo_accion": "General",
            "clase_accion": "Mantenimiento / Integridad",
            "estado_accion": "En ejecución"
        },

        # E-002 – LOPA PSV R-101
        {
            "id_estudio": "E-002",
            "id_escenario": "RP-004",
            "instalacion": "Planta Mezclas Norte",
            "unidad": "Reactor 1",
            "equipo": "R-101 / PSV",
            "descripcion_escenario": "Demanda frecuente al PSV de R-101 por operación cerca del límite.",
            "tipo_peligro": "Sobrepresión / Operación",
            "fase_operativa": "Operación",
            "causa_principal": "Ajustes de control y estrategia de operación cercana al máximo caudal.",
            "consecuencia_principal": "Desgaste acelerado del PSV y mayor probabilidad de fallo en demanda.",
            "salvaguardas_clave": "PSV dimensionado, monitoreo de disparos, alarmas de alta presión.",
            "severidad": 3,
            "frecuencia": 4,
            "riesgo_residual": 12,
            "nivel_riesgo": "Alto",
            "accion_sugerida": "Analizar datos históricos de disparos y optimizar puntos de operación junto con operación y proceso.",
            "tipo_accion": "Trabajo en equipo",
            "clase_accion": "Operación / Optimización",
            "estado_accion": "Sin iniciar"
        },
        {
            "id_estudio": "E-002",
            "id_escenario": "RP-005",
            "instalacion": "Planta Mezclas Norte",
            "unidad": "Reactor 1 / Antorcha",
            "equipo": "Sistema de descarga",
            "descripcion_escenario": "PSV descargando hacia antorcha cuando esta está en mantenimiento.",
            "tipo_peligro": "Descarga / Gestión de cambios",
            "fase_operativa": "Mantenimiento",
            "causa_principal": "Mantenimiento simultáneo de antorcha con operación del reactor.",
            "consecuencia_principal": "Riesgo de liberación directa a atmósfera.",
            "salvaguardas_clave": "Procedimiento de bloqueo de operación durante mantenimiento de antorcha.",
            "severidad": 4,
            "frecuencia": 2,
            "riesgo_residual": 8,
            "nivel_riesgo": "Medio",
            "accion_sugerida": "Reforzar cumplimiento del procedimiento en permisos de trabajo y coordinaciones de mantenimiento.",
            "tipo_accion": "General",
            "clase_accion": "Permisos de trabajo / Coordinación",
            "estado_accion": "Pendiente"
        },

        # E-003 – What-if tanques
        {
            "id_estudio": "E-003",
            "id_escenario": "RP-006",
            "instalacion": "Terminal Almacenamiento Sur",
            "unidad": "Área de tanques",
            "equipo": "TK-201-ESF",
            "descripcion_escenario": "Sobrellenado de TK-201-ESF durante recepción de producto.",
            "tipo_peligro": "Sobrellenado / Derrame",
            "fase_operativa": "Operación / Recepción",
            "causa_principal": "Fallo de medición de nivel o error de comunicación operador–contratista.",
            "consecuencia_principal": "Derrame de producto inflamable en dique.",
            "salvaguardas_clave": "Alarmas de alto nivel, procedimientos de recepción, diques de contención.",
            "severidad": 4,
            "frecuencia": 3,
            "riesgo_residual": 12,
            "nivel_riesgo": "Alto",
            "accion_sugerida": "Estandarizar checklist de recepción y entrenamiento de contratistas.",
            "tipo_accion": "General",
            "clase_accion": "Contratistas / Procedimientos",
            "estado_accion": "Pendiente"
        },

        # E-004 – QRA planta reactores
        {
            "id_estudio": "E-004",
            "id_escenario": "RP-007",
            "instalacion": "Planta Reactores Oriente",
            "unidad": "Complejo de reactores",
            "equipo": "Reactores / Edificios",
            "descripcion_escenario": "Explosión en reactor con afectación a oficinas administrativas cercanas.",
            "tipo_peligro": "Explosión / Ubicación de personas",
            "fase_operativa": "Operación",
            "causa_principal": "Falla múltiple en sistemas de protección y ubicación de personal en zona de afectación.",
            "consecuencia_principal": "Daño estructural y afectación a personas en edificios cercanos.",
            "salvaguardas_clave": "Diseño de reactor, barreras físicas, rutas de evacuación, PEC.",
            "severidad": 5,
            "frecuencia": 2,
            "riesgo_residual": 10,
            "nivel_riesgo": "Alto",
            "accion_sugerida": "Revisar ubicación de oficinas (facility siting) y definir medidas de relocalización o refuerzo.",
            "tipo_accion": "Trabajo en equipo",
            "clase_accion": "Layout / Facility siting",
            "estado_accion": "Pendiente"
        },
    ]

    df = pd.DataFrame(base)
    if estudios_ids:
        df = df[df["id_estudio"].isin(estudios_ids)]
    return df.reset_index(drop=True)


def resumir_riesgos_y_acciones(df_rp: pd.DataFrame) -> dict:
    """
    Calcula métricas generales para la vista de análisis de riesgos de procesos.
    """
    if df_rp.empty:
        return {
            "n_escenarios": 0,
            "n_generales": 0,
            "n_equipo": 0,
            "prom_riesgo_residual": 0.0,
            "top_peligros": [],
        }

    n_escenarios = len(df_rp)
    n_generales = int((df_rp["tipo_accion"] == "General").sum())
    n_equipo = int((df_rp["tipo_accion"] == "Trabajo en equipo").sum())
    prom_riesgo = round(df_rp["riesgo_residual"].mean(), 1)

    top_peligros = (
        df_rp["tipo_peligro"]
        .value_counts()
        .head(3)
        .index
        .tolist()
    )

    return {
        "n_escenarios": n_escenarios,
        "n_generales": n_generales,
        "n_equipo": n_equipo,
        "prom_riesgo_residual": prom_riesgo,
        "top_peligros": top_peligros,
    }


def agrupar_acciones_generales(df_rp: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa acciones generales por clase/tema para ver patrones que se pueden
    convertir en estándares corporativos.
    """
    df_gen = df_rp[df_rp["tipo_accion"] == "General"].copy()
    if df_gen.empty:
        return pd.DataFrame()

    df_gen["tema_accion"] = df_gen["clase_accion"]
    resumen = (
        df_gen.groupby("tema_accion")
        .agg(
            n_acciones=("accion_sugerida", "count"),
            ejemplos=("accion_sugerida", lambda x: " | ".join(x.head(3)))
        )
        .reset_index()
        .sort_values("n_acciones", ascending=False)
    )
    return resumen


def clasificar_acciones_rp_agente(df_rp: pd.DataFrame) -> str:
    """
    Texto tipo agente que diferencia:
    - acciones generales,
    - acciones para trabajar en equipo,
    y las conecta con riesgos y tipos de peligro.
    """
    if df_rp.empty:
        return (
            "🔍 **[DEMO SKUDO] Análisis de riesgos de procesos**\n\n"
            "Todavía no hay escenarios cargados para esta selección. "
            "Cuando conectes SKUDO a tus PHA/HAZOP/LOPA/QRA, verás aquí el resumen."
        )

    met = resumir_riesgos_y_acciones(df_rp)
    df_gen = df_rp[df_rp["tipo_accion"] == "General"]
    df_team = df_rp[df_rp["tipo_accion"] == "Trabajo en equipo"]

    texto = "🔍 **[DEMO SKUDO] Análisis de riesgos de procesos**\n\n"
    texto += f"- Escenarios considerados: **{met['n_escenarios']}**\n"
    texto += f"- Nivel promedio de riesgo residual (S×F): **{met['prom_riesgo_residual']}**\n"
    texto += f"- Acciones generales: **{met['n_generales']}**\n"
    texto += f"- Acciones que requieren trabajo en equipo: **{met['n_equipo']}**\n"

    if met["top_peligros"]:
        texto += (
            f"- Tipos de peligro más frecuentes: **{', '.join(met['top_peligros'])}**\n\n"
        )
    else:
        texto += "\n"

    if not df_gen.empty:
        texto += (
            "**¿Qué podrías estandarizar?**\n"
            "Las acciones marcadas como **generales** son candidatas a convertir en estándares corporativos:\n"
            "- Procedimientos tipo\n"
            "- Entrenamientos recurrentes\n"
            "- Rutinas de mantenimiento / inspección\n\n"
        )

    if not df_team.empty:
        texto += (
            "**¿Qué requiere taller de equipo?**\n"
            "Las acciones marcadas como **trabajo en equipo** son las que conviene llevar a un comité o taller, "
            "porque implican decisiones de diseño, inversión o cambios de operación relevantes.\n\n"
        )

    texto += (
        "_En la versión completa, SKUDO usaría estos patrones para proponer catálogos de acciones estándar y "
        "agendas automáticas para reuniones de análisis de riesgo._"
    )

    return texto


def sugerir_consecuencias_y_salvaguardas_por_causa(causa_texto: str, df_hist: pd.DataFrame):
    """
    Dado un texto de causa (del estudio actual), busca en TODO el histórico
    de riesgos de proceso causas similares y sugiere consecuencias y salvaguardas
    típicas, más temas para trabajo en equipo.

    DEMO: usa una similitud muy sencilla por palabras clave.
    """
    causa = (causa_texto or "").strip()
    if not causa:
        return (
            "✏️ Escribe una causa para que SKUDO busque patrones en el histórico.",
            pd.DataFrame()
        )

    if df_hist.empty:
        return (
            "No hay histórico de riesgos de proceso cargado en esta DEMO. "
            "Cuando conectes SKUDO a tus PHA/HAZOP/LOPA/QRA, se utilizará esa base.",
            pd.DataFrame()
        )

    causa_tokens = [
        w.lower() for w in causa.split()
        if len(w) >= 4
    ]

    if not causa_tokens:
        return (
            "La causa es demasiado corta o genérica. Intenta describirla con más detalle "
            "(ej. 'sobrepresión por bloqueo aguas abajo', 'fuga por corrosión en bridas críticas').",
            pd.DataFrame()
        )

    df = df_hist.copy()

    def score_row(row):
        texto = (
            str(row.get("causa_principal", "")) + " " +
            str(row.get("descripcion_escenario", "")) + " " +
            str(row.get("tipo_peligro", ""))
        ).lower()
        score = 0
        for t in causa_tokens:
            if t in texto:
                score += 1
        return score

    df["sim_score"] = df.apply(score_row, axis=1)
    df_match = df[df["sim_score"] >= 1].copy()

    if df_match.empty:
        return (
            "No encontré causas similares en el histórico DEMO. "
            "En la versión real, se usarán modelos más avanzados para encontrar patrones.",
            pd.DataFrame()
        )

    # Ordenar por similitud y riesgo
    df_match = df_match.sort_values(
        ["sim_score", "riesgo_residual"],
        ascending=[False, False]
    ).head(10)

    # Consecuencias y salvaguardas típicas
    consecuencias = (
        df_match["consecuencia_principal"]
        .dropna()
        .drop_duplicates()
        .tolist()
    )
    salvaguardas = (
        df_match["salvaguardas_clave"]
        .dropna()
        .drop_duplicates()
        .tolist()
    )

    # Qué tipo de acciones suelen acompañar estas causas
    acciones_team = df_match[df_match["tipo_accion"] == "Trabajo en equipo"]["accion_sugerida"].tolist()
    acciones_gen = df_match[df_match["tipo_accion"] == "General"]["accion_sugerida"].tolist()

    texto = "🤖 **[DEMO SKUDO] Patrones históricos para la causa propuesta**\n\n"
    texto += f"Causa que quieres analizar:\n> {causa_texto}\n\n"
    texto += f"He encontrado **{len(df_match)}** escenarios con causas/peligros similares en el histórico.\n\n"

    if consecuencias:
        texto += "**Consecuencias típicas observadas en casos similares:**\n"
        for c in consecuencias[:5]:
            texto += f"- {c}\n"
        texto += "\n"

    if salvaguardas:
        texto += "**Salvaguardas típicas que se han usado en estos casos:**\n"
        for s in salvaguardas[:5]:
            texto += f"- {s}\n"
        texto += "\n"

    if acciones_team:
        texto += (
            "**Temas de trabajo en equipo que suelen aparecer en estos casos:**\n"
        )
        for a in acciones_team[:5]:
            texto += f"- {a}\n"
        texto += "\n"
    elif acciones_gen:
        texto += (
            "**Acciones generales frecuentes en casos similares (que podrían convertirse en estándar):**\n"
        )
        for a in acciones_gen[:5]:
            texto += f"- {a}\n"
        texto += "\n"

    texto += (
        "_Siguiente paso para la sesión de equipo:_\n"
        "- Validar si estas consecuencias aplican a tu escenario.\n"
        "- Confirmar qué salvaguardas existen realmente y si son suficientes.\n"
        "- Definir si se requieren salvaguardas adicionales (SIS, cambios de diseño, límites operativos, etc.)."
    )

    return texto, df_match



def generar_resumen_agente_accion_rapida(accion: str, df_diag: pd.DataFrame, instalacion_activa: str | None, perfil: str):
    df = df_diag.copy()
    if instalacion_activa and instalacion_activa != "Todas":
        df = df[df["instalacion"] == instalacion_activa]

    madurez = calcular_madurez_global(df)
    prios = prioridades_desde_diag(df, top_n=5)

    if accion == "Hoy":
        if perfil == "Gerencia":
            texto = (
                f"[DEMO SKUDO] La madurez promedio de CCPS en la instalación seleccionada es **{madurez}%**.\n\n"
                "Para **hoy**, como gerencia deberías poner el foco en habilitar recursos para:\n"
            )
        else:
            texto = (
                f"[DEMO SKUDO] La madurez promedio de CCPS en tu ámbito es **{madurez}%**.\n\n"
                "Para **hoy en campo**, concéntrate en estos temas técnicos:\n"
            )
        for _, r in prios.head(3).iterrows():
            texto += f"- **{r['Nodo / Tema']}** ({r['Nivel']} – {r['Plazo sugerido']}, Pilar {r['Pilar']})\n"
        texto += "\n> Recuerda: esta es una DEMO, los datos reales vendrán del diagnóstico y estudios de tu planta."
        return texto

    if accion == "Brechas":
        texto = (
            f"[DEMO SKUDO] He identificado las principales brechas a partir del diagnóstico simulado. "
            f"La madurez promedio es **{madurez}%**.\n\n"
            "Brechas con mayor impacto:\n"
        )
        for _, r in prios.iterrows():
            texto += f"- {r['Nodo / Tema']} en **{r['Instalación']}** ({r['Nivel']} – {r['Impacto']})\n"
        texto += "\n> DEMO: en la versión real, esto se arma con tus datos CCPS y PPAM."
        return texto

    if accion == "Resumen":
        if perfil == "Gerencia":
            texto = (
                f"[DEMO SKUDO] Resumen ejecutivo: madurez promedio CCPS **{madurez}%** "
                f"y **{len(prios)} ítems** clave de mejora.\n\n"
                "Decisiones críticas sugeridas (demo):\n"
                "1. Definir presupuesto para cerrar ítems críticos 0–3 meses.\n"
                "2. Alinear metas de gerencia con indicadores de madurez CCPS.\n"
                "3. Priorizar inversiones en integridad mecánica y emergencias.\n"
            )
        else:
            texto = (
                f"[DEMO SKUDO] Resumen técnico: madurez promedio **{madurez}%** "
                f"y **{len(prios)} ítems** relevantes.\n\n"
                "Para el equipo técnico (demo), enfócate en:\n"
                "1. Actualizar evidencias y registros de ítems críticos.\n"
                "2. Revisar matrices de riesgo y salvaguardas.\n"
                "3. Preparar información base para el Informe de Seguridad.\n"
            )
        texto += "\n> Esta es una DEMO, el agente real usará tus datos y reglas normativas."
        return texto

    return "[DEMO SKUDO] Acción rápida no reconocida en esta demo."


def respuesta_dummy_chat(user_msg: str) -> str:
    """Siempre responde que es una demo, sin importar el mensaje."""
    return (
        "🔧 **DEMO de SKUDO**\n\n"
        "Esta versión es solo un mockup funcional. El agente todavía **no está conectado** "
        "a modelos de IA ni a tus datos reales.\n\n"
        f"Lo que escribiste fue:\n> {user_msg}\n\n"
        "En la versión completa, aquí verías respuestas basadas en tu diagnóstico CCPS, PHA, QRA "
        "e Informe de Seguridad. Por ahora, la idea es mostrar la estructura del agente."
    )


def construir_plan_acciones_generales(df_rp: pd.DataFrame) -> pd.DataFrame:
    """
    Construye plan base a partir de acciones marcadas como 'General'.
    Cada fila es una acción editable que se puede convertir en estándar.
    """
    df_gen = df_rp[df_rp["tipo_accion"] == "General"].copy()
    if df_gen.empty:
        return pd.DataFrame(columns=[
            "id_escenario", "id_estudio", "instalacion", "unidad", "equipo",
            "tema", "accion", "prioridad", "responsable", "plazo", "estado"
        ])

    plan = df_gen[[
        "id_escenario", "id_estudio", "instalacion", "unidad", "equipo",
        "clase_accion", "accion_sugerida", "nivel_riesgo"
    ]].copy()

    plan = plan.rename(columns={
        "clase_accion": "tema",
        "accion_sugerida": "accion",
        "nivel_riesgo": "prioridad"
    })
    plan["responsable"] = ""
    plan["plazo"] = ""
    plan["estado"] = "Pendiente"

    return plan.reset_index(drop=True)


def construir_plan_trabajo_equipo(df_rp: pd.DataFrame) -> pd.DataFrame:
    """
    Construye plan base de temas para trabajar en sesión de equipo
    (acciones 'Trabajo en equipo').
    """
    df_team = df_rp[df_rp["tipo_accion"] == "Trabajo en equipo"].copy()
    if df_team.empty:
        return pd.DataFrame(columns=[
            "id_escenario", "id_estudio", "instalacion", "unidad", "equipo",
            "asunto_taller", "objetivo", "participantes_sugeridos",
            "nivel_riesgo", "estado"
        ])

    plan = df_team[[
        "id_escenario", "id_estudio", "instalacion", "unidad", "equipo",
        "accion_sugerida", "nivel_riesgo"
    ]].copy()

    plan = plan.rename(columns={
        "accion_sugerida": "asunto_taller"
    })
    plan["objetivo"] = ""
    plan["participantes_sugeridos"] = "Proceso / Operación / Mantenimiento / HSE"
    plan["estado"] = "Pendiente"

    return plan.reset_index(drop=True)


def seleccionar_escenarios_para_taller(df_rp: pd.DataFrame) -> list[str]:
    """
    Recomienda qué escenarios trabajar en taller:
    - primero todos los de 'Trabajo en equipo'
    - si son pocos, completa con los de riesgo residual más alto.
    """
    if df_rp.empty:
        return []

    ids_team = df_rp[df_rp["tipo_accion"] == "Trabajo en equipo"]["id_escenario"].tolist()

    if len(ids_team) < 3:
        df_rest = df_rp[~df_rp["id_escenario"].isin(ids_team)].copy()
        df_rest = df_rest.sort_values("riesgo_residual", ascending=False)
        extra = df_rest["id_escenario"].head(3 - len(ids_team)).tolist()
        ids_team = list(dict.fromkeys(ids_team + extra))  # sin duplicados

    return ids_team


def filtrar_nodos_relacionados_desde_rp(df_rp: pd.DataFrame, df_nodos_base: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra nodos que están relacionados con los escenarios analizados:
    misma instalación y, si es posible, misma unidad.
    """
    if df_rp.empty or df_nodos_base.empty:
        return pd.DataFrame(columns=df_nodos_base.columns)

    instalaciones = df_rp["instalacion"].dropna().unique().tolist()
    unidades = df_rp["unidad"].dropna().unique().tolist()

    df = df_nodos_base.copy()
    mask = df["instalacion"].isin(instalaciones)
    if unidades:
        mask &= df["unidad"].isin(unidades)

    return df[mask].reset_index(drop=True)



# =========================================================
# COMPONENTES DE PÁGINA (tablero, diagnóstico, nodos) – SIN CAMBIOS GRANDES
# =========================================================
def render_hero(instalacion_activa: str, perfil: str):
    nombre = "todas las instalaciones" if instalacion_activa == "Todas" else instalacion_activa
    if perfil == "Gerencia":
        sub = f"Vista ejecutiva de riesgo, madurez CCPS y cumplimiento normativo para {nombre}."
    else:
        sub = f"Vista técnica para gestionar brechas de CCPS, nodos de riesgo y evidencias en {nombre}."

    st.markdown(
        f"""
        <div class="hero-card">
          <div class="hero-title">SKUDO – Seguridad de procesos en una sola vista</div>
          <div class="hero-sub">{sub}</div>
          <div>
            <span class="badge-pill">Perfil: {perfil}</span>
            <span class="badge-pill">Modo: Diagnóstico &amp; Recomendaciones</span>
            <span class="badge-pill">Agente SKUDO (DEMO)</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def metric_card(title: str, value: str, subtitle: str):
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-title">{title}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard(instalacion_activa: str, perfil: str):
    # Cabecera tipo hero (ya la tenías)
    render_hero(instalacion_activa, perfil)

    # --------------------------
    # FILTROS BASE DE DATOS
    # --------------------------
    if instalacion_activa == "Todas":
        df_diag_f = df_diag.copy()
        df_sites_f = df_sites.copy()
        df_nodos_f = df_nodos.copy()
    else:
        df_diag_f = df_diag[df_diag["instalacion"] == instalacion_activa]
        df_sites_f = df_sites[df_sites["sitio"] == instalacion_activa]
        df_nodos_f = df_nodos[df_nodos["instalacion"] == instalacion_activa]

    madurez_global = calcular_madurez_global(df_diag_f)

    # Escenarios de riesgo ALTO desde nodos
    n_escenarios_alto = len(df_nodos_f[df_nodos_f["riesgo"] == "ALTO"])

    # Críticos de diagnóstico (Muy bajo / Bajo)
    crit_mask = df_diag_f["calificacion"].isin(["Muy bajo", "Bajo"])
    n_brechas_criticas = int(crit_mask.sum())
    total_items_diag = int(len(df_diag_f))

    # % acciones cerradas desde estado_plan
    if total_items_diag > 0:
        n_cerradas = int((df_diag_f["estado_plan"] == "Cerrado").sum())
        porcentaje_cerradas = round(100 * n_cerradas / total_items_diag, 1)
    else:
        porcentaje_cerradas = 0.0

    # "Cumplimiento normativo" demo (cuanto menos brecha crítica, más alto)
    if total_items_diag > 0:
        ratio_criticos = n_brechas_criticas / total_items_diag
        cumplimiento_3687 = max(0, min(100, round(100 - ratio_criticos * 60, 1)))
    else:
        cumplimiento_3687 = 0.0

    # Riesgo global instalación (demo a partir de df_sites)
    def map_riesgo_val(r):
        if r == "ALTO":
            return 3
        if r == "MEDIO":
            return 2
        if r == "BAJO":
            return 1
        return 0

    if not df_sites_f.empty:
        riesgo_score_prom = df_sites_f["riesgo_global"].map(map_riesgo_val).mean()
    else:
        riesgo_score_prom = 0

    if riesgo_score_prom >= 2.5:
        etiqueta_riesgo = "Crítico / Alto"
    elif riesgo_score_prom >= 1.5:
        etiqueta_riesgo = "Medio"
    elif riesgo_score_prom > 0:
        etiqueta_riesgo = "Moderado"
    else:
        etiqueta_riesgo = "Sin datos"

    # --------------------------
    # MÉTRICAS PRINCIPALES
    # --------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Madurez CCPS promedio",
            value=f"{madurez_global}%"
        )
        st.caption("Promedio ponderado de calificaciones del diagnóstico.")

    with col2:
        st.metric(
            label="Escenarios de riesgo ALTO",
            value=str(n_escenarios_alto)
        )
        st.caption("Escenarios críticos identificados en nodos (demo).")

    if perfil == "Gerencia":
        with col3:
            st.metric(
                label="Cumplimiento normativo (demo)",
                value=f"{cumplimiento_3687}%"
            )
            st.caption("Aproximación con base en brechas críticas del diagnóstico.")

        with col4:
            st.metric(
                label="Nivel de riesgo global",
                value=etiqueta_riesgo
            )
            st.caption("Clasificación cualitativa según instalaciones seleccionadas.")
    else:
        with col3:
            st.metric(
                label="Brechas críticas abiertas",
                value=str(n_brechas_criticas)
            )
            st.caption("Ítems con calificación Muy bajo / Bajo.")

        with col4:
            st.metric(
                label="Acciones cerradas (demo)",
                value=f"{porcentaje_cerradas}%"
            )
            st.caption("Porcentaje de ítems marcados como 'Cerrado'.")

    st.markdown("---")

    # =====================================================
    # VISTA PARA GERENCIA
    # =====================================================
    if perfil == "Gerencia":
        c_top, c_bottom = st.columns([1.3, 1.7])

        # ---- Izquierda: mapa + tabla de instalaciones ----
        with c_top:
            st.markdown('<div class="section-title">Mapa de instalaciones y riesgo</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-sub">Ubicación y clasificación de riesgo global de cada sitio (demo).</div>',
                unsafe_allow_html=True
            )
            if not df_sites_f.empty:
                df_map = df_sites_f.rename(columns={"lat": "latitude", "lon": "longitude"})
                st.map(df_map[["latitude", "longitude"]])

                df_sites_show = df_sites_f.copy()
                df_sites_show["Riesgo (1–3)"] = df_sites_show["riesgo_global"].map(map_riesgo_val)
                st.dataframe(
                    df_sites_show[["sitio", "riesgo_global", "madurez_ccps", "Riesgo (1–3)"]],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No hay instalaciones asociadas al filtro actual (demo).")

        # ---- Derecha: madurez + top brechas + “relato ejecutivo” ----
        with c_bottom:
            st.markdown('<div class="section-title">Madurez por pilar CCPS</div>', unsafe_allow_html=True)
            if not df_diag_f.empty:
                df_pilar = df_diag_f.copy()
                df_pilar["score"] = df_pilar["calificacion"].apply(calificacion_to_score)
                df_pilar = df_pilar.groupby("pilar", as_index=False)["score"].mean()
                df_pilar["score"] = df_pilar["score"].round(1)

                chart_pilar = (
                    alt.Chart(df_pilar)
                    .mark_bar()
                    .encode(
                        x=alt.X("pilar:N", title="Pilar CCPS"),
                        y=alt.Y("score:Q", title="Madurez (%)", scale=alt.Scale(domain=[0, 100])),
                        tooltip=["pilar", "score"]
                    )
                    .properties(height=230)
                )
                st.altair_chart(chart_pilar, use_container_width=True)
            else:
                st.info("Sin datos de diagnóstico para calcular madurez (demo).")

            st.markdown("#### Top 5 brechas (demo)")
            prios = prioridades_desde_diag(df_diag_f, top_n=5)
            if not prios.empty:
                st.dataframe(prios, use_container_width=True, hide_index=True)
            else:
                st.info("No hay brechas para mostrar (demo).")

            # Resumen tipo “3 decisiones”
            st.markdown("#### 3 decisiones clave (demo)")
            bullets = [
                f"Acelerar cierre de **{n_brechas_criticas} brechas críticas** en un horizonte de 0–6 meses.",
                f"Elevar la madurez CCPS de **{madurez_global}%** a >80% en pilares con mayor rezago.",
                "Alinear presupuesto, metas de gerencia y planes de acción críticos antes del próximo comité."
            ]
            for b in bullets:
                st.write(f"- {b}")

    # =====================================================
    # VISTA PARA TÉCNICO / HSE
    # =====================================================
    else:
        st.markdown(
            '<div class="section-sub">Vista técnica: foco en brechas, elementos CCPS y acciones.</div>',
            unsafe_allow_html=True
        )

        tab1, tab2, tab3 = st.tabs(["⚠️ Brechas y acciones", "📊 Elementos CCPS", "🏭 Por instalación"])

        # --------- TAB 1: Brechas y acciones ----------
        with tab1:
            col_b1, col_b2 = st.columns([1.7, 1.3])

            with col_b1:
                st.markdown('<div class="section-title">Brechas priorizadas (demo)</div>', unsafe_allow_html=True)
                prios = prioridades_desde_diag(df_diag_f, top_n=12)
                if not prios.empty:
                    st.dataframe(prios, use_container_width=True, hide_index=True)
                else:
                    st.info("No hay brechas para mostrar (demo).")

            with col_b2:
                st.markdown('<div class="section-title">Brechas críticas por elemento</div>', unsafe_allow_html=True)
                if not df_diag_f.empty:
                    df_crit = df_diag_f[crit_mask].copy()
                    if not df_crit.empty:
                        df_count_elem = (
                            df_crit.groupby("elemento", as_index=False)["id"]
                            .count()
                            .rename(columns={"id": "Brechas críticas"})
                        )
                        chart_crit = (
                            alt.Chart(df_count_elem)
                            .mark_bar()
                            .encode(
                                x=alt.X("Brechas críticas:Q"),
                                y=alt.Y("elemento:N", sort="-x", title="Elemento CCPS"),
                                tooltip=["elemento", "Brechas críticas"]
                            )
                            .properties(height=260)
                        )
                        st.altair_chart(chart_crit, use_container_width=True)
                    else:
                        st.info("No hay ítems con calificación Muy bajo / Bajo (demo).")
                else:
                    st.info("Sin datos de diagnóstico (demo).")

        # --------- TAB 2: Elementos CCPS ----------
        with tab2:
            c_e1, c_e2 = st.columns([1.7, 1.3])

            with c_e1:
                st.markdown('<div class="section-title">Madurez por elemento CCPS</div>', unsafe_allow_html=True)
                if not df_diag_f.empty:
                    df_elem = df_diag_f.copy()
                    df_elem["score"] = df_elem["calificacion"].apply(calificacion_to_score)
                    df_elem = df_elem.groupby("elemento", as_index=False)["score"].mean()
                    df_elem["score"] = df_elem["score"].round(1)

                    chart_elem = (
                        alt.Chart(df_elem)
                        .mark_bar()
                        .encode(
                            x=alt.X("score:Q", title="Madurez (%)", scale=alt.Scale(domain=[0, 100])),
                            y=alt.Y("elemento:N", title="Elemento CCPS", sort="-x"),
                            tooltip=["elemento", "score"]
                        )
                        .properties(height=320)
                    )
                    st.altair_chart(chart_elem, use_container_width=True)
                else:
                    st.info("Sin datos de diagnóstico para calcular madurez (demo).")

            with c_e2:
                st.markdown('<div class="section-title">Distribución de calificaciones</div>', unsafe_allow_html=True)
                dist = resumen_calificaciones(df_diag_f)
                if not dist.empty:
                    chart_dist = (
                        alt.Chart(dist)
                        .mark_bar()
                        .encode(
                            x=alt.X("Calificación:N"),
                            y=alt.Y("Cantidad:Q"),
                            tooltip=["Calificación", "Cantidad"]
                        )
                        .properties(height=220)
                    )
                    st.altair_chart(chart_dist, use_container_width=True)
                else:
                    st.info("Sin datos de diagnóstico (demo).")

        # --------- TAB 3: Por instalación ----------
        with tab3:
            st.markdown('<div class="section-title">Comparativo por instalación</div>', unsafe_allow_html=True)
            if instalacion_activa != "Todas":
                st.info(
                    "Para ver el comparativo por instalación, selecciona **'Todas'** en el filtro de instalación "
                    "en la barra lateral."
                )
            else:
                if not df_diag_f.empty:
                    df_site_mad = df_diag_f.copy()
                    df_site_mad["score"] = df_site_mad["calificacion"].apply(calificacion_to_score)
                    df_site_mad = df_site_mad.groupby("instalacion", as_index=False)["score"].mean()
                    df_site_mad["score"] = df_site_mad["score"].round(1)

                    chart_site = (
                        alt.Chart(df_site_mad)
                        .mark_bar()
                        .encode(
                            x=alt.X("instalacion:N", title="Instalación"),
                            y=alt.Y("score:Q", title="Madurez (%)", scale=alt.Scale(domain=[0, 100])),
                            tooltip=["instalacion", "score"]
                        )
                        .properties(height=280)
                    )
                    st.altair_chart(chart_site, use_container_width=True)

                    st.markdown("#### Tabla resumen por instalación (demo)")
                    st.dataframe(df_site_mad, use_container_width=True, hide_index=True)
                else:
                    st.info("Sin datos para construir el comparativo (demo).")


def render_diagnostico(instalacion_activa: str, perfil: str):
    st.markdown("### Diagnóstico CCPS – Madurez, cultura y brechas")

    # --------------------------
    # BASE: diagnostico filtrado por instalación
    # --------------------------
    if instalacion_activa == "Todas":
        df_diag_f = df_diag.copy()
    else:
        df_diag_f = df_diag[df_diag["instalacion"] == instalacion_activa]

    madurez_global = calcular_madurez_global(df_diag_f)
    total_items = len(df_diag_f)
    brechas_criticas = int(
        df_diag_f["calificacion"].isin(["Muy bajo", "Bajo"]).sum()
    )

    # --------------------------
    # FILTROS SUPERIORES
    # --------------------------
    fc1, fc2, fc3 = st.columns([1.5, 1.5, 1])
    with fc1:
        filtro_pilar = st.selectbox(
            "Filtro por pilar",
            options=["Todos"] + sorted(df_diag_f["pilar"].unique().tolist()),
        )
    with fc2:
        filtro_elemento = st.selectbox(
            "Filtro por elemento",
            options=["Todos"] + sorted(df_diag_f["elemento"].unique().tolist()),
        )
    with fc3:
        solo_criticos = st.checkbox("Solo críticos (Muy bajo / Bajo)", value=False)

    df_filtrado = df_diag_f.copy()
    if filtro_pilar != "Todos":
        df_filtrado = df_filtrado[df_filtrado["pilar"] == filtro_pilar]
    if filtro_elemento != "Todos":
        df_filtrado = df_filtrado[df_filtrado["elemento"] == filtro_elemento]
    if solo_criticos:
        df_filtrado = df_filtrado[df_filtrado["calificacion"].isin(["Muy bajo", "Bajo"])]

    # =====================================================
    # CARD 1 – Calificación promedio + resumen por elemento
    # =====================================================
    st.markdown(
        "<div class='panel-card'>",
        unsafe_allow_html=True,
    )

    # mini métricas arriba
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("**Madurez promedio CCPS**")
        st.markdown(f"<h3 style='margin:0.1rem 0'>{madurez_global}%</h3>", unsafe_allow_html=True)
        st.caption(f"Basado en {total_items} ítems del diagnóstico.")
    with m2:
        st.markdown("**Brechas críticas**")
        st.markdown(f"<h3 style='margin:0.1rem 0'>{brechas_criticas}</h3>", unsafe_allow_html=True)
        st.caption("Ítems con calificación Muy bajo / Bajo.")
    with m3:
        st.markdown("**Instalación**")
        st.markdown(
            f"<h4 style='margin:0.1rem 0'>{instalacion_activa}</h4>",
            unsafe_allow_html=True,
        )
        st.caption("Contexto actual del diagnóstico.")

    st.markdown("---")

    c1, c2 = st.columns([1.2, 1.8])

    # --------- IZQUIERDA: GRÁFICA TIPO PILAR / ELEMENTO ----------
    with c1:
        st.markdown(
            """
            <div class="panel-header">
              <div class="panel-header-title">Calificación promedio</div>
              <div class="panel-header-sub">Explora por pilar o por elemento</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        modo_grafica = st.radio(
            "Ver promedio por:",
            options=["Pilar CCPS", "Elemento CCPS"],
            horizontal=True,
            label_visibility="collapsed",
        )

        df_plot = df_filtrado.copy()
        if df_plot.empty:
            st.info("No hay datos para el filtro seleccionado (demo).")
        else:
            df_plot["score"] = df_plot["calificacion"].apply(calificacion_to_score)

            if modo_grafica == "Pilar CCPS":
                df_plot = df_plot.groupby("pilar", as_index=False)["score"].mean()
                df_plot["score"] = df_plot["score"].round(1)
                chart = (
                    alt.Chart(df_plot)
                    .mark_bar()
                    .encode(
                        x=alt.X("pilar:N", title="Pilar CCPS"),
                        y=alt.Y(
                            "score:Q",
                            title="Nivel de madurez (%)",
                            scale=alt.Scale(domain=[0, 100]),
                        ),
                        color=alt.value("#FBBF24"),
                        tooltip=["pilar", "score"],
                    )
                    .properties(height=260)
                )
            else:
                df_plot = df_plot.groupby("elemento", as_index=False)["score"].mean()
                df_plot["score"] = df_plot["score"].round(1)
                chart = (
                    alt.Chart(df_plot)
                    .mark_bar()
                    .encode(
                        x=alt.X(
                            "score:Q",
                            title="Nivel de madurez (%)",
                            scale=alt.Scale(domain=[0, 100]),
                        ),
                        y=alt.Y("elemento:N", title="Elemento CCPS", sort="-x"),
                        color=alt.value("#FBBF24"),
                        tooltip=["elemento", "score"],
                    )
                    .properties(height=260)
                )

            st.altair_chart(chart, use_container_width=True)

        st.caption(
            "TIP: cambia entre pilar y elemento para ver dónde se concentran las brechas."
        )

    # --------- DERECHA: TABLA RESUMEN POR ELEMENTO ----------
    with c2:
        st.markdown(
            """
            <div class="panel-header">
              <div class="panel-header-title">Resumen por elemento</div>
              <div class="panel-header-sub">Promedio y nivel de implementación (demo)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        df_resumen_elem = build_resumen_elementos(df_filtrado)
        if df_resumen_elem.empty:
            st.info("No hay datos para construir el resumen (demo).")
        else:
            df_show = df_resumen_elem.rename(
                columns={
                    "Elemento": "Elemento",
                    "Promedio": "Promedio",
                    "Impl. completa": "Impl. completa",
                    "Impl. parcial (toda)": "Impl. parcial en toda la compañía",
                    "Impl. parcial (algunas)": "Impl. parcial en algunas plantas",
                    "No implementado": "No implementado",
                    "No aplica": "No aplica",
                }
            )
            st.dataframe(
                df_show,
                use_container_width=True,
                hide_index=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # CARD 2 – Cultura + simulador de impacto
    # =====================================================
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">Cultura de Seguridad de Procesos</div>
          <div class="panel-header-sub">
            Percepción, reporte y aprendizaje (simulación demo)
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cc1, cc2 = st.columns([1.2, 1.8])

    # --------- IZQUIERDA: GRÁFICA CULTURA ----------
    with cc1:
        st.markdown("**Distribución de cultura (demo)**")

        df_cultura = df_filtrado[
            df_filtrado["elemento"] == "Cultura de Seguridad de Procesos"
        ].copy()

        if df_cultura.empty:
            # si no hay datos reales, armamos dimensiones ficticias pero creíbles
            df_cultura = pd.DataFrame(
                {
                    "dimensión": [
                        "Reporte de incidentes",
                        "Aprendizaje de errores",
                        "Participación en PHA",
                        "Confianza en el sistema",
                    ],
                    "nivel": [55, 65, 50, 60],
                }
            )
            chart_cult = (
                alt.Chart(df_cultura)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "nivel:Q",
                        title="Nivel (%)",
                        scale=alt.Scale(domain=[0, 100]),
                    ),
                    y=alt.Y("dimensión:N", sort="-x", title="Dimensión cultural"),
                    color=alt.value("#0EA5E9"),
                    tooltip=["dimensión", "nivel"],
                )
                .properties(height=1000)
            )
        else:
            dist = (
                df_cultura["calificacion"]
                .value_counts()
                .rename_axis("Calificación")
                .reset_index(name="Cantidad")
            )
            chart_cult = (
                alt.Chart(dist)
                .mark_bar()
                .encode(
                    x=alt.X("Calificación:N"),
                    y=alt.Y("Cantidad:Q"),
                    color=alt.value("#0EA5E9"),
                    tooltip=["Calificación", "Cantidad"],
                )
                .properties(height=220)
            )

        st.altair_chart(chart_cult, use_container_width=True)
        st.caption(
            "En la versión completa, aquí se verían resultados de encuestas, observaciones y reportes de cultura."
        )

    # --------- DERECHA: SIMULADOR “COOL” ----------
    with cc2:
        st.markdown("**Simulador de impacto de mejora (demo)**")

        st.write(
            "Mueve el control para simular qué pasa si cierras un porcentaje de las brechas "
            "críticas (Muy bajo / Bajo) en los próximos meses."
        )

        porcentaje_mejora = st.slider(
            "Porcentaje de brechas críticas que logras cerrar",
            min_value=0,
            max_value=100,
            value=30,
            step=10,
        )

        # modelo simplificado: cada 10 % de brechas cerradas suma 3 puntos de madurez
        impacto = porcentaje_mejora * 0.3
        madurez_nueva = min(100.0, round(madurez_global + impacto, 1))

        df_mad_comp = pd.DataFrame(
            {
                "Escenario": ["Actual", "Con mejora (demo)"],
                "Madurez": [madurez_global, madurez_nueva],
            }
        )

        chart_mad = (
            alt.Chart(df_mad_comp)
            .mark_bar()
            .encode(
                x=alt.X("Escenario:N", title="Escenario"),
                y=alt.Y(
                    "Madurez:Q",
                    title="Madurez CCPS (%)",
                    scale=alt.Scale(domain=[0, 100]),
                ),
                color=alt.value("#10B981"),
                tooltip=["Escenario", "Madurez"],
            )
            .properties(height=220)
        )
        st.altair_chart(chart_mad, use_container_width=True)

        st.markdown(
            f"- Madurez actual estimada: **{madurez_global}%**  \n"
            f"- Madurez simulada con la mejora seleccionada: **{madurez_nueva}%**"
        )
        st.caption(
            "En la versión real, el simulador usaría los ítems concretos del plan de acción para recalcular "
            "la madurez por pilar, elemento e instalación."
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_nodos(instalacion_activa: str):
    st.markdown("### Nodos & Estudios – Asistente de estudios y P&ID (DEMO)")

    # Base de datos filtrada por instalación
    df_n_base = df_nodos.copy()
    if instalacion_activa != "Todas":
        df_n_base = df_n_base[df_n_base["instalacion"] == instalacion_activa]

    df_e_base = df_estudios.copy()
    if instalacion_activa != "Todas":
        df_e_base = df_e_base[df_e_base["instalacion"] == instalacion_activa]

    # Estado local para esta pestaña
    if "nodos_sugerencia_texto" not in st.session_state:
        st.session_state["nodos_sugerencia_texto"] = ""
    if "nodos_estudios_rel" not in st.session_state:
        st.session_state["nodos_estudios_rel"] = pd.DataFrame()
    if "nodos_relevantes_ids" not in st.session_state:
        st.session_state["nodos_relevantes_ids"] = []

    # =====================================================
    # BLOQUE A – Asistente: "Dile a SKUDO tu problema"
    # =====================================================
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">1. Dile a SKUDO tu problema</div>
          <div class="panel-header-sub">
            Describe la situación y el agente sugerirá el estudio adecuado y estudios previos relacionados.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a1, col_a2 = st.columns([1.6, 1.4])

    with col_a1:
        # Campos del contexto del problema
        desc_default = st.session_state.get("problema_descripcion", "")
        unidad_default = st.session_state.get("problema_unidad", "")
        equipo_default = st.session_state.get("problema_equipo", "")
        tipo_default = st.session_state.get(
            "problema_tipo_situacion",
            "Problema recurrente / desviación operacional"
        )
        fase_default = st.session_state.get("problema_fase", "Operación")

        desc = st.text_area(
            "Describe brevemente el problema o necesidad",
            value=desc_default,
            height=120,
            placeholder=(
                "Ejemplo: 'Tenemos disparos frecuentes del PSV en el reactor R-101 cuando "
                "estamos cerca del máximo caudal de alimentación.'"
            ),
        )
        st.session_state["problema_descripcion"] = desc

        c_ctx1, c_ctx2 = st.columns(2)
        with c_ctx1:
            unidad = st.text_input(
                "Unidad / área",
                value=unidad_default,
                placeholder="Ejemplo: Reactor 1, Área de carga..."
            )
            st.session_state["problema_unidad"] = unidad
        with c_ctx2:
            equipo = st.text_input(
                "Equipo involucrado (si aplica)",
                value=equipo_default,
                placeholder="Ejemplo: R-101, TK-201-ESF..."
            )
            st.session_state["problema_equipo"] = equipo

        c_ctx3, c_ctx4 = st.columns(2)
        with c_ctx3:
            tipo_situacion = st.selectbox(
                "Tipo de situación",
                options=[
                    "Nuevo proyecto / diseño",
                    "Cambio (MOC)",
                    "Problema recurrente / desviación operacional",
                    "Incidente / casi incidente",
                    "Otro / no estoy seguro"
                ],
                index=[
                    "Nuevo proyecto / diseño",
                    "Cambio (MOC)",
                    "Problema recurrente / desviación operacional",
                    "Incidente / casi incidente",
                    "Otro / no estoy seguro"
                ].index(tipo_default) if tipo_default in [
                    "Nuevo proyecto / diseño",
                    "Cambio (MOC)",
                    "Problema recurrente / desviación operacional",
                    "Incidente / casi incidente",
                    "Otro / no estoy seguro"
                ] else 2,
            )
            st.session_state["problema_tipo_situacion"] = tipo_situacion
        with c_ctx4:
            fase = st.selectbox(
                "Fase del ciclo de vida",
                options=[
                    "Conceptual",
                    "Básico / FEED",
                    "Detalle",
                    "Operación",
                    "Desmantelamiento"
                ],
                index=[
                    "Conceptual",
                    "Básico / FEED",
                    "Detalle",
                    "Operación",
                    "Desmantelamiento"
                ].index(fase_default) if fase_default in [
                    "Conceptual",
                    "Básico / FEED",
                    "Detalle",
                    "Operación",
                    "Desmantelamiento"
                ] else 3,
            )
            st.session_state["problema_fase"] = fase

        if st.button("Sugerir estudio / revisión (DEMO)"):
            contexto = {
                "instalacion": instalacion_activa,
                "unidad": unidad,
                "equipo": equipo,
                "tipo_situacion": tipo_situacion,
                "fase": fase,
                "descripcion": desc,
            }
            texto, df_est_rel, nodos_rel_ids = sugerir_estudio_y_estudios(
                contexto, df_e_base, df_n_base
            )
            st.session_state["nodos_sugerencia_texto"] = texto
            st.session_state["nodos_estudios_rel"] = df_est_rel
            st.session_state["nodos_relevantes_ids"] = nodos_rel_ids

    with col_a2:
        st.markdown('<div class="section-title">Respuesta del agente (DEMO)</div>', unsafe_allow_html=True)
        if st.session_state["nodos_sugerencia_texto"]:
            st.markdown(st.session_state["nodos_sugerencia_texto"])
        else:
            st.info(
                "Cuando describas el problema y hagas clic en **'Sugerir estudio / revisión (DEMO)'**, "
                "el agente mostrará aquí el método recomendado y estudios previos relacionados."
            )

        st.markdown("---")
        st.markdown('<div class="section-title">Contexto activo</div>', unsafe_allow_html=True)
        st.markdown(f"<span class='chip'>Instalación: {instalacion_activa}</span>", unsafe_allow_html=True)
        if st.session_state.get("problema_unidad"):
            st.markdown(
                f"<span class='chip'>Unidad: {st.session_state['problema_unidad']}</span>",
                unsafe_allow_html=True
            )
        if st.session_state.get("problema_equipo"):
            st.markdown(
                f"<span class='chip'>Equipo: {st.session_state['problema_equipo']}</span>",
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # BLOQUE B – Estudios históricos relacionados
    # =====================================================
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">2. Estudios históricos relacionados (DEMO)</div>
          <div class="panel-header-sub">
            Revisa primero lo que ya se ha estudiado antes de lanzar un estudio nuevo.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df_est_rel = st.session_state["nodos_estudios_rel"]
    if df_est_rel is not None and not df_est_rel.empty:
        df_show = df_est_rel[[
            "id_estudio",
            "tipo",
            "anio",
            "instalacion",
            "unidad",
            "equipo",
            "cobertura",
            "estado",
            "accion_sugerida",
        ]].copy()
        st.dataframe(df_show, use_container_width=True, hide_index=True)
    else:
        st.info(
            "Aquí verás los estudios que el agente identifica como relacionados con el problema. "
            "Por ahora no se ha ejecutado ninguna búsqueda (DEMO)."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # BLOQUE C – Nodos & P&ID (vista limpia)
    # =====================================================

    # Config por P&ID: qué imagen usar, qué nodos mostrar y mensaje base del agente
    pid_configs = {
        "P&ID 1 – Línea con Nodo 1 y 2": {
            "file": "Imagen1.png",          # imagen central (nodos 1 y 2)
            "ids": ["N-001"],
            "texto_agente": (
                "Este diagrama muestra una **línea de proceso** con dos nodos principales. "
                "Es clave revisar escenarios de **sobrepresión y fugas** en la línea, y "
                "verificar que los dispositivos de alivio y seccionamiento estén cubiertos "
                "en HAZOP/LOPA y en los procedimientos de operación."
            ),
        },
        "P&ID 2 – Trenes en paralelo (Nodo 1, 2, 5)": {
            "file": "Imagen2.png",
            "ids": ["N-002"],
            "texto_agente": (
                "Aquí se visualizan **trenes en paralelo**. El foco está en la **consistencia "
                "de salvaguardas entre trenes** (alarmas, interlocks, válvulas) y en "
                "estandarizar acciones generales entre ellos: procedimientos, entrenamientos "
                "y mantenimiento."
            ),
        },
        "P&ID 3 – Columna / sistema con Nodo 2, 5 y 7": {
            "file": "Imagen0.png",
            "ids": ["N-003"],
            "texto_agente": (
                "Este P&ID representa una **unidad más compleja** conectada con temas de "
                "**cumplimiento normativo e Informe de Seguridad**. Hay que asegurar que los "
                "escenarios de accidente mayor estén reflejados en el QRA y en el PEC, y "
                "definir qué cambios requieren trabajo en equipo (proceso, operación, ingeniería, HSE)."
            ),
        },
    }

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">3. Nodos & P&ID resaltado (DEMO)</div>
          <div class="panel-header-sub">
            Cambia el P&ID y el nodo, y SKUDO ajusta el contexto y las recomendaciones.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df_n_base.empty:
        st.info("No hay nodos configurados para esta instalación en la DEMO.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # -------- Selección de P&ID (arriba, horizontal) --------
    pid_label = st.radio(
        "Seleccione el P&ID a analizar",
        options=list(pid_configs.keys()),
        horizontal=True,
    )
    pid_cfg = pid_configs[pid_label]

    ids_pid = pid_cfg["ids"]
    df_pid = df_n_base[df_n_base["id"].isin(ids_pid)].copy()
    if df_pid.empty:
        df_pid = df_n_base.copy()  # fallback por si cambias IDs y se te olvida el mapping

    # -------- Selección de nodo (chips / radio, nada de tabla fea) --------
    opciones_nodo = []
    for _, r in df_pid.iterrows():
        label = f"{r['id']} – {r['tipo']} ({r['riesgo']})"
        opciones_nodo.append(label)

    nodo_label = st.radio(
        "Nodo dentro de este P&ID",
        options=opciones_nodo,
        horizontal=True,
    )
    nodo_sel = nodo_label.split(" – ")[0]
    nodo_row = df_pid[df_pid["id"] == nodo_sel].iloc[0]

    # -------- Layout principal: izquierda imagen, derecha info + agente --------
    col_img, col_info = st.columns([2, 1])

    with col_img:
        ruta_img = IMG_DIR / pid_cfg["file"]
        try:
            st.image(
                str(ruta_img),
                caption=pid_label,
                use_column_width=True,
            )
        except Exception as e:
            st.error(
                f"No pude cargar la imagen '{ruta_img}'. "
                "Verifica que exista en la carpeta 'imagenes' y que el nombre coincida.\n\n"
                f"Detalle técnico: {e}"
            )

    with col_info:
        st.markdown('<div class="section-title">Detalle del nodo seleccionado</div>', unsafe_allow_html=True)
        st.markdown(
            f"**{nodo_row['id']} – {nodo_row['tipo']} ({nodo_row['riesgo']})**"
        )
        st.write(f"- Instalación: `{nodo_row['instalacion']}`")
        st.write(f"- Unidad: `{nodo_row.get('unidad', '')}`")
        st.write(f"- Equipo: `{nodo_row.get('equipo', '')}`")
        st.write(f"- Pilar asociado: `{nodo_row['pilar']}`")
        st.write(f"- Descripción: {nodo_row['descripcion']}")

        rels = [
            r.strip() for r in str(nodo_row["relacionados"]).split("|") if r.strip()
        ]
        if rels:
            st.markdown("**Nodos / referencias relacionadas (diagnóstico, acciones, requisitos):**")
            for r in rels:
                st.write(f"- {r}")

        st.markdown("---")
        st.markdown('<div class="section-title">Agente SKUDO – Recomendaciones para este nodo</div>', unsafe_allow_html=True)

        # Texto del agente combinando P&ID + nodo
        texto_nodo = f"""
- Nivel de riesgo declarado del nodo: **{nodo_row['riesgo']}**  
- Este nodo está ubicado en **{nodo_row.get('unidad', '')} – {nodo_row.get('equipo', '')}**.  
- En la versión completa, SKUDO traería las **causas, consecuencias y salvaguardas** de los estudios
  asociados (PHA/HAZOP/LOPA/QRA) y propondría:
  - Acciones **generales** que puedan estandarizarse (procedimientos, entrenamientos, mantenimiento).
  - Temas a tratar en **reuniones de trabajo en equipo** cuando el cambio implique diseño o inversión.
- Además, vincularía este nodo con el **Informe de Seguridad** para evidenciar cómo se gestionan
  los escenarios de accidente mayor en esta parte del P&ID.
        """

        st.markdown(pid_cfg["texto_agente"])
        st.markdown("")
        st.markdown(texto_nodo)

    st.markdown("</div>", unsafe_allow_html=True)


def render_analisis_riesgos_proceso(instalacion_activa: str, perfil: str):
    st.markdown("### Análisis de riesgos de procesos (DEMO)")

    # -------------------------
    # 1. Selección de estudios
    # -------------------------
    if instalacion_activa == "Todas":
        df_e = df_estudios.copy()
    else:
        df_e = df_estudios[df_estudios["instalacion"] == instalacion_activa].copy()

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">1. Alcance del análisis</div>
          <div class="panel-header-sub">
            Elige los estudios desde los que se consolidan los escenarios de riesgo de proceso.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df_e.empty:
        st.info(
            "No hay estudios dummy configurados para esta instalación en la DEMO. "
            "Cuando conectes SKUDO a tus PHA/HAZOP/LOPA/QRA, aparecerán aquí."
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return

    df_e = df_e.sort_values(["instalacion", "anio", "tipo"])
    opciones = []
    mapping = {}
    for _, row in df_e.iterrows():
        label = f"{row['id_estudio']} – {row['tipo']} ({row['anio']}) – {row['instalacion']} / {row['unidad'] or 'Sin unidad'}"
        opciones.append(label)
        mapping[label] = row["id_estudio"]

    estudios_sel_labels = st.multiselect(
        "Estudios a considerar",
        options=opciones,
        default=opciones[:1]
    )
    estudios_sel_ids = [mapping[l] for l in estudios_sel_labels]

    incluir_todos = st.checkbox(
        "Incluir también otros estudios de la instalación como contexto (DEMO)",
        value=False
    )
    if incluir_todos and instalacion_activa != "Todas":
        estudios_sel_ids = list(set(estudios_sel_ids + df_e["id_estudio"].tolist()))

    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------
    # 2. Escenarios consolidados y KPIs
    # -------------------------
    df_rp = get_dummy_riesgos_por_estudios(estudios_sel_ids)
    met = resumir_riesgos_y_acciones(df_rp)

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">2. Escenarios, niveles de riesgo y acciones</div>
          <div class="panel-header-sub">
            Vista ejecutiva y técnica del riesgo de proceso consolidado.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df_rp.empty:
        st.info(
            "No hay escenarios dummy para los estudios seleccionados. "
            "En producción aquí verías el consolidado de tus PHA/HAZOP/LOPA/QRA."
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("**Escenarios analizados**")
        st.markdown(f"<h3 style='margin:0.1rem 0'>{met['n_escenarios']}</h3>", unsafe_allow_html=True)
    with k2:
        st.markdown("**Acciones generales**")
        st.markdown(f"<h3 style='margin:0.1rem 0'>{met['n_generales']}</h3>", unsafe_allow_html=True)
    with k3:
        st.markdown("**Acciones equipo multidisciplinario**")
        st.markdown(f"<h3 style='margin:0.1rem 0'>{met['n_equipo']}</h3>", unsafe_allow_html=True)
    with k4:
        st.markdown("**Riesgo residual promedio (S×F)**")
        st.markdown(f"<h3 style='margin:0.1rem 0'>{met['prom_riesgo_residual']}</h3>", unsafe_allow_html=True)
        if met["top_peligros"]:
            st.caption("Peligros frecuentes: " + ", ".join(met["top_peligros"]))
        else:
            st.caption("Sin datos en la DEMO.")

    st.markdown("---")

    # ==========================
    # 3. Pestañas
    # ==========================
    tab_mapa, tab_generales, tab_equipo, tab_nodos = st.tabs([
        "🗺️ Mapa de riesgo de procesos",
        "📚 Acciones generales / típicas",
        "🤝 Acciones para trabajo en equipo",
        "🧩 Nodos & Estudios"
    ])

    # ---- TAB 1: Mapa de riesgo ----
    with tab_mapa:
        st.markdown("#### Mapa de riesgo (Severidad vs Frecuencia) – DEMO")

        df_plot = df_rp.copy()

        chart = (
            alt.Chart(df_plot)
            .mark_circle()
            .encode(
                x=alt.X("frecuencia:Q", title="Frecuencia (1–5)", scale=alt.Scale(domain=[0.5, 5.5])),
                y=alt.Y("severidad:Q", title="Severidad (1–5)", scale=alt.Scale(domain=[0.5, 5.5])),
                size=alt.Size("riesgo_residual:Q", title="Riesgo residual (S×F)", scale=alt.Scale(range=[50, 800])),
                color=alt.Color("nivel_riesgo:N", title="Nivel de riesgo"),
                shape=alt.Shape("tipo_accion:N", title="Tipo de acción"),
                tooltip=[
                    "id_escenario",
                    "id_estudio",
                    "instalacion",
                    "unidad",
                    "equipo",
                    "tipo_peligro",
                    "fase_operativa",
                    "descripcion_escenario",
                    "causa_principal",
                    "consecuencia_principal",
                    "salvaguardas_clave",
                    "nivel_riesgo",
                    "riesgo_residual",
                    "tipo_accion",
                    "clase_accion"
                ],
            )
            .properties(height=340)
        )
        st.altair_chart(chart, use_container_width=True)

        st.caption(
            "El tamaño refleja el riesgo residual (S×F), el color el nivel de riesgo "
            "y la forma el tipo de acción (general vs trabajo en equipo)."
        )

        st.markdown("#### Tabla de escenarios (DEMO)")
        st.dataframe(
            df_plot[[
                "id_escenario",
                "id_estudio",
                "instalacion",
                "unidad",
                "equipo",
                "tipo_peligro",
                "fase_operativa",
                "nivel_riesgo",
                "riesgo_residual",
                "tipo_accion",
                "clase_accion",
                "accion_sugerida"
            ]],
            use_container_width=True,
            hide_index=True
        )

    # ---- TAB 2: Acciones generales / típicas ----
    with tab_generales:
        st.markdown("#### Acciones generales / típicas (para estandarizar)")

        df_gen = df_rp[df_rp["tipo_accion"] == "General"].copy()
        if df_gen.empty:
            st.info("No hay acciones generales en los escenarios analizados (DEMO).")
        else:
            df_res = agrupar_acciones_generales(df_rp)
            st.markdown("**Patrones de acción general por tema**")
            st.dataframe(df_res, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("**Detalle de acciones generales por escenario**")
            st.dataframe(
                df_gen[[
                    "id_escenario",
                    "id_estudio",
                    "instalacion",
                    "unidad",
                    "equipo",
                    "descripcion_escenario",
                    "tipo_peligro",
                    "accion_sugerida",
                    "clase_accion",
                    "nivel_riesgo",
                    "estado_accion"
                ]],
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "Estas son acciones que el agente podría proponer como base para estándares "
                "(procedimientos tipo, entrenamientos, rutinas de mantenimiento) en la versión real."
            )

    # ---- TAB 3: Acciones para trabajo en equipo ----
    with tab_equipo:
        st.markdown("#### Acciones y temas para trabajo en equipo")

        df_team = df_rp[df_rp["tipo_accion"] == "Trabajo en equipo"].copy()
        if df_team.empty:
            st.info("No hay acciones marcadas como 'Trabajo en equipo' en los escenarios seleccionados (DEMO).")
        else:
            st.markdown("**Acciones / temas de sesión**")
            st.dataframe(
                df_team[[
                    "id_escenario",
                    "id_estudio",
                    "instalacion",
                    "unidad",
                    "equipo",
                    "descripcion_escenario",
                    "tipo_peligro",
                    "fase_operativa",
                    "nivel_riesgo",
                    "riesgo_residual",
                    "accion_sugerida",
                    "clase_accion",
                    "estado_accion"
                ]],
                use_container_width=True,
                hide_index=True
            )

        st.markdown("---")
        st.markdown("**Resumen del agente (DEMO)**")
        texto_agente = clasificar_acciones_rp_agente(df_rp)
        st.markdown(texto_agente)

        st.markdown("---")
        st.markdown("#### Asistente por causa (usar histórico)")

        causa_actual = st.text_input(
            "Escribe una causa del estudio que quieras analizar con el histórico",
            value=st.session_state.get("causa_rp_input", ""),
            placeholder="Ejemplo: 'obstrucción por acumulación de sedimentos y parafinas en la línea...'"
        )
        st.session_state["causa_rp_input"] = causa_actual

        if st.button("Buscar consecuencias y salvaguardas típicas (DEMO)"):
            df_hist = get_dummy_riesgos_por_estudios([])  # todos en DEMO
            texto_causa, df_match = sugerir_consecuencias_y_salvaguardas_por_causa(causa_actual, df_hist)
            st.markdown(texto_causa)

            if df_match is not None and not df_match.empty:
                st.markdown("**Escenarios históricos utilizados como referencia (DEMO):**")
                st.dataframe(
                    df_match[[
                        "id_escenario",
                        "id_estudio",
                        "instalacion",
                        "unidad",
                        "equipo",
                        "tipo_peligro",
                        "fase_operativa",
                        "causa_principal",
                        "consecuencia_principal",
                        "salvaguardas_clave",
                        "nivel_riesgo",
                        "riesgo_residual",
                        "tipo_accion",
                        "clase_accion"
                    ]],
                    use_container_width=True,
                    hide_index=True
                )

    # ---- TAB 4: Nodos & Estudios (TODO lo que ya tienes) ----
    with tab_nodos:
        # Reusamos TODO el módulo actual de nodos dentro de esta pestaña
        render_nodos(instalacion_activa)

    st.markdown("</div>", unsafe_allow_html=True)



def render_analisis_riesgos(instalacion_activa: str):
    st.markdown("### Análisis de riesgos – Condiciones, causas, consecuencias y acciones (DEMO)")

    # -------------------------
    # 1. Selección de estudio
    # -------------------------
    if instalacion_activa == "Todas":
        df_e = df_estudios.copy()
    else:
        df_e = df_estudios[df_estudios["instalacion"] == instalacion_activa].copy()

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">1. Selección y precarga del estudio</div>
          <div class="panel-header-sub">
            Elige el estudio de referencia para revisar sus condiciones, causas, consecuencias y acciones.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df_e.empty:
        st.info(
            "No hay estudios dummy configurados para esta instalación en la DEMO. "
            "Cuando conectes SKUDO a tus bases PHA/HAZOP/LOPA, aparecerán aquí."
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return

    df_e = df_e.sort_values(["instalacion", "anio", "tipo"])
    opciones = []
    mapping = {}
    for _, row in df_e.iterrows():
        label = f"{row['id_estudio']} – {row['tipo']} ({row['anio']}) – {row['instalacion']} / {row['unidad'] or 'Sin unidad'}"
        opciones.append(label)
        mapping[label] = row["id_estudio"]

    sel_label = st.selectbox(
        "Estudio de referencia",
        options=opciones
    )
    id_est_sel = mapping[sel_label]
    estudio_row = df_e[df_e["id_estudio"] == id_est_sel].iloc[0]

    col_info1, col_info2 = st.columns([1.5, 1.5])
    with col_info1:
        st.markdown("**Resumen del estudio (DEMO)**")
        st.write(f"- Tipo: `{estudio_row['tipo']}`")
        st.write(f"- Año: `{estudio_row['anio']}`")
        st.write(f"- Instalación: `{estudio_row['instalacion']}`")
        st.write(f"- Unidad: `{estudio_row['unidad']}`")
        st.write(f"- Equipo principal: `{estudio_row['equipo'] or 'N/A'}`")

    with col_info2:
        st.markdown("**Cobertura y estado**")
        st.write(f"- Cobertura declarada: `{estudio_row['cobertura']}`")
        st.write(f"- Estado: `{estudio_row['estado']}`")
        st.write(f"- Acción sugerida global: {estudio_row['accion_sugerida']}")
        st.caption("En la versión real, aquí se verían metadatos completos del estudio, versión, revalidaciones, etc.")

    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------
    # 2. Condiciones del estudio + agente
    # -------------------------
    df_cond = get_dummy_condiciones_para_estudio(id_est_sel)

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">2. Condiciones analizadas y acciones asociadas (DEMO)</div>
          <div class="panel-header-sub">
            Se listan las condiciones (escenarios), sus causas, consecuencias, salvaguardas y acciones propuestas.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_c1, col_c2 = st.columns([1.8, 1.2])

    with col_c1:
        if df_cond.empty:
            st.info(
                "Este estudio no tiene condiciones dummy asociadas en la DEMO. "
                "En producción se precargarían desde tus hojas PHA/HAZOP/LOPA."
            )
        else:
            st.markdown("**Tabla de condiciones y acciones**")
            df_show = df_cond[[
                "id_condicion",
                "condicion",
                "causa",
                "consecuencia",
                "salvaguardas",
                "accion_sugerida",
                "tipo_accion",
                "criticidad",
                "estado_accion"
            ]].copy()
            st.dataframe(df_show, use_container_width=True, hide_index=True)

    with col_c2:
        st.markdown('<div class="section-title">Agente de análisis (DEMO)</div>', unsafe_allow_html=True)
        texto_agente, df_gen, df_team = clasificar_acciones_riesgos(df_cond)
        st.markdown(texto_agente)

        if not df_gen.empty:
            st.markdown("---")
            st.markdown("**Resumen rápido – Acciones generales**")
            st.write(f"- Se identifican {len(df_gen)} acciones que podrían estandarizarse.")
        if not df_team.empty:
            st.markdown("**Resumen rápido – Acciones a trabajar en equipo**")
            st.write(f"- Se identifican {len(df_team)} acciones que requieren revisión conjunta.")

    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------
    # 3. Futuro: integración con planes y comité
    # -------------------------
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">3. Siguiente paso (DEMO)</div>
          <div class="panel-header-sub">
            Cómo se usaría este análisis en SKUDO real.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(
        "- En la versión completa, las **acciones generales** alimentarían catálogos corporativos "
        "de estándares (procedimientos tipo, entrenamientos base, lineamientos de permisos de trabajo)."
    )
    st.write(
        "- Las **acciones que requieren trabajo en equipo** se usarían para armar agendas de reuniones "
        "de análisis de riesgo (ingeniería, operación, HSE) y priorizar recursos."
    )
    st.write(
        "- Además, el resultado se conectaría con el **plan de acción de SKUDO** y con el **Informe de Seguridad** "
        "para evidenciar cómo se gestionan los escenarios de riesgo identificados."
    )
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# INFORME – AQUÍ VIENE LA PARTE CRÍTICA DEL % DE AVANCE
# =========================================================
def render_informe():
    st.markdown("### Informe de Seguridad – Construcción guiada (DEMO)")

    paso = st.radio(
        "Secciones del informe",
        options=[
            "1. Conocimiento del riesgo",
            "2. Reducción del riesgo",
            "3. Manejo del desastre",
            "4. Anexos"
        ],
        horizontal=True
    )

    c1, c2 = st.columns([2, 1])

    # ---- COLUMNA DERECHA: autocompletar + cálculo de avance ----
    with c2:
        st.markdown('<div class="section-title">Asistente del informe (DEMO)</div>', unsafe_allow_html=True)
        st.markdown(
            "En la versión real, SKUDO jalonaría datos de nodos, PHA, QRA y PEC para "
            "prellenar el informe según la Resolución 3687.",
            unsafe_allow_html=True
        )

        if paso == "1. Conocimiento del riesgo":
            if st.button("Autocompletar esta sección (demo)"):
                set_inf("inf_1_desc_instalacion",
                        "Instalación dedicada a almacenamiento y manejo de sustancias inflamables y tóxicas, con operación continua 24/7.")
                set_inf("inf_1_contexto_ext",
                        "Ubicada en zona industrial con otras plantas de proceso y áreas residenciales próximas.")
                set_inf("inf_1_contexto_int",
                        "Incluye procesos de recepción, mezclado y despacho de productos químicos, con sustancias inflamables, corrosivas y tóxicas.")
                set_inf("inf_1_peligros",
                        "Se han identificado escenarios de fuga, incendio y explosión en tanques, líneas de transferencia y equipos de proceso mediante PHA/HAZOP y QRA.")

        elif paso == "2. Reducción del riesgo":
            if st.button("Autocompletar esta sección (demo)"):
                set_inf("inf_2_medidas_prev",
                        "Dispone de sistemas de detección de gas, protección contra incendios, controles de ingeniería, procedimientos operativos y programas de mantenimiento basado en riesgo.")
                set_inf("inf_2_proteccion_fin",
                        "Cuenta con pólizas de seguro para daños a la propiedad, responsabilidad civil y pérdida de beneficio.")

        elif paso == "3. Manejo del desastre":
            if st.button("Autocompletar esta sección (demo)"):
                set_inf("inf_3_manejo_desastre",
                        "Existe un plan de emergencias y contingencias formalmente aprobado, con roles definidos, coordinación con autoridades externas y simulacros periódicos.")

        else:  # "4. Anexos"
            if st.button("Autocompletar esta sección (demo)"):
                set_inf("inf_4_ot",
                        "Se suministra información de escenarios de accidente mayor y áreas de afectación para apoyo al ordenamiento territorial.")
                set_inf("inf_4_pec",
                        "El PEC está actualizado e incluye procedimientos de notificación, respuesta y recuperación.")
                set_inf("inf_4_adicional",
                        "Se anexan mapas de isocontornos de riesgo y planos con ubicación de equipos críticos.")

        st.markdown("---")

        # Cálculo del avance: cuenta cuántos campos tienen texto
        total_campos = len(INF_FIELDS)
        campos_llenos = 0
        for name in INF_FIELDS:
            if get_inf(name).strip():
                campos_llenos += 1

        avance = int((campos_llenos / total_campos) * 100) if total_campos > 0 else 0

        st.markdown(f"**Campos diligenciados:** {campos_llenos} de {total_campos}")
        st.progress(avance / 100, text=f"{avance}% completado (aprox.)")

    # ---- COLUMNA IZQUIERDA: inputs que leen/escriben a session_state (claves internas) ----
    with c1:
        if paso == "1. Conocimiento del riesgo":
            st.subheader("1. Conocimiento del riesgo")

            v1 = st.text_input(
                "Descripción general de la instalación",
                value=get_inf("inf_1_desc_instalacion"),
            )
            set_inf("inf_1_desc_instalacion", v1)

            v2 = st.text_area(
                "Contexto externo (entorno, comunidades, etc.)",
                value=get_inf("inf_1_contexto_ext"),
                height=100
            )
            set_inf("inf_1_contexto_ext", v2)

            v3 = st.text_area(
                "Contexto interno (procesos, sustancias peligrosas)",
                value=get_inf("inf_1_contexto_int"),
                height=100
            )
            set_inf("inf_1_contexto_int", v3)

            v4 = st.text_area(
                "Identificación de peligros, análisis y evaluación del riesgo de accidente mayor",
                value=get_inf("inf_1_peligros"),
                height=140
            )
            set_inf("inf_1_peligros", v4)

        elif paso == "2. Reducción del riesgo":
            st.subheader("2. Reducción del riesgo")

            v5 = st.text_area(
                "Medidas de prevención y mitigación (técnicas, organizacionales, procedimentales)",
                value=get_inf("inf_2_medidas_prev"),
                height=160
            )
            set_inf("inf_2_medidas_prev", v5)

            v6 = st.text_area(
                "Medidas de protección financiera (seguros, reservas, etc.)",
                value=get_inf("inf_2_proteccion_fin"),
                height=100
            )
            set_inf("inf_2_proteccion_fin", v6)

        elif paso == "3. Manejo del desastre":
            st.subheader("3. Manejo del desastre")

            v7 = st.text_area(
                "Preparación y atención de emergencias y contingencias",
                value=get_inf("inf_3_manejo_desastre"),
                height=180
            )
            set_inf("inf_3_manejo_desastre", v7)

        else:  # "4. Anexos"
            st.subheader("4. Anexos")

            v8 = st.text_area(
                "Insumos para ordenamiento territorial",
                value=get_inf("inf_4_ot"),
                height=100
            )
            set_inf("inf_4_ot", v8)

            v9 = st.text_area(
                "Plan de Emergencias y Contingencias (PEC)",
                value=get_inf("inf_4_pec"),
                height=100
            )
            set_inf("inf_4_pec", v9)

            v10 = st.text_area(
                "Información adicional (isocontornos de riesgo, mapas, etc.)",
                value=get_inf("inf_4_adicional"),
                height=100
            )
            set_inf("inf_4_adicional", v10)

    st.markdown("---")
    st.button("Generar borrador de Informe de Seguridad (PDF/Word) – DEMO")


def render_agente(instalacion_activa: str, perfil: str):
    st.markdown("### Mi Agente SKUDO – DEMO")

    c1, c2 = st.columns([1.4, 1.6])

    with c1:
        st.markdown('<div class="section-title">Acciones rápidas (DEMO)</div>', unsafe_allow_html=True)
        colb1, colb2 = st.columns(2)
        with colb1:
            btn_hoy = st.button("🔥 ¿Qué hago hoy? (demo)")
        with colb2:
            btn_brechas = st.button("⚠️ Brechas críticas (demo)")

        btn_resumen = st.button("📑 Resumen para comité (demo)")

        if instalacion_activa == "Todas":
            df_diag_f = df_diag.copy()
        else:
            df_diag_f = df_diag[df_diag["instalacion"] == instalacion_activa]

        if btn_hoy:
            texto = generar_resumen_agente_accion_rapida("Hoy", df_diag_f, instalacion_activa, perfil)
            st.session_state["chat_history"].append(("assistant", texto, datetime.now().strftime("%H:%M:%S")))
        if btn_brechas:
            texto = generar_resumen_agente_accion_rapida("Brechas", df_diag_f, instalacion_activa, perfil)
            st.session_state["chat_history"].append(("assistant", texto, datetime.now().strftime("%H:%M:%S")))
        if btn_resumen:
            texto = generar_resumen_agente_accion_rapida("Resumen", df_diag_f, instalacion_activa, perfil)
            st.session_state["chat_history"].append(("assistant", texto, datetime.now().strftime("%H:%M:%S")))

        st.markdown("---")
        st.markdown('<div class="section-title">Contexto activo (DEMO)</div>', unsafe_allow_html=True)
        st.markdown(f"<span class='chip'>Instalación: {instalacion_activa}</span>", unsafe_allow_html=True)
        st.markdown("<span class='chip'>Diagnóstico CCPS 2025</span>", unsafe_allow_html=True)
        st.markdown("<span class='chip'>Nodos de riesgo ALTO</span>", unsafe_allow_html=True)
        st.markdown("<span class='chip'>Pendientes normativos</span>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-title">Chat con SKUDO (DEMO)</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-sub">Cualquier mensaje que envíes responderá indicando que es una demo.</div>',
            unsafe_allow_html=True
        )

        for role, msg, ts in st.session_state["chat_history"]:
            label = "Tú" if role == "user" else "SKUDO"
            st.markdown(f"**{label} ({ts})**")
            st.markdown(msg)
            st.markdown("---")

        user_msg = st.text_input("Escribe tu pregunta o comentario (DEMO)", "")
        if st.button("Enviar mensaje (DEMO)"):
            if user_msg.strip():
                ts = datetime.now().strftime("%H:%M:%S")
                st.session_state["chat_history"].append(("user", user_msg, ts))
                resp = respuesta_dummy_chat(user_msg)
                st.session_state["chat_history"].append(("assistant", resp, datetime.now().strftime("%H:%M:%S")))

# =========================================================
# SIDEBAR / NAVEGACIÓN
# =========================================================
with st.sidebar:
    st.markdown("## SKUDO")
    st.caption("Módulo de seguridad de procesos – Soluquim (DEMO).")

    perfil = st.selectbox(
        "Perfil de vista",
        ["Gerencia", "Técnico / HSE"],
        index=0
    )

    instalaciones_opts = ["Todas"] + df_sites["sitio"].tolist()
    instalacion_activa = st.selectbox(
        "Instalación activa",
        instalaciones_opts,
        index=0
    )

    st.markdown("---")
    menu = st.radio(
    "Navegación",
    options=[
        "Tablero de control",
        "Agente inteligente & Estudios",     # ✅ NUEVO 2do
        "Análisis de riesgos de procesos",   # ✅ 3ro
        "Informe de Seguridad",              # ✅ 4to
        "Mi Agente SKUDO"                    # ✅ último
    ]
    )



# =========================================================
# ROUTER
# =========================================================
if menu == "Tablero de control":
    render_dashboard(instalacion_activa, perfil)

elif menu == "Agente inteligente & Estudios":
    render_agente_inteligente_estudios(instalacion_activa, perfil)

elif menu == "Análisis de riesgos de procesos":
    render_analisis_riesgos_proceso(instalacion_activa, perfil)

elif menu == "Informe de Seguridad":
    render_informe()

else:
    render_agente(instalacion_activa, perfil)

