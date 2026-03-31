import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA Y ESTADO DE SESIÓN ---
st.set_page_config(page_title="TEAM ARBITRAJE Pro", layout="wide", initial_sidebar_state="expanded")

# --- IDENTIDAD VISUAL: LOGO (USANDO TU NOMBRE DE ARCHIVO REAL) ---
# Mostramos la imagen del encabezado adaptada al ancho del móvil
st.image("1774925854444.png", use_container_width=True)

# Inicializar variables de estado para el cálculo bidireccional (Blindado)
if 'tasa_c' not in st.session_state: st.session_state.tasa_c = 570.0
if 'cap_bs' not in st.session_state: st.session_state.cap_bs = 400000.0
if 'usd_banco' not in st.session_state: st.session_state.usd_banco = 0.0
if 'c_asig_val' not in st.session_state: st.session_state.c_asig_val = 0.005 

def update_usd():
    tasa_real = st.session_state.tasa_c * (1 + st.session_state.c_asig_val)
    if tasa_real > 0:
        st.session_state.usd_banco = st.session_state.cap_bs / tasa_real

def update_bs():
    tasa_real = st.session_state.tasa_c * (1 + st.session_state.c_asig_val)
    st.session_state.cap_bs = st.session_state.usd_banco * tasa_real

def update_tasa():
    update_usd()

# --- CONEXIÓN A GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        # TTL de 1s para asegurar que vemos los datos borrados de inmediato
        return conn.read(ttl="1s") 
    except:
        return pd.DataFrame(columns=["Fecha", "Día", "Mes", "Titular", "Cuenta_Zinli", "Banco", "Ruta", "USD_Comprados", "Ganancia_Bs", "Usdt_Retenidos", "ROI_%"])

df_h = load_data()

