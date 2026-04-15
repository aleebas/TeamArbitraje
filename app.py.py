import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración inicial de la página
st.set_page_config(page_title="Team Arbitraje Directo", layout="wide", initial_sidebar_state="collapsed")

# Estilo Premium (Glassmorphism) COMPACTADO
st.markdown("""
    <style>
    .block-container { padding-top: 3.5rem !important; padding-bottom: 1.0rem !important; }
    .main { background-color: #0f172a; color: #e2e8f0; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    h1, h2, h3, h4, p, label, .stMarkdown { color: #f8fafc !important; font-weight: 700 !important; }
    
    h1 { font-size: 1.5rem !important; margin-bottom: 0rem !important; padding-bottom: 0 !important; }
    h3 { font-size: 1.1rem !important; margin-bottom: 0.1rem !important; margin-top: 0.5rem !important; }
    h4 { font-size: 1.0rem !important; margin-bottom: 0.2rem !important; }
    hr { margin-top: 0.5rem !important; margin-bottom: 0.8rem !important; border-color: rgba(255,255,255,0.05) !important; }
    
    .stNumberInput div div input { 
        color: #38bdf8 !important; 
        background-color: rgba(15, 23, 42, 0.8) !important; 
        border: 2px solid #334155 !important; 
        border-radius: 8px;
        font-weight: 900 !important; 
        font-size: 15px !important; 
        text-align: center;
        transition: all 0.3s ease;
        padding: 4px !important;
        height: 34px !important;
    }
    .stNumberInput div div input:focus { border-color: #38bdf8 !important; box-shadow: 0 0 8px rgba(56,189,248,0.2) !important; }
    
    .dashboard-panel, .radar-box { 
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        backdrop-filter: blur(12px);
        padding: 12px 15px !important; 
        border-radius: 12px; 
        border: 1px solid rgba(255, 255, 255, 0.05); 
        margin-bottom: 10px !important; 
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); 
    }
    
    div[data-testid="stMetric"] { 
        background: linear-gradient(145deg, #1e293b, #0f172a) !important; 
        padding: 6px 10px !important; 
        border-radius: 10px; 
        border: 1px solid rgba(56, 189, 248, 0.2) !important; 
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stMetricValue"] { font-size: 1.2rem !important; font-weight: 900 !important; color: #38bdf8 !important; text-shadow: 0 0 5px rgba(56,189,248,0.3); }
    div[data-testid="stMetricLabel"] p { font-weight: 800 !important; color: #94a3b8 !important; font-size: 11px !important; letter-spacing: 0.5px; margin-bottom: 0 !important; }
    
    .highlight-action { background: linear-gradient(135deg, #fef08a, #facc15); padding: 6px; border-radius: 8px; color: #000; text-align: center; font-size: 15px; font-weight: 900; margin-bottom: 5px; border: 1px dashed #854d0e; }
    
    /* NUEVO: ESTILO DEL RESUMEN DIARIO DINÁMICO */
    .summary-box { 
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.98)); 
        border-radius: 16px; 
        padding: 18px; 
        border: 1px solid rgba(56,189,248,0.4); 
        box-shadow: 0 8px 25px rgba(0,0,0,0.5); 
        margin-top: 20px; 
        margin-bottom: 15px;
    }
    .summary-header { text-align: center; color: #facc15; font-size: 16px; font-weight: 900; letter-spacing: 1px; border-bottom: 1px dashed rgba(255,255,255,0.2); padding-bottom: 10px; margin-bottom: 15px; text-transform: uppercase; }
    .summary-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
    .summary-item { background: rgba(0,0,0,0.25); padding: 12px; border-radius: 10px; text-align: center; border: 1px solid rgba(255,255,255,0.05); }
    .summary-item-full { grid-column: span 2; background: linear-gradient(to right, rgba(16,185,129,0.1), rgba(15,23,42,0.5)); border: 1px solid rgba(16,185,129,0.4); padding: 15px; border-radius: 12px; text-align: center;}
    .sum-label { font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 800; margin-bottom: 4px; display: block; }
    .sum-val { font-size: 15px; color: #e2e8f0; font-weight: 900; }
    .sum-val.highlight { color: #38bdf8; font-size: 17px; }
    .sum-val.success { color: #10b981; font-size: 22px; text-shadow: 0 0 10px rgba(16,185,129,0.3);}
    </style>
    """, unsafe_allow_html=True)

