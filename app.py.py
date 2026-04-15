import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración inicial de la página (Más compacta)
st.set_page_config(page_title="Team Arbitraje Directo", layout="wide", initial_sidebar_state="collapsed")

# Estilo Premium (Glassmorphism) COMPACTADO PARA CERO SCROLL
st.markdown("""
    <style>
    /* Reducir espacio superior de Streamlit */
    .block-container { padding-top: 1.0rem !important; padding-bottom: 1.0rem !important; }
    
    /* Fondo principal y textos */
    .main { background-color: #0f172a; color: #e2e8f0; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    h1, h2, h3, h4, p, label, .stMarkdown { color: #f8fafc !important; font-weight: 700 !important; }
    
    /* Achicar Títulos para ahorrar espacio */
    h1 { font-size: 1.4rem !important; margin-bottom: 0rem !important; padding-bottom: 0 !important; }
    h3 { font-size: 1.0rem !important; margin-bottom: 0.1rem !important; margin-top: 0.5rem !important; }
    h4 { font-size: 1.0rem !important; margin-bottom: 0.2rem !important; }
    hr { margin-top: 0.3rem !important; margin-bottom: 0.5rem !important; border-color: rgba(255,255,255,0.05) !important; }
    
    /* Inputs Modernos y más delgados */
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
    
    /* Dashboard y Pasos Glassmorphism COMPACTOS */
    .dashboard-panel, .radar-box { 
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        backdrop-filter: blur(12px);
        padding: 10px 12px !important; 
        border-radius: 12px; 
        border: 1px solid rgba(255, 255, 255, 0.05); 
        margin-bottom: 10px !important; 
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); 
    }
    
    /* Cajas de Métricas Estilo Neón COMPACTAS (Para rendimiento) */
    div[data-testid="stMetric"] { 
        background: linear-gradient(145deg, #1e293b, #0f172a) !important; 
        padding: 6px 10px !important; 
        border-radius: 10px; 
        border: 1px solid rgba(56, 189, 248, 0.2) !important; 
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stMetricValue"] { font-size: 1.2rem !important; font-weight: 900 !important; color: #38bdf8 !important; text-shadow: 0 0 5px rgba(56,189,248,0.3); }
    div[data-testid="stMetricLabel"] p { font-weight: 800 !important; color: #94a3b8 !important; font-size: 11px !important; letter-spacing: 0.5px; margin-bottom: 0 !important; }
    
    /* Alertas y Tickets COMPACTOS */
    .highlight-action { background: linear-gradient(135deg, #fef08a, #facc15); padding: 6px; border-radius: 8px; color: #000; text-align: center; font-size: 15px; font-weight: 900; margin-bottom: 5px; border: 1px dashed #854d0e; }
    .ticket-wrapper { display: flex; justify-content: center; padding: 5px; }
    .whatsapp-ticket { background: linear-gradient(to bottom, #ffffff, #f8fafc); border: 3px dashed #16a34a; border-radius: 20px; padding: 12px; width: 100%; max-width: 450px; color: #000000; margin-top: 5px;}
    .ticket-header { text-align: center; font-size: 15px; font-weight: 900; color: #16a34a; border-bottom: 2px solid #16a34a; padding-bottom: 6px; margin-bottom: 10px; }
    .ticket-row { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #cbd5e1; color: #000000; align-items: center; }
    .ticket-label { font-size: 13px; font-weight: 700; color: #334155; }
    .ticket-value { font-size: 13px; font-weight: 900; color: #000000; text-align: right; }
    .ticket-roi-box { text-align: center; font-size: 16px; font-weight: 900; color: #16a34a; background-color: #f0fdf4; padding: 8px; border-radius: 12px; margin-top: 10px; border: 2px solid #16a34a; }
    </style>
    """, unsafe_allow_html=True)

# Título Principal (Compacto)
st.markdown("<h1 style='text-align: center; color: #38bdf8 !important;'>🚀 RUTA DIRECTA (BDV)</h1><hr>", unsafe_allow_html=True)

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
# DASHBOARD DE CONTROL (Compactación Extrema)
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

