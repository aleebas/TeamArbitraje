import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import math

# --- 1. CONFIGURACIÓN E INFRAESTRUCTURA ---
st.set_page_config(page_title="TEAM ARBITRAJE ELITE", layout="wide", initial_sidebar_state="expanded")

# PERSISTENCIA DE DATOS (Escudo anti-borrado de caché móvil)
keys = ['tasa_c', 'cap_bs', 'usd_banco', 'tasa_u', 'tasa_v', 'u_vender', 'banco_sel', 'metodo_sel']
for key in keys:
    if key not in st.session_state:
        if key == 'tasa_c': st.session_state[key] = 580.0
        elif key == 'cap_bs': st.session_state[key] = 100000.0
        elif key == 'tasa_u': st.session_state[key] = 1.033
        elif key == 'tasa_v': st.session_state[key] = 680.0
        elif key == 'banco_sel': st.session_state[key] = "BDV"
        elif key == 'metodo_sel': st.session_state[key] = "ZINLI"
        else: st.session_state[key] = 0.0

conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try: return conn.read(ttl="1s")
    except: return pd.DataFrame(columns=["Fecha", "Día", "Mes", "Titular", "Cuenta_Zinli", "Banco", "Ruta", "USD_Comprados", "Ganancia_Bs", "Usdt_Retenidos", "ROI_%"])

df_h = load_data()

# --- 2. LÓGICA BIDIRECCIONAL (Sincronización Total) ---
def sync_to_usd():
    comm = 0.008 if st.session_state.banco_sel == "BANCAMIGA" else 0.005
    tr = st.session_state.tasa_c * (1 + comm)
    if tr > 0: st.session_state.usd_banco = st.session_state.cap_bs / tr

def sync_to_bs():
    comm = 0.008 if st.session_state.banco_sel == "BANCAMIGA" else 0.005
    tr = st.session_state.tasa_c * (1 + comm)
    st.session_state.cap_bs = st.session_state.usd_banco * tr

