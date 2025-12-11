import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

import matplotlib.pyplot as plt
import networkx as nx  # pip install networkx

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
        padding-top: 0.5rem;
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
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("**Madurez CCPS promedio**")
        st.markdown(f"<h3 style='margin:0.2rem 0'>{madurez_global}%</h3>", unsafe_allow_html=True)
        st.caption("Promedio ponderado de calificaciones del diagnóstico.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("**Escenarios de riesgo ALTO**")
        st.markdown(f"<h3 style='margin:0.2rem 0'>{n_escenarios_alto}</h3>", unsafe_allow_html=True)
        st.caption("Escenarios críticos identificados en nodos (demo).")
        st.markdown("</div>", unsafe_allow_html=True)

    if perfil == "Gerencia":
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("**Cumplimiento normativo (demo)**")
            st.markdown(f"<h3 style='margin:0.2rem 0'>{cumplimiento_3687}%</h3>", unsafe_allow_html=True)
            st.caption("Aproximación con base en brechas críticas del diagnóstico.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("**Nivel de riesgo global**")
            st.markdown(f"<h3 style='margin:0.2rem 0'>{etiqueta_riesgo}</h3>", unsafe_allow_html=True)
            st.caption("Clasificación cualitativa según instalaciones seleccionadas.")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("**Brechas críticas abiertas**")
            st.markdown(f"<h3 style='margin:0.2rem 0'>{n_brechas_criticas}</h3>", unsafe_allow_html=True)
            st.caption("Ítems con calificación Muy bajo / Bajo.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("**Acciones cerradas (demo)**")
            st.markdown(f"<h3 style='margin:0.2rem 0'>{porcentaje_cerradas}%</h3>", unsafe_allow_html=True)
            st.caption("Porcentaje de ítems marcados como 'Cerrado'.")
            st.markdown("</div>", unsafe_allow_html=True)

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
    st.markdown("### Nodos & Estudios – Asistente de estudios y grafo (DEMO)")

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
        tipo_default = st.session_state.get("problema_tipo_situacion", "Problema recurrente / desviación operacional")
        fase_default = st.session_state.get("problema_fase", "Operación")

        desc = st.text_area(
            "Describe brevemente el problema o necesidad",
            value=desc_default,
            height=120,
            placeholder="Ejemplo: 'Tenemos disparos frecuentes del PSV en el reactor R-101 cuando estamos cerca del máximo caudal de alimentación.'",
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
            texto, df_est_rel, nodos_rel_ids = sugerir_estudio_y_estudios(contexto, df_e_base, df_n_base)
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
        if unidad_default:
            st.markdown(f"<span class='chip'>Unidad: {unidad_default}</span>", unsafe_allow_html=True)
        if equipo_default:
            st.markdown(f"<span class='chip'>Equipo: {equipo_default}</span>", unsafe_allow_html=True)

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
    # BLOQUE C – Nodos & grafo de relaciones
    # =====================================================
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-header">
          <div class="panel-header-title">3. Nodos & relaciones entre escenarios, acciones y requisitos (DEMO)</div>
          <div class="panel-header-sub">
            Visualiza cómo se conectan escenarios de riesgo, acciones del plan y requisitos normativos.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    colf1, colf2, colf3 = st.columns(3)
    with colf1:
        tipo_sel = st.selectbox(
            "Tipo de nodo",
            ["Todos"] + sorted(df_n_base["tipo"].unique().tolist())
        )
    with colf2:
        riesgo_sel = st.selectbox(
            "Riesgo",
            ["Todos"] + sorted(df_n_base["riesgo"].unique().tolist())
        )
    with colf3:
        modo_sel = st.selectbox(
            "Modo de vista",
            ["Lista", "Relaciones (grafo demo)"],
            index=1
        )

    df_f = df_n_base.copy()
    if tipo_sel != "Todos":
        df_f = df_f[df_f["tipo"] == tipo_sel]
    if riesgo_sel != "Todos":
        df_f = df_f[df_f["riesgo"] == riesgo_sel]

    st.markdown("---")

    nodos_relevantes_ids = st.session_state.get("nodos_relevantes_ids", [])

    if modo_sel == "Lista":
        if df_f.empty:
            st.info("No hay nodos para mostrar con los filtros actuales (DEMO).")
        else:
            st.dataframe(df_f, use_container_width=True, hide_index=True)
    else:
        c1, c2 = st.columns([2, 1])

        with c1:
            st.markdown('<div class="section-title">Relaciones entre nodos (grafo demo)</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-sub">Los nodos resaltados están relacionados con el problema descrito.</div>',
                unsafe_allow_html=True
            )

            if df_f.empty:
                st.info("No hay nodos para mostrar con los filtros actuales (DEMO).")
            else:
                G = nx.Graph()
                main_ids = df_f["id"].tolist()

                for _, row in df_f.iterrows():
                    main_id = row["id"]
                    G.add_node(main_id, tipo=row["tipo"], riesgo=row["riesgo"])

                    rels = [r.strip() for r in str(row["relacionados"]).split("|") if r.strip()]
                    for rel in rels:
                        if rel not in G:
                            G.add_node(rel, tipo="Relacionado", riesgo="N/A")
                        G.add_edge(main_id, rel)

                pos = nx.spring_layout(G, k=0.8, seed=42)
                fig, ax = plt.subplots(figsize=(7, 5))

                node_colors = []
                node_sizes = []
                for n in G.nodes():
                    if n in nodos_relevantes_ids:
                        # Nodos destacados por el agente
                        node_colors.append(SECONDARY)
                        node_sizes.append(900)
                    elif n in main_ids:
                        # Nodos principales filtrados
                        node_colors.append(PRIMARY)
                        node_sizes.append(700)
                    else:
                        # Nodos relacionados (por ejemplo, IDs de diagnóstico, requisitos)
                        node_colors.append(ACCENT)
                        node_sizes.append(400)

                nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.3)
                nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, ax=ax)
                nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
                ax.axis("off")
                st.pyplot(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="section-title">Detalle de nodo (simulación de clic)</div>', unsafe_allow_html=True)
            if df_f.empty:
                st.info("No hay nodos para mostrar (DEMO).")
            else:
                nodo_sel = st.selectbox("Selecciona un nodo principal", options=df_f["id"].tolist())
                nodo_row = df_f[df_f["id"] == nodo_sel].iloc[0]

                destacado = "Sí" if nodo_sel in nodos_relevantes_ids else "No"

                st.markdown(f"**{nodo_row['id']} – {nodo_row['tipo']} ({nodo_row['riesgo']})**")
                st.write(f"- Instalación: `{nodo_row['instalacion']}`")
                st.write(f"- Unidad: `{nodo_row.get('unidad', '')}`")
                st.write(f"- Equipo: `{nodo_row.get('equipo', '')}`")
                st.write(f"- Pilar asociado: `{nodo_row['pilar']}`")
                st.write(f"- Relacionado con el problema actual (DEMO): **{destacado}**")
                st.write(f"- Descripción: {nodo_row['descripcion']}")

                rels = [r.strip() for r in str(nodo_row["relacionados"]).split("|") if r.strip()]
                st.markdown("**Nodos relacionados (diagnóstico, acción, requisito):**")
                for r in rels:
                    st.write(f"- {r}")

                st.info(
                    "DEMO: piensa esto como si hubieras hecho clic en el nodo del grafo. "
                    "En la versión completa, aquí se integraría el detalle del PHA, "
                    "planes de acción y requisitos normativos vinculados, además del vínculo al Informe de Seguridad."
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
            "Diagnóstico CCPS",
            "Nodos & Estudios",
            "Informe de Seguridad",
            "Mi Agente SKUDO"
        ]
    )

# =========================================================
# ROUTER
# =========================================================
if menu == "Tablero de control":
    render_dashboard(instalacion_activa, perfil)
elif menu == "Diagnóstico CCPS":
    render_diagnostico(instalacion_activa, perfil)
elif menu == "Nodos & Estudios":
    render_nodos(instalacion_activa)
elif menu == "Informe de Seguridad":
    render_informe()
else:
    render_agente(instalacion_activa, perfil)
