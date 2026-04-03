import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# Configuración inicial de la página
st.set_page_config(page_title="Team Arbitraje Directo", layout="wide")

# Estilo Restful Blue y Ticket WhatsApp Mobile-First
st.markdown("""
    <style>
    .main { background-color: #10172a; color: #e2e8f0; }
    div[data-testid="stMetric"] { background-color: #1e293b !important; padding: 10px; border-radius: 12px; border: 1px solid #334155 !important; }
    div[data-testid="stMetricValue"] { font-weight: 900 !important; color: #38bdf8 !important; }
    div[data-testid="stMetricLabel"] p { font-weight: 800 !important; color: #94a3b8 !important; font-size: 14px !important; text-transform: uppercase; }
    h1, h2, h3, p, label, .stMarkdown { color: #e2e8f0 !important; font-weight: 700 !important; }
    .stNumberInput div div input { color: #e2e8f0 !important; background-color: #1f2937 !important; border: 1px solid #334155 !important; font-weight: 800 !important; }
    .ticket-wrapper { display: flex; justify-content: center; padding: 10px; }
    
    /* Optimización Mobile para el Ticket */
    .whatsapp-ticket { background-color: #ffffff; border: 4px dashed #16a34a; border-radius: 20px; padding: 20px; width: 100%; max-width: 450px; color: #000000; box-shadow: 0 8px 20px rgba(0,0,0,0.3); margin-top: 20px;}
    
    .ticket-header { text-align: center; font-size: 18px; font-weight: 900; color: #16a34a; border-bottom: 3px solid #16a34a; padding-bottom: 10px; margin-bottom: 15px; }
    .ticket-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #e2e8f0; color: #000000; align-items: center; }
    .ticket-label { font-size: 15px; font-weight: 700; color: #334155; }
    .ticket-value { font-size: 15px; font-weight: 900; color: #000000; text-align: right; }
    .ticket-roi-box { text-align: center; font-size: 22px; font-weight: 900; color: #16a34a; background-color: #f0fdf4; padding: 12px; border-radius: 12px; margin-top: 15px; border: 2px solid #16a34a; }
    </style>
    """, unsafe_allow_html=True)

# Logo SVG Blindado con Base64 (Nunca se romperá en móvil)
logo_svg = """<svg viewBox="0 0 200 200" width="180" height="180" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#020617"/>
    </radialGradient>
    <path id="textPathTop" d="M 30,100 A 70,70 0 0,1 170,100" />
    <path id="textPathBot" d="M 170,105 A 70,70 0 0,1 30,105" />
  </defs>
  <circle cx="100" cy="100" r="95" fill="url(#bgGrad)" stroke="#38bdf8" stroke-width="2"/>
  <text fill="#e2e8f0" font-size="16" font-weight="900" font-family="sans-serif" letter-spacing="1">
    <textPath href="#textPathTop" startOffset="50%" text-anchor="middle">TEAM ARBITRAJE</textPath>
  </text>
  <text fill="#22d3ee" font-size="14" font-weight="800" font-family="sans-serif" letter-spacing="2">
    <textPath href="#textPathBot" startOffset="50%" text-anchor="middle">RUTA DIRECTA</textPath>
  </text>
  <rect x="75" y="95" width="12" height="30" fill="#475569" rx="2"/>
  <rect x="95" y="80" width="12" height="45" fill="#94a3b8" rx="2"/>
  <rect x="115" y="60" width="12" height="65" fill="#38bdf8" rx="2"/>
  <path d="M 55,130 Q 100,130 135,75" fill="none" stroke="#22d3ee" stroke-width="4" stroke-linecap="round"/>
  <polygon points="142,65 125,75 140,85" fill="#22d3ee" transform="rotate(-15 135 75)"/>
  <rect x="45" y="120" width="20" height="20" fill="#cbd5e1" rx="4"/>
  <path d="M 50,135 L 60,135" stroke="#475569" stroke-width="2"/>
  <polygon points="150,45 162,52 162,65 150,72 138,65 138,52" fill="#020617" stroke="#22d3ee" stroke-width="2"/>
  <text x="150" y="62" fill="#22d3ee" font-size="10" font-weight="bold" font-family="sans-serif" text-anchor="middle">₮</text>
</svg>"""

