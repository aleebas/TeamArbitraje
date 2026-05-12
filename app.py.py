import streamlit as st
import math

st.set_page_config(page_title="Team Arbitraje", layout="wide", initial_sidebar_state="collapsed")

# --- CSS APLANADO Y CORTO ---
st.markdown("<style>.block-container{padding-top:3.5rem!important;padding-bottom:1rem!important} h1,h2,h3,h4,p,label,.stMarkdown{font-weight:700!important} .stNumberInput div div input {background-color: var(--background-color)!important; color: var(--text-color)!important; border: 2px solid rgba(128,128,128,0.3)!important; border-radius: 8px; font-weight: 900!important; font-size: 15px!important; text-align: center; padding: 4px!important; height: 34px!important;} .stNumberInput div div input:focus { border-color: #0ea5e9!important; } .highlight-action { background-color: #fef08a; padding:6px; border-radius:8px; color:#854d0e; text-align:center; font-size:15px; font-weight:900; margin-bottom:5px; border:1px dashed #ca8a04; } .highlight-celeste { background-color: #e0f2fe; padding:6px; border-radius:8px; color:#0369a1; text-align:center; font-size:15px; font-weight:900; margin-bottom:5px; border:1px dashed #0284c7; } div[data-testid='stMetric']{background-color: var(--secondary-background-color); padding: 6px 10px!important; border-radius: 10px; border: 1px solid rgba(128,128,128,0.2)!important;}</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;color:#0ea5e9!important;'>🚀 RUTA DIRECTA (BDV)</h1><div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

# --- TASAS GLOBALES ---
c1, c2 = st.columns(2)
with c1: tasa_c = st.number_input("📉 Tasa Compra BDV", value=611.00, step=0.01)
with c2: tasa_v = st.number_input("📈 Tasa Venta P2P", value=648.00, step=0.01)
tasa_real_b = tasa_c * 1.005

radar_placeholder = st.empty()
st.markdown("<hr>", unsafe_allow_html=True)

# --- FLUJO DE CÁLCULO ---
tipo_v = st.radio("🔄 Dirección:", ["➡️ Normal", "⬅️ Inversa"], horizontal=True)

if tipo_v == "➡️ Normal":
    st.markdown("<h3 style='margin:0;'>1️⃣ Fondeo BDV</h3>", unsafe_allow_html=True)
    t_ing = st.radio("Ingreso en:", ["Bs", "USD"], horizontal=True, label_visibility="collapsed")
    
    if t_ing == "Bs":
        cap_bs = st.number_input("Monto (Bs.)", value=61100.00, step=100.0)
        usd_banco = cap_bs/tasa_real_b if tasa_real_b>0 else 0
        st.markdown(f"<div class='highlight-celeste'>💵 COMPRASTE:<br><span style='font-size:22px;'>${usd_banco:,.2f}</span></div>", unsafe_allow_html=True)
    else:
        usd_banco = st.number_input("Monto (USD)", value=100.00, step=10.0)
        cap_bs = usd_banco*tasa_real_b
        st.markdown(f"<div class='highlight-celeste'>🇻🇪 FONDEO NECESARIO:<br><span style='font-size:22px;'>Bs.{cap_bs:,.2f}</span></div>", unsafe_allow_html=True)

    if usd_banco > 0:
        vueltas_sug = math.ceil(1950 / usd_banco)
        st.markdown(f"<p style='text-align:center; font-size:11.5px; color:#6b7280; margin-top:-3px; margin-bottom:12px;'>💡 <b>Sugerencia:</b> {vueltas_sug} vueltas aprox. para límite ($1,950).</p>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin:0;'>2️⃣ Recarga Tarjeta</h3>", unsafe_allow_html=True)
    tipo_tarjeta = st.radio("Tipo de Tarjeta BDV:", ["💳 Física (1.5%)", "📱 Digital (2.5%)"], horizontal=True)
    factor_tarjeta = 0.985 if "Física" in tipo_tarjeta else 0.975

    dej_usd = st.checkbox("Dejar $0.30 holgura (Fallas)", value=True)
    usd_base = max(0.0, (usd_banco-0.30) if dej_usd else usd_banco)
    
    sug_tarj = usd_base * factor_tarjeta
    st.markdown(f"<div class='highlight-action'>⚠️ TECLEAR EN APP:<br><span style='font-size:22px;'>${sug_tarj:,.2f}</span></div>", unsafe_allow_html=True)
    conf_tarj = st.number_input("👉 Confirma monto app:", value=float(f"{sug_tarj:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;'>3️⃣ Recibido Binance</h3>", unsafe_allow_html=True)
    sug_bin = conf_tarj * 0.964
    conf_usdt = st.number_input(f"👉 USDT acreditados reales (≈₮{sug_bin:,.2f}):", value=float(f"{sug_bin:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;'>4️⃣ Venta P2P</h3>", unsafe_allow_html=True)
    usdt_vend = st.number_input("USDT a Vender:", value=float(conf_usdt), step=1.0)
    sug_bs_rec = usdt_vend * tasa_v
    conf_bs_rec = st.number_input(f"👉 Bs. Recibidos (≈Bs.{sug_bs_rec:,.2f}):", value=float(f"{sug_bs_rec:.2f}"), step=100.0)

    g_bs = conf_bs_rec - cap_bs
    g_usdt = g_bs/tasa_v if tasa_v>0 else 0
    roi = (g_bs/cap_bs)*100 if cap_bs>0 else 0
    h_cap = cap_bs

else:
    st.markdown("<h3 style='margin:0;'>1️⃣ Venta Inicial P2P</h3>", unsafe_allow_html=True)
    usdt_ini = st.number_input("USDT Iniciales:", value=100.00, step=1.0)
    sug_bs_inv = usdt_ini * tasa_v
    conf_bs_inv = st.number_input(f"👉 Bs. Recibidos (≈Bs.{sug_bs_inv:,.2f}):", value=float(f"{sug_bs_inv:.2f}"), step=100.0)

    st.markdown("<h3 style='margin:0;'>2️⃣ Fondeo BDV (Re-inversión)</h3>", unsafe_allow_html=True)
    bs_inv = st.number_input("Bs. para comprar USD:", value=float(conf_bs_inv), step=100.0)
    usd_banco = bs_inv/tasa_real_b if tasa_real_b>0 else 0
    st.markdown(f"<div class='highlight-celeste'>💵 COMPRASTE:<br><span style='font-size:22px;'>${usd_banco:,.2f}</span></div>", unsafe_allow_html=True)
    
    if usd_banco > 0:
        vueltas_sug = math.ceil(1950 / usd_banco)
        st.markdown(f"<p style='text-align:center; font-size:11.5px; color:#6b7280; margin-top:-3px; margin-bottom:12px;'>💡 <b>Sugerencia:</b> {vueltas_sug} vueltas aprox. para límite ($1,950).</p>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin:0;'>3️⃣ Recarga Tarjeta</h3>", unsafe_allow_html=True)
    tipo_tarjeta = st.radio("Tipo de Tarjeta BDV:", ["💳 Física (1.5%)", "📱 Digital (2.5%)"], horizontal=True)
    factor_tarjeta = 0.985 if "Física" in tipo_tarjeta else 0.975

    dej_usd = st.checkbox("Dejar $0.30 holgura (Fallas)", value=True)
    usd_base_inv = max(0.0, (usd_banco-0.30) if dej_usd else usd_banco)
    
    sug_tarj_inv = usd_base_inv * factor_tarjeta
    st.markdown(f"<div class='highlight-action'>⚠️ TECLEAR EN APP:<br><span style='font-size:22px;'>${sug_tarj_inv:,.2f}</span></div>", unsafe_allow_html=True)
    conf_tarj_inv = st.number_input("👉 Confirma monto app:", value=float(f"{sug_tarj_inv:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;'>4️⃣ USDT Recuperados</h3>", unsafe_allow_html=True)
    sug_bin_inv = conf_tarj_inv * 0.964
    usdt_fin = st.number_input(f"👉 USDT recuperados reales (≈₮{sug_bin_inv:,.2f}):", value=float(f"{sug_bin_inv:.2f}"), step=1.0)

    g_usdt = usdt_fin - usdt_ini
    g_bs = g_usdt * tasa_v
    roi = (g_usdt/usdt_ini)*100 if usdt_ini>0 else 0
    h_cap = bs_inv

# --- RADAR DE PROYECCIÓN (Se inyecta arriba) ---
u_base_teo = max(0.0, (usd_banco-0.30) if dej_usd else usd_banco)
u_fin_teo = u_base_teo * factor_tarjeta * 0.964
t_sug = (h_cap*1.02)/u_fin_teo if u_fin_teo>0 else 0
bs_rec_teo = u_fin_teo * tasa_v
g_bs_teo = bs_rec_teo - h_cap
g_u_teo = g_bs_teo/tasa_v if tasa_v>0 else 0
roi_teo = (g_bs_teo/h_cap)*100 if h_cap>0 else 0
c_roi = '#ef4444' if roi_teo<2 else '#10b981'

radar_html = f"<div style='background-color: var(--secondary-background-color); border:1px solid rgba(16,185,129,.3); padding:12px; border-radius:12px; margin:5px 0 15px;'><p style='margin:0;font-size:11px;color:#6b7280;'>🔍 PROYECCIÓN P2P (Basado en ${usd_banco:,.2f})</p><div style='display:flex;justify-content:space-between;margin-top:5px;'><div><p style='margin:0;font-size:13px;color:var(--text-color);'>🎯 Sugerida(2%): <b style='color:#f59e0b;'>Bs.{t_sug:,.2f}</b></p><p style='margin:0;font-size:13px;color:var(--text-color);'>📊 ROI Teórico: <b style='color:{c_roi};'>{roi_teo:,.2f}%</b></p></div><div style='text-align:right;'><p style='margin:0;font-size:10px;color:#6b7280;'>GANANCIA</p><p style='margin:0;font-size:16px;font-weight:900;color:#0ea5e9;'>Bs.{g_bs_teo:,.2f}</p><p style='margin:0;font-size:13px;color:#10b981;'>≈₮{g_u_teo:,.2f}</p></div></div></div>"
radar_placeholder.markdown(radar_html, unsafe_allow_html=True)

# --- MÉTRICAS FINALES REALES ---
st.markdown("<hr style='margin-bottom:8px; border-color:rgba(128,128,128,0.2);'>", unsafe_allow_html=True)
r1, r2 = st.columns(2)
r1.markdown(f"<div data-testid='stMetric'><p style='font-size:11px;color:#6b7280;margin:0;font-weight:800;'>GANANCIA NETA</p><div style='display:flex;gap:6px;margin-top:2px;'><span style='font-size:18px;color:#0ea5e9;font-weight:900;'>Bs.{g_bs:,.2f}</span><span style='font-size:13px;color:#10b981;font-weight:800;'>₮{g_usdt:,.2f}</span></div></div>", unsafe_allow_html=True)
r2.metric("ROI REAL", f"{roi:.2f}%")
