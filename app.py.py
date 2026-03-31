import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import math

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="TEAM ARBITRAJE Pro", layout="wide", initial_sidebar_state="expanded")

# --- CONEXIÓN A GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        return conn.read(ttl="1s") 
    except:
        return pd.DataFrame(columns=["Fecha", "Día", "Mes", "Titular", "Cuenta_Zinli", "Banco", "Ruta", "USD_Comprados", "Ganancia_Bs", "Usdt_Retenidos", "ROI_%"])

df_h = load_data()

# --- ESTILO VISUAL MÓVIL (Preservado V17.5) ---
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
    div[data-testid="stMetricLabel"] p { font-size: 12px !important; color: #94a3b8 !important; }
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
    .ticket-header { text-align: center; font-size: 16px; font-weight: 900; color: #16a34a !important; border-bottom: 2px solid #16a34a; padding-bottom: 5px; margin-bottom: 10px; }
    .ticket-row { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #e2e8f0; }
    .ticket-label { font-size: 13px; font-weight: 700; color: #334155 !important; }
    .ticket-value { font-size: 14px; font-weight: 900; }
    .ticket-retenido-box { background-color: #f0fdf4 !important; padding: 8px; border-radius: 8px; border: 2px solid #16a34a; margin-bottom: 10px; text-align: center; }
    .ticket-retenido-label { font-size: 12px; font-weight: 700; color: #16a34a !important; }
    .ticket-retenido-valor { font-size: 18px; font-weight: 900; color: #16a34a !important; }
    </style>
""", unsafe_allow_html=True)

st.image("1774925854444.png", use_container_width=True)

# Lógica de Estado (Inmutable V16.5)
if 'tasa_c' not in st.session_state: st.session_state.tasa_c = 570.0
if 'cap_bs' not in st.session_state: st.session_state.cap_bs = 400000.0
if 'usd_banco' not in st.session_state: st.session_state.usd_banco = 0.0
if 'c_asig_val' not in st.session_state: st.session_state.c_asig_val = 0.005 

def update_usd():
    tasa_real = st.session_state.tasa_c * (1 + st.session_state.c_asig_val)
    if tasa_real > 0: st.session_state.usd_banco = st.session_state.cap_bs / tasa_real

def update_bs():
    tasa_real = st.session_state.tasa_c * (1 + st.session_state.c_asig_val)
    st.session_state.cap_bs = st.session_state.usd_banco * tasa_real

def update_tasa(): update_usd()

hoy_str = datetime.now().strftime("%Y-%m-%d")
mes_str = datetime.now().strftime("%Y-%m")

# --- ESTADÍSTICAS GLOBALES ---
if not df_h.empty:
    df_hoy = df_h[df_h['Día'] == hoy_str]
    ganancia_bs_hoy = df_hoy['Ganancia_Bs'].sum()
    ganancia_usd_hoy = df_hoy['Usdt_Retenidos'].sum()
    ganancia_usd_total = df_h['Usdt_Retenidos'].sum()
else:
    ganancia_bs_hoy, ganancia_usd_hoy, ganancia_usd_total = 0, 0, 0

# --- SIDEBAR ---
st.sidebar.header("👥 SELECCIÓN DE CUENTAS")
titular_actual = st.sidebar.selectbox("Titular Actual:", ["Alejandro", "Rosa", "Rubén", "Luz", "Yngianni"])
zinli_actual = st.sidebar.selectbox("Cuenta Zinli:", [f"Zinli {i:02d}" for i in range(1, 16)])

st.sidebar.divider()
st.sidebar.header("🛡️ LÍMITES EN VIVO")
uso_dia_banco = df_h[(df_h['Día'] == hoy_str) & (df_h['Titular'] == titular_actual)]['USD_Comprados'].sum() if not df_h.empty else 0
uso_mes_banco = df_h[(df_h['Mes'] == mes_str) & (df_h['Titular'] == titular_actual)]['USD_Comprados'].sum() if not df_h.empty else 0
uso_mes_zinli = df_h[(df_h['Mes'] == mes_str) & (df_h['Cuenta_Zinli'] == zinli_actual) & (df_h['Ruta'] == 'ZINLI')]['USD_Comprados'].sum() if not df_h.empty else 0

st.sidebar.metric(f"DÍA - {titular_actual}", f"$ {2000 - uso_dia_banco:,.2f}")
st.sidebar.metric(f"MES - {titular_actual}", f"$ {10000 - uso_mes_banco:,.2f}")
st.sidebar.metric(f"MES - {zinli_actual}", f"$ {1000 - uso_mes_zinli:,.2f}")

st.sidebar.divider()
c_asig_bdv = st.sidebar.number_input("% Asig. BDV", value=0.50) / 100
c_asig_bancamiga = st.sidebar.number_input("% Asig. Bancamiga", value=0.80) / 100
c_tarjeta = st.sidebar.number_input("% Uso Tarjeta", value=2.50) / 100
c_zinli_com = st.sidebar.number_input("% Comisión Zinli", value=3.75) / 100
c_envio_z = st.sidebar.number_input("% Envío Zinli", value=1.00) / 100
fijo_z = st.sidebar.number_input("Fijo Zinli ($)", value=0.40)
c_bin_dep = st.sidebar.number_input("% Comis. Binance", value=3.30) / 100

# --- CONTROLES SUPERIORES ---
st.markdown('<div class="top-controls">', unsafe_allow_html=True)
col_head1, col_head2 = st.columns(2)
with col_head1: banco = st.radio("🏦 Entidad:", ["BDV", "BANCAMIGA"], horizontal=True)
with col_head2: metodo = st.radio("📍 Mecanismo:", ["ZINLI", "TARJETA DIRECTA"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

st.session_state.c_asig_val = c_asig_bancamiga if banco == "BANCAMIGA" else c_asig_bdv

# --- PASO 1, 2 Y 3 ---
st.markdown("### 1️⃣ COMPRA EN BANCO")
tasa_c = st.number_input("Tasa Compra", key="tasa_c", on_change=update_tasa)
cap_bs = st.number_input("Capital (Bs.)", key="cap_bs", on_change=update_usd)
usd_reales_b = st.number_input(f"USD en {banco}", key="usd_banco", on_change=update_bs)
tasa_real_b = st.session_state.tasa_c * (1 + st.session_state.c_asig_val)

st.markdown("### 2️⃣ MOVIMIENTO Y CONVERSIÓN")
if metodo == "ZINLI":
    monto_rec_sug = (usd_reales_b - 1.0) / (1 + c_zinli_com + c_tarjeta)
    st.markdown(f'<div class="sugerencia-box">💡 Sugerencia Recarga {zinli_actual}: <b>$ {monto_rec_sug:,.2f}</b></div>', unsafe_allow_html=True)
    usd_netos_zinli = st.number_input("NETO Zinli (Exacto)", value=float(monto_rec_sug))
    oferta_p2p = (usd_netos_zinli - fijo_z) / (1 + c_envio_z)
    tasa_u = st.number_input("Tasa P2P (USD/USDT)", value=1.033, format="%.3f")
    usdt_recibidos = float(oferta_p2p / tasa_u) if tasa_u > 0 else 0.0
else:
    sugerido_t = (usd_reales_b - 1.0) / (1 + c_tarjeta)
    st.markdown(f'<div class="sugerencia-box">💡 Sugerencia Tarjeta: <b>$ {sugerido_t:,.2f}</b></div>', unsafe_allow_html=True)
    usd_directo = st.number_input("USD Gastados de Tarjeta", value=float(sugerido_t))
    usdt_recibidos = float(usd_directo * (1 - c_bin_dep))

st.markdown(f'<div class="usdt-box">📥 RECIBIRÁS: {usdt_recibidos:.2f} USDT</div>', unsafe_allow_html=True)

st.markdown("### 3️⃣ VENTA PARA RECUPERAR")
tasa_v = st.number_input("Tasa Venta (Bs/USDT)", value=660.0)
usdt_minimos_recuperar = cap_bs / tasa_v if tasa_v > 0 else 0.0
st.markdown(f'<div class="sugerencia-box">⚠️ Debes vender mínimo <b>{usdt_minimos_recuperar:.2f} USDT</b> para reponer los Bs. {cap_bs:,.2f}</div>', unsafe_allow_html=True)
usdt_a_vender = st.number_input("¿Cuántos USDT vas a vender realmente?", value=float(usdt_minimos_recuperar))

# --- CÁLCULOS FINALES (BLOQUEADOS) ---
ganancia_usdt = usdt_recibidos - usdt_a_vender
bs_recup = usdt_a_vender * tasa_v

# ESCUDO MATEMÁTICO: Forzar resultados a ser números válidos o 0.0
def safe_val(val):
    return val if math.isfinite(val) else 0.0

brecha_num = safe_val(((tasa_v / tasa_real_b) - 1) * 100) if tasa_real_b > 0 else 0.0
roi_num = safe_val(((ganancia_usdt * tasa_v) / cap_bs) * 100) if cap_bs > 0 else 0.0
retenido_num = safe_val(ganancia_usdt)

# PRE-FORMATEO DE TEXTO PARA EL TICKET (Sincronización Total)
t_brecha = "{:,.2f}%".format(brecha_num)
t_roi = "{:,.2f}%".format(roi_num)
t_retenido = "{:,.2f} USDT".format(retenido_num)
t_compra = "Bs. {:,.2f}".format(tasa_real_b)
t_venta = "Bs. {:,.2f}".format(tasa_v)

# --- PANEL DINÁMICO ---
st.markdown(f"""
<div class="panel-dinamico">
    <div class="panel-item"><div class="panel-titulo">↔️ BRECHA REAL</div><div class="panel-valor">{t_brecha}</div></div>
    <div class="panel-item"><div class="panel-titulo">🚀 ROI NETO</div><div class="panel-valor">{t_roi}</div></div>
</div>
""", unsafe_allow_html=True)

col_stats1, col_stats2, col_stats3 = st.columns(3)
col_stats1.metric("Ganancia Hoy (Bs)", f"Bs. {ganancia_bs_hoy:,.2f}")
col_stats2.metric("Retenido Hoy (USDT)", f"{ganancia_usd_hoy:,.2f} USDT")
col_stats3.metric("🔥 ACUMULADO TOTAL", f"{ganancia_usd_total:,.2f} USDT")

# --- TICKET DEFINITIVO (ORDEN IMAGEN 3) ---
ticket_html = f"""
<div class="ticket-wrapper">
    <div class="whatsapp-ticket">
        <div class="ticket-header">👥 {titular_actual}</div>
        <div class="ticket-retenido-box">
            <div class="ticket-retenido-label">🛡️ RETENIDO</div>
            <div class="ticket-retenido-valor">{t_retenido}</div>
        </div>
        <div class="ticket-row"><span class="ticket-label">🚀 ROI NETO:</span><b class="ticket-value">{t_roi}</b></div>
        <div class="ticket-row"><span class="ticket-label">🏦 Banco:</span><b class="ticket-value">{banco}</b></div>
        <div class="ticket-row"><span class="ticket-label">📉 Compra Real:</span><b class="ticket-value">{t_compra}</b></div>
        <div class="ticket-row"><span class="ticket-label">📈 Tasa Venta:</span><b class="ticket-value">{t_venta}</b></div>
        <div class="ticket-row"><span class="ticket-label">📍 Ruta:</span><b class="ticket-value">{metodo}</b></div>
        <div class="ticket-row" style="border:none;"><span class="ticket-label">↔️ Brecha Real:</span><b class="ticket-value">{t_brecha}</b></div>
    </div>
</div>
"""
st.write(ticket_html, unsafe_allow_html=True)

# --- BOTONES Y REGISTROS ---
if st.button("💾 REGISTRAR EN LA NUBE", type="primary", use_container_width=True):
    nuevo = pd.DataFrame([{
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "Día": hoy_str, "Mes": mes_str,
        "Titular": titular_actual, "Cuenta_Zinli": zinli_actual if metodo == 'ZINLI' else "N/A",
        "Banco": banco, "Ruta": metodo, "USD_Comprados": usd_reales_b, 
        "Ganancia_Bs": retenido_num * tasa_v, "Usdt_Retenidos": round(retenido_num, 2), "ROI_%": round(roi_num, 2)
    }])
    updated_df = pd.concat([df_h, nuevo], ignore_index=True)
    conn.update(data=updated_df)
    st.success("¡Operación Registrada!")
    st.rerun()

st.divider()
with st.expander("📚 VER / EDITAR HISTORIAL"):
    df_editado = st.data_editor(df_h.sort_index(ascending=False), num_rows="dynamic", use_container_width=True, key="history_editor")
    if st.button("🛠️ Guardar Cambios en Historial", use_container_width=True):
        conn.update(data=df_editado)
        st.success("¡Historial actualizado!")
        st.rerun()
