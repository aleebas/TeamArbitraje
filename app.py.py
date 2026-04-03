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

# ELIMINADO: Bloque del Logo (SVG y Base64). 

# Comienzo limpio directamente con el título y separador
st.markdown("<h2 style='text-align: center;'>🚀 RUTA DIRECTA</h2><hr style='margin-bottom: 15px;'>", unsafe_allow_html=True)

# Lógica de Cupo y Récords Diario (PRESERVADA AL 100%)
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

# SIDEBAR: Control de Cupo y Récord (PRESERVADO AL 100%)
st.sidebar.header("🛡️ CONTROL DE CUPO")
st.sidebar.metric("Cupo Diario Libre", f"$ {2000 - cupo_dia_usado:,.2f}")
st.sidebar.progress(min(cupo_dia_usado / 2000, 1.0))

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏆 RÉCORD DE HOY")
st.sidebar.metric("🔄 Vueltas Completadas", vueltas_hoy)
st.sidebar.metric("💰 Ganancia Acumulada", f"Bs. {ganancia_acumulada:,.2f}")
st.sidebar.metric("🔥 Mejor Vuelta", f"Bs. {mejor_vuelta:,.2f}")

# Comisiones Fijas (PRESERVADAS AL 100%)
c_tarjeta = 0.025 # 2.5%
c_binance = 0.033 # 3.3%

# INPUTS: Datos de Entrada (PRESERVADO AL 100%)
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

# LÓGICA DE NEGOCIO EN CASCADA (Calculo Exacto - PRESERVADO AL 100%)
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

# --- MODIFICACIÓN DE MÉTRICA DE GANANCIA (image_2.png) ---
# Reemplazo st.metric por HTML customizado para el diseño híbrido Bs + USDT Verde
gan_usdt = gan_bs / tasa_v if tasa_v != 0 else 0
# res1.metric("GANANCIA NETA", f"Bs. {gan_bs:,.2f}") # Reemplazado

with res1:
    st.markdown(f"""
    <div data-testid="stMetric" style="background-color: #1e293b !important; padding: 10px; border-radius: 12px; border: 1px solid #334155 !important;">
        <p style="font-weight: 800 !important; color: #94a3b8 !important; font-size: 14px !important; text-transform: uppercase; margin: 0;">GANANCIA NETA</p>
        <p style="font-weight: 900 !important; color: #38bdf8 !important; font-size: 32px !important; margin: 0;">Bs. {gan_bs:,.2f}</p>
        <p style="color: #16a34a !important; font-weight: 700 !important; font-size: 14px !important; margin-top: -5px; margin-bottom: 0;">≈ ₮ {gan_usdt:,.2f} Netos</p>
    </div>
    """, unsafe_allow_html=True)

# Resto de métricas estándar (PRESERVADO AL 100%)
res2.metric("ROI REAL", f"{roi:.2f}%")
res3.metric("BRECHA", f"{brecha:.2f}%")

# Ticket Estilo WhatsApp (PRESERVADO AL 100%)
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

# Guardar en Historial (PRESERVADO AL 100%)
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
    
