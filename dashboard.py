import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Performance Report — k6 vs Locust",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── DARK INDUSTRIAL THEME ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0A0A0F;
    color: #E8E6E0;
}
.stApp { background-color: #0A0A0F; }
.stTabs [data-baseweb="tab-list"] {
    background: #12121A;
    border-bottom: 1px solid #1E1E2E;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #555;
    padding: 12px 24px;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: #FF4B2B !important;
    border-bottom: 2px solid #FF4B2B !important;
    background: transparent !important;
}
div[data-testid="metric-container"] {
    background: #12121A;
    border: 1px solid #1E1E2E;
    border-left: 3px solid #FF4B2B;
    padding: 16px 20px;
    border-radius: 2px;
}
div[data-testid="metric-container"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #666 !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    color: #E8E6E0 !important;
}
footer, #MainMenu, header { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── PALETA ────────────────────────────────────────────────────────────
BG      = "#0A0A0F"
SURFACE = "#12121A"
BORDER  = "#1E1E2E"
RED     = "#FF4B2B"
ORANGE  = "#FFAA33"
GREEN   = "#2ECC9A"
BLUE    = "#4B8BFF"
TEXT    = "#E8E6E0"
MUTED   = "#555566"

BASE = dict(
    paper_bgcolor=BG, plot_bgcolor=SURFACE,
    font=dict(family="Space Mono, monospace", color=TEXT, size=11),
    xaxis=dict(showgrid=False, zeroline=False,
               tickfont=dict(size=10, color=MUTED), linecolor=BORDER),
    yaxis=dict(gridcolor=BORDER, zeroline=False,
               tickfont=dict(size=10, color=MUTED), linecolor=BORDER),
    margin=dict(l=16, r=16, t=44, b=16),
)

# ── DATOS ─────────────────────────────────────────────────────────────
pruebas = ["P1 — 7 VUs", "P2 — 25 VUs", "P3 — 50 VUs", "P4 — 100 VUs"]
vus     = [7, 25, 50, 100]
p95_cm  = [707,  850,  5240,  12180]
p95_ps  = [313,  679,  4150,  11890]
err_k6  = [4.93, 0.00, 0.00,  6.31]
rps_k6  = [3.1,  10.8, 10.1,  8.9]
chk_ok  = [97.48,100.0,100.0, 93.66]

loc_req  = [101,  1270, 467,  3708]
loc_fail = [0,    1156, 413,  3507]
loc_ferr = [0.0,  91.0, 88.4, 94.6]
loc_avg  = [7187, 1406, 6250, 6424]

LIMIT = 1000

# ── HERO ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:48px 0 28px;">
  <div style="font-family:'Space Mono',monospace;font-size:0.68rem;
              letter-spacing:0.2em;color:#444;text-transform:uppercase;
              margin-bottom:10px;">
    Reporte de rendimiento &mdash; Mayo 2026
  </div>
  <div style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;
              letter-spacing:-0.03em;line-height:1.05;color:#E8E6E0;">
    Performance<br>Analysis<span style="color:#FF4B2B">.</span>
  </div>
  <div style="display:flex;gap:28px;flex-wrap:wrap;margin-top:18px;">
    <span style="font-family:'Space Mono',monospace;font-size:0.68rem;
                 color:#333;letter-spacing:0.1em;">k6 &mdash; 4 escenarios</span>
    <span style="font-family:'Space Mono',monospace;font-size:0.68rem;
                 color:#333;letter-spacing:0.1em;">Locust &mdash; 4 escenarios</span>
    <span style="font-family:'Space Mono',monospace;font-size:0.68rem;
                 color:#333;letter-spacing:0.1em;">Umbral p(95) &lt; 1 000 ms</span>
    <span style="font-family:'Space Mono',monospace;font-size:0.68rem;
                 color:#333;letter-spacing:0.1em;">Error rate &lt; 5%</span>
  </div>
</div>
<hr style="border:none;border-top:1px solid #1E1E2E;margin:0 0 28px;">
""", unsafe_allow_html=True)

# ── KPI STRIP ─────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.metric("Limite limpio k6",   "25 VUs")
with c2: st.metric("Quiebre k6",         "50 VUs")
with c3: st.metric("Limite limpio Locust","7 users")
with c4: st.metric("Quiebre Locust",     "25 users")
with c5: st.metric("Maximo Locust",      "128 923 ms")

st.markdown("<hr style='border:none;border-top:1px solid #1E1E2E;margin:28px 0;'>",
            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
t1, t2, t3, t4 = st.tabs([
    "01  k6 — Tiempos p(95)",
    "02  Locust — Errores",
    "03  Comparativa",
    "04  Diagnostico",
])

# ─────────────────────────────────────────────────────────────────────
# TAB 1 — k6
# ─────────────────────────────────────────────────────────────────────
with t1:
    st.markdown("""
    <div style="margin-bottom:4px;">
      <span style="font-family:'Space Mono',monospace;font-size:0.62rem;
                   letter-spacing:0.2em;text-transform:uppercase;color:#FF4B2B;">
        Analisis k6
      </span>
    </div>
    <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;
                color:#E8E6E0;margin-bottom:14px;">Tiempos de respuesta p(95)</div>
    <div style="background:#12121A;border-left:3px solid #FF4B2B;
                padding:12px 16px;border-radius:0 4px 4px 0;
                font-family:'Space Mono',monospace;font-size:0.76rem;
                color:#888;line-height:1.7;margin-bottom:20px;">
      <b style="color:#E8E6E0;">p(95)</b> = el 95% de las peticiones respondio en menos de este tiempo.
      Las barras en <b style="color:#FF4B2B;">rojo/naranja</b> superan el umbral de 1 segundo.
    </div>
    """, unsafe_allow_html=True)

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        name="counter-moper", x=pruebas, y=p95_cm,
        marker=dict(color=[GREEN if v <= LIMIT else RED for v in p95_cm],
                    line=dict(width=0)),
        text=[f"{v}ms" if v < 1000 else f"{v/1000:.1f}s" for v in p95_cm],
        textfont=dict(family="Space Mono", size=10, color=TEXT),
        textposition="outside", offsetgroup=0,
    ))
    fig1.add_trace(go.Bar(
        name="pending-signatures", x=pruebas, y=p95_ps,
        marker=dict(color=[BLUE if v <= LIMIT else ORANGE for v in p95_ps],
                    line=dict(width=0)),
        text=[f"{v}ms" if v < 1000 else f"{v/1000:.1f}s" for v in p95_ps],
        textfont=dict(family="Space Mono", size=10, color=TEXT),
        textposition="outside", offsetgroup=1,
    ))
    fig1.add_hline(y=LIMIT, line=dict(color=RED, width=1.5, dash="dot"),
                   annotation_text="LIMITE 1 000 ms",
                   annotation_font=dict(family="Space Mono", size=10, color=RED),
                   annotation_position="top right")
    fig1.update_layout(**BASE, barmode="group", height=420,
                       yaxis_title="ms", bargap=0.25, bargroupgap=0.08,
                       legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                   font=dict(family="Space Mono", size=10)))
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("<hr style='border:none;border-top:1px solid #1E1E2E;margin:24px 0;'>",
                unsafe_allow_html=True)
    ca, cb = st.columns(2)

    with ca:
        st.markdown("""
        <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;
                    color:#E8E6E0;margin-bottom:14px;">Tasa de error</div>""",
                    unsafe_allow_html=True)
        fig2 = go.Figure(go.Bar(
            x=pruebas, y=err_k6,
            marker=dict(color=[GREEN if e < 5 else RED for e in err_k6],
                        line=dict(width=0)),
            text=[f"{e:.2f}%" for e in err_k6],
            textfont=dict(family="Space Mono", size=11, color=TEXT),
            textposition="outside",
        ))
        fig2.add_hline(y=5, line=dict(color=ORANGE, width=1.5, dash="dot"),
                       annotation_text="LIMITE 5%",
                       annotation_font=dict(family="Space Mono", size=10, color=ORANGE),
                       annotation_position="top right")
        fig2.update_layout(**BASE, height=300, yaxis_title="%",
                           yaxis_range=[0, 12], showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with cb:
        st.markdown("""
        <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;
                    color:#E8E6E0;margin-bottom:14px;">Throughput — req/s</div>""",
                    unsafe_allow_html=True)
        fig3 = go.Figure(go.Scatter(
            x=vus, y=rps_k6, mode="lines+markers",
            line=dict(color=BLUE, width=2.5),
            marker=dict(size=12, color=BLUE, line=dict(width=2, color=BG)),
            fill="tozeroy", fillcolor="rgba(75,139,255,0.07)",
        ))
        fig3.update_layout(**BASE, height=300,
                           xaxis_title="VUs", yaxis_title="req/s",
                           showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<hr style='border:none;border-top:1px solid #1E1E2E;margin:24px 0;'>",
                unsafe_allow_html=True)
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.1rem;
                font-weight:700;color:#E8E6E0;margin-bottom:12px;">
                Tabla completa k6</div>""", unsafe_allow_html=True)
    df_k6 = pd.DataFrame({
        "Prueba": pruebas, "VUs": vus,
        "p(95) counter (ms)": p95_cm, "p(95) signatures (ms)": p95_ps,
        "Error rate (%)": err_k6, "Req/s": rps_k6,
        "Checks ok (%)": chk_ok,
        "Resultado": ["Advertencia", "Pasa", "Falla p95", "Falla p95+err"],
    })
    st.dataframe(df_k6, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────
# TAB 2 — Locust
# ─────────────────────────────────────────────────────────────────────
with t2:
    st.markdown("""
    <div style="margin-bottom:4px;">
      <span style="font-family:'Space Mono',monospace;font-size:0.62rem;
                   letter-spacing:0.2em;text-transform:uppercase;color:#FF4B2B;">
        Analisis Locust
      </span>
    </div>
    <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;
                color:#E8E6E0;margin-bottom:14px;">Tasa de fallos por escenario</div>
    <div style="background:#12121A;border-left:3px solid #FF4B2B;
                padding:12px 16px;border-radius:0 4px 4px 0;
                font-family:'Space Mono',monospace;font-size:0.76rem;
                color:#888;line-height:1.7;margin-bottom:20px;">
      Locust colapsa desde <b style="color:#E8E6E0;">25 usuarios</b> con
      <b style="color:#FF4B2B;">401 Unauthorized</b>.
      El backend invalida tokens cuando varios usuarios hacen login concurrente.
      No es un problema de latencia — es de autenticacion.
    </div>
    """, unsafe_allow_html=True)

    fig4 = go.Figure(go.Bar(
        x=["P1 — 7", "P2 — 25", "P3 — 50", "P4 — 100"],
        y=loc_ferr,
        marker=dict(color=[GREEN if f < 5 else RED for f in loc_ferr],
                    line=dict(width=0)),
        text=[f"{v:.1f}%" for v in loc_ferr],
        textfont=dict(family="Space Mono", size=13, color=TEXT),
        textposition="outside", width=0.5,
    ))
    fig4.add_hline(y=5, line=dict(color=ORANGE, width=1.5, dash="dot"),
                   annotation_text="LIMITE 5%",
                   annotation_font=dict(family="Space Mono", size=10, color=ORANGE),
                   annotation_position="top right")
    fig4.update_layout(**BASE, height=360, yaxis_title="%",
                       yaxis_range=[0, 110], showlegend=False,
                       xaxis_title="Escenario")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<hr style='border:none;border-top:1px solid #1E1E2E;margin:24px 0;'>",
                unsafe_allow_html=True)
    cx, cy = st.columns(2)

    with cx:
        st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.1rem;
                    font-weight:700;color:#E8E6E0;margin-bottom:12px;">
                    Distribucion de errores — P4 (100 users)</div>""",
                    unsafe_allow_html=True)
        fig5 = go.Figure(go.Pie(
            labels=["401 Unauthorized", "500 Internal Server",
                    "403 Forbidden", "400 Bad Request"],
            values=[3132, 92, 80, 3],
            hole=0.55,
            marker=dict(colors=[RED, ORANGE, "#FF8C5A", MUTED],
                        line=dict(color=BG, width=3)),
            textfont=dict(family="Space Mono", size=10, color=TEXT),
            textinfo="percent+label",
        ))
        fig5.update_layout(
            paper_bgcolor=BG, font=dict(family="Space Mono", color=TEXT),
            showlegend=False, height=320,
            margin=dict(l=0, r=0, t=20, b=0),
            annotations=[dict(text="3 307<br>errores", x=0.5, y=0.5,
                              showarrow=False,
                              font=dict(family="Syne", size=18, color=TEXT))],
        )
        st.plotly_chart(fig5, use_container_width=True)

    with cy:
        st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.1rem;
                    font-weight:700;color:#E8E6E0;margin-bottom:12px;">
                    Tiempos maximos por endpoint — P4</div>""",
                    unsafe_allow_html=True)
        eps   = ["Lista Asistencia","Lista Usuarios","Firmas Todo","Por firmar","Login"]
        avgs  = [8196, 6831, 6316, 632, 589]
        maxes = [128923, 53161, 41177, 1049, 765]
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(name="Promedio", y=eps, x=avgs, orientation="h",
                               marker=dict(color=BLUE, line=dict(width=0)),
                               text=[f"{v:,}ms" for v in avgs],
                               textfont=dict(family="Space Mono", size=9, color=TEXT),
                               textposition="outside"))
        fig6.add_trace(go.Bar(name="Maximo", y=eps, x=maxes, orientation="h",
                               marker=dict(color=RED, opacity=0.45, line=dict(width=0)),
                               text=[f"{v:,}ms" for v in maxes],
                               textfont=dict(family="Space Mono", size=9, color=TEXT),
                               textposition="outside"))
        fig6.update_layout(
            **{k: v for k, v in BASE.items() if k != "yaxis"},
            barmode="overlay",
            height=320,
            xaxis_title="ms",
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                tickfont=dict(size=9, color=MUTED),
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                font=dict(family="Space Mono", size=10),
            ),
        )
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown("<hr style='border:none;border-top:1px solid #1E1E2E;margin:24px 0;'>",
                unsafe_allow_html=True)
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.1rem;
                font-weight:700;color:#E8E6E0;margin-bottom:12px;">
                Requests exitosos vs fallos</div>""", unsafe_allow_html=True)
    loc_ok = [r - f for r, f in zip(loc_req, loc_fail)]
    fig7 = go.Figure()
    fig7.add_trace(go.Bar(name="Exitosos",
                          x=["P1 — 7","P2 — 25","P3 — 50","P4 — 100"],
                          y=loc_ok, marker=dict(color=GREEN, line=dict(width=0))))
    fig7.add_trace(go.Bar(name="Fallos",
                          x=["P1 — 7","P2 — 25","P3 — 50","P4 — 100"],
                          y=loc_fail, marker=dict(color=RED, line=dict(width=0))))
    fig7.update_layout(**BASE, barmode="stack", height=300, yaxis_title="Peticiones",
                       legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                   font=dict(family="Space Mono", size=10)))
    st.plotly_chart(fig7, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────
# TAB 3 — Comparativa
# ─────────────────────────────────────────────────────────────────────
with t3:
    st.markdown("""
    <div style="margin-bottom:4px;">
      <span style="font-family:'Space Mono',monospace;font-size:0.62rem;
                   letter-spacing:0.2em;text-transform:uppercase;color:#FF4B2B;">
        Comparativa directa
      </span>
    </div>
    <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;
                color:#E8E6E0;margin-bottom:14px;">k6 vs Locust — Error rate</div>
    <div style="background:#12121A;border-left:3px solid #FF4B2B;
                padding:12px 16px;border-radius:0 4px 4px 0;
                font-family:'Space Mono',monospace;font-size:0.76rem;
                color:#888;line-height:1.7;margin-bottom:20px;">
      Las herramientas miden estrategias distintas.
      <b style="color:#E8E6E0;">k6</b> hace login una vez y reutiliza el token.
      <b style="color:#E8E6E0;">Locust</b> hace login por cada usuario nuevo y satura el auth.
      No es que el sistema sea mas rapido en k6 — es que evita el cuello de botella de autenticacion.
    </div>
    """, unsafe_allow_html=True)

    xs = ["P1 (7)", "P2 (25)", "P3 (50)", "P4 (100)"]
    fig8 = go.Figure()
    fig8.add_trace(go.Scatter(
        x=xs, y=err_k6, name="k6", mode="lines+markers",
        line=dict(color=BLUE, width=2.5),
        marker=dict(size=12, color=BLUE, symbol="circle",
                    line=dict(width=2, color=BG)),
        fill="tozeroy", fillcolor="rgba(75,139,255,0.06)",
    ))
    fig8.add_trace(go.Scatter(
        x=xs, y=loc_ferr, name="Locust", mode="lines+markers",
        line=dict(color=RED, width=2.5),
        marker=dict(size=12, color=RED, symbol="diamond",
                    line=dict(width=2, color=BG)),
        fill="tozeroy", fillcolor="rgba(255,75,43,0.06)",
    ))
    fig8.add_hline(y=5, line=dict(color=ORANGE, width=1.5, dash="dot"),
                   annotation_text="LIMITE ACEPTABLE 5%",
                   annotation_font=dict(family="Space Mono", size=10, color=ORANGE),
                   annotation_position="top right")
    fig8.update_layout(**BASE, height=400, yaxis_title="Error rate (%)",
                       legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                   font=dict(family="Space Mono", size=11)))
    st.plotly_chart(fig8, use_container_width=True)

    st.markdown("<hr style='border:none;border-top:1px solid #1E1E2E;margin:24px 0;'>",
                unsafe_allow_html=True)
    cr, cl = st.columns(2)

    with cr:
        st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.1rem;
                    font-weight:700;color:#E8E6E0;margin-bottom:12px;">
                    k6 — Evolucion p(95) vs VUs</div>""", unsafe_allow_html=True)
        fig9 = go.Figure()
        fig9.add_trace(go.Scatter(
            x=vus, y=p95_cm, name="counter-moper", mode="lines+markers",
            line=dict(color=GREEN, width=2.5),
            marker=dict(size=10, color=GREEN, line=dict(width=2, color=BG)),
        ))
        fig9.add_trace(go.Scatter(
            x=vus, y=p95_ps, name="pending-signatures", mode="lines+markers",
            line=dict(color=BLUE, width=2.5),
            marker=dict(size=10, color=BLUE, line=dict(width=2, color=BG)),
        ))
        fig9.add_hline(y=LIMIT, line=dict(color=RED, width=1.5, dash="dot"),
                       annotation_text="1 000 ms",
                       annotation_font=dict(family="Space Mono", size=10, color=RED))
        fig9.add_vrect(x0=25, x1=50, fillcolor=RED, opacity=0.05, line_width=0,
                       annotation_text="QUIEBRE",
                       annotation_font=dict(family="Space Mono", size=9, color=RED),
                       annotation_position="top left")
        fig9.update_layout(**BASE, height=360,
                           xaxis_title="VUs", yaxis_title="ms",
                           legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                       font=dict(family="Space Mono", size=10)))
        st.plotly_chart(fig9, use_container_width=True)

    with cl:
        st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.1rem;
                    font-weight:700;color:#E8E6E0;margin-bottom:12px;">
                    Radar — Perfil P1 baseline</div>""", unsafe_allow_html=True)
        cats = ["Sin errores HTTP","Latencia baja","Auth estable",
                "Req/s alto","Checks completos"]
        fig10 = go.Figure()
        fig10.add_trace(go.Scatterpolar(
            r=[60, 90, 55, 40, 97], theta=cats, fill="toself", name="k6",
            line=dict(color=BLUE, width=2), fillcolor="rgba(75,139,255,0.12)",
        ))
        fig10.add_trace(go.Scatterpolar(
            r=[100, 80, 100, 20, 100], theta=cats, fill="toself", name="Locust P1",
            line=dict(color=GREEN, width=2), fillcolor="rgba(46,204,154,0.12)",
        ))
        fig10.update_layout(
            paper_bgcolor=BG,
            polar=dict(
                bgcolor=SURFACE,
                radialaxis=dict(visible=True, range=[0,100], gridcolor=BORDER,
                                tickfont=dict(size=8, color=MUTED)),
                angularaxis=dict(gridcolor=BORDER,
                                 tickfont=dict(family="Space Mono", size=9, color=MUTED)),
            ),
            legend=dict(orientation="h", font=dict(family="Space Mono", size=10),
                        yanchor="bottom", y=-0.18),
            height=360, margin=dict(l=40, r=40, t=20, b=50),
        )
        st.plotly_chart(fig10, use_container_width=True)

    st.markdown("<hr style='border:none;border-top:1px solid #1E1E2E;margin:24px 0;'>",
                unsafe_allow_html=True)
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.1rem;
                font-weight:700;color:#E8E6E0;margin-bottom:12px;">
                Tabla comparativa</div>""", unsafe_allow_html=True)
    comp = pd.DataFrame({
        "Aspecto": ["Estrategia login","Tokens","P1 error %","P2 error %",
                    "P3 error %","P4 error %","Punto quiebre","Causa principal fallo","Tipo medicion"],
        "k6": ["setup() — una vez","7 tokens reutilizados","4.93% (reset)","0.00%",
               "0.00% (pero p95 > 5s)","6.31%","Entre 25 y 50 VUs",
               "Latencia — backend lento","Rendimiento puro del endpoint"],
        "Locust": ["on_start() — por usuario","Token nuevo por sesion","0.00%","91.0%",
                   "88.4%","94.6%","Entre 7 y 25 users",
                   "401 Unauthorized — auth saturada","Flujo real usuario (login + uso)"],
    })
    st.dataframe(comp, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────
# TAB 4 — Diagnostico
# ─────────────────────────────────────────────────────────────────────
with t4:
    st.markdown("""
    <div style="margin-bottom:4px;">
      <span style="font-family:'Space Mono',monospace;font-size:0.62rem;
                   letter-spacing:0.2em;text-transform:uppercase;color:#FF4B2B;">
        Diagnostico tecnico
      </span>
    </div>
    <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;
                color:#E8E6E0;margin-bottom:24px;">Hallazgos y plan de accion</div>
    """, unsafe_allow_html=True)

    dg1, dg2 = st.columns(2)
    with dg1:
        for color, titulo, cuerpo in [
            (RED, "Problema 1 — Autenticacion concurrente",
             "Locust colapsa desde 25 usuarios con 401 Unauthorized.<br>"
             "El backend invalida tokens bajo login concurrente.<br><br>"
             "— TOKEN_LIMIT_PER_USER en Knox / JWT<br>"
             "— Rate limiting en /api/login/ via axes<br>"
             "— Sesiones sobreescritas entre usuarios<br>"
             "— axes bloqueando IPs por intentos simultaneos"),
            (RED, "Problema 2 — Latencia alta a 50+ VUs",
             "k6 muestra p(95) de 5 segundos desde 50 VUs sin errores HTTP.<br>"
             "El servidor responde pero muy lento.<br><br>"
             "— DEBUG=True activo — guarda cada query en memoria<br>"
             "— Pool PostgreSQL agotado sin CONN_MAX_AGE<br>"
             "— Pocos workers Daphne activos en local"),
        ]:
            st.markdown(f"""
            <div style="background:#12121A;border-left:3px solid {color};
                        padding:16px 18px;border-radius:0 4px 4px 0;margin-bottom:14px;">
              <div style="font-family:'Syne',sans-serif;font-size:0.95rem;
                          font-weight:700;color:{color};margin-bottom:8px;">{titulo}</div>
              <div style="font-family:'Space Mono',monospace;font-size:0.72rem;
                          color:#888;line-height:1.7;">{cuerpo}</div>
            </div>""", unsafe_allow_html=True)

    with dg2:
        for color, titulo, cuerpo in [
            (GREEN, "Lo que funciona bien",
             "Con 7 a 25 usuarios los endpoints responden en menos de 1 segundo.<br><br>"
             "— counter-moper p(95) = 707 ms con 7 VUs<br>"
             "— pending-signatures p(95) = 313 ms con 7 VUs<br>"
             "— 0% errores HTTP en P2 de k6 con 25 VUs<br>"
             "— counter-moper p(95) = 850 ms con 25 VUs"),
            (ORANGE, "Endpoints criticos en Locust",
             "En P1 con solo 7 usuarios y 0 errores, dos endpoints fueron inaceptables:<br><br>"
             "— Lista Asistencia: avg 30 055 ms, max 33 942 ms<br>"
             "— Lista Usuarios: avg 13 195 ms, max 16 427 ms<br><br>"
             "Son lentos incluso sin concurrencia — problema de queries, no de carga."),
        ]:
            st.markdown(f"""
            <div style="background:#12121A;border-left:3px solid {color};
                        padding:16px 18px;border-radius:0 4px 4px 0;margin-bottom:14px;">
              <div style="font-family:'Syne',sans-serif;font-size:0.95rem;
                          font-weight:700;color:{color};margin-bottom:8px;">{titulo}</div>
              <div style="font-family:'Space Mono',monospace;font-size:0.72rem;
                          color:#888;line-height:1.7;">{cuerpo}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid #1E1E2E;margin:24px 0;'>",
                unsafe_allow_html=True)
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.1rem;
                font-weight:700;color:#E8E6E0;margin-bottom:16px;">
                Recomendaciones priorizadas</div>""", unsafe_allow_html=True)

    recs = [
        (RED,    "ALTA",  "Desactivar DEBUG=False",
         "Django guarda cada query SQL en memoria con DEBUG=True. Puede reducir latencia 30-50%. Cambio mas rapido y de mayor impacto."),
        (RED,    "ALTA",  "Revisar TOKEN_LIMIT_PER_USER en Knox",
         "El 401 masivo de Locust apunta a un limite de sesiones por usuario. Revisar knox.REST_KNOX y el middleware axes que puede bloquear IPs."),
        (ORANGE, "MEDIA", "Agregar CONN_MAX_AGE=60 en DATABASES",
         "Sin este parametro Django abre y cierra una conexion a PostgreSQL en cada peticion. Bajo 50+ VUs agota el pool rapidamente."),
        (ORANGE, "MEDIA", "Aumentar workers Daphne/Gunicorn",
         "Regla: (2 x nucleos CPU) + 1. En Mac con 8 nucleos = 17 workers. La concurrencia esta limitada por workers activos."),
        (GREEN,  "BAJA",  "Optimizar Lista Asistencia con EXPLAIN ANALYZE",
         "30 segundos de avg con 7 usuarios indica queries N+1 o falta de indices. Usar select_related/prefetch_related."),
        (GREEN,  "BAJA",  "Prueba biseccion k6 entre 25 y 50 VUs",
         "Probar 30, 35, 40 VUs con DEBUG=False para encontrar el limite real del sistema con configuracion correcta."),
    ]

    for color, prio, titulo, cuerpo in recs:
        st.markdown(f"""
        <div style="background:#12121A;border-left:3px solid {color};
                    border-radius:0 4px 4px 0;padding:14px 18px;margin-bottom:10px;
                    display:flex;gap:16px;align-items:flex-start;">
          <div style="min-width:48px;">
            <span style="font-family:'Space Mono',monospace;font-size:0.6rem;
                         letter-spacing:0.1em;color:{color};">{prio}</span>
          </div>
          <div>
            <div style="font-family:'Syne',sans-serif;font-size:0.92rem;
                        font-weight:700;color:#E8E6E0;margin-bottom:4px;">{titulo}</div>
            <div style="font-family:'Space Mono',monospace;font-size:0.7rem;
                        color:#777;line-height:1.6;">{cuerpo}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid #1E1E2E;margin:24px 0;'>",
                unsafe_allow_html=True)
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.1rem;
                font-weight:700;color:#E8E6E0;margin-bottom:12px;">
                Mapa de calor — Estado por escenario</div>""", unsafe_allow_html=True)

    fig_heat = go.Figure(go.Heatmap(
        z=[[0.3, 0.0, 1.0, 1.0], [0.0, 1.0, 1.0, 1.0]],
        x=["P1 — 7", "P2 — 25", "P3 — 50", "P4 — 100"],
        y=["k6", "Locust"],
        text=[["Advertencia","Pasa","Falla p95","Falla p95+err"],
              ["Estable","91% 401","88% 401","95% 401"]],
        texttemplate="%{text}",
        textfont=dict(family="Space Mono", size=11, color=TEXT),
        colorscale=[[0,"#0A2A1A"],[0.35,"#2A1A00"],[1,"#2A0A0A"]],
        showscale=False, xgap=4, ygap=4,
    ))
    fig_heat.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(family="Space Mono", color=TEXT),
        height=180,
        margin=dict(l=80, r=16, t=16, b=40),
        xaxis=dict(tickfont=dict(size=11, color=MUTED), side="bottom"),
        yaxis=dict(tickfont=dict(size=11, color=MUTED)),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:0.6rem;
                color:#222;text-align:center;margin-top:32px;letter-spacing:0.12em;">
      PERFORMANCE ANALYSIS &mdash; MAYO 2026 &mdash; LOCAL MAC &mdash; DEBUG=TRUE
    </div>""", unsafe_allow_html=True)