# Título Principal
st.markdown("<h1 style='text-align: center; color: #38bdf8 !important;'>🚀 RUTA DIRECTA (BDV)</h1><div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# LÓGICA DE HISTORIAL BLINDADA (SESSION STATE + CSV)
# ---------------------------------------------------------
hoy_str = datetime.now().strftime("%Y-%m-%d")
mes_str = datetime.now().strftime("%Y-%m")
archivo_historial = "historial_directo.csv"

columnas_historial = ['Fecha', 'Día', 'Mes', 'Cuenta', 'Cap_Invertido_Bs', 'USD_Comprados', 'USDT_Vendidos', 'Tasa_Venta', 'Bs_Recibidos', 'Ganancia_Bs', 'ROI']

if 'historial_df' not in st.session_state:
    if os.path.exists(archivo_historial):
        df_temp = pd.read_csv(archivo_historial)
        for col in columnas_historial:
            if col not in df_temp.columns:
                df_temp[col] = 0.0
        st.session_state.historial_df = df_temp
    else:
        st.session_state.historial_df = pd.DataFrame(columns=columnas_historial)

df_h = st.session_state.historial_df

# ---------------------------------------------------------
# DASHBOARD DE CONTROL 
# ---------------------------------------------------------
cuentas_lista = [f"Cuenta {i}" for i in range(1, 7)]
cuenta_activa = st.session_state.get('cuenta_activa', cuentas_lista[0])

df_cuenta_hoy = df_h[(df_h['Cuenta'] == cuenta_activa) & (df_h['Día'] == hoy_str)]
df_cuenta_mes = df_h[(df_h['Cuenta'] == cuenta_activa) & (df_h['Mes'] == mes_str)]
cupo_dia_usado = df_cuenta_hoy['USD_Comprados'].sum() if not df_cuenta_hoy.empty else 0.0
cupo_mes_usado = df_cuenta_mes['USD_Comprados'].sum() if not df_cuenta_mes.empty else 0.0
cupo_diario_restante = max(0, 2000 - cupo_dia_usado)
cupo_mensual_restante = max(0, 10000 - cupo_mes_usado)
vueltas_hoy = len(df_cuenta_hoy)
ganancia_acumulada = df_cuenta_hoy['Ganancia_Bs'].sum() if not df_cuenta_hoy.empty else 0.0
ganancia_total_hoy = df_h[df_h['Día'] == hoy_str]['Ganancia_Bs'].sum() if not df_h.empty else 0.0

dashboard_html = f"""
<div class='dashboard-panel'>
    <p style='text-align: center; margin: 0; font-size: 13px; color:#94a3b8; font-weight:800;'>🎛️ PANEL DE CONTROL</p>
    <p style='text-align:center; color:#e2e8f0; font-size:12px; margin-top:4px; margin-bottom:4px;'>Vueltas Hoy: <b style='color:#10b981;'>{vueltas_hoy}</b> | Día: <span style='color:#38bdf8;'>$ {cupo_diario_restante:,.0f}</span> | Mes: <span style='color:#38bdf8;'>$ {cupo_mensual_restante:,.0f}</span></p>
    <p style='text-align:center; font-size:13px; margin-top:0px; margin-bottom:0;'>Ganancia Cuenta: <span style='color:#16a34a;'>Bs. {ganancia_acumulada:,.2f}</span> | 🌍 GLOBAL: <span style='color:#facc15; font-weight:900;'>Bs. {ganancia_total_hoy:,.2f}</span></p>
</div>
"""
st.markdown(dashboard_html, unsafe_allow_html=True)
st.session_state.cuenta_activa = st.selectbox("💳 Cuenta Activa:", cuentas_lista, index=cuentas_lista.index(cuenta_activa), label_visibility="collapsed")

# ---------------------------------------------------------
# TASAS BASE
# ---------------------------------------------------------
col_t1, col_t2 = st.columns(2)
with col_t1:
    tasa_c = st.number_input("📉 Tasa Compra BDV", value=570.75, format="%.2f", step=0.01)
with col_t2:
    tasa_v = st.number_input("📈 Tasa Venta P2P", value=648.00, format="%.2f", step=0.01)

c_asig = 0.005 
c_tarjeta = 0.025 # 2.5%
c_binance = 0.033 # 3.3%
tasa_real_b = tasa_c * (1 + c_asig)

# 🪟 ESPACIO RESERVADO PARA EL RADAR
radar_placeholder = st.empty()
st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------------------------------------------
# FLUJO DIRECCIONAL DE LA VUELTA
# ---------------------------------------------------------
tipo_vuelta = st.radio("🔄 Dirección de la Vuelta:", ["➡️ Normal (Comprar BDV primero)", "⬅️ Inversa (Vender USDT primero)"], horizontal=True)

if tipo_vuelta == "➡️ Normal (Comprar BDV primero)":
    st.markdown("<h3 style='margin:0;'>1️⃣ Fondeo BDV</h3>", unsafe_allow_html=True)
    tipo_ingreso = st.radio("Ingresar monto en:", ["Bolívares (Bs)", "Dólares (USD)"], horizontal=True, label_visibility="collapsed")
    
    if tipo_ingreso == "Bolívares (Bs)":
        cap_bs = st.number_input("Monto Invertido (Bs.)", value=57360.00, format="%.2f", step=100.0)
        usd_en_banco = cap_bs / tasa_real_b if tasa_real_b > 0 else 0
        st.info(f"💵 Compraste aprox: **$ {usd_en_banco:,.2f}**")
    else:
        usd_en_banco = st.number_input("Monto a Comprar (USD)", value=100.00, format="%.2f", step=10.0)
        cap_bs = usd_en_banco * tasa_real_b
        st.info(f"🇻🇪 Necesitas fondear: **Bs. {cap_bs:,.2f}**")

    st.markdown("<h3 style='margin:0;'>2️⃣ Recarga Tarjeta</h3>", unsafe_allow_html=True)
    dejar_dolar = st.checkbox("Dejar $1 de holgura por seguridad", value=True)
    usd_base = max(0.0, (usd_en_banco - 1.0) if dejar_dolar else usd_en_banco)
    sugerido_tarjeta = usd_base * (1 - c_tarjeta)
    st.markdown(f"<div class='highlight-action'>⚠️ MONTO EXACTO A TECLEAR:<br><span style='font-size: 22px;'>$ {sugerido_tarjeta:,.2f}</span></div>", unsafe_allow_html=True)
    confirmado_tarjeta = st.number_input("👉 Confirma el monto escrito en la app:", value=float(f"{sugerido_tarjeta:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;'>3️⃣ Recibido Binance</h3>", unsafe_allow_html=True)
    sugerido_binance = confirmado_tarjeta * (1 - c_binance)
    confirmado_usdt_recibido = st.number_input(f"👉 Confirma USDT acreditados (Aprox ₮ {sugerido_binance:,.2f}):", value=float(f"{sugerido_binance:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;'>4️⃣ Venta P2P</h3>", unsafe_allow_html=True)
    usdt_a_vender = st.number_input("USDT a Vender:", value=float(confirmado_usdt_recibido), step=1.0)
    sugerido_bs_recibir = usdt_a_vender * tasa_v
    confirmado_bs_recibidos = st.number_input(f"👉 Confirma Bs. Recibidos (Aprox Bs. {sugerido_bs_recibir:,.2f}):", value=float(f"{sugerido_bs_recibir:.2f}"), step=100.0)

    gan_bs = confirmado_bs_recibidos - cap_bs
    roi = (gan_bs / cap_bs) * 100 if cap_bs > 0 else 0
    brecha = ((tasa_v / tasa_real_b) - 1) * 100 if tasa_real_b > 0 else 0
    gan_usdt = gan_bs / tasa_v if tasa_v != 0 else 0
    
    hist_cap_invertido = cap_bs
    hist_usd_comprados = usd_en_banco
    hist_usdt_vendidos = usdt_a_vender
    hist_bs_recibidos = confirmado_bs_recibidos

else:
    st.markdown("<h3 style='margin:0;'>1️⃣ Venta Inicial P2P</h3>", unsafe_allow_html=True)
    usdt_iniciales = st.number_input("USDT Iniciales a Vender:", value=100.00, format="%.2f", step=1.0)
    sugerido_bs_inverso = usdt_iniciales * tasa_v
    confirmado_bs_inverso = st.number_input(f"👉 Confirma Bs. Recibidos en BDV (Aprox Bs. {sugerido_bs_inverso:,.2f}):", value=float(f"{sugerido_bs_inverso:.2f}"), step=100.0)

    st.markdown("<h3 style='margin:0;'>2️⃣ Fondeo BDV (Re-inversión)</h3>", unsafe_allow_html=True)
    bs_a_invertir = st.number_input("Bs. a usar para comprar USD:", value=float(confirmado_bs_inverso), step=100.0)
    usd_en_banco_inv = bs_a_invertir / tasa_real_b if tasa_real_b > 0 else 0
    st.info(f"💵 Compraste aprox: **$ {usd_en_banco_inv:,.2f}**")

    st.markdown("<h3 style='margin:0;'>3️⃣ Recarga Tarjeta</h3>", unsafe_allow_html=True)
    dejar_dolar = st.checkbox("Dejar $1 de holgura por seguridad", value=True)
    usd_base_inv = max(0.0, (usd_en_banco_inv - 1.0) if dejar_dolar else usd_en_banco_inv)
    sugerido_tarjeta_inv = usd_base_inv * (1 - c_tarjeta)
    st.markdown(f"<div class='highlight-action'>⚠️ MONTO EXACTO A TECLEAR:<br><span style='font-size: 22px;'>$ {sugerido_tarjeta_inv:,.2f}</span></div>", unsafe_allow_html=True)
    confirmado_tarjeta_inv = st.number_input("👉 Confirma el monto escrito en la app:", value=float(f"{sugerido_tarjeta_inv:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;'>4️⃣ USDT Recuperados</h3>", unsafe_allow_html=True)
    sugerido_binance_inv = confirmado_tarjeta_inv * (1 - c_binance)
    usdt_finales = st.number_input(f"👉 Confirma USDT recuperados (Aprox ₮ {sugerido_binance_inv:,.2f}):", value=float(f"{sugerido_binance_inv:.2f}"), step=1.0)

    gan_usdt = usdt_finales - usdt_iniciales
    gan_bs = gan_usdt * tasa_v
    roi = (gan_usdt / usdt_iniciales) * 100 if usdt_iniciales > 0 else 0
    brecha = ((tasa_v / tasa_real_b) - 1) * 100 if tasa_real_b > 0 else 0
    
    hist_cap_invertido = bs_a_invertir
    hist_usd_comprados = usd_en_banco_inv
    hist_usdt_vendidos = usdt_iniciales
    hist_bs_recibidos = confirmado_bs_inverso
    usd_en_banco = usd_en_banco_inv 

# ---------------------------------------------------------
# INYECCIÓN DEL RADAR EN VIVO
# ---------------------------------------------------------
cap_bs_teorico = hist_cap_invertido
usd_base_teorico = max(0.0, (usd_en_banco - 1.0) if dejar_dolar else usd_en_banco)
usdt_finales_teorico = usd_base_teorico * (1 - c_tarjeta) * (1 - c_binance)

tasa_sugerida_2pct = (cap_bs_teorico * 1.02) / usdt_finales_teorico if usdt_finales_teorico > 0 else 0
bs_recibidos_teorico = usdt_finales_teorico * tasa_v
gan_bs_teorico = bs_recibidos_teorico - cap_bs_teorico
gan_usdt_teorico = gan_bs_teorico / tasa_v if tasa_v > 0 else 0
roi_teorico = (gan_bs_teorico / cap_bs_teorico) * 100 if cap_bs_teorico > 0 else 0
color_roi = '#ef4444' if roi_teorico < 2 else '#10b981'

proyeccion_html = f"""
<div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(15, 23, 42, 0.6)); border: 1px solid rgba(16, 185, 129, 0.3); padding: 12px; border-radius: 12px; margin-top: 5px; margin-bottom: 15px;">
    <p style="margin: 0; font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 800;">🔍 Radar Proyección P2P (Basado en $ {usd_en_banco:,.2f})</p>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 5px;">
        <div>
            <p style="margin: 0; font-size: 13px; color: #e2e8f0;">🎯 Sugerida (ROI 2%): <b style="color: #facc15;">Bs. {tasa_sugerida_2pct:,.2f}</b></p>
            <p style="margin: 0; font-size: 13px; color: #e2e8f0; margin-top: 3px;">📊 ROI Proyectado: <b style="color: {color_roi};">{roi_teorico:,.2f}%</b></p>
        </div>
        <div style="text-align: right;">
            <p style="margin: 0; font-size: 10px; color: #94a3b8;">GANANCIA PROYECTADA</p>
            <p style="margin: 0; font-size: 16px; font-weight: 900; color: #38bdf8;">Bs. {gan_bs_teorico:,.2f}</p>
            <p style="margin: 0; font-size: 13px; font-weight: 800; color: #10b981;">≈ ₮ {gan_usdt_teorico:,.2f}</p>
        </div>
    </div>
</div>
"""
radar_placeholder.markdown(proyeccion_html, unsafe_allow_html=True)


# ---------------------------------------------------------
# MÉTRICAS EN VIVO
# ---------------------------------------------------------
st.markdown("<hr style='margin-bottom:8px;'>", unsafe_allow_html=True)
res1, res2, res3 = st.columns(3)

with res1:
    st.markdown(f"""
    <div data-testid="stMetric" style="background-color: #1e293b !important; padding: 6px; border-radius: 10px; border: 1px solid #334155 !important;">
        <p style="font-weight: 800 !important; color: #94a3b8 !important; font-size: 11px !important; text-transform: uppercase; margin: 0;">GANANCIA NETA</p>
        <div style="display: flex; align-items: baseline; flex-wrap: wrap; gap: 6px; margin-top: 2px;">
            <span style="font-weight: 900 !important; color: #38bdf8 !important; font-size: 18px !important; line-height: 1;">Bs. {gan_bs:,.2f}</span>
            <span style="color: #10b981 !important; font-weight: 800 !important; font-size: 13px !important; line-height: 1;">₮ {gan_usdt:,.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

res2.metric("ROI REAL", f"{roi:.2f}%")
res3.metric("BRECHA", f"{brecha:.2f}%")

if usd_en_banco > 0 and roi > 0:
    capital_simulado = usd_en_banco
    cupo_disponible_sim = cupo_diario_restante
    vueltas_posibles = 0
    while capital_simulado <= cupo_disponible_sim:
        vueltas_posibles += 1
        cupo_disponible_sim -= capital_simulado
        capital_simulado = capital_simulado * (1 + (roi/100))
    excedente = capital_simulado - cupo_disponible_sim
    html_radar = f"<div class='radar-box'><p style='margin:0; font-size:12px; color:#38bdf8;'>🔄 Radar de Interés: <b>{vueltas_posibles} vueltas más.</b> Límite día en: $ {cupo_disponible_sim:,.0f} (Excedente $ {excedente:,.0f}).</p></div>"
    st.markdown(html_radar, unsafe_allow_html=True)

# ---------------------------------------------------------
# NUEVO: RESUMEN GLOBAL DIARIO (Reemplaza Ticket)
# ---------------------------------------------------------
df_hoy_global = df_h[df_h['Día'] == hoy_str]

# Calculos del resumen de hoy (Registrados)
if not df_hoy_global.empty:
    vueltas_totales_hoy = len(df_hoy_global)
    cuentas_usadas = df_hoy_global['Cuenta'].nunique()
    nombres_cuentas = ", ".join(df_hoy_global['Cuenta'].str.replace('Cuenta ', '#').unique())
    promedio_tasa_v = df_hoy_global['Tasa_Venta'].mean()
    promedio_roi = df_hoy_global['ROI'].mean()
    ganancia_total_bs = df_hoy_global['Ganancia_Bs'].sum()
    
    # Calcular USDT aproximado dividiendo la ganancia de cada vuelta por su tasa de venta
    df_hoy_global['Ganancia_USDT'] = df_hoy_global['Ganancia_Bs'] / df_hoy_global['Tasa_Venta']
    ganancia_total_usdt = df_hoy_global['Ganancia_USDT'].sum()
    volumen_usd = df_hoy_global['USD_Comprados'].sum()
else:
    vueltas_totales_hoy, cuentas_usadas, nombres_cuentas = 0, 0, "Ninguna"
    promedio_tasa_v, promedio_roi, ganancia_total_bs, ganancia_total_usdt, volumen_usd = 0.0, 0.0, 0.0, 0.0, 0.0

summary_html = f"""
<div class="summary-box">
    <div class="summary-header">🏆 RESUMEN GLOBAL DEL DÍA</div>
    <div class="summary-grid">
        <div class="summary-item">
            <span class="sum-label">🔄 Vueltas / Cuentas</span>
            <span class="sum-val">{vueltas_totales_hoy} <span style="font-size:11px; color:#94a3b8;">({nombres_cuentas})</span></span>
        </div>
        <div class="summary-item">
            <span class="sum-label">💸 Volumen Movido</span>
            <span class="sum-val highlight">$ {volumen_usd:,.2f}</span>
        </div>
        <div class="summary-item">
            <span class="sum-label">📈 Tasa Promedio</span>
            <span class="sum-val">Bs. {promedio_tasa_v:,.2f}</span>
        </div>
        <div class="summary-item">
            <span class="sum-label">🚀 ROI Promedio</span>
            <span class="sum-val" style="color: {'#10b981' if promedio_roi >= 2 else '#ef4444'};">{promedio_roi:,.2f}%</span>
        </div>
        <div class="summary-item-full">
            <span class="sum-label" style="color: #38bdf8; font-size:12px;">💰 GANANCIA TOTAL HOY</span>
            <div style="display:flex; justify-content:center; align-items:baseline; gap:10px; margin-top:5px;">
                <span class="sum-val success">Bs. {ganancia_total_bs:,.2f}</span>
                <span style="color:#e2e8f0; font-weight:900; font-size:16px;">≈ ₮ {ganancia_total_usdt:,.2f}</span>
            </div>
        </div>
    </div>
</div>
"""
st.markdown(summary_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# GUARDADO Y VISUALIZACIÓN DE HISTORIAL
# ---------------------------------------------------------
if st.button("💾 GUARDAR VUELTA EXACTA", use_container_width=True):
    if usd_en_banco > cupo_diario_restante or usd_en_banco > cupo_mensual_restante:
        st.error(f"❌ No puedes guardar. Supera los límites operativos de la {cuenta_activa}.")
    else:
        nuevo_registro = {
            "Fecha": datetime.now().