st.markdown("<div class='dashboard-panel'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin: 0; font-size: 13px; color:#94a3b8;'>🎛️ PANEL DE CONTROL</p>", unsafe_allow_html=True)
st.session_state.cuenta_activa = st.selectbox("💳 Cuenta Activa:", cuentas_lista, index=cuentas_lista.index(cuenta_activa), label_visibility="collapsed")
st.markdown(f"<p style='text-align:center; color:#94a3b8 !important; font-size:11px; margin-top:2px; margin-bottom:0;'>Vueltas Hoy: <b>{vueltas_hoy}</b> | Día ($2k): <span style='color:#38bdf8;'>$ {cupo_diario_restante:,.0f}</span> | Mes ($10k): <span style='color:#38bdf8;'>$ {cupo_mensual_restante:,.0f}</span></p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:12px; margin-top:2px; margin-bottom:0;'>Ganancia Cuenta: <span style='color:#16a34a;'>Bs. {ganancia_acumulada:,.2f}</span> | 🌍 GLOBAL: <span style='color:#facc15;'>Bs. {ganancia_total_hoy:,.2f}</span></p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# FLUJO OPERATIVO
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

tipo_vuelta = st.radio("🔄 Dirección de la Vuelta:", ["➡️ Normal (Comprar BDV primero)", "⬅️ Inversa (Vender USDT primero)"], horizontal=True)

if tipo_vuelta == "➡️ Normal (Comprar BDV primero)":
    # --- FLUJO NORMAL (Restaurado Bs./USD) ---
    st.markdown("<h3 style='margin:0;'>1️⃣ Fondeo BDV</h3>", unsafe_allow_html=True)
    
    # NUEVO: st.radio para elegir entre ingresar en bolívares (Bs) o dólares (USD)
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

    # Matemáticas Normal
    gan_bs = confirmado_bs_recibidos - cap_bs
    roi = (gan_bs / cap_bs) * 100 if cap_bs > 0 else 0
    brecha = ((tasa_v / tasa_real_b) - 1) * 100 if tasa_real_b > 0 else 0
    gan_usdt = gan_bs / tasa_v if tasa_v != 0 else 0
    
    # Para historial
    hist_cap_invertido = cap_bs
    hist_usd_comprados = usd_en_banco
    hist_usdt_vendidos = usdt_a_vender
    hist_bs_recibidos = confirmado_bs_recibidos

else:
    # --- FLUJO INVERSO (NUEVO) ---
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

    # Matemáticas Inversas (Ganancia directa en USDT)
    gan_usdt = usdt_finales - usdt_iniciales
    gan_bs = gan_usdt * tasa_v
    roi = (gan_usdt / usdt_iniciales) * 100 if usdt_iniciales > 0 else 0
    brecha = ((tasa_v / tasa_real_b) - 1) * 100 if tasa_real_b > 0 else 0
    
    # Para historial
    hist_cap_invertido = bs_a_invertir
    hist_usd_comprados = usd_en_banco_inv
    hist_usdt_vendidos = usdt_iniciales
    hist_bs_recibidos = confirmado_bs_inverso
    usd_en_banco = usd_en_banco_inv # Para usar en la alerta de radar

# ---------------------------------------------------------
# MÉTRICAS Y ALERTAS (COMPACTADOS)
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

# Alertas
tasa_minima_venta = cap_bs / usdt_a_vender if tipo_vuelta.startswith('➡️') and usdt_a_vender > 0 else 0
if tasa_minima_venta > 0 and tasa_v <= tasa_minima_venta:
    st.error(f"🚨 Tasa mínima sin pérdidas: **Bs. {tasa_minima_venta:,.2f}**.")
elif tasa_minima_venta > 0 and tasa_v < (tasa_minima_venta * 1.015): 
    st.warning(f"⚠️ Margen ajustado. Tasa mínima: **Bs. {tasa_minima_venta:,.2f}**.")

# Radar
if usd_en_banco > 0 and roi > 0:
    capital_simulado = usd_en_banco
    cupo_disponible_sim = cupo_diario_restante
    vueltas_posibles = 0
    while capital_simulado <= cupo_disponible_sim:
        vueltas_posibles += 1
        cupo_disponible_sim -= capital_simulado
        capital_simulado = capital_simulado * (1 + (roi/100))
    excedente = capital_simulado - cupo_disponible_sim
    html_radar = f"<div class='radar-box'><p style='margin:0; font-size:12px; color:#38bdf8;'>🔄 Radar: {vueltas_posibles} vueltas más. Límite día en: $ {cupo_disponible_sim:,.0f} (Excedente $ {excedente:,.0f}).</p></div>"
    st.markdown(html_radar, unsafe_allow_html=True)

# Ticket Estilo WhatsApp
ticket_html = f"""
<div class="ticket-wrapper">
    <div class="whatsapp-ticket">
        <div class="ticket-header">📋 REPORTE DIRECTO - BDV</div>
        <div class="ticket-row"><span class="ticket-label">💵 Cap. Invertido:</span><span class="ticket-value">Bs. {hist_cap_invertido:,.2f}</span></div>
        <div class="ticket-row"><span class="ticket-label">📈 Tasa Venta:</span><span class="ticket-value">Bs. {tasa_v:,.2f}</span></div>
        <div class="ticket-row" style="border:none;"><span class="ticket-label">🟢 Ganancia:</span><span class="ticket-value" style="color:#16a34a;">Bs. {gan_bs:,.2f}</span></div>
        <div class="ticket-roi-box">🚀 ROI REAL: {roi:.2f}%</div>
    </div>
</div>
"""
st.write(ticket_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# GUARDADO Y VISUALIZACIÓN DE HISTORIAL (SESSION STATE + CSV)
# ---------------------------------------------------------
if st.button("💾 GUARDAR VUELTA EXACTA", use_container_width=True):
    # Blindaje de guardado usando Session State y CSV
    if usd_en_banco > cupo_diario_restante or usd_en_banco > cupo_mensual_restante:
        st.error(f"❌ No puedes guardar. Supera los límites operativos de la {cuenta_activa}.")
    else:
        nuevo_registro = {
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), 
            "Día": hoy_str,
            "Mes": mes_str,
            "Cuenta": cuenta_activa,
            "Cap_Invertido_Bs": hist_cap_invertido,
            "USD_Comprados": hist_usd_comprados, 
            "USDT_Vendidos": hist_usdt_vendidos,
            "Tasa_Venta": tasa_v,
            "Bs_Recibidos": hist_bs_recibidos,
            "Ganancia_Bs": gan_bs, 
            "ROI": roi
        }
        df_nuevo = pd.DataFrame([nuevo_registro])
        # Guardar en memoria de sesión y en archivo CSV
        st.session_state.historial_df = pd.concat([st.session_state.historial_df, df_nuevo], ignore_index=True)
        st.session_state.historial_df.to_csv(archivo_historial, index=False)
        st.success(f"¡Vuelta registrada en {cuenta_activa}! Actualiza para ver el Récord.")
        st.balloons()

with st.expander("📂 VER HISTORIAL"):
    if not st.session_state.historial_df.empty:
        df_mostrar = st.session_state.historial_df[['Día', 'Cuenta', 'USD_Comprados', 'Ganancia_Bs', 'ROI']].tail(10).sort_index(ascending=False)
        st.dataframe(df_mostrar, use_container_width=True)
        
        col_del1, col_del2 = st.columns(2)
        with col_del1:
            if st.button("🗑️ Borrar Última", use_container_width=True):
                st.session_state.historial_df = st.session_state.historial_df.iloc[:-1]
                st.session_state.historial_df.to_csv(archivo_historial, index=False)
                st.success("Última vuelta eliminada. ¡Actualiza!")
        with col_del2:
            if st.button("🚨 Borrar TODO", use_container_width=True):
                st.session_state.historial_df = pd.DataFrame(columns=columnas_historial)
                if os.path.exists(archivo_historial):
                    os.remove(archivo_historial)
                st.success("Historial reseteado por completo. ¡Actualiza!")
        