# --- ESTILO VISUAL: MODO OSCURO COMPACTO ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a !important; color: #f8fafc !important; }
    .block-container { padding-top: 1.0rem !important; padding-bottom: 1rem !important; max-width: 98% !important; }
    h1, h2, h3, p, label, .stMarkdown { color: #f8fafc !important; font-weight: 700 !important; margin-bottom: 2px !important;}
    h3 { font-size: 1.1rem !important; margin-top: 0.5rem !important; color: #38bdf8 !important; }
    div[data-testid="stMetric"], div.stNumberInput, div.stRadio, div.stSelectbox {
        background-color: #1e293b !important; padding: 5px 10px !important; border-radius: 8px !important; border: 1px solid #334155 !important;
    }
    div[data-testid="stNumberInputContainer"] { max-width: 180px !important; margin: 0 auto; }
    .stNumberInput div div input { color: #f8fafc !important; background-color: #0f172a !important; border: 1px solid #475569 !important; font-weight: 900 !important; text-align: center !important; }
    div[data-testid="stMetricValue"] { font-weight: 900 !important; color: #38bdf8 !important; font-size: 1.2rem !important;}
    div[data-testid="stMetricLabel"] p { font-size: 12px !important; color: #94a3b8 !important; }
    section[data-testid="stSidebar"] { background-color: #1e293b !important; border-right: 1px solid #334155;}
    .sugerencia-box { background-color: #064e3b; padding: 5px; border-radius: 8px; border: 1px solid #10b981; color: #a7f3d0; text-align: center; margin-bottom: 2px; }
    
    .ticket-wrapper { display: flex; justify-content: center; padding: 5px; }
    .whatsapp-ticket { background-color: #ffffff !important; border: 3px dashed #16a34a; border-radius: 15px; padding: 15px; width: 380px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
    .whatsapp-ticket * { color: #000000 !important; } 
    .ticket-header { text-align: center; font-size: 16px; font-weight: 900; color: #16a34a !important; border-bottom: 2px solid #16a34a; padding-bottom: 5px; margin-bottom: 10px; }
    .ticket-row { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #e2e8f0; }
    .ticket-label { font-size: 13px; font-weight: 700; color: #334155 !important; }
    .ticket-value { font-size: 14px; font-weight: 900; }
    .ticket-roi-box { text-align: center; font-size: 18px; font-weight: 900; color: #16a34a !important; background-color: #f0fdf4 !important; padding: 8px; border-radius: 8px; margin-top: 10px; border: 2px solid #16a34a; }
    </style>
""", unsafe_allow_html=True)

hoy_str = datetime.now().strftime("%Y-%m-%d")
mes_str = datetime.now().strftime("%Y-%m")

# --- SIDEBAR: GESTIÓN DE CUENTAS ---
st.sidebar.header("👥 CUENTAS ACTIVAS")
titular_actual = st.sidebar.selectbox("Titular:", ["Alejandro", "Rosa", "Rubén", "Luz", "Yngianni"])
zinli_actual = st.sidebar.selectbox("Cuenta Zinli:", [f"Zinli {i:02d}" for i in range(1, 16)])

st.sidebar.divider()
st.sidebar.header("🛡️ LÍMITES EN VIVO")

# Filtrar uso por Titular y por Zinli
uso_dia_banco = df_h[(df_h['Día'] == hoy_str) & (df_h['Titular'] == titular_actual)]['USD_Comprados'].sum()
uso_mes_banco = df_h[(df_h['Mes'] == mes_str) & (df_h['Titular'] == titular_actual)]['USD_Comprados'].sum()
uso_mes_zinli = df_h[(df_h['Mes'] == mes_str) & (df_h['Cuenta_Zinli'] == zinli_actual) & (df_h['Ruta'] == 'ZINLI')]['USD_Comprados'].sum()

st.sidebar.metric(f"DÍA - {titular_actual}", f"$ {2000 - uso_dia_banco:,.2f}")
st.sidebar.metric(f"MES - {titular_actual}", f"$ {10000 - uso_mes_banco:,.2f}")
st.sidebar.metric(f"MES - {zinli_actual}", f"$ {1000 - uso_mes_zinli:,.2f}")

# --- COMISIONES ---
st.sidebar.divider()
c_asig_bdv = st.sidebar.number_input("% Asig. BDV", value=0.50) / 100
c_asig_bancamiga = st.sidebar.number_input("% Asig. Bancamiga", value=0.80) / 100
c_tarjeta = st.sidebar.number_input("% Uso Tarjeta", value=2.50) / 100
c_zinli_com = st.sidebar.number_input("% Comisión Zinli", value=3.75) / 100
c_envio_z = st.sidebar.number_input("% Envío Zinli", value=1.00) / 100
fijo_z = st.sidebar.number_input("Fijo Zinli ($)", value=0.40)
c_bin_dep = st.sidebar.number_input("% Comis. Binance", value=3.30) / 100

# --- LÓGICA DE OPERACIÓN ---
col_head1, col_head2 = st.columns(2)
with col_head1: banco = st.radio("🏦 Entidad:", ["BDV", "BANCAMIGA"], horizontal=True)
with col_head2: metodo = st.radio("📍 Mecanismo:", ["ZINLI", "TARJETA DIRECTA"], horizontal=True)

st.session_state.c_asig_val = c_asig_bancamiga if banco == "BANCAMIGA" else c_asig_bdv

st.divider()

col_op1, col_op2 = st.columns([1.2, 2])
with col_op1:
    st.markdown(f"### 1️⃣ COMPRA")
    tasa_c = st.number_input("Tasa Compra", key="tasa_c", on_change=update_tasa)
    cap_bs = st.number_input("Capital (Bs.)", key="cap_bs", on_change=update_usd)
    usd_reales_b = st.number_input(f"USD en {banco}", key="usd_banco", on_change=update_bs)
    tasa_real_b = st.session_state.tasa_c * (1 + st.session_state.c_asig_val)

with col_op2:
    st.markdown("### 2️⃣ MOVIMIENTO Y 3️⃣ VENTA")
    col_sub1, col_sub2 = st.columns(2)
    if metodo == "ZINLI":
        with col_sub1:
            monto_rec_sug = (usd_reales_b - 1.0) / (1 + c_zinli_com + c_tarjeta)
            st.markdown(f'<div class="sugerencia-box">RECARGA {zinli_actual}: <b>$ {monto_rec_sug:,.2f}</b></div>', unsafe_allow_html=True)
            usd_netos_zinli = st.number_input("NETO Zinli", value=float(monto_rec_sug))
            oferta_p2p = (usd_netos_zinli - fijo_z) / (1 + c_envio_z)
        with col_sub2:
            tasa_u = st.number_input("Tasa USD/USDT", value=1.033, format="%.3f")
            usdt_recibidos = float(oferta_p2p / tasa_u)
            tasa_v = st.number_input("Tasa Venta", value=660.0)
    else:
        with col_sub1:
            sugerido_t = (usd_reales_b - 1.0) / (1 + c_tarjeta)
            st.markdown(f'<div class="sugerencia-box">MONTO TARJETA: <b>$ {sugerido_t:,.2f}</b></div>', unsafe_allow_html=True)
            usd_directo = st.number_input("USD tras Tarjeta", value=float(sugerido_t))
        with col_sub2:
            usdt_recibidos = float(usd_directo * (1 - c_bin_dep))
            tasa_v = st.number_input("Tasa Venta", value=660.0)

# --- CÁLCULOS Y TICKET ---
usdt_para_recuperar = cap_bs / tasa_v
usdt_ganancia = usdt_recibidos - usdt_para_recuperar
roi = ((usdt_ganancia * tasa_v) / cap_bs) * 100
brecha = ((tasa_v / tasa_real_b) - 1) * 100

st.divider()
col_met1, col_met2, col_met3 = st.columns(3)
col_met1.metric("A Vender para Recuperar", f"{usdt_para_recuperar:.2f} USDT")
col_met2.metric("GANANCIA RETENIDA", f"{usdt_ganancia:.2f} USDT")
col_met3.metric("ROI", f"{roi:.2f}%")

ticket_html = f"""
<div class="ticket-wrapper">
    <div class="whatsapp-ticket">
        <div class="ticket-header">📋 REPORTE ({titular_actual})</div>
        <div class="ticket-row"><span>🏦 Banco:</span><b>{banco}</b></div>
        <div class="ticket-row"><span>📉 Compra Real:</span><b>Bs. {tasa_real_b:,.2f}</b></div>
        <div class="ticket-row"><span>📈 Venta P2P:</span><b>Bs. {tasa_v:,.2f}</b></div>
        <div class="ticket-row"><span>↔️ Brecha:</span><b>{brecha:.2f}%</b></div>
        <div class="ticket-row" style="border:none;"><span>🛡️ RETENIDO:</span><b style="color:#16a34a;">{usdt_ganancia:.2f} USDT</b></div>
        <div class="ticket-roi-box">🚀 ROI: {roi:.2f}%</div>
    </div>
</div>
"""
st.write(ticket_html, unsafe_allow_html=True)

# --- GUARDAR EN GOOGLE SHEETS ---
if st.button("💾 REGISTRAR EN LA NUBE", type="primary", use_container_width=True):
    nuevo = pd.DataFrame([{
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "Día": hoy_str, "Mes": mes_str,
        "Titular": titular_actual, "Cuenta_Zinli": zinli_actual if metodo == 'ZINLI' else "N/A",
        "Banco": banco, "Ruta": metodo, "USD_Comprados": usd_reales_b, 
        "Ganancia_Bs": usdt_ganancia * tasa_v, "Usdt_Retenidos": round(usdt_ganancia, 2), "ROI_%": round(roi, 2)
    }])
    updated_df = pd.concat([df_h, nuevo], ignore_index=True)
    conn.update(data=updated_df)
    st.success("¡Guardado en Google Sheets!")
    st.rerun()

# --- HISTORIAL EN LA NUBE (EDITABLE PARA BORRAR) ---
st.divider()
st.subheader("📚 HISTORIAL EN LA NUBE (Editable)")
st.info("💡 Haz doble clic en una celda para editar, o selecciona una fila a la izquierda y presiona 'Supr' en tu teclado para borrar.")

df_editado = st.data_editor(df_h.sort_index(ascending=False), num_rows="dynamic", use_container_width=True, key="history_editor")

if st.button("🛠️ Guardar Cambios en Historial (Confirmar Borrado)", use_container_width=True):
    conn.update(data=df_editado)
    st.success("¡Historial actualizado correctamente!")
    st.rerun()
    