# --- 3. ESTILO VISUAL (Móvil y PC) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f1a !important; color: #e2e8f0 !important; }
    .block-container { padding-top: 2rem !important; max-width: 1100px !important; margin: 0 auto !important; }
    
    h3 { font-size: 1.3rem !important; color: #38bdf8 !important; border-left: 5px solid #38bdf8; padding-left: 10px; margin-top: 20px !important; }
    
    div[data-testid="stMetric"], div.stNumberInput, div.stRadio, div.stSelectbox {
        background-color: #161e2e !important; border-radius: 12px !important; border: 1px solid #1f2937 !important; padding: 10px !important;
    }
    
    .stNumberInput div div input { font-size: 1.2rem !important; font-weight: 900 !important; color: #ffffff !important; text-align: center !important; }
    
    .sugerencia-box { background-color: #064e3b; padding: 10px; border-radius: 10px; border: 1px solid #10b981; color: #d1fae5; text-align: center; margin: 10px 0; font-size: 15px; }
    .usdt-box { background-color: #1e3a8a; padding: 15px; border-radius: 12px; border: 1px solid #3b82f6; color: #dbeafe; text-align: center; margin: 15px 0; font-weight: 900; font-size: 20px; }
    
    .panel-dinamico { display: flex; justify-content: space-around; background: #111827; padding: 15px; border-radius: 15px; border: 1px solid #374151; margin: 20px 0; }
    .panel-item { text-align: center; }
    .panel-titulo { font-size: 12px; color: #94a3b8; text-transform: uppercase; }
    .panel-valor { font-size: 22px; font-weight: 900; color: #10b981; }

    /* TICKET ESTILO WHATSAPP */
    .whatsapp-ticket { background-color: #ffffff !important; border-radius: 20px; padding: 20px; width: 100%; max-width: 400px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border: 2px solid #e2e8f0; }
    .whatsapp-ticket * { color: #1e293b !important; }
    .ticket-header { text-align: center; font-weight: 900; font-size: 18px; color: #059669 !important; border-bottom: 2px solid #10b981; padding-bottom: 8px; margin-bottom: 15px; }
    .ticket-row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f1f5f9; }
    .ticket-label { font-weight: 700; font-size: 14px; }
    .ticket-value { font-weight: 800; font-size: 14px; }
    .ticket-profit-box { background-color: #ecfdf5 !important; border: 2px solid #10b981; border-radius: 12px; padding: 12px; text-align: center; margin-bottom: 15px; }
    .profit-label { font-size: 12px; font-weight: 700; color: #065f46 !important; }
    .profit-val { font-size: 20px; font-weight: 900; color: #059669 !important; }
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.image("1774925854444.png", use_container_width=True)

# --- 4. SIDEBAR (Límites y Comisiones) ---
st.sidebar.header("👥 TITULAR Y CUENTA")
titular = st.sidebar.selectbox("Operador:", ["Alejandro", "Rosa", "Rubén", "Luz", "Yngianni"])
zinli_id = st.sidebar.selectbox("Zinli:", [f"Zinli {i:02d}" for i in range(1, 16)])

st.sidebar.divider()
st.sidebar.header("🛡️ LÍMITES EN VIVO")
hoy = datetime.now().strftime("%Y-%m-%d")
mes = datetime.now().strftime("%Y-%m")

uso_d = df_h[(df_h['Día'] == hoy) & (df_h['Titular'] == titular)]['USD_Comprados'].sum() if not df_h.empty else 0
uso_m = df_h[(df_h['Mes'] == mes) & (df_h['Titular'] == titular)]['USD_Comprados'].sum() if not df_h.empty else 0
st.sidebar.metric(f"Día - {titular}", f"$ {2000 - uso_d:,.2f}")
st.sidebar.metric(f"Mes - {titular}", f"$ {10000 - uso_m:,.2f}")

st.sidebar.divider()
c_bdv = st.sidebar.number_input("% Asig. BDV", value=0.50) / 100
c_bam = st.sidebar.number_input("% Asig. Bancamiga", value=0.80) / 100
c_tarj = st.sidebar.number_input("% Uso Tarjeta", value=2.50) / 100
c_zin_c = st.sidebar.number_input("% Com. Zinli", value=3.75) / 100
c_env_z = st.sidebar.number_input("% Envío Zinli", value=1.00) / 100
f_zin = st.sidebar.number_input("Fijo Zinli ($)", value=0.40)
c_bin = st.sidebar.number_input("% Com. Binance", value=3.30) / 100

# --- 5. CUERPO DE OPERACIÓN ---
col_h1, col_h2 = st.columns(2)
with col_h1: st.session_state.banco_sel = st.radio("🏦 Banco:", ["BDV", "BANCAMIGA"], horizontal=True)
with col_h2: st.session_state.metodo_sel = st.radio("📍 Ruta:", ["ZINLI", "TARJETA DIRECTA"], horizontal=True)

st.divider()

# PASO 1: COMPRA (BIDIRECCIONAL)
st.markdown("### 1️⃣ PASO: COMPRA EN BANCO")
col_b1, col_b2 = st.columns(2)
with col_b1:
    st.number_input("Tasa de Compra (BCV)", key="tasa_c", on_change=sync_to_usd)
    st.number_input("Monto en Bolívares (Bs.)", key="cap_bs", on_change=sync_to_usd)
with col_b2:
    st.number_input(f"USD a comprar en {st.session_state.banco_sel}", key="usd_banco", on_change=sync_to_bs)
    com_actual = c_bam if st.session_state.banco_sel == "BANCAMIGA" else c_bdv
    tr_banco = st.session_state.tasa_c * (1 + com_actual)
    st.info(f"Tasa Real con Comisión: Bs. {tr_banco:,.2f}")

# PASO 2: MOVIMIENTO
st.markdown("### 2️⃣ PASO: MOVIMIENTO Y P2P")
if st.session_state.metodo_sel == "ZINLI":
    sug_rec = (st.session_state.usd_banco - 1.0) / (1 + c_zin_c + c_tarj)
    st.markdown(f'<div class="sugerencia-box">💡 RECARGA SUGERIDA EN {zinli_id}: <b>$ {sug_rec:,.2f}</b></div>', unsafe_allow_html=True)
    u_neto = st.number_input("Neto en Zinli (Confirmado)", value=float(sug_rec))
    t_p2p = st.number_input("Tasa P2P (USD/USDT)", key="tasa_u")
    u_recibidos = ((u_neto - f_zin) / (1 + c_env_z)) / t_p2p if t_p2p > 0 else 0
else:
    sug_tar = (st.session_state.usd_banco - 1.0) / (1 + c_tarj)
    st.markdown(f'<div class="sugerencia-box">💡 MONTO SUGERIDO TARJETA: <b>$ {sug_tar:,.2f}</b></div>', unsafe_allow_html=True)
    u_dir = st.number_input("USD Gastados con Tarjeta", value=float(sug_tar))
    u_recibidos = u_dir * (1 - c_bin)

st.markdown(f'<div class="usdt-box">📥 RECIBIRÁS EN BINANCE: {u_recibidos:,.2f} USDT</div>', unsafe_allow_html=True)

# PASO 3: VENTA
st.markdown("### 3️⃣ PASO: VENTA Y CIERRE")
t_venta = st.number_input("Tasa de Venta P2P (Bs.)", key="tasa_v")
u_para_rep = st.session_state.cap_bs / t_venta if t_venta > 0 else 0
st.markdown(f'<div class="sugerencia-box">⚠️ Vende mínimo <b>{u_para_rep:,.2f} USDT</b> para recuperar tu capital.</div>', unsafe_allow_html=True)
u_vendidos = st.number_input("USDT Vendidos para reponer Bs.", value=float(u_para_rep))

# --- 6. RESULTADOS Y TICKET ---
g_usdt = u_recibidos - u_vendidos
g_bs = g_usdt * t_venta
roi = (g_bs / st.session_state.cap_bs) * 100 if st.session_state.cap_bs > 0 else 0
brecha = ((t_venta / tr_banco) - 1) * 100 if tr_banco > 0 else 0

# PANEL DINÁMICO
st.markdown(f"""
<div class="panel-dinamico">
    <div class="panel-item"><div class="panel-titulo">↔️ BRECHA</div><div class="panel-valor">{brecha:,.2f}%</div></div>
    <div class="panel-item"><div class="panel-titulo">🚀 ROI NETO</div><div class="panel-valor">{roi:,.2f}%</div></div>
</div>
""", unsafe_allow_html=True)

# TICKET WHATSAPP
ticket = f"""
<div class="whatsapp-ticket">
    <div class="ticket-header">👥 {titular.upper()} - {zinli_id}</div>
    <div class="ticket-profit-box">
        <div class="profit-label">💰 GANANCIA POR VUELTA</div>
        <div class="profit-val">{g_usdt:,.2f} USDT / Bs. {g_bs:,.2f}</div>
    </div>
    <div class="ticket-row"><span class="ticket-label">🚀 ROI NETO:</span><span class="ticket-value">{roi:,.2f}%</span></div>
    <div class="ticket-row"><span class="ticket-label">🏦 Banco:</span><span class="ticket-value">{st.session_state.banco_sel}</span></div>
    <div class="ticket-row"><span class="ticket-label">📉 Compra Real:</span><span class="ticket-value">Bs. {tr_banco:,.2f}</span></div>
    <div class="ticket-row"><span class="ticket-label">📈 Tasa Venta:</span><span class="ticket-value">Bs. {t_venta:,.2f}</span></div>
    <div class="ticket-row"><span class="ticket-label">📍 Ruta:</span><span class="ticket-value">{st.session_state.metodo_sel}</span></div>
    <div class="ticket-row" style="border:none;"><span class="ticket-label">↔️ Brecha Real:</span><span class="ticket-value">{brecha:,.2f}%</span></div>
</div>
"""
st.write(ticket, unsafe_allow_html=True)

# REGISTRO
if st.button("💾 REGISTRAR EN LA NUBE", type="primary", use_container_width=True):
    nuevo = pd.DataFrame([{
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "Día": hoy, "Mes": mes,
        "Titular": titular, "Cuenta_Zinli": zinli_id if st.session_state.metodo_sel == 'ZINLI' else "N/A",
        "Banco": st.session_state.banco_sel, "Ruta": st.session_state.metodo_sel, "USD_Comprados": st.session_state.usd_banco, 
        "Ganancia_Bs": g_bs, "Usdt_Retenidos": round(g_usdt, 2), "ROI_%": round(roi, 2)
    }])
    updated = pd.concat([df_h, nuevo], ignore_index=True)
    conn.update(data=updated)
    st.success("¡Operación Registrada!")
    st.rerun()

# HISTORIAL
st.divider()
with st.expander("📚 VER HISTORIAL COMPLETO"):
    st.data_editor(df_h.sort_index(ascending=False), num_rows="dynamic", use_container_width=True)
