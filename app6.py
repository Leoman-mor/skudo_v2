import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

# =========================================================
# RUTAS
# =========================================================
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

# =========================================================
# ESTILO PERSONALIZADO
# =========================================================
PRIMARY = "#005F73"
SECONDARY = "#0A9396"
ACCENT = "#EE9B00"
BG = "#0B1220"  # dark
PANEL = "#111827"
BORDER = "#1F2937"
TEXT_SUB = "#9CA3AF"

st.markdown(
    f"""
    <style>
    .main {{
        background-color: {BG};
    }}
    .block-container {{
        padding-top: 3.8rem !important;
        padding-bottom: 2rem;
        max-width: 1500px;
    }}
    h1, h2, h3, h4, h5, h6, p, div, span {{
        color: #E5E7EB;
    }}
    .hero-card {{
        background: radial-gradient(circle at top left, {SECONDARY} 0, {PRIMARY} 60%);
        color: white;
        border-radius: 1rem;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.0rem;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 10px 25px rgba(0,0,0,0.25);
    }}
    .hero-title {{
        font-size: 1.55rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }}
    .hero-sub {{
        font-size: 0.95rem;
        opacity: 0.95;
        margin-bottom: 0.75rem;
    }}
    .badge-pill {{
        display: inline-block;
        background: rgba(255,255,255,0.18);
        border-radius: 999px;
        padding: 0.18rem 0.7rem;
        font-size: 0.75rem;
        margin-right: 0.35rem;
        margin-bottom: 0.25rem;
    }}
    .panel-card {{
        background-color: {PANEL};
        padding: 1.1rem 1.25rem;
        border-radius: 1rem;
        border: 1px solid {BORDER};
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        margin-bottom: 1.0rem;
    }}
    .panel-header {{
        display:flex;
        justify-content:space-between;
        align-items:baseline;
        margin-bottom:0.65rem;
    }}
    .panel-header-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: #F9FAFB;
    }}
    .panel-header-sub {{
        font-size: 0.82rem;
        color: {TEXT_SUB};
    }}
    .section-title {{
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        color: #F9FAFB;
    }}
    .section-sub {{
        font-size: 0.82rem;
        color: {TEXT_SUB};
        margin-bottom: 0.55rem;
    }}
    .chip {{
        display: inline-block;
        padding: 0.18rem 0.6rem;
        border-radius: 999px;
        font-size: 0.75rem;
        background-color: #0F172A;
        border: 1px solid #223049;
        margin-right: 0.35rem;
        margin-bottom: 0.25rem;
        color: #E5E7EB;
    }}
    .kpi {{
        background: #0F172A;
        border: 1px solid #223049;
        border-radius: 0.85rem;
        padding: 0.9rem 1rem;
    }}
    .kpi-title {{
        font-size: 0.82rem;
        color: {TEXT_SUB};
        margin-bottom: 0.2rem;
    }}
    .kpi-value {{
        font-size: 1.55rem;
        font-weight: 800;
        color: #F9FAFB;
        margin-bottom: 0.15rem;
    }}
    .kpi-sub {{
        font-size: 0.75rem;
        color: {TEXT_SUB};
    }}
    .ai-box {{
        background: #0F172A;
        border: 1px solid #223049;
        border-radius: 0.85rem;
        padding: 0.9rem 1rem;
        margin-bottom: 0.75rem;
    }}
    .ai-title {{
        font-weight: 800;
        font-size: 0.92rem;
        margin-bottom: 0.25rem;
    }}
    .ai-small {{
        font-size: 0.82rem;
        color: {TEXT_SUB};
    }}
    .ws-header {{
        background: #0F172A;
        border: 1px solid #223049;
        border-radius: 0.75rem;
        padding: 0.7rem 0.9rem;
        margin-bottom: 0.65rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# DATOS DUMMY
# =========================================================
def calificacion_to_score(calif: str) -> int:
    mapping = {"Muy bajo": 20, "Bajo": 40, "Medio": 60, "Alto": 80, "Muy alto": 95}
    return mapping.get(calif, 50)

def load_dummy_data():
    df_sites = pd.DataFrame([
        {"sitio": "Planta Mezclas Norte", "lat": 6.2518, "lon": -75.5636, "riesgo_global": "ALTO", "madurez_ccps": 58},
        {"sitio": "Terminal Almacenamiento Sur", "lat": 4.7110, "lon": -74.0721, "riesgo_global": "MEDIO", "madurez_ccps": 72},
        {"sitio": "Planta Reactores Oriente", "lat": 7.1193, "lon": -73.1227, "riesgo_global": "ALTO", "madurez_ccps": 63},
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

    # Diagnóstico CCPS (demo)
    diag_rows = []
    califs = ["Muy bajo", "Bajo", "Medio", "Alto", "Muy alto"]
    for i in range(1, 60):
        diag_rows.append({
            "id": f"D-{i:03d}",
            "pilar": np.random.choice(pilares),
            "elemento": np.random.choice(elementos),
            "instalacion": np.random.choice(sitios),
            "descripcion": f"Ítem de evaluación CCPS #{i}",
            "calificacion": np.random.choice(califs, p=[0.1, 0.2, 0.3, 0.25, 0.15]),
            "evidencia": "Documento / Registros / Entrevistas",
            "estado_plan": np.random.choice(["Sin plan", "En diseño", "En ejecución", "Cerrado"], p=[0.35, 0.25, 0.25, 0.15])
        })
    df_diag = pd.DataFrame(diag_rows)

    # Nodos (demo) — esto ahora se usa dentro del flujo de “Estudios”
    df_nodos = pd.DataFrame([
        {
            "id": "N-001",
            "tipo": "Nodo de proceso",
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
            "tipo": "Nodo de proceso",
            "instalacion": "Terminal Almacenamiento Sur",
            "unidad": "Área de tanques",
            "equipo": "TK-201-ESF",
            "descripcion": "Sobrellenado de tanque durante recepción y posible derrame inflamable.",
            "riesgo": "ALTO",
            "pilar": "Gestionar el riesgo",
            "relacionados": "D-011 | A-010"
        },
        {
            "id": "N-003",
            "tipo": "Nodo de proceso",
            "instalacion": "Planta Reactores Oriente",
            "unidad": "Reactor 2",
            "equipo": "R-202",
            "descripcion": "Reacción fuera de control con aumento de presión y temperatura.",
            "riesgo": "ALTO",
            "pilar": "Gestionar el riesgo",
            "relacionados": "D-020 | D-021"
        },
    ])

    # Estudios históricos (demo)
    df_estudios = pd.DataFrame([
        {
            "id_estudio": "E-001", "tipo": "HAZOP", "anio": 2019,
            "instalacion": "Planta Mezclas Norte", "unidad": "Reactor 1", "equipo": "R-101",
            "cobertura": "Alta", "estado": "Vigente",
            "accion_sugerida": "Revalidar enfocado en escenarios de sobrepresión.",
            "comentario": "HAZOP de detalle para operación normal y arranque."
        },
        {
            "id_estudio": "E-002", "tipo": "LOPA", "anio": 2020,
            "instalacion": "Planta Mezclas Norte", "unidad": "Reactor 1", "equipo": "R-101",
            "cobertura": "Media", "estado": "Vigente",
            "accion_sugerida": "Revisar supuestos de frecuencias y fallas de PSV.",
            "comentario": "LOPA para escenarios de sobrepresión y fallo de SIS."
        },
        {
            "id_estudio": "E-003", "tipo": "What-if", "anio": 2017,
            "instalacion": "Terminal Almacenamiento Sur", "unidad": "Área de tanques", "equipo": "TK-201-ESF",
            "cobertura": "Baja", "estado": "Obsoleto",
            "accion_sugerida": "No repetir completo, documentar decisiones previas.",
            "comentario": "What-if del arranque inicial del terminal."
        },
        {
            "id_estudio": "E-004", "tipo": "QRA", "anio": 2021,
            "instalacion": "Planta Reactores Oriente", "unidad": "Complejo de reactores", "equipo": "",
            "cobertura": "Alta", "estado": "Vigente",
            "accion_sugerida": "Usar como base para ordenamiento territorial y PEC.",
            "comentario": "Análisis cuantitativo de riesgo para toda la planta."
        },
    ])

    return df_sites, df_diag, df_nodos, df_estudios

df_sites, df_diag, df_nodos, df_estudios = load_dummy_data()

# =========================================================
# ESTADO GLOBAL
# =========================================================
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Campos del informe (para % avance)
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

def get_inf(name: str) -> str:
    return str(st.session_state.get(name, ""))

def set_inf(name: str, value: str):
    st.session_state[name] = value

# =========================================================
# KPIs / RESÚMENES
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
        return pd.DataFrame(columns=["Tema", "Nivel", "Pilar", "Instalación", "Impacto", "Plazo sugerido"])

    df = df_diag_filtrado.copy()
    df["score"] = df["calificacion"].apply(calificacion_to_score)
    df = df.sort_values("score").head(top_n)

    prioridades = []
    for _, row in df.iterrows():
        s = row["score"]
        if s <= 40:
            nivel, plazo, impacto = "Crítico", "0–3 meses", "Muy alto"
        elif s <= 60:
            nivel, plazo, impacto = "Importante", "3–6 meses", "Alto"
        else:
            nivel, plazo, impacto = "Mejorable", "6–12 meses", "Medio"

        prioridades.append({
            "Tema": row["descripcion"],
            "Nivel": nivel,
            "Pilar": row["pilar"],
            "Instalación": row["instalacion"],
            "Impacto": impacto,
            "Plazo sugerido": plazo
        })
    return pd.DataFrame(prioridades)

# =========================================================
# HERO
# =========================================================
def render_hero(instalacion_activa: str, perfil: str, modo: str):
    nombre = "todas las instalaciones" if instalacion_activa == "Todas" else instalacion_activa
    if perfil == "Gerencia":
        sub = f"Vista ejecutiva para {nombre}: riesgo, decisiones y cumplimiento."
    else:
        sub = f"Vista técnica para {nombre}: brechas, nodos, evidencias y planes."

    st.markdown(
        f"""
        <div class="hero-card">
          <div class="hero-title">SKUDO – Seguridad de procesos en una sola vista</div>
          <div class="hero-sub">{sub}</div>
          <div>
            <span class="badge-pill">Perfil: {perfil}</span>
            <span class="badge-pill">Modo: {modo}</span>
            <span class="badge-pill">IA (DEMO)</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def kpi_box(title: str, value: str, sub: str):
    st.markdown(
        f"""
        <div class="kpi">
          <div class="kpi-title">{title}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# PANTALLA 1: TABLERO
# =========================================================
def render_dashboard(instalacion_activa: str, perfil: str):
    render_hero(instalacion_activa, perfil, "Tablero")

    if instalacion_activa == "Todas":
        df_diag_f = df_diag.copy()
        df_nodos_f = df_nodos.copy()
        df_sites_f = df_sites.copy()
    else:
        df_diag_f = df_diag[df_diag["instalacion"] == instalacion_activa].copy()
        df_nodos_f = df_nodos[df_nodos["instalacion"] == instalacion_activa].copy()
        df_sites_f = df_sites[df_sites["sitio"] == instalacion_activa].copy()

    madurez = calcular_madurez_global(df_diag_f)
    crit = int(df_diag_f["calificacion"].isin(["Muy bajo", "Bajo"]).sum())
    escenarios_alto = int((df_nodos_f["riesgo"] == "ALTO").sum())

    total = len(df_diag_f)
    cerradas = int((df_diag_f["estado_plan"] == "Cerrado").sum()) if total > 0 else 0
    pct_cerradas = round(100 * cerradas / total, 1) if total > 0 else 0.0

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_box("Madurez CCPS", f"{madurez}%", "Promedio del diagnóstico")
    with c2: kpi_box("Escenarios ALTO", str(escenarios_alto), "Nodos críticos (demo)")
    if perfil == "Gerencia":
        cumplimiento_demo = max(0, min(100, round(100 - (crit / max(total, 1)) * 60, 1)))
        with c3: kpi_box("Cumplimiento (demo)", f"{cumplimiento_demo}%", "Aprox. por brechas críticas")
        with c4: kpi_box("Acciones cerradas", f"{pct_cerradas}%", "Cierre de plan (demo)")
    else:
        with c3: kpi_box("Brechas críticas", str(crit), "Muy bajo / Bajo")
        with c4: kpi_box("Acciones cerradas", f"{pct_cerradas}%", "Cierre de plan (demo)")

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">Top brechas y madurez por pilar</div>
          <div class="panel-header-sub">Resumen ejecutivo/técnico (demo)</div>
        </div>
        """, unsafe_allow_html=True
    )

    colL, colR = st.columns([1.2, 1.8])
    with colL:
        pr = prioridades_desde_diag(df_diag_f, top_n=8)
        st.dataframe(pr, use_container_width=True, hide_index=True)
    with colR:
        if not df_diag_f.empty:
            df_p = df_diag_f.copy()
            df_p["score"] = df_p["calificacion"].apply(calificacion_to_score)
            df_p = df_p.groupby("pilar", as_index=False)["score"].mean()
            chart = (
                alt.Chart(df_p)
                .mark_bar()
                .encode(
                    x=alt.X("pilar:N", title="Pilar"),
                    y=alt.Y("score:Q", title="Madurez (%)", scale=alt.Scale(domain=[0, 100])),
                    tooltip=["pilar", "score"]
                )
                .properties(height=260)
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Sin datos de diagnóstico (demo).")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">Mapa de instalaciones (demo)</div>
          <div class="panel-header-sub">Ubicación y riesgo global</div>
        </div>
        """, unsafe_allow_html=True
    )
    if not df_sites_f.empty:
        df_map = df_sites_f.rename(columns={"lat": "latitude", "lon": "longitude"})
        st.map(df_map[["latitude", "longitude"]])
        st.dataframe(df_sites_f[["sitio", "riesgo_global", "madurez_ccps"]], use_container_width=True, hide_index=True)
    else:
        st.info("No hay instalaciones para el filtro actual.")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# MOTOR “RECOMENDAR ESTUDIO” (reusa idea de nodos)
# =========================================================
def sugerir_estudio_y_estudios(contexto: dict, df_estudios_base: pd.DataFrame, df_nodos_base: pd.DataFrame):
    tipo_situacion = contexto.get("tipo_situacion", "")
    fase = contexto.get("fase", "")

    if tipo_situacion == "Nuevo proyecto / diseño":
        metodo = "What-if + checklist" if "Conceptual" in fase else "HAZOP completo"
        motivo = "Proyecto nuevo: exploración amplia o HAZOP según fase."
    elif tipo_situacion == "Cambio (MOC)":
        metodo = "Revalidación HAZOP / PHA focalizada"
        motivo = "Cambio: revalidar nodos impactados en vez de reiniciar."
    elif tipo_situacion == "Incidente / casi incidente":
        metodo = "Investigación + actualización PHA/HAZOP"
        motivo = "Incidente: investigar y capturar lecciones en PHA."
    else:
        metodo = "HAZOP focalizado"
        motivo = "Problema operativo: enfocar en desviaciones y salvaguardas del nodo."

    instalacion = contexto.get("instalacion", "Todas")
    unidad = (contexto.get("unidad") or "").strip().lower()
    equipo = (contexto.get("equipo") or "").strip().lower()
    desc = (contexto.get("descripcion") or "").strip().lower()

    # estudios relacionados (demo)
    df_rel = df_estudios_base.copy()
    if instalacion != "Todas":
        df_rel = df_rel[df_rel["instalacion"] == instalacion]
    if unidad:
        df_rel = df_rel[df_rel["unidad"].str.lower().str.contains(unidad, na=False)]
    if equipo:
        df_rel = df_rel[df_rel["equipo"].str.lower().str.contains(equipo, na=False)]
    if df_rel.empty:
        df_rel = df_estudios_base[df_estudios_base["instalacion"] == instalacion] if instalacion != "Todas" else df_estudios_base
        df_rel = df_rel.head(3)

    # nodos relacionados (demo por keywords)
    df_n = df_nodos_base.copy()
    if instalacion != "Todas":
        df_n = df_n[df_n["instalacion"] == instalacion]

    def score_row(row):
        text = (str(row.get("descripcion", "")) + " " + str(row.get("equipo", "")) + " " + str(row.get("unidad", ""))).lower()
        score = 0
        for token in desc.split():
            if len(token) >= 5 and token in text:
                score += 1
        if equipo and equipo in text:
            score += 2
        if unidad and unidad in text:
            score += 1
        return score

    if desc or unidad or equipo:
        df_n = df_n.copy()
        df_n["score"] = df_n.apply(score_row, axis=1)
        df_n_rel = df_n[df_n["score"] >= 2].copy()
        if df_n_rel.empty:
            df_n_rel = df_n.head(3).copy()
    else:
        df_n_rel = df_n.head(3).copy()

    nodos_rel_ids = df_n_rel["id"].tolist()

    texto = (
        f"**{metodo}**\n\n"
        f"**¿Por qué?** {motivo}\n\n"
        f"Se encontraron **{len(df_rel)}** estudios previos potencialmente relevantes."
    )

    return texto, metodo, motivo, df_rel, nodos_rel_ids

# =========================================================
# ESTUDIOS – FLUJO COMPLETO (lo que pediste)
# =========================================================
if "estudios_flow" not in st.session_state:
    st.session_state["estudios_flow"] = {"active_id": None, "items": {}}

def new_study_id() -> str:
    n = len(st.session_state["estudios_flow"]["items"]) + 1
    return f"ST-2025-{n:04d}"

def get_active_study() -> Optional[Dict[str, Any]]:
    sid = st.session_state["estudios_flow"]["active_id"]
    if not sid:
        return None
    return st.session_state["estudios_flow"]["items"].get(sid)

def ensure_study_struct(study: Dict[str, Any], instalacion_activa: str):
    study.setdefault("study_id", study.get("study_id") or new_study_id())
    study.setdefault("meta", {
        "cliente": "PROMIGAS",
        "titulo": "",
        "lider": "",
        "estado_sesion": "Borrador",
        "instalacion": instalacion_activa
    })
    study.setdefault("estado", "RECOMENDADO")  # RECOMENDADO|PREPARACION|PREFAB|CURACION|COMPLETAR|APROBADO|ASIGNADO
    study.setdefault("contexto_problema", {
        "instalacion": instalacion_activa,
        "unidad": "",
        "equipo": "",
        "tipo_situacion": "Problema recurrente / desviación operacional",
        "fase": "Operación",
        "descripcion": ""
    })
    study.setdefault("recomendacion", {"metodo": "", "motivo": ""})
    study.setdefault("preparacion", {"pid_files": [], "disciplinas": [], "participantes": ""})
    study.setdefault("historico_estudios", pd.DataFrame())
    study.setdefault("nodos_rel", pd.DataFrame())
    study.setdefault("hazop_by_nodo", {})  # {nodo_id: {"recomendacion_nodo":"", "rows":[...]}}
    study.setdefault("aprobacion", {"aprobado": False, "aprobador": "", "fecha": ""})
    study.setdefault("asignaciones", pd.DataFrame(columns=["id_row", "responsable", "fecha", "estado"]))
    study.setdefault("ai_log", [])

def log_ai(study: Dict[str, Any], msg: str):
    study["ai_log"].append({"ts": datetime.now().strftime("%H:%M:%S"), "msg": msg})

def build_prefab_hazop_from_nodos(nodos_df: pd.DataFrame, metodo: str) -> Dict[str, Any]:
    """
    Prefabricado DEMO: arma filas estilo HAZOP worksheet por nodo.
    """
    out: Dict[str, Any] = {}
    for _, n in nodos_df.iterrows():
        nid = n["id"]
        rec = (
            f"Enfocar el {metodo} en este nodo: validar desviaciones, salvaguardas y acciones. "
            f"Conectar con estudios previos y con plan de acción."
        )
        rows = [
            {
                "id_row": f"{nid}-R-001",
                "Nodo": f"{n.get('unidad','')} – {n.get('equipo','')}".strip(" – "),
                "Desviación": "Alta presión",
                "Causa": "Falla del transmisor / bloqueo aguas abajo (editable)",
                "Consecuencia": n.get("descripcion", ""),
                "Salvaguarda": "Alarma de alta presión + PSV + procedimiento (editable)",
                "Recomendación": ""
            },
            {
                "id_row": f"{nid}-R-002",
                "Nodo": f"{n.get('unidad','')} – {n.get('equipo','')}".strip(" – "),
                "Desviación": "Pérdida de contención",
                "Causa": "Corrosión / bridas / mantenimiento deficiente (editable)",
                "Consecuencia": n.get("descripcion", ""),
                "Salvaguarda": "Inspección + detección + contención (editable)",
                "Recomendación": ""
            },
        ]
        out[nid] = {"recomendacion_nodo": rec, "rows": rows}
    return out

def hazop_rows_to_df(hazop_by_nodo: Dict[str, Any]) -> pd.DataFrame:
    all_rows = []
    for nid, pack in hazop_by_nodo.items():
        for r in pack.get("rows", []):
            rr = r.copy()
            rr["id_nodo"] = nid
            all_rows.append(rr)
    cols = ["id_row","id_nodo","Nodo","Desviación","Causa","Consecuencia","Salvaguarda","Recomendación"]
    if not all_rows:
        return pd.DataFrame(columns=cols)
    df = pd.DataFrame(all_rows)
    # asegurar orden de columnas
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    return df[cols]

def render_estudios_flujo(instalacion_activa: str, perfil: str):
    render_hero(instalacion_activa, perfil, "Agente inteligente & Estudios")

    # selector / crear estudio
    topL, topR = st.columns([2.2, 1.0])
    with topL:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="panel-header">
              <div class="panel-header-title">Estudios (sesiones)</div>
              <div class="panel-header-sub">Crea y gestiona estudios con flujo completo</div>
            </div>
            """, unsafe_allow_html=True
        )

        existentes = list(st.session_state["estudios_flow"]["items"].keys())
        opciones = ["(Crear nuevo)"] + existentes

        idx = 0
        if st.session_state["estudios_flow"]["active_id"] in existentes:
            idx = existentes.index(st.session_state["estudios_flow"]["active_id"]) + 1

        sel = st.selectbox("Estudio activo", opciones, index=idx)
        cbtn1, cbtn2 = st.columns([1,1])
        with cbtn1:
            if sel == "(Crear nuevo)":
                if st.button("Crear estudio"):
                    sid = new_study_id()
                    st.session_state["estudios_flow"]["items"][sid] = {"study_id": sid}
                    st.session_state["estudios_flow"]["active_id"] = sid
                    st.rerun()
            else:
                st.session_state["estudios_flow"]["active_id"] = sel
        with cbtn2:
            if st.button("Reset flujo (solo este estudio)"):
                sid = st.session_state["estudios_flow"]["active_id"]
                if sid:
                    st.session_state["estudios_flow"]["items"][sid] = {"study_id": sid}
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    study = get_active_study()
    if not study:
        st.info("Crea un estudio para comenzar.")
        return
    ensure_study_struct(study, instalacion_activa)

    # Layout tipo tu mockup: izquierda worksheet / flujo, derecha asistente
    left, right = st.columns([2.25, 1.0], gap="large")

    # PANEL DERECHO: asistente + histórico
    with right:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("#### ASISTENTE IA SKUDO (DEMO)")
        st.caption(f"Estado del estudio: {study['estado']}")

        if study["ai_log"]:
            for e in study["ai_log"][-10:]:
                st.write(f"- {e['ts']} — {e['msg']}")
        else:
            st.write("— Aún no hay eventos. Ejecuta el paso 1 para iniciar.")

        st.markdown("---")
        st.markdown("#### Historial de estudios guardados")
        df_hist = df_estudios.copy()
        if instalacion_activa != "Todas":
            df_hist = df_hist[df_hist["instalacion"] == instalacion_activa]
        st.dataframe(
            df_hist[["id_estudio","tipo","anio","instalacion","unidad","equipo","estado","accion_sugerida"]],
            use_container_width=True,
            hide_index=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # IZQUIERDA: flujo
    with left:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)

        pasos = [
            "1) Estudio recomendado",
            "2) Preparación",
            "3) Estudio prefabricado",
            "4) Curación humana por nodo",
            "5) Completar estudio",
            "6) Aprobar",
            "7) Asignar y enviar"
        ]
        paso = st.radio("Flujo del estudio", pasos, horizontal=True)

        # Encabezado del modo (como tu imagen)
        meta = study["meta"]
        st.markdown(
            f"""
            <div class="ws-header">
                <div style="font-weight:900; font-size:1.05rem;">
                    HAZOP: {meta.get('titulo','(sin título)') or '(sin título)'} | 
                    Líder: {meta.get('lider','(sin líder)') or '(sin líder)'} | 
                    Estado: <span style="color:#22C55E;">{study['estado']}</span>
                </div>
                <div style="margin-top:0.3rem;">
                    <span class="chip">Cliente: {meta.get('cliente','')}</span>
                    <span class="chip">Instalación: {instalacion_activa}</span>
                    <span class="chip">Perfil: {perfil}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ===== PASO 1 =====
        if paso == "1) Estudio recomendado":
            st.markdown("### 1) Hay un estudio recomendado")
            ctx = study["contexto_problema"]

            cmeta1, cmeta2 = st.columns(2)
            with cmeta1:
                meta["titulo"] = st.text_input("Título del estudio", value=meta.get("titulo",""))
            with cmeta2:
                meta["lider"] = st.text_input("Líder / facilitador", value=meta.get("lider",""))

            ctx["descripcion"] = st.text_area(
                "Describe el problema o necesidad",
                value=ctx["descripcion"],
                height=120,
                placeholder="Ej: disparos frecuentes del PSV en R-101 cuando operamos cerca del máximo caudal…"
            )

            c1, c2 = st.columns(2)
            with c1:
                ctx["unidad"] = st.text_input("Unidad / área", value=ctx["unidad"])
            with c2:
                ctx["equipo"] = st.text_input("Equipo", value=ctx["equipo"])

            c3, c4 = st.columns(2)
            with c3:
                ctx["tipo_situacion"] = st.selectbox(
                    "Tipo de situación",
                    options=[
                        "Nuevo proyecto / diseño",
                        "Cambio (MOC)",
                        "Problema recurrente / desviación operacional",
                        "Incidente / casi incidente",
                        "Otro / no estoy seguro"
                    ],
                    index=2
                )
            with c4:
                ctx["fase"] = st.selectbox(
                    "Fase del ciclo de vida",
                    options=["Conceptual","Básico / FEED","Detalle","Operación","Desmantelamiento"],
                    index=3
                )

            if st.button("Sugerir estudio + traer estudios/nodos relacionados (DEMO)"):
                df_e = df_estudios.copy()
                df_n = df_nodos.copy()
                if instalacion_activa != "Todas":
                    df_e = df_e[df_e["instalacion"] == instalacion_activa]
                    df_n = df_n[df_n["instalacion"] == instalacion_activa]

                texto, metodo, motivo, df_rel, nodos_rel_ids = sugerir_estudio_y_estudios(ctx, df_e, df_n)

                study["recomendacion"]["metodo"] = metodo
                study["recomendacion"]["motivo"] = texto
                study["historico_estudios"] = df_rel

                df_n_rel = df_n[df_n["id"].isin(nodos_rel_ids)].copy()
                if df_n_rel.empty:
                    df_n_rel = df_n.head(3).copy()
                study["nodos_rel"] = df_n_rel

                study["estado"] = "PREPARACION"
                log_ai(study, "Recomendación generada + estudios históricos + nodos relacionados cargados.")

            st.markdown("**Recomendación (editable):**")
            study["recomendacion"]["metodo"] = st.text_input("Método recomendado", value=study["recomendacion"]["metodo"])
            study["recomendacion"]["motivo"] = st.text_area("Motivo", value=study["recomendacion"]["motivo"], height=140)

            if st.button("Continuar a preparación"):
                study["estado"] = "PREPARACION"
                log_ai(study, "Paso 1 cerrado → preparación.")

        # ===== PASO 2 =====
        elif paso == "2) Preparación":
            st.markdown("### 2) Preparación para el estudio (PID, disciplinas, equipo)")

            files = st.file_uploader(
                "Cargar P&ID / documentos base (PDF/PNG/JPG)",
                accept_multiple_files=True,
                type=["pdf","png","jpg","jpeg"]
            )
            if files:
                for f in files:
                    study["preparacion"]["pid_files"].append({"name": f.name, "size": f.size})
                log_ai(study, f"Se cargaron {len(files)} documento(s) base.")

            study["preparacion"]["disciplinas"] = st.multiselect(
                "Disciplinas",
                ["Proceso","Operación","Mantenimiento","Instrumentación","Eléctrica","HSE","Integridad mecánica","Contratistas"],
                default=study["preparacion"]["disciplinas"]
            )
            study["preparacion"]["participantes"] = st.text_area(
                "Participantes (texto libre)",
                value=study["preparacion"]["participantes"],
                height=90,
                placeholder="Ej: Carlos Ruiz (Proceso), Ana Pérez (Operación)…"
            )

            st.markdown("---")
            st.markdown("**Nodos relacionados que se van a trabajar:**")
            if study["nodos_rel"].empty:
                st.warning("No hay nodos cargados. Vuelve al paso 1 y ejecuta la sugerencia.")
            else:
                st.dataframe(
                    study["nodos_rel"][["id","instalacion","unidad","equipo","riesgo","descripcion"]],
                    use_container_width=True,
                    hide_index=True
                )

            if st.button("Preparación completa → Generar prefabricado HAZOP"):
                study["estado"] = "PREFAB"
                log_ai(study, "Preparación completa → listo para prefabricado.")

        # ===== PASO 3 =====
        elif paso == "3) Prefabricado (HAZOP)":
            st.markdown("### 3) Prefabricado del estudio (HAZOP Worksheet)")

            if study["nodos_rel"].empty:
                st.warning("No hay nodos. Vuelve al paso 1/2.")
            else:
                nodos_ids = study["nodos_rel"]["id"].tolist()
                include = st.multiselect("Nodos a incluir", nodos_ids, default=nodos_ids)

                if st.button("Generar estudio con SKUDO"):
                    df_sel = study["nodos_rel"][study["nodos_rel"]["id"].isin(include)].copy()
                    metodo = study["recomendacion"]["metodo"] or "HAZOP"
                    study["hazop_by_nodo"] = build_prefab_hazop_from_nodos(df_sel, metodo=metodo)
                    study["estado"] = "CURACION"
                    log_ai(study, f"Prefabricado HAZOP generado para {len(include)} nodo(s).")

                st.markdown("---")
                st.markdown("**Vista previa consolidada del worksheet:**")
                df_ws = hazop_rows_to_df(study["hazop_by_nodo"])
                st.dataframe(df_ws, use_container_width=True, hide_index=True)

        # ===== PASO 4 =====
        elif paso == "4) Curación humana por nodo":
            st.markdown("### 4) Curación humana por nodo")
            st.markdown("<div class='section-sub'>El humano define qué aplica por nodo: edita, agrega o quita filas.</div>", unsafe_allow_html=True)

            if not study["hazop_by_nodo"]:
                st.warning("No hay prefabricado. Ve al paso 3.")
            else:
                # Selector nodo
                nodos = list(study["hazop_by_nodo"].keys())
                nid = st.selectbox("Nodo", nodos)
                pack = study["hazop_by_nodo"][nid]

                # Recomendación por nodo editable
                pack["recomendacion_nodo"] = st.text_area(
                    "Recomendación para este nodo (editable)",
                    value=pack.get("recomendacion_nodo",""),
                    height=90
                )

                # Worksheet por nodo (editor)
                df_n = pd.DataFrame(pack["rows"])
                st.markdown("**HAZOP Worksheet (solo este nodo)**")
                df_n_edit = st.data_editor(
                    df_n,
                    use_container_width=True,
                    num_rows="dynamic",
                    hide_index=True,
                    key=f"hazop_node_{nid}"
                )
                pack["rows"] = df_n_edit.to_dict(orient="records")

                # Panel rápido de “sugerencias IA” (DEMO) tipo tu mockup
                st.markdown("---")
                st.markdown("**Sugerencia IA (DEMO) para la fila seleccionada**")
                st.caption("Esto simula tu panel: similitud histórica + recomendación y botones.")

                # elegimos una fila (si existe)
                if not df_n_edit.empty:
                    row_pick = st.selectbox(
                        "Selecciona fila para sugerencia",
                        options=df_n_edit["id_row"].tolist(),
                        index=0
                    )
                    sug = (
                        "Inteligencia Histórica Detectada: escenario 92% similar a uno ocurrido en ‘Planta Cartagena (2022)’. "
                        "Sugerencia: evaluar trazado eléctrico en líneas de impulso para evitar congelamiento/obstrucción."
                    )
                    st.markdown(f"<div class='ai-box'><div class='ai-title'>{sug}</div><div class='ai-small'>Normas cruzadas (demo): NFPA 59A, ASME B31.8 chequeadas.</div></div>", unsafe_allow_html=True)

                    b1, b2, b3 = st.columns(3)
                    with b1:
                        if st.button("Aceptar sugerencia"):
                            # aplicarla a recomendación de esa fila
                            for r in pack["rows"]:
                                if r.get("id_row") == row_pick:
                                    r["Recomendación"] = "Evaluar trazado eléctrico en líneas de impulso para evitar congelamiento/obstrucción."
                            log_ai(study, f"Sugerencia aceptada en {row_pick}.")
                            st.rerun()
                    with b2:
                        if st.button("Editar sugerencia"):
                            # no hace nada sofisticado; deja listo el campo en la tabla
                            log_ai(study, f"Sugerencia marcada para edición en {row_pick}.")
                            st.info("Edita directamente la celda 'Recomendación' en la tabla.")
                    with b3:
                        if st.button("Ignorar"):
                            log_ai(study, f"Sugerencia ignorada en {row_pick}.")
                            st.success("Ignorada (DEMO).")

                cadd, cnext = st.columns([1,1])
                with cadd:
                    if st.button("Agregar fila manual"):
                        pack["rows"].append({
                            "id_row": f"{nid}-R-{len(pack['rows'])+1:03d}",
                            "Nodo": "",
                            "Desviación": "",
                            "Causa": "",
                            "Consecuencia": "",
                            "Salvaguarda": "",
                            "Recomendación": ""
                        })
                        log_ai(study, f"Fila manual agregada en {nid}.")
                        st.rerun()
                with cnext:
                    if st.button("Curación lista → Completar estudio"):
                        study["estado"] = "COMPLETAR"
                        log_ai(study, "Curación finalizada → completar estudio.")

        # ===== PASO 5 =====
        elif paso == "5) Completar estudio":
            st.markdown("### 5) Completar el estudio (consolidado)")

            df_ws = hazop_rows_to_df(study["hazop_by_nodo"])
            if df_ws.empty:
                st.warning("No hay filas. Vuelve al paso 3/4.")
            else:
                vacias = df_ws[df_ws["Recomendación"].fillna("").str.strip() == ""]
                st.markdown(f"- Filas totales: **{len(df_ws)}**")
                st.markdown(f"- Filas sin recomendación: **{len(vacias)}**")

                st.dataframe(df_ws, use_container_width=True, hide_index=True)

                if st.button("Marcar como listo para aprobación"):
                    study["estado"] = "APROBADO"
                    log_ai(study, "Listo para aprobación.")

        # ===== PASO 6 =====
        elif paso == "6) Aprobar":
            st.markdown("### 6) Aprobación del estudio")

            study["aprobacion"]["aprobador"] = st.text_input("Aprobador", value=study["aprobacion"]["aprobador"])
            study["aprobacion"]["fecha"] = st.text_input("Fecha (YYYY-MM-DD)", value=study["aprobacion"]["fecha"])
            study["aprobacion"]["aprobado"] = st.checkbox("Aprobado", value=study["aprobacion"]["aprobado"])

            if st.button("Guardar aprobación"):
                if study["aprobacion"]["aprobado"]:
                    study["estado"] = "ASIGNADO"
                    log_ai(study, "Estudio aprobado → asignación y envío.")
                    st.success("Aprobado (DEMO).")
                else:
                    log_ai(study, "Aprobación guardada (aún no aprobado).")
                    st.info("Guardado.")

        # ===== PASO 7 =====
        else:
            st.markdown("### 7) Asignar responsables + fechas + enviar recomendaciones")

            df_ws = hazop_rows_to_df(study["hazop_by_nodo"])
            if df_ws.empty:
                st.warning("No hay filas para asignar.")
            else:
                df_to_assign = df_ws[df_ws["Recomendación"].fillna("").str.strip() != ""].copy()
                if df_to_assign.empty:
                    st.warning("No hay recomendaciones diligenciadas. Vuelve al paso 4/5.")
                else:
                    st.markdown("**Recomendaciones a asignar (solo con recomendación):**")
                    st.dataframe(
                        df_to_assign[["id_row","id_nodo","Desviación","Causa","Recomendación"]],
                        use_container_width=True,
                        hide_index=True
                    )

                    if study["asignaciones"].empty or len(study["asignaciones"]) != len(df_to_assign):
                        study["asignaciones"] = pd.DataFrame({
                            "id_row": df_to_assign["id_row"].tolist(),
                            "responsable": [""] * len(df_to_assign),
                            "fecha": [""] * len(df_to_assign),
                            "estado": ["Pendiente"] * len(df_to_assign)
                        })

                    st.caption("Completa responsable y fecha por recomendación.")
                    asign = st.data_editor(
                        study["asignaciones"],
                        use_container_width=True,
                        hide_index=True,
                        num_rows="fixed",
                        key="asig_editor"
                    )
                    study["asignaciones"] = asign

                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Guardar asignaciones"):
                            log_ai(study, "Asignaciones guardadas.")
                            st.success("Asignaciones guardadas (DEMO).")
                    with c2:
                        if st.button("Enviar recomendaciones (DEMO)"):
                            log_ai(study, "Recomendaciones enviadas a responsables (DEMO).")
                            st.success("Enviado (DEMO).")

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# PANTALLA 3: ANÁLISIS DE RIESGOS (separado del flujo)
# =========================================================
def render_analisis_riesgos(instalacion_activa: str, perfil: str):
    render_hero(instalacion_activa, perfil, "Análisis de riesgos")

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">Mapa de riesgo (DEMO)</div>
          <div class="panel-header-sub">Severidad vs Frecuencia (ejemplo)</div>
        </div>
        """, unsafe_allow_html=True
    )

    # demo dataset rápido
    data = []
    np.random.seed(7)
    for i in range(1, 16):
        sev = np.random.randint(1, 6)
        fre = np.random.randint(1, 6)
        rr = sev * fre
        data.append({
            "Escenario": f"RP-{i:03d}",
            "Severidad": sev,
            "Frecuencia": fre,
            "Riesgo_residual": rr,
            "Nivel": "Alto" if rr >= 12 else ("Medio" if rr >= 8 else "Bajo")
        })
    df_rp = pd.DataFrame(data)

    chart = (
        alt.Chart(df_rp)
        .mark_circle()
        .encode(
            x=alt.X("Frecuencia:Q", scale=alt.Scale(domain=[0.5, 5.5])),
            y=alt.Y("Severidad:Q", scale=alt.Scale(domain=[0.5, 5.5])),
            size=alt.Size("Riesgo_residual:Q"),
            color=alt.Color("Nivel:N"),
            tooltip=["Escenario","Severidad","Frecuencia","Riesgo_residual","Nivel"]
        )
        .properties(height=360)
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("---")
    st.markdown("**Tabla de escenarios (DEMO)**")
    st.dataframe(df_rp, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# PANTALLA 4: INFORME
# =========================================================
def render_informe():
    render_hero("—", "—", "Informe de Seguridad (DEMO)")

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">Informe de Seguridad</div>
          <div class="panel-header-sub">Construcción guiada + % avance</div>
        </div>
        """, unsafe_allow_html=True
    )

    paso = st.radio(
        "Secciones del informe",
        ["1. Conocimiento del riesgo", "2. Reducción del riesgo", "3. Manejo del desastre", "4. Anexos"],
        horizontal=True
    )

    c1, c2 = st.columns([2, 1])

    with c2:
        st.markdown("#### Asistente del informe (DEMO)")
        st.caption("Autocompleta texto demo y calcula avance.")

        if paso == "1. Conocimiento del riesgo":
            if st.button("Autocompletar sección 1 (demo)"):
                set_inf("inf_1_desc_instalacion", "Instalación dedicada a almacenamiento y manejo de sustancias peligrosas, operación 24/7.")
                set_inf("inf_1_contexto_ext", "Zona industrial con presencia de comunidades cercanas.")
                set_inf("inf_1_contexto_int", "Procesos de recepción, almacenamiento y despacho.")
                set_inf("inf_1_peligros", "Escenarios: fuga, incendio y explosión identificados mediante PHA/HAZOP y QRA.")
        elif paso == "2. Reducción del riesgo":
            if st.button("Autocompletar sección 2 (demo)"):
                set_inf("inf_2_medidas_prev", "Detección de gas, protección contra incendio, controles de ingeniería y procedimientos.")
                set_inf("inf_2_proteccion_fin", "Pólizas de seguro y reservas para contingencias.")
        elif paso == "3. Manejo del desastre":
            if st.button("Autocompletar sección 3 (demo)"):
                set_inf("inf_3_manejo_desastre", "PEC aprobado, coordinación con autoridades y simulacros periódicos.")
        else:
            if st.button("Autocompletar anexos (demo)"):
                set_inf("inf_4_ot", "Insumos para ordenamiento territorial con escenarios de afectación.")
                set_inf("inf_4_pec", "PEC actualizado y anexado.")
                set_inf("inf_4_adicional", "Isocontornos de riesgo y planos de equipos críticos.")

        st.markdown("---")
        total_campos = len(INF_FIELDS)
        campos_llenos = sum(1 for name in INF_FIELDS if get_inf(name).strip())
        avance = int((campos_llenos / total_campos) * 100) if total_campos else 0
        st.markdown(f"**Campos diligenciados:** {campos_llenos} de {total_campos}")
        st.progress(avance / 100, text=f"{avance}% completado (aprox.)")

    with c1:
        if paso == "1. Conocimiento del riesgo":
            st.subheader("1. Conocimiento del riesgo")
            v1 = st.text_input("Descripción general de la instalación", value=get_inf("inf_1_desc_instalacion"))
            set_inf("inf_1_desc_instalacion", v1)
            v2 = st.text_area("Contexto externo", value=get_inf("inf_1_contexto_ext"), height=90)
            set_inf("inf_1_contexto_ext", v2)
            v3 = st.text_area("Contexto interno", value=get_inf("inf_1_contexto_int"), height=90)
            set_inf("inf_1_contexto_int", v3)
            v4 = st.text_area("Identificación de peligros", value=get_inf("inf_1_peligros"), height=120)
            set_inf("inf_1_peligros", v4)

        elif paso == "2. Reducción del riesgo":
            st.subheader("2. Reducción del riesgo")
            v5 = st.text_area("Medidas de prevención y mitigación", value=get_inf("inf_2_medidas_prev"), height=130)
            set_inf("inf_2_medidas_prev", v5)
            v6 = st.text_area("Protección financiera", value=get_inf("inf_2_proteccion_fin"), height=90)
            set_inf("inf_2_proteccion_fin", v6)

        elif paso == "3. Manejo del desastre":
            st.subheader("3. Manejo del desastre")
            v7 = st.text_area("Preparación y atención de emergencias", value=get_inf("inf_3_manejo_desastre"), height=160)
            set_inf("inf_3_manejo_desastre", v7)

        else:
            st.subheader("4. Anexos")
            v8 = st.text_area("Ordenamiento territorial", value=get_inf("inf_4_ot"), height=80)
            set_inf("inf_4_ot", v8)
            v9 = st.text_area("PEC", value=get_inf("inf_4_pec"), height=80)
            set_inf("inf_4_pec", v9)
            v10 = st.text_area("Adicional", value=get_inf("inf_4_adicional"), height=90)
            set_inf("inf_4_adicional", v10)

    st.markdown("---")
    st.button("Generar borrador (PDF/Word) – DEMO")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# PANTALLA 5: MI AGENTE SKUDO (chat simple)
# =========================================================
def respuesta_dummy_chat(user_msg: str) -> str:
    return (
        "🔧 **DEMO de SKUDO**\n\n"
        "Este chat es un mockup. En la versión completa, responderá con base en diagnóstico CCPS, "
        "estudios (HAZOP/LOPA/QRA), nodos y el informe.\n\n"
        f"Tu mensaje:\n> {user_msg}\n"
    )

def render_agente_skudo(instalacion_activa: str, perfil: str):
    render_hero(instalacion_activa, perfil, "Mi Agente SKUDO")

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">Chat con SKUDO (DEMO)</div>
          <div class="panel-header-sub">Mensajes guardados en session_state</div>
        </div>
        """, unsafe_allow_html=True
    )

    # historial
    for role, msg, ts in st.session_state["chat_history"]:
        who = "Tú" if role == "user" else "SKUDO"
        st.markdown(f"**{who} ({ts})**")
        st.markdown(msg)
        st.markdown("---")

    user_msg = st.text_input("Escribe tu pregunta o comentario (DEMO)", "")
    if st.button("Enviar"):
        if user_msg.strip():
            ts = datetime.now().strftime("%H:%M:%S")
            st.session_state["chat_history"].append(("user", user_msg, ts))
            st.session_state["chat_history"].append(("assistant", respuesta_dummy_chat(user_msg), datetime.now().strftime("%H:%M:%S")))
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# SIDEBAR / NAVEGACIÓN (ORDEN PEDIDO)
# =========================================================
with st.sidebar:
    st.markdown("## SKUDO")
    st.caption("Módulo seguridad de procesos – Soluquim (DEMO)")

    perfil = st.selectbox("Perfil de vista", ["Gerencia", "Técnico / HSE"], index=0)

    instalaciones_opts = ["Todas"] + df_sites["sitio"].tolist()
    instalacion_activa = st.selectbox("Instalación activa", instalaciones_opts, index=0)

    st.markdown("---")
    menu = st.radio(
        "Navegación",
        options=[
            "Tablero",
            "Estudios con SKUDO",
            "Análisis de riesgos",
            "Informe",
            "Mi Agente SKUDO"
        ],
        index=0
    )

# =========================================================
# ROUTER (ORDEN PEDIDO)
# =========================================================
if menu == "Tablero":
    render_dashboard(instalacion_activa, perfil)
elif menu == "Estudios con SKUDO":
    render_estudios_flujo(instalacion_activa, perfil)
elif menu == "Análisis de riesgos":
    render_analisis_riesgos(instalacion_activa, perfil)
elif menu == "Informe":
    render_informe()
else:
    render_agente_skudo(instalacion_activa, perfil)
