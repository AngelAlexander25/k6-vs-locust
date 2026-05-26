import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Reporte de Rendimiento",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #F7F5FF;
    color: #111111;
}
.stApp { background-color: #F7F5FF; }

/* ── TÍTULOS EN NEGRO ─────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6 {
    color: #111111 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── TABS ─────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF;
    border-bottom: 1px solid #E8E4F8;
    gap: 0;
    border-radius: 12px 12px 0 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    color: #5A5570;
    padding: 12px 22px;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: #4A3FB8 !important;
    border-bottom: 2px solid #6B5CE7 !important;
    background: transparent !important;
}

/* ── KPIs ─────────────────────────────────────────────────────── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
}
@media (max-width: 900px) {
    .kpi-grid {
        grid-template-columns: 1fr;
    }
}
.kpi-card {
    background: #FFFFFF;
    border: 2px solid #111111;
    border-top: 6px solid #111111;
    border-radius: 20px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.10);
    padding: 18px 20px;
    min-height: 112px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    inset: 0 auto 0 0;
    width: 6px;
    background: #111111;
}
.kpi-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #111111;
    margin-bottom: 10px;
}
.kpi-value {
    font-family: 'Inter', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #111111;
    line-height: 1.2;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 30px rgba(0,0,0,0.16);
}

/* Ocultar UI sobrante de Streamlit */
footer, #MainMenu, header { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── PALETA ─────────────────────────────────────────────────────────
BG      = "#F7F5FF"
WHITE   = "#FFFFFF"
PURPLE  = "#6B5CE7"
PURPLE2 = "#A89DF0"
MINT    = "#2ECC9A"
CORAL   = "#FF6B8A"
PEACH   = "#FF9F6B"
SKY     = "#5B9CF6"
LAVENDER= "#C4B8FF"
TEXT    = "#111111"
MUTED   = "#4A4560"
BORDER  = "#EAE6FF"

BASE = dict(
    paper_bgcolor=BG,
    plot_bgcolor="#FAF8FF",
    font=dict(family="Inter, sans-serif", color=TEXT, size=12),
    xaxis=dict(showgrid=False, zeroline=False,
               tickfont=dict(size=12, color=TEXT), linecolor=BORDER),
    yaxis=dict(gridcolor=BORDER, zeroline=False,
               tickfont=dict(size=12, color=TEXT), linecolor=BORDER),
    margin=dict(l=16, r=16, t=70, b=20),
)


def callout(texto, color=PURPLE):
    st.markdown(f"""
    <div style="background:#F1ECFF;border-left:4px solid {color};
                padding:14px 18px;border-radius:0 10px 10px 0;
                font-size:0.85rem;color:#111111;line-height:1.7;
                margin-bottom:20px;box-shadow:0 2px 8px rgba(107,92,231,0.04);">
      {texto}
    </div>
    """, unsafe_allow_html=True)


def card(titulo, cuerpo, color=PURPLE):
    st.markdown(f"""
    <div style="background:#F3EEFF;border-left:4px solid {color};
                padding:16px 18px;border-radius:0 10px 10px 0;
                margin-bottom:12px;box-shadow:0 2px 8px rgba(0,0,0,0.03);">
        <div style="font-weight:700;font-size:0.95rem;color:#111111;margin-bottom:6px;">{titulo}</div>
        <div style="font-size:0.83rem;color:#111111;line-height:1.7;">{cuerpo}</div>
    </div>
    """, unsafe_allow_html=True)


def tabla_html(df, columnas_centradas=None):
    if columnas_centradas is None:
        columnas_centradas = []

    headers = df.columns.tolist()

    html = """
    <div style="background:#FFFFFF;border:1px solid #DDD6FA;border-radius:12px;
                overflow:hidden;box-shadow:0 2px 8px rgba(107,92,231,0.05);
                margin-bottom:18px;font-family:Inter,sans-serif;">
      <table style="width:100%;border-collapse:collapse;font-size:0.85rem;">
        <thead>
          <tr style="background:#F1ECFF;">
    """
    for h in headers:
        align = "center" if h in columnas_centradas else "left"
        html += (
            f'<th style="padding:12px 14px;text-align:{align};color:#111111;'
            f'font-weight:700;border-bottom:2px solid #DDD6FA;font-size:0.78rem;'
            f'letter-spacing:0.02em;">{h}</th>'
        )
    html += "</tr></thead><tbody>"

    for i, row in df.iterrows():
        bg = "#FAF8FF" if i % 2 == 1 else "#FFFFFF"
        html += f'<tr style="background:{bg};">'
        for h in headers:
            cell = row[h]
            align = "center" if h in columnas_centradas else "left"
            valor = str(cell)
            color_cell = "#111111"
            font_weight = "400"
            if valor.strip() in ("Sí", "Si"):
                color_cell = "#1A8C66"
                font_weight = "600"
            elif valor.strip() == "No":
                color_cell = "#C04A6B"
                font_weight = "600"
            elif valor.startswith("Sí,") or valor.startswith("Si,"):
                color_cell = "#B8860B"
                font_weight = "600"
            elif valor.startswith("No,"):
                color_cell = "#C04A6B"
                font_weight = "600"

            html += (
                f'<td style="padding:11px 14px;text-align:{align};color:{color_cell};'
                f'font-weight:{font_weight};border-bottom:1px solid #F0EDFB;">{valor}</td>'
            )
        html += "</tr>"
    html += "</tbody></table></div>"

    st.markdown(html, unsafe_allow_html=True)


# ── DATOS ──────────────────────────────────────────────────────────
loc_labels = ["7 usuarios", "25 usuarios", "50 usuarios", "100 usuarios"]
loc_users  = [7, 25, 50, 100]

loc_err_rate = [8.6, 72.8, 77.4, 87.5]

loc_cm_p50 = [1, 1, 1, 1]
loc_cm_p95 = [3, 4, 3, 4]
loc_cm_max = [12, 32, 11, 27]

loc_ps_p50 = [1, 1, 1, 1]
loc_ps_p95 = [3, 3, 3, 4]
loc_ps_max = [11, 29, 16, 24]

loc_total_req = [561, 2412, 2521, 15012]

pruebas_k6 = ["7 usuarios", "25 usuarios", "50 usuarios", "100 usuarios"]
vus_k6     = [7, 25, 50, 100]

k6_cm_p95  = [302, 856, 5880, 5240]
k6_ps_p95  = [204, 682, 4150, 5420]
k6_checks  = [100.0, 99.75, 85.49, 79.26]
k6_cm_lt1  = [100, 98, 35, 16]
k6_ps_lt1  = [100, 100, 48, 19]
k6_avg_dur = [196, 356, 1210, 3100]
k6_rps     = [3.18, 10.6, 14.4, 15.7]
k6_err     = [0.00, 0.00, 0.00, 0.41]

vus_pred   = [7, 25, 50, 100, 150, 200]
p95_local  = [302, 856, 5880, 5240, 9000, 12000]
p95_cons   = [round(v * 0.35) for v in p95_local]
p95_opt    = [round(v * 0.20) for v in p95_local]
LIMIT      = 1000

usuarios_p4 = ["shernandez","iarias","jcolli","gchavez","fobregon","gucan","lguatemala"]
err_ps_p4   = [1662, 1567, 1680, 1557, 1572, 1586, 1555]
err_cm_p4   = [583, 523, 560, 520, 501, 515, 531]

# ══════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div style="padding:40px 0 20px;">
  <div style="font-size:0.72rem;letter-spacing:0.15em;color:#6B5CE7;
              text-transform:uppercase;margin-bottom:10px;font-weight:700;">
    Reporte de Rendimiento · Mayo 2026
  </div>
  <div style="font-size:2.6rem;font-weight:700;letter-spacing:-0.02em;
              line-height:1.15;color:#111111;">
    ¿Cómo aguanta el sistema<br>cuando llegan muchos usuarios?
    <span style="color:#6B5CE7">.</span>
  </div>
  <div style="font-size:0.9rem;color:#111111;margin-top:14px;line-height:1.6;max-width:620px;">
    Corrimos pruebas con distintas cantidades de usuarios al mismo tiempo para ver
    en qué punto el sistema local empieza a fallar o a responder lento.
    Estas son las herramientas que usamos y lo que encontramos.
  </div>
</div>
<hr style="border:none;border-top:1px solid #EAE6FF;margin:0 0 24px;">
""", unsafe_allow_html=True)

st.markdown(
        """
        <div class="kpi-grid">
            <div class="kpi-card"><div class="kpi-label">k6 — todo bien hasta</div><div class="kpi-value">25 usuarios</div></div>
            <div class="kpi-card"><div class="kpi-label">k6 — empieza a fallar</div><div class="kpi-value">50 usuarios</div></div>
            <div class="kpi-card"><div class="kpi-label">Locust — todo bien hasta</div><div class="kpi-value">7 usuarios</div></div>
            <div class="kpi-card"><div class="kpi-label">Locust — empieza a fallar</div><div class="kpi-value">25 usuarios</div></div>
            <div class="kpi-card"><div class="kpi-label">Mejor tiempo de respuesta</div><div class="kpi-value">196 ms</div></div>
            <div class="kpi-card"><div class="kpi-label">Máximo de fallos registrado</div><div class="kpi-value">87.5%</div></div>
        </div>
        """,
        unsafe_allow_html=True,
)

st.markdown("<hr style='border:none;border-top:1px solid #EAE6FF;margin:24px 0;'>",
            unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "01  Resultados Locust",
    "02  Resultados k6",
    "03  Comparativa",
    "04  Predicción local",
    "05  Qué encontramos",
    "06  ¿Locust o k6?",
])

# ─────────────────────────────────────────────────────────────────
# TAB 1 — LOCUST
# ─────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("### Pruebas con Locust — resultados nuevos")
    callout(
        "Locust simula el comportamiento real de un usuario: primero hace login, "
        "luego usa la aplicación. Con <b>7 usuarios todo funcionó bien</b>. "
        "A partir de <b>25 usuarios</b> el sistema empezó a rechazar conexiones — "
        "los usuarios enviaban peticiones pero el servidor las ignoraba o no podía atenderlas. "
        "Con 100 usuarios, casi <b>9 de cada 10 peticiones</b> fallaron.",
        PURPLE
    )

    st.markdown("#### ¿Cuántas peticiones fallaron en cada prueba?")

    col_desc, col_chart = st.columns([1, 2])
    with col_desc:
        st.markdown("""
        <div style="background:#FFFFFF;padding:18px;border-radius:12px;
                    border:1px solid #DDD6FA;font-size:0.85rem;color:#111111;
                    line-height:1.75;box-shadow:0 2px 8px rgba(107,92,231,0.05);">
          <b style="color:#111111;">Cómo leer esta gráfica:</b><br><br>
          Cada barra muestra qué porcentaje de las peticiones
          enviadas <b>no recibieron respuesta</b>.<br><br>
          La línea naranja es el límite aceptable: <b>máximo 5% de fallos</b>.<br><br>
          Verde = dentro del límite<br>
          Rojo = fuera del límite
        </div>
        """, unsafe_allow_html=True)

    with col_chart:
        fig = go.Figure(go.Bar(
            x=loc_labels, y=loc_err_rate,
            marker=dict(
                color=[MINT if e < 5 else CORAL for e in loc_err_rate],
                line=dict(width=0),
            ),
            text=[f"{e:.1f}% de fallos" for e in loc_err_rate],
            textfont=dict(family="Inter", size=13, color=WHITE),
            textposition="inside",
            width=0.5,
            cliponaxis=False,
        ))
        fig.add_hline(y=5, line=dict(color=PEACH, width=2, dash="dot"),
                      annotation_text="Límite aceptable: 5%",
                      annotation_font=dict(size=12, color=PEACH),
                      annotation_position="top right")
        fig.update_layout(**BASE, height=340,
                          yaxis_title="% de peticiones que fallaron",
                          yaxis_range=[0, 100], showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr style='border:none;border-top:1px solid #EAE6FF;margin:20px 0;'>",
                unsafe_allow_html=True)
    st.markdown("#### Las peticiones que sí llegaron — ¿qué tan rápido respondió el servidor?")

    callout(
        "Aunque muchas conexiones fallaban, las que sí lograban llegar al servidor "
        "recibían una respuesta <b>muy rápida</b> (1–4 milisegundos). "
        "Esto nos dice que el servidor <b>puede responder bien</b> — el problema "
        "es que no puede aceptar tantas conexiones al mismo tiempo.",
        MINT
    )

    col_a, col_b = st.columns(2)

    def graf_percentiles(x, p50, p95, max_v, titulo):
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Tiempo típico (p50)",
            x=x, y=p50,
            marker=dict(color=LAVENDER, line=dict(width=0)),
            text=[f"{v} ms" for v in p50], textposition="outside",
            textfont=dict(size=11, color=TEXT),
            cliponaxis=False))
        fig.add_trace(go.Bar(name="Tiempo del 95% (p95)",
            x=x, y=p95,
            marker=dict(color=PURPLE, line=dict(width=0)),
            text=[f"{v} ms" for v in p95], textposition="outside",
            textfont=dict(size=11, color=TEXT),
            cliponaxis=False))
        fig.add_trace(go.Bar(name="Peor caso registrado",
            x=x, y=max_v,
            marker=dict(color=CORAL, opacity=0.85, line=dict(width=0)),
            text=[f"{v} ms" for v in max_v], textposition="outside",
            textfont=dict(size=11, color=TEXT),
            cliponaxis=False))
        fig.update_layout(
            paper_bgcolor=BG,
            plot_bgcolor="#FAF8FF",
            font=dict(family="Inter, sans-serif", color=TEXT, size=12),
            xaxis=dict(showgrid=False, zeroline=False,
                       tickfont=dict(size=12, color=TEXT), linecolor=BORDER),
            yaxis=dict(gridcolor=BORDER, zeroline=False,
                       tickfont=dict(size=12, color=TEXT), linecolor=BORDER,
                       range=[0, max(max_v) * 1.30]),
            margin=dict(l=16, r=16, t=120, b=20),
            barmode="group", height=400,
            title=dict(text=titulo, font=dict(size=14, color=TEXT),
                       x=0.0, y=0.97, xanchor="left"),
            yaxis_title="Milisegundos (ms)",
            legend=dict(orientation="h", yanchor="bottom", y=1.05,
                        xanchor="left", x=0,
                        font=dict(size=11, color=TEXT)))
        return fig

    with col_a:
        st.plotly_chart(
            graf_percentiles(loc_labels, loc_cm_p50, loc_cm_p95, loc_cm_max,
                             "Endpoint: contador de firmas"),
            use_container_width=True
        )
    with col_b:
        st.plotly_chart(
            graf_percentiles(loc_labels, loc_ps_p50, loc_ps_p95, loc_ps_max,
                             "Endpoint: firmas pendientes"),
            use_container_width=True
        )

    st.markdown("<hr style='border:none;border-top:1px solid #EAE6FF;margin:20px 0;'>",
                unsafe_allow_html=True)
    st.markdown("#### ¿Los fallos afectaron a todos por igual? — prueba con 100 usuarios")

    callout(
        "Revisamos si algún usuario específico fallaba más que otros. "
        "El resultado fue que <b>todos fallaron casi la misma cantidad de veces</b>. "
        "Eso nos dice que no es un problema de una sesión en particular — "
        "es el servidor el que no puede con tantas conexiones al mismo tiempo.",
        PEACH
    )

    fig_usr = go.Figure()
    fig_usr.add_trace(go.Bar(name="Firmas pendientes",
        x=usuarios_p4, y=err_ps_p4,
        marker=dict(color=CORAL, line=dict(width=0)),
        text=[f"{v:,}" for v in err_ps_p4],
        textposition="outside", textfont=dict(size=11, color=TEXT),
        cliponaxis=False))
    fig_usr.add_trace(go.Bar(name="Contador de firmas",
        x=usuarios_p4, y=err_cm_p4,
        marker=dict(color=PEACH, line=dict(width=0)),
        text=[f"{v:,}" for v in err_cm_p4],
        textposition="outside", textfont=dict(size=11, color=TEXT),
        cliponaxis=False))
    fig_usr.update_layout(**BASE, barmode="group", height=400,
                          yaxis_range=[0, max(max(err_ps_p4), max(err_cm_p4)) * 1.22],
                          yaxis_title="Número de peticiones que fallaron",
                          legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                      font=dict(size=11, color=TEXT)))
    st.plotly_chart(fig_usr, use_container_width=True)

    st.markdown("<hr style='border:none;border-top:1px solid #EAE6FF;margin:20px 0;'>",
                unsafe_allow_html=True)
    st.markdown("#### Resumen de las pruebas Locust")

    df_loc = pd.DataFrame({
        "Escenario": loc_labels,
        "Usuarios simultáneos": loc_users,
        "Peticiones totales enviadas": [f"{v:,}" for v in loc_total_req],
        "Porcentaje que falló": [f"{e:.1f}%" for e in loc_err_rate],
        "Tiempo típico (p50)": [f"{v} ms" for v in loc_cm_p50],
        "Tiempo del 95% (p95)": [f"{v} ms" for v in loc_cm_p95],
        "Peor caso registrado": [f"{v} ms" for v in loc_cm_max],
        "¿Pasó la prueba?": ["Sí", "No", "No", "No"],
    })
    tabla_html(df_loc, columnas_centradas=[
        "Usuarios simultáneos", "Peticiones totales enviadas",
        "Porcentaje que falló", "Tiempo típico (p50)",
        "Tiempo del 95% (p95)", "Peor caso registrado", "¿Pasó la prueba?"
    ])


# ─────────────────────────────────────────────────────────────────
# TAB 2 — k6
# ─────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### Pruebas con k6 — resultados históricos")
    callout(
        "k6 prueba el sistema local de una forma diferente: hace el login una sola vez "
        "al inicio y luego reutiliza esa sesión para todas las peticiones. "
        "Esto mide qué tan rápido responde el sistema sin presionar el login. "
        "Con <b>7 y 25 usuarios todo funcionó dentro del límite</b>. "
        "A <b>50 usuarios la velocidad se desplomó</b> aunque el sistema no devolvió errores — "
        "respondía, pero muy lento.",
        SKY
    )

    st.markdown("#### ¿Qué tan rápido respondió el sistema local en cada prueba?")
    st.markdown("""
    <div style="background:#F1ECFF;padding:14px 18px;border-radius:10px;
                border:1px solid #DDD6FA;font-size:0.85rem;color:#111111;
                line-height:1.7;margin-bottom:16px;">
      <b style="color:#111111;">Cómo leer esta gráfica:</b>
      El <b>tiempo p95</b> significa que <b>95 de cada 100 usuarios</b> recibieron
      su respuesta en ese tiempo o menos. La línea roja es nuestro límite:
      <b>máximo 1 segundo (1,000 ms)</b>. Las barras rojas/naranjas están fuera del límite.
    </div>
    """, unsafe_allow_html=True)

    fig_p95 = go.Figure()
    fig_p95.add_trace(go.Bar(
        name="Contador de firmas",
        x=pruebas_k6, y=k6_cm_p95,
        marker=dict(color=[MINT if v <= LIMIT else CORAL for v in k6_cm_p95],
                    line=dict(width=0)),
        text=[f"{v} ms" if v < 1000 else f"{v/1000:.1f} seg" for v in k6_cm_p95],
        textfont=dict(size=12, color=TEXT),
        textposition="outside", offsetgroup=0,
        cliponaxis=False,
    ))
    fig_p95.add_trace(go.Bar(
        name="Firmas pendientes",
        x=pruebas_k6, y=k6_ps_p95,
        marker=dict(color=[SKY if v <= LIMIT else PEACH for v in k6_ps_p95],
                    line=dict(width=0)),
        text=[f"{v} ms" if v < 1000 else f"{v/1000:.1f} seg" for v in k6_ps_p95],
        textfont=dict(size=12, color=TEXT),
        textposition="outside", offsetgroup=1,
        cliponaxis=False,
    ))
    fig_p95.add_hline(y=LIMIT,
                      line=dict(color=CORAL, width=2, dash="dot"),
                      annotation_text="Límite: 1 segundo",
                      annotation_font=dict(size=12, color=CORAL),
                      annotation_position="top right")
    fig_p95.update_layout(**BASE, barmode="group", height=460,
                          yaxis_range=[0, max(max(k6_cm_p95), max(k6_ps_p95)) * 1.20],
                          yaxis_title="Milisegundos (ms)",
                          bargap=0.25, bargroupgap=0.08,
                          legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                      font=dict(size=12, color=TEXT)))
    st.plotly_chart(fig_p95, use_container_width=True)

    st.markdown("<hr style='border:none;border-top:1px solid #EAE6FF;margin:20px 0;'>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ¿Cuántos usuarios recibieron respuesta en menos de 1 segundo?")
        callout(
            "Esta gráfica muestra el porcentaje de peticiones que cumplieron el objetivo "
            "de responder en menos de 1 segundo. Con 100 usuarios, solo el 16% lo logró.",
            SKY
        )
        fig_lt1 = go.Figure()
        fig_lt1.add_trace(go.Scatter(
            x=pruebas_k6, y=k6_cm_lt1, name="Contador de firmas",
            mode="lines+markers+text",
            line=dict(color=MINT, width=2.5),
            marker=dict(size=10, color=MINT, line=dict(width=2, color=WHITE)),
            text=[f"{v}%" for v in k6_cm_lt1], textposition="top center",
            textfont=dict(size=12, color=TEXT),
            cliponaxis=False))
        fig_lt1.add_trace(go.Scatter(
            x=pruebas_k6, y=k6_ps_lt1, name="Firmas pendientes",
            mode="lines+markers+text",
            line=dict(color=SKY, width=2.5),
            marker=dict(size=10, color=SKY, line=dict(width=2, color=WHITE)),
            text=[f"{v}%" for v in k6_ps_lt1], textposition="bottom center",
            textfont=dict(size=12, color=TEXT),
            cliponaxis=False))
        fig_lt1.add_hline(y=95, line=dict(color=PEACH, width=2, dash="dot"),
                          annotation_text="Objetivo: 95%",
                          annotation_font=dict(size=12, color=PEACH))
        fig_lt1.update_layout(**BASE, height=340,
                              yaxis_title="% de peticiones bajo 1 segundo",
                              yaxis_range=[-8, 125],
                              legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                          font=dict(size=11, color=TEXT)))
        st.plotly_chart(fig_lt1, use_container_width=True)

    with col2:
        st.markdown("#### ¿Cuántas peticiones procesó el servidor por segundo?")
        callout(
            "El servidor procesó más peticiones por segundo conforme subieron los usuarios, "
            "pero se saturó en 50 usuarios. Agregar más usuarios no hizo que procesara más — "
            "solo generó espera.",
            PURPLE
        )
        fig_rps = go.Figure(go.Scatter(
            x=vus_k6, y=k6_rps, mode="lines+markers+text",
            line=dict(color=PURPLE, width=2.5),
            marker=dict(size=12, color=PURPLE, line=dict(width=2, color=WHITE)),
            fill="tozeroy", fillcolor="rgba(107,92,231,0.08)",
            text=[f"{v} req/s" for v in k6_rps], textposition="top center",
            textfont=dict(size=11, color=TEXT),
            cliponaxis=False,
        ))
        fig_rps.update_layout(**BASE, height=340,
                              xaxis_title="Número de usuarios simultáneos",
                              yaxis_range=[0, max(k6_rps) * 1.30],
                              yaxis_title="Peticiones por segundo",
                              showlegend=False)
        st.plotly_chart(fig_rps, use_container_width=True)

    st.markdown("<hr style='border:none;border-top:1px solid #EAE6FF;margin:20px 0;'>",
                unsafe_allow_html=True)
    st.markdown("#### Resumen de las pruebas k6")

    df_k6 = pd.DataFrame({
        "Usuarios simultáneos": vus_k6,
        "95% de usuarios respondió en": [f"{v} ms" if v < 1000 else f"{v/1000:.1f} seg" for v in k6_cm_p95],
        "Promedio de respuesta": [f"{v} ms" if v < 1000 else f"{v/1000:.1f} seg" for v in k6_avg_dur],
        "Peticiones por segundo": k6_rps,
        "Errores HTTP": [f"{e:.2f}%" for e in k6_err],
        "Usuarios con respuesta en < 1s": [f"{v}%" for v in k6_cm_lt1],
        "¿Pasó la prueba?": ["Sí", "Sí, casi", "No, muy lento", "No, muy lento"],
    })
    tabla_html(df_k6, columnas_centradas=[
        "Usuarios simultáneos", "95% de usuarios respondió en",
        "Promedio de respuesta", "Peticiones por segundo", "Errores HTTP",
        "Usuarios con respuesta en < 1s", "¿Pasó la prueba?"
    ])


# ─────────────────────────────────────────────────────────────────
# TAB 3 — COMPARATIVA
# ─────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("### k6 vs Locust — ¿por qué dan resultados tan distintos?")
    callout(
        "No es que una herramienta sea más precisa que la otra — es que "
        "<b>miden cosas distintas</b>. k6 entra con la puerta ya abierta "
        "(sesión iniciada), Locust toca el timbre cada vez (login nuevo). "
        "Juntas nos dan una imagen más completa del sistema.",
        PURPLE
    )

    col_k6, col_loc = st.columns(2)
    with col_k6:
        card("k6 — mide la velocidad del servidor",
             "Hace login una sola vez al inicio y reutiliza esa sesión. "
             "Sirve para saber si el servidor responde rápido cuando ya tiene "
             "una conexión activa. Es como probar un empleado que ya está en su escritorio.",
             SKY)
    with col_loc:
        card("Locust — mide el flujo completo",
             "Cada usuario hace login desde cero en cada vuelta, igual que un "
             "usuario real. Detecta problemas en autenticación bajo carga. "
             "Es como probar la fila de entrada antes de llegar al escritorio.",
             CORAL)

    st.markdown("#### Porcentaje de fallos por herramienta y escenario")
    callout(
        "k6 casi no reporta errores porque evita presionar el login. "
        "Locust sí lo presiona y ahí es donde el sistema falla. "
        "Ambos patrones son reales — son problemas distintos en el mismo sistema.",
        PEACH
    )

    xs = ["7", "25", "50", "100"]
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(
        x=xs, y=k6_err, name="k6 — errores HTTP reales",
        mode="lines+markers",
        line=dict(color=SKY, width=2.5),
        marker=dict(size=12, color=SKY, symbol="circle",
                    line=dict(width=2, color=WHITE)),
        fill="tozeroy", fillcolor="rgba(91,156,246,0.07)",
    ))
    fig_comp.add_trace(go.Scatter(
        x=xs, y=loc_err_rate, name="Locust — conexiones que no llegaron",
        mode="lines+markers",
        line=dict(color=CORAL, width=2.5),
        marker=dict(size=12, color=CORAL, symbol="diamond",
                    line=dict(width=2, color=WHITE)),
        fill="tozeroy", fillcolor="rgba(255,107,138,0.07)",
    ))
    fig_comp.add_hline(y=5, line=dict(color=PEACH, width=2, dash="dot"),
                       annotation_text="Límite aceptable: 5%",
                       annotation_font=dict(size=12, color=PEACH),
                       annotation_position="top right")
    fig_comp.update_layout(**BASE, height=400,
                           yaxis_title="% de peticiones que fallaron",
                           xaxis_title="Número de usuarios simultáneos",
                           legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                       font=dict(size=12, color=TEXT)))
    st.plotly_chart(fig_comp, use_container_width=True)

    st.markdown("<hr style='border:none;border-top:1px solid #EAE6FF;margin:20px 0;'>",
                unsafe_allow_html=True)
    st.markdown("#### Qué detectó cada herramienta")

    comp = pd.DataFrame({
        "Aspecto": [
            "Cómo entra al sistema",
            "Cuándo empieza a fallar",
            "Tipo de fallo",
            "¿Qué mide mejor?",
        ],
        "k6": [
            "Una sesión iniciada de antemano, compartida",
            "50 usuarios — responde pero muy lento",
            "Latencia alta — el servidor tarda mucho",
            "Qué tan rápido responden los endpoints",
        ],
        "Locust": [
            "Cada usuario hace su propio login desde cero",
            "25 usuarios — empieza a rechazar conexiones",
            "Conexiones rechazadas — no puede atender a todos",
            "Cómo se comporta el flujo completo de un usuario real",
        ],
    })
    tabla_html(comp)

    st.markdown("<hr style='border:none;border-top:1px solid #EAE6FF;margin:20px 0;'>",
                unsafe_allow_html=True)
    st.markdown("#### Estado general — ¿qué pasó en cada prueba?")

    fig_heat = go.Figure(go.Heatmap(
        z=[[0.0, 0.0, 1.0, 1.0],
           [0.0, 1.0, 1.0, 1.0]],
        x=["7 usuarios", "25 usuarios", "50 usuarios", "100 usuarios"],
        y=["k6", "Locust"],
        text=[
            ["Todo bien", "Casi perfecto", "Muy lento", "Falla"],
            ["Todo bien", "Falla de conexiones", "Falla de conexiones", "Colapso"],
        ],
        texttemplate="%{text}",
        textfont=dict(family="Inter", size=13, color="#111111"),
        colorscale=[[0, "#E8FAF3"], [0.5, "#FFF4E6"], [1, "#FFE8EE"]],
        showscale=False, xgap=6, ygap=6,
    ))
    fig_heat.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(family="Inter", color=TEXT),
        height=220,
        margin=dict(l=80, r=16, t=16, b=40),
        xaxis=dict(tickfont=dict(size=12, color=TEXT)),
        yaxis=dict(tickfont=dict(size=12, color=TEXT)),
    )
    st.plotly_chart(fig_heat, use_container_width=True)


# ─────────────────────────────────────────────────────────────────
# TAB 4 — PREDICCIÓN
# ─────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("### ¿Cómo se vería esto en un servidor real?")
    callout(
        "Todas estas pruebas se corrieron en una computadora local con configuración "
        "de desarrollo — no en un servidor de producción. Aplicando los ajustes "
        "típicos de producción (modo no-debug, pool de conexiones reutilizables y "
        "más workers en paralelo) el sistema debería responder significativamente más rápido. "
        "Esta sección estima cuánto mejoraría.<br><br>"
        "<b>Importante:</b> es una estimación basada en el comportamiento documentado "
        "de estas tecnologías. Para confirmarla se necesitan pruebas reales en el servidor.",
        PURPLE
    )

    st.markdown("#### Proyección: tiempo de respuesta local vs servidor")
    st.markdown("""
    <div style="background:#F1ECFF;padding:14px 18px;border-radius:10px;
                border:1px solid #DDD6FA;font-size:0.85rem;color:#111111;
                line-height:1.7;margin-bottom:16px;">
      <b style="color:#111111;">Cómo leer esta gráfica:</b>
      La línea roja es cómo está el sistema hoy (local).
      La línea naranja es la estimación siendo conservadores (asumiendo menos mejora).
      La línea verde es la estimación siendo optimistas (asumiendo que todo mejora bien).
      La línea morada es el límite de 1 segundo — lo que queremos lograr.
    </div>
    """, unsafe_allow_html=True)

    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(
        x=[str(v) for v in vus_pred], y=p95_local,
        name="Hoy — en local (real)",
        mode="lines+markers",
        line=dict(color=CORAL, width=2.5),
        marker=dict(size=10, color=CORAL, line=dict(width=2, color=WHITE)),
        fill="tozeroy", fillcolor="rgba(255,107,138,0.05)",
    ))
    fig_pred.add_trace(go.Scatter(
        x=[str(v) for v in vus_pred], y=p95_cons,
        name="Servidor — estimación conservadora (mejora 65%)",
        mode="lines+markers",
        line=dict(color=PEACH, width=2.5, dash="dash"),
        marker=dict(size=10, color=PEACH, symbol="square",
                    line=dict(width=2, color=WHITE)),
    ))
    fig_pred.add_trace(go.Scatter(
        x=[str(v) for v in vus_pred], y=p95_opt,
        name="Servidor — estimación optimista (mejora 80%)",
        mode="lines+markers",
        line=dict(color=MINT, width=2.5, dash="dash"),
        marker=dict(size=10, color=MINT, symbol="diamond",
                    line=dict(width=2, color=WHITE)),
    ))
    fig_pred.add_hline(y=LIMIT, line=dict(color=PURPLE, width=2, dash="dot"),
                       annotation_text="Objetivo: 1 segundo",
                       annotation_font=dict(size=12, color=PURPLE),
                       annotation_position="top right")
    fig_pred.update_layout(**BASE, height=460,
                           xaxis_title="Número de usuarios simultáneos",
                           yaxis_title="Tiempo de respuesta (ms)",
                           legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                       font=dict(size=11, color=TEXT)))
    st.plotly_chart(fig_pred, use_container_width=True)

    st.markdown("<hr style='border:none;border-top:1px solid #EAE6FF;margin:20px 0;'>",
                unsafe_allow_html=True)
    st.markdown("#### ¿Qué esperar por número de usuarios?")

    df_pred = pd.DataFrame({
        "Usuarios simultáneos": vus_pred,
        "Tiempo actual en local": [f"{v} ms" if v < 1000 else f"{v/1000:.1f} seg" for v in p95_local],
        "Servidor — estimación conservadora": [f"{v} ms" if v < 1000 else f"{v/1000:.1f} seg" for v in p95_cons],
        "Servidor — estimación optimista": [f"{v} ms" if v < 1000 else f"{v/1000:.1f} seg" for v in p95_opt],
        "¿Pasa el objetivo conservador?": ["Sí" if v <= 1000 else "No" for v in p95_cons],
        "¿Pasa el objetivo optimista?":   ["Sí" if v <= 1000 else "No" for v in p95_opt],
    })
    tabla_html(df_pred, columnas_centradas=[
        "Usuarios simultáneos", "Tiempo actual en local",
        "Servidor — estimación conservadora", "Servidor — estimación optimista",
        "¿Pasa el objetivo conservador?", "¿Pasa el objetivo optimista?"
    ])

    callout(
        "Con la estimación conservadora el sistema aguantaría hasta <b>25 usuarios</b> "
        "dentro del límite de 1 segundo. Con la optimista, hasta <b>50 usuarios</b>. "
        "Para ir más allá se necesitaría también optimizar las consultas a la base de datos. "
        "El siguiente paso es correr estas mismas pruebas en el servidor con los cambios aplicados.",
        MINT
    )


# ─────────────────────────────────────────────────────────────────
# TAB 5 — QUÉ ENCONTRAMOS
# ─────────────────────────────────────────────────────────────────
with tab5:
    st.markdown("### Qué nos dicen los datos — en lenguaje simple")
    callout(
        "Aquí resumimos lo que encontramos en las pruebas locales, "
        "sin términos técnicos. Cada punto explica qué pasó y por qué importa.",
        PURPLE
    )

    col1, col2 = st.columns(2)
    with col1:
        card("El sistema funciona bien con pocos usuarios",
             "Con 7 usuarios simultáneos, tanto k6 como Locust reportaron que "
             "todo funcionó correctamente y rápido. El servidor respondió en menos "
             "de 300 ms en el 95% de los casos. Esto confirma que el sistema tiene "
             "capacidad real — el problema no es el código sino la configuración bajo carga.",
             MINT)
        card("El sistema se satura a los 50 usuarios (k6)",
             "Con k6, cuando subimos a 50 usuarios, el tiempo de respuesta pasó "
             "de menos de 1 segundo a casi 6 segundos de golpe. No hubo errores HTTP — "
             "el sistema respondía, pero tardaba tanto que era inaceptable. "
             "Es como una caja registradora que sigue funcionando pero hace esperar "
             "6 minutos por operación.",
             PEACH)
        card("El throughput llega a un techo",
             "Con k6 el servidor procesó cada vez más peticiones por segundo al aumentar usuarios, "
             "hasta llegar a ~14 peticiones/segundo con 50 usuarios. Con 100 usuarios "
             "el número no subió — el sistema llegó a su límite y empezó a generar cola. "
             "Más usuarios solo significaron más espera, no más trabajo hecho.",
             SKY)

    with col2:
        card("Las conexiones se rechazan desde 25 usuarios virtuales (Locust)",
             "Con Locust, al llegar a 25 usuarios el 72% de las peticiones no llegaron "
             "al servidor — fueron rechazadas antes de procesarse. "
             "Esto ocurre porque Locust simula el login completo cada vez, "
             "lo que satura el sistema de autenticación.",
             CORAL)
        card("Las peticiones que sí llegan son rápidas",
             "Lo interesante de Locust es que las peticiones que sí lograban "
             "llegar al servidor respondían en 1–4 ms incluso con 100 usuarios. "
             "Eso nos dice que el servidor puede responder rápido — el cuello de "
             "botella está en poder aceptar muchas conexiones al mismo tiempo, "
             "no en el tiempo de procesamiento.",
             PURPLE)
        card("Los fallos son iguales para todos los usuarios virtuales",
             "En la prueba de 100 usuarios con Locust, revisamos si algún usuario "
             "específico fallaba más que otro. Todos fallaron prácticamente lo mismo "
             "(entre 1,555 y 1,680 veces en firmas pendientes). Eso confirma que "
             "el problema es del servidor, no de una sesión o usuario en particular.",
             PEACH)

    st.markdown("<hr style='border:none;border-top:1px solid #EAE6FF;margin:20px 0;'>",
                unsafe_allow_html=True)
    st.markdown("#### Guía rápida para entender las gráficas")

    df_guia = pd.DataFrame({
        "Término": ["p50 — tiempo típico", "p95 — tiempo del 95%", "p99 — peor caso frecuente",
                    "Max — peor caso absoluto", "req/s — peticiones por segundo",
                    "ms — milisegundos", "Error rate", "Throughput"],
        "Qué significa en palabras simples": [
            "La mitad de los usuarios tuvo este tiempo o mejor — como el promedio pero más justo",
            "95 de cada 100 usuarios recibieron respuesta en este tiempo o menos — el estándar de la industria",
            "Solo 1 de cada 100 usuarios tuvo una experiencia peor que este tiempo",
            "El caso más lento registrado en toda la prueba — puede ser un caso raro",
            "Cuántas peticiones procesa el servidor en un segundo — más es mejor",
            "Milésima de segundo. 1,000 ms = 1 segundo. 300 ms = 0.3 segundos",
            "Qué porcentaje de peticiones falló — idealmente menos del 5%",
            "Cuánto trabajo útil hace el servidor por segundo — se satura cuando deja de crecer",
        ],
    })
    tabla_html(df_guia)


# ─────────────────────────────────────────────────────────────────
# TAB 6 — ¿LOCUST O K6?
# ─────────────────────────────────────────────────────────────────
with tab6:
    st.markdown("### ¿Cuál es mejor para aplicar pruebas de rendimiento: Locust o k6?")
    callout(
        "La respuesta honesta es: <b>depende de qué quieres descubrir</b>. "
        "No hay una herramienta ganadora — cada una tiene un propósito distinto. "
        "Lo ideal es usarlas juntas, como lo hicimos nosotros.",
        PURPLE
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div style="background:#FFFFFF;border:1px solid #DDD6FA;border-radius:12px;
                    border-top:3px solid #5B9CF6;
                    padding:20px;box-shadow:0 2px 8px rgba(91,156,246,0.08);margin-bottom:16px;">
          <div style="font-size:1.1rem;font-weight:700;color:#111111;margin-bottom:12px;">
            k6 — para medir velocidad pura
          </div>
          <div style="font-size:0.85rem;color:#111111;line-height:1.75;">
            <b style="color:#111111;">Úsalo cuando quieras saber</b> qué tan rápido
            responden tus endpoints bajo carga sostenida, sin que el login sea parte del problema.<br><br>
            <b style="color:#111111;">Ideal para</b> pruebas de estrés graduales,
            encontrar el punto de quiebre de latencia, monitoreo continuo de rendimiento.<br><br>
            <b style="color:#111111;">Ventajas:</b> muy rápido de configurar, resultados
            claros, excelente para automatizar en pipelines de CI/CD, gratuito y de código abierto.<br><br>
            <b style="color:#111111;">Limitación:</b> no simula el flujo real del usuario —
            si el login falla bajo carga, k6 no lo va a detectar porque hace login solo una vez.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div style="background:#FFFFFF;border:1px solid #DDD6FA;border-radius:12px;
                    border-top:3px solid #FF6B8A;
                    padding:20px;box-shadow:0 2px 8px rgba(255,107,138,0.08);margin-bottom:16px;">
          <div style="font-size:1.1rem;font-weight:700;color:#111111;margin-bottom:12px;">
            Locust — para simular usuarios reales
          </div>
          <div style="font-size:0.85rem;color:#111111;line-height:1.75;">
            <b style="color:#111111;">Úsalo cuando quieras saber</b> cómo se comporta
            el sistema cuando muchos usuarios nuevos llegan al mismo tiempo — login incluido.<br><br>
            <b style="color:#111111;">Ideal para</b> detectar problemas de autenticación
            bajo carga, simular flujos completos de usuario, pruebas de escenarios reales.<br><br>
            <b style="color:#111111;">Ventajas:</b> se escribe en Python (más accesible),
            interfaz visual en tiempo real, fácil de adaptar a flujos complejos.<br><br>
            <b style="color:#111111;">Limitación:</b> si el login falla, todo lo demás
            también falla — a veces es difícil saber si el problema es el login o el endpoint.
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### Mi recomendación")
    st.markdown("""
    <div style="background:linear-gradient(135deg, #EAE6FF 0%, #E8F4FF 100%);
                border-radius:12px;padding:22px 24px;
                font-size:0.88rem;color:#111111;line-height:1.75;margin-bottom:20px;">
      <b style="font-size:1rem;">Para este proyecto específico, recomiendo usar ambas — como lo hicimos.</b><br><br>
      <b>k6 primero:</b> para encontrar cuántos usuarios aguanta el sistema antes de volverse lento.
      Es más fácil de interpretar y te da una línea base clara.<br><br>
      <b>Locust después:</b> para simular el flujo real y detectar problemas que k6 no ve,
      como el colapso del sistema de autenticación bajo carga concurrente.<br><br>
      <b>Si solo puedes elegir una:</b> usa <b style="color:#4A3FB8;">k6</b> si lo que más
      te importa es la velocidad de los endpoints, o <b style="color:#D14A6E;">Locust</b>
      si lo que más te importa es simular cómo se comporta el sistema con usuarios reales.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Comparación directa")
    df_tools = pd.DataFrame({
        "Característica": [
            "Lenguaje de scripting",
            "Curva de aprendizaje",
            "Interfaz visual",
            "Simula flujo real de usuario",
            "Detecta problemas de login bajo carga",
            "Ideal para pipelines automatizados",
            "Reportes y métricas",
            "Precio",
        ],
        "k6": [
            "JavaScript",
            "Media — requiere saber un poco de JS",
            "No (solo en la versión cloud de pago)",
            "Parcialmente — si lo configuras a mano",
            "No — hace login una sola vez",
            "Sí — muy bueno para CI/CD",
            "Muy detallados y estandarizados",
            "Gratuito y open source",
        ],
        "Locust": [
            "Python",
            "Baja — Python es más accesible",
            "Sí — interfaz web incluida",
            "Sí — por diseño",
            "Sí — detecta exactamente este problema",
            "Sí — también se puede automatizar",
            "Buenos, con más contexto de usuario",
            "Gratuito y open source",
        ],
    })
    tabla_html(df_tools)

    st.markdown("""
    <div style="font-size:0.7rem;color:#5A5570;text-align:center;
                margin-top:40px;letter-spacing:0.08em;">
      REPORTE DE RENDIMIENTO · MAYO 2026 · ENTORNO LOCAL · MODO DESARROLLO
    </div>
    """, unsafe_allow_html=True)
