import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import math

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="TEAM ARBITRAJE PRO", layout="wide", initial_sidebar_state="expanded")

# --- CONEXIÓN A GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        return conn.read(ttl="1s") 
    except:
        return pd.DataFrame(columns=["Fecha", "Día", "Mes", "Titular", "Cuenta_Zinli", "Banco", "Ruta", "USD_Comprados", "Ganancia_Bs", "Usdt_Retenidos", "ROI_%"])

df_h = load_data()

# --- ESTILO VISUAL MÓVIL AVANZADO (OPTIMIZADO) ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a !important; color: #f8fafc !important; }
    .block-container { padding-top: 3.5rem !important; padding-bottom: 1rem !important; max-width: 98% !important; }
    h1, h2, h3, p, label, .stMarkdown { color: #f8fafc !important; font-weight: 700 !important; margin-bottom: 2px !important;}
    h3 { font-size: 1.2rem !important; margin-top: 1rem !important; color: #38bdf8 !important; border-bottom: 1px solid #334155; padding-bottom: 5px; }
    div[data-testid="stMetric"], div.stNumberInput, div.stRadio, div.stSelectbox {
        background-color: #1e293b !important; padding: 5px 10px !important; border-radius: 8px !important; border: 1px solid #334155 !important;
    }
    div[data-testid="stNumberInputContainer"] { max-width: 100% !important; margin: 0 auto; }
    .stNumberInput div div input { color: #f8fafc !important; background-color: #0f172a !important; border: 1px solid #475569 !important; font-weight: 900 !important; text-align: center !important; font-size: 1.1rem !important;}
    div[data-testid="stMetricValue"] { font-weight: 900 !important; color: #38bdf8 !important; font-size: 1.2rem !important;}
    section[data-testid="stSidebar"] { background-color: #1e293b !important; border-right: 1px solid #334155;}
    .sugerencia-box { background-color: #064e3b; padding: 8px; border-radius: 8px; border: 1px solid #10b981; color: #a7f3d0; text-align: center; margin-bottom: 5px; font-size: 14px;}
    .usdt-box { background-color: #1e3a8a; padding: 10px; border-radius: 8px; border: 1px solid #3b82f6; color: #bfdbfe; text-align: center; margin-top: 5px; margin-bottom: 15px; font-weight: 900; font-size: 18px;}
    
    @media (max-width: 768px) {
        .top-controls [data-testid="column"] { width: 50% !important; flex: 1 1 50% !important; min-width: 50% !important; }
    }

    .panel-dinamico { display: flex; justify-content: space-around; background: #020617; padding: 10px; border-radius: 10px; border: 1px solid #475569; margin: 15px 0 5px 0;}
    .panel-item { text-align: center; }
    .panel-titulo { font-size: 12px; color: #94a3b8; }
    .panel-valor { font-size: 20px; font-weight: 900; color: #10b981; }

    .ticket-wrapper { display: flex; justify-content: center; padding: 5px; margin-top: 5px; margin-bottom: 10px;}
    .whatsapp-ticket { background-color: #ffffff !important; border: 3px dashed #16a34a; border-radius: 15px; padding: 15px; width: 100%; max-width: 380px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
    .whatsapp-ticket * { color: #000000 !important; } 
    .ticket-header { text-align: center; font-size: 18px; font-weight: 900; color: #16a34a !important; border-bottom: 2px solid #16a34a; padding-bottom: 5px; margin-bottom: 10px; }
    .ticket-row { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #e2e8f0; }
    .ticket-label { font-size: 13px; font-weight: 700; color: #334155 !important; }
    .ticket-value { font-size: 14px; font-weight: 900; }
    .ticket-retenido-box { background-color: #f0fdf4 !important; padding: 8px; border-radius: 8px; border: 2px solid #16a34a; margin-bottom: 10px; text-align: center; }
    .ticket-retenido-label { font-size: 12px; font-weight: 700; color: #16a34a !important; }
    .ticket-retenido-valor { font-size: 22px; font-weight: 900; color: #16a34a !important; }
    .ticket-footer { text-align: center; font-size: 10px; color: #64748b !important; margin-top: 10px; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

st.image("1774925854444.png", use_container_width=True)

# Lógica de Estado (Conservando V16.5)
if 'tasa_c' not in st.session_state: st.session_state.tasa_c = 570.0
if 'cap_bs' not in st.session_state: st.session_state.cap_bs = 400000.0
if 'usd_banco' not in st.session_state: st.session_state.usd_banco = 0.0
if 'c_asig_val' not in st.session_state: st.session_state.c_asig_val = 0.005 

def update_usd():
    tr = st.session_state.tasa_c * (1 + st.session_state.c_asig_val)
    if tr > 0: st.session_state.usd_banco = st.session_state.cap_bs / tr

def update_bs():
    tr = st.session_state.tasa_c * (1 + st.session_state.c_asig_val)
    st.session_state.cap_bs = st.session_state.usd_banco * tr

def update_tasa(): update_usd()

hoy_str = datetime.now().strftime("%Y-%m-%d")
mes_str = datetime.now().strftime("%Y-%m")

# --- SIDEBAR: GESTIÓN DE CUENTAS Y LÍMITES ---
if not df_h.empty:
    df_hoy = df_h[df_h['Día'] == hoy_str]
    gan_bs_h = df_hoy['Ganancia_Bs'].sum()
    gan_usd_h = df_hoy['Usdt_Retenidos'].sum()
    gan_usd_t = df_h['Usdt_Retenidos'].sum()
else:
    gan_bs_h, gan_usd_h, gan_usd_t = 0, 0, 0

st.sidebar.header("👥 SELECCIÓN")
titular_actual = st.sidebar.selectbox("Titular:", ["Alejandro", "Rosa", "Rubén", "Luz", "Yngianni"])
zinli_actual = st.sidebar.selectbox("Cuenta Zinli:", [f"Zinli {i:02d}" for i in range(1, 16)])

st.sidebar.divider()
st.sidebar.header("🛡️ LÍMITES")
uso_d = df_h[(df_h['Día'] == hoy_str) & (df_h['Titular'] == titular_actual)]['USD_Comprados'].sum() if not df_h.empty else 0
uso_m = df_h[(df_h['Mes'] == mes_str) & (df_h['Titular'] == titular_actual)]['USD_Comprados'].sum() if not df_h.empty else 0
st.sidebar.metric(f"DÍA - {titular_actual}", f"$ {2000 - uso_d:,.2f}")
st.sidebar.metric(f"MES - {titular_actual}", f"$ {10000 - uso_m:,.2f}")

st.sidebar.divider()
c_asig_bdv = st.sidebar.number_input("% Asig. BDV", value=0.50) / 100
c_asig_bancamiga = st.sidebar.number_input("% Asig. Bancamiga", value=0.80) / 100
c_tarjeta = st.sidebar.number_input("% Uso Tarjeta", value=2.50) / 100
c_zinli_com = st.sidebar.number_input("% Comisión Zinli", value=3.75) / 100
c_envio_z = st.sidebar.number_input("% Envío Zinli", value=1.00) / 100
fijo_z = st.sidebar.number_input("Fijo Zinli ($)", value=0.40)
c_bin_dep = st.sidebar.number_input("% Comis. Binance", value=3.30) / 100

# --- CONTROLES LADO A LADO ---
st.markdown('<div class="top-controls">', unsafe_allow_html=True)
col_h1, col_h2 = st.columns(2)
with col_h1: banco = st.radio("🏦 Entidad:", ["BDV", "BANCAMIGA"], horizontal=True)
with col_h2: metodo = st.radio("📍 Mecanismo:", ["ZINLI", "TARJETA DIRECTA"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

st.session_state.c_asig_val = c_asig_bancamiga if banco == "BANCAMIGA" else c_asig_bdv

# --- PASO 1: COMPRA ---
st.markdown("### 1️⃣ COMPRA EN BANCO")
tc = st.number_input("Tasa Compra", key="tasa_c", on_change=update_tasa)
c_bs = st.number_input("Capital (Bs.)", key="cap_bs", on_change=update_usd)
u_b = st.number_input(f"USD en {banco}", key="usd_banco", on_change=update_bs)
tr_b = tc * (1 + st.session_state.c_asig_val)

# --- PASO 2: MOVIMIENTO Y CONVERSIÓN ---
st.markdown("### 2️⃣ MOVIMIENTO Y CONVERSIÓN")
if metodo == "ZINLI":
    m_sug = (u_b - 1.0) / (1 + c_zinli_com + c_tarjeta)
    st.markdown(f'<div class="sugerencia-box">💡 Sugerencia Recarga {zinli_actual}: <b>$ {m_sug:,.2f}</b></div>', unsafe_allow_html=True)
    u_neto_z = st.number_input("NETO Zinli (Exacto)", value=float(m_sug))
    t_u = st.number_input("Tasa P2P (USD/USDT)", value=1.033, format="%.3f")
    u_recibidos = float(((u_neto_z - fijo_z) / (1 + c_envio_z)) / t_u) if t_u > 0 else 0.0
    u_alt = float((u_b - 1.0) / (1 + c_tarjeta)) * (1 - c_bin_dep) # Para ROI comparativo
else:
    m_sug = (u_b - 1.0) / (1 + c_tarjeta)
    st.markdown(f'<div class="sugerencia-box">💡 Sugerencia Tarjeta: <b>$ {m_sug:,.2f}</b></div>', unsafe_allow_html=True)
    u_dir = st.number_input("USD Gastados de Tarjeta", value=float(m_sug))
    u_recibidos = float(u_dir * (1 - c_bin_dep))
    m_s_z = (u_b - 1.0) / (1 + c_zinli_com + c_tarjeta)
    u_alt = float(((m_s_z - fijo_z) / (1 + c_envio_z)) / 1.033) # Para ROI comparativo

st.markdown(f'<div class="usdt-box">📥 RECIBIRÁS: {u_recibidos:.2f} USDT</div>', unsafe_allow_html=True)

# --- PASO 3: VENTA PARA RECUPERAR ---
st.markdown("### 3️⃣ VENTA PARA RECUPERAR")
tv = st.number_input("Tasa Venta (Bs/USDT)", value=660.0)
u_min_rec = c_bs / tv if tv > 0 else 0.0
st.markdown(f'<div class="sugerencia-box">⚠️ Debes vender mínimo <b>{u_min_rec:.2f} USDT</b> para reponer los Bs. {c_bs:,.2f}</div>', unsafe_allow_html=True)
u_vender = st.number_input("¿Cuántos USDT vas a vender realmente?", value=float(u_min_rec))

# --- CÁLCULOS TICKET (CON ESCUDO ANTI-NaN) ---
def safe_calc(v): return v if math.isfinite(v) else 0.0

g_usdt = safe_calc(u_recibidos - u_vender)
brecha = safe_calc(((tv / tr_b) - 1) * 100 if tr_b > 0 else 0.0)
roi = safe_calc(((g_usdt * tv) / c_bs) * 100 if c_bs > 0 else 0.0)
roi_alt = safe_calc((((u_alt - u_vender) * tv) / c_bs) * 100 if c_bs > 0 else 0.0)
ruta_alt_txt = "Tarjeta Directa" if metodo == "ZINLI" else "Zinli"

# --- PANELES DINÁMICOS ---
st.markdown(f"""
<div class="panel-dinamico">
    <div class="panel-item"><div class="panel-titulo">↔️ BRECHA REAL</div><div class="panel-valor">{brecha:,.2f}%</div></div>
    <div class="panel-item"><div class="panel-titulo">🚀 ROI NETO</div><div class="panel-valor">{roi:,.2f}%</div></div>
</div>
""", unsafe_allow_html=True)

col_s1, col_s2, col_s3 = st.columns(3)
col_s1.metric("Ganancia Hoy (Bs)", f"Bs.{gan_bs_h:,.0f}")
col_s2.metric("Retenido Hoy (USDT)", f"{gan_usd_h:,.2f}")
col_s3.metric("🔥 ACUMULADO", f"{gan_usd_t:,.2f}")

# --- TICKET FINAL (RESTAURADO SEGÚN IMAGEN 3) ---
ticket_html = f"""
<div class="ticket-wrapper">
    <div class="whatsapp-ticket">
        <div class="ticket-header">👥 {titular_actual.upper()}</div>
        <div class="ticket-retenido-box">
            <div class="ticket-retenido-label">🛡️ RETENIDO</div>
            <div class="ticket-retenido-valor">{g_usdt:,.2f} USDT</div>
        </div>
        <div class="ticket-row"><span>🚀 ROI NETO:</span><b>{roi:,.2f}%</b></div>
        <div class="ticket-row"><span>🏦 Banco:</span><b>{banco}</b></div>
        <div class="ticket-row"><span>📉 Compra Real:</span><b>Bs.{tr_b:,.2f}</b></div>
        <div class="ticket-row"><span>📈 Tasa Venta:</span><b>Bs.{tv:,.2f}</b></div>
        <div class="ticket-row"><span>📍 Ruta:</span><b>{metodo}</b></div>
        <div class="ticket-row" style="border:none;"><span>↔️ Brecha:</span><b>{brecha:,.2f}%</b></div>
        <div class="ticket-footer">ROI comparativo con {ruta_alt_txt}: {roi_alt:,.2f}%</div>
    </div>
</div>
"""
st.write(ticket_html, unsafe_allow_html=True)

# --- BOTONES Y REGISTRO ---
if st.button("💾 REGISTRAR EN LA NUBE", type="primary", use_container_width=True):
    nuevo = pd.DataFrame([{"Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "Día": hoy_str, "Mes": mes_str, "Titular": titular_actual, "Cuenta_Zinli": zinli_actual if metodo == 'ZINLI' else "N/A", "Banco": banco, "Ruta": metodo, "USD_Comprados": u_b, "Ganancia_Bs": g_usdt * tv, "Usdt_Retenidos": round(g_usdt, 2), "ROI_%": round(roi, 2)}])
    updated_df = pd.concat([df_h, nuevo], ignore_index=True)
    conn.update(data=updated_df)
    st.success("¡Operación Registrada con Éxito!")
    st.rerun()

st.divider()
with st.expander("📚 VER / EDITAR HISTORIAL"):
    df_ed = st.data_editor(df_h.sort_index(ascending=False), num_rows="dynamic", use_container_width=True)
    if st.button("🛠️ Sincronizar Cambios"):
        conn.update(data=df_ed)
        st.success("¡Base de datos actualizada!")
        st.rerun()
                              