b64_logo = base64.b64encode(logo_svg.encode('utf-8')).decode('utf-8')
st.markdown(f'<div style="text-align: center; margin-bottom: 10px;"><img src="data:image/svg+xml;base64,{b64_logo}"></div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>🚀 RUTA DIRECTA</h2><hr>", unsafe_allow_html=True)

# Lógica de Cupo y Récords Diario
hoy_str = datetime.now().strftime("%Y-%m-%d")
archivo_historial = "historial_directo.csv"

if os.path.exists(archivo_historial):
    df_h = pd.read_csv(archivo_historial)
    df_hoy = df_h[df_h['Día'] == hoy_str]
    cupo_dia_usado = df_hoy['USD_Comprados'].sum()
    if not df_hoy.empty:
        mejor_vuelta = df_hoy['Ganancia_Bs'].max()
        ganancia_acumulada = df_hoy['Ganancia_Bs'].sum()
        vueltas_hoy = len(df_hoy)
    else:
        mejor_vuelta = 0.0
        ganancia_acumulada = 0.0
        vueltas_hoy = 0
else: 
    cupo_dia_usado = 0.0
    mejor_vuelta = 0.0
    ganancia_acumulada = 0.0
    vueltas_hoy = 0

# SIDEBAR: Control de Cupo y Récord
st.sidebar.header("🛡️ CONTROL DE CUPO")
st.sidebar.metric("Cupo Diario Libre", f"$ {2000 - cupo_dia_usado:,.2f}")
st.sidebar.progress(min(cupo_dia_usado / 2000, 1.0))

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏆 RÉCORD DE HOY")
st.sidebar.metric("🔄 Vueltas Completadas", vueltas_hoy)
st.sidebar.metric("💰 Ganancia Acumulada", f"Bs. {ganancia_acumulada:,.2f}")
st.sidebar.metric("🔥 Mejor Vuelta", f"Bs. {mejor_vuelta:,.2f}")

# Comisiones Fijas
c_tarjeta = 0.025 # 2.5%
c_binance = 0.033 # 3.3%

# INPUTS: Datos de Entrada
col1, col2 = st.columns(2)
with col1:
    banco = st.selectbox("🏦 Banco Origen:", ["BDV", "BANCAMIGA"])
    cap_bs = st.number_input("Capital Invertido (Bs.)", value=40000.0)
with col2:
    tasa_c = st.number_input("📉 Tasa Compra (Base)", value=57.0)
    tasa_v = st.number_input("📈 Tasa Venta P2P", value=66.0)

c_asig = 0.005 if banco == "BDV" else 0.008
tasa_real_b = tasa_c * (1 + c_asig)
usd_en_banco = cap_bs / tasa_real_b

# LÓGICA DE NEGOCIO EN CASCADA (Calculo Exacto)
st.markdown("### 🧮 Simulación en Cascada")
dejar_dolar = st.checkbox("Dejar $1 en la cuenta por seguridad", value=True)

# Matematicas
usd_base = (usd_en_banco - 1.0) if dejar_dolar else usd_en_banco
usd_post_tarjeta = usd_base * (1 - c_tarjeta)
usdt_finales = usd_post_tarjeta * (1 - c_binance)

gan_bs = (usdt_finales * tasa_v) - cap_bs
roi = (gan_bs / cap_bs) * 100
brecha = ((tasa_v / tasa_real_b) - 1) * 100

# Panel visual del descuento
st.info(f"""
1️⃣ **Fondo Total Disponible:** $ {usd_en_banco:,.2f} \n
2️⃣ **Monto a pasar por Tarjeta:** $ {usd_base:,.2f} \n
3️⃣ **Neto tras Tarjeta (-2.5%):** $ {usd_post_tarjeta:,.2f} \n
4️⃣ **Final en Binance (-3.3%):** ₮ {usdt_finales:,.2f}
""")

st.markdown("### 📊 Rendimiento de esta Vuelta")
res1, res2, res3 = st.columns(3)
res1.metric("GANANCIA NETA", f"Bs. {gan_bs:,.2f}")
res2.metric("ROI REAL", f"{roi:.2f}%")
res3.metric("BRECHA", f"{brecha:.2f}%")

# Ticket Estilo WhatsApp
ticket_html = f"""
<div class="ticket-wrapper">
    <div class="whatsapp-ticket">
        <div class="ticket-header">📋 REPORTE DIRECTO - {banco}</div>
        <div class="ticket-row"><span class="ticket-label">💵 Capital:</span><span class="ticket-value">Bs. {cap_bs:,.2f}</span></div>
        <div class="ticket-row"><span class="ticket-label">📉 Compra:</span><span class="ticket-value">Bs. {tasa_real_b:,.2f}</span></div>
        <div class="ticket-row"><span class="ticket-label">📈 Venta:</span><span class="ticket-value">Bs. {tasa_v:,.2f}</span></div>
        <div class="ticket-row"><span class="ticket-label">↔️ Brecha:</span><span class="ticket-value">{brecha:.2f}%</span></div>
        <div class="ticket-row" style="border:none;"><span class="ticket-label">💰 Ganancia:</span><span class="ticket-value" style="color:#16a34a;">Bs. {gan_bs:,.2f}</span></div>
        <div class="ticket-roi-box">🚀 ROI REAL: {roi:.2f}%</div>
    </div>
</div>
"""
st.write(ticket_html, unsafe_allow_html=True)

# Guardar en Historial
st.markdown("<br>", unsafe_allow_html=True)
if st.button("💾 GUARDAR VUELTA", use_container_width=True):
    nuevo_registro = {
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), 
        "Día": hoy_str, 
        "USD_Comprados": usd_en_banco, 
        "Ganancia_Bs": gan_bs, 
        "ROI": roi
    }
    pd.DataFrame([nuevo_registro]).to_csv(
        archivo_historial, 
        mode='a', 
        header=not os.path.exists(archivo_historial), 
        index=False
    )
    st.success("¡Vuelta registrada con éxito! Actualiza la página para ver tu nuevo Récord.")
    st.balloons()
