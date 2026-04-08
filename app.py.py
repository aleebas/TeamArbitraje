import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración inicial de la página
st.set_page_config(page_title="Team Arbitraje Directo", layout="wide", initial_sidebar_state="collapsed")

# Estilo Restful Blue, Ticket y Dashboard Optimizado
st.markdown("""
    <style>
    .main { background-color: #10172a; color: #e2e8f0; }
    
    /* Cajas de Métricas */
    div[data-testid="stMetric"] { background-color: #1e293b !important; padding: 10px; border-radius: 12px; border: 1px solid #334155 !important; }
    div[data-testid="stMetricValue"] { font-weight: 900 !important; color: #38bdf8 !important; }
    div[data-testid="stMetricLabel"] p { font-weight: 800 !important; color: #94a3b8 !important; font-size: 14px !important; text-transform: uppercase; }
    
    /* Textos Generales */
    h1, h2, h3, h4, p, label, .stMarkdown { color: #e2e8f0 !important; font-weight: 700 !important; }
    
    /* Inputs */
    .stNumberInput div div input { color: #38bdf8 !important; background-color: #0f172a !important; border: 2px solid #334155 !important; font-weight: 900 !important; font-size: 18px !important; text-align: center;}
    .stNumberInput div div input:focus { border-color: #38bdf8 !important; }
    
    /* Elementos UI Específicos */
    .dashboard-panel { background-color: #0f172a; padding: 20px; border-radius: 15px; border: 1px solid #38bdf8; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.1); }
    .step-box { background-color: #1e293b; padding: 20px; border-radius: 15px; border-left: 5px solid #16a34a; margin-bottom: 20px; }
    .highlight-action { background-color: #fef08a; padding: 10px; border-radius: 8px; color: #000; text-align: center; font-size: 18px; font-weight: 900; margin-bottom: 10px; border: 2px dashed #ca8a04; }
    
    /* Ticket y Radar */
    .ticket-wrapper { display: flex; justify-content: center; padding: 10px; }
    .whatsapp-ticket { background-color: #ffffff; border: 4px dashed #16a34a; border-radius: 20px; padding: 20px; width: 100%; max-width: 450px; color: #000000; box-shadow: 0 8px 20px rgba(0,0,0,0.3); margin-top: 20px;}
    .ticket-header { text-align: center; font-size: 18px; font-weight: 900; color: #16a34a; border-bottom: 3px solid #16a34a; padding-bottom: 10px; margin-bottom: 15px; }
    .ticket-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #e2e8f0; color: #000000; align-items: center; }
    .ticket-label { font-size: 15px; font-weight: 700; color: #334155; }
    .ticket-value { font-size: 15px; font-weight: 900; color: #000000; text-align: right; }
    .ticket-roi-box { text-align: center; font-size: 22px; font-weight: 900; color: #16a34a; background-color: #f0fdf4; padding: 12px; border-radius: 12px; margin-top: 15px; border: 2px solid #16a34a; }
    .radar-box { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #3b82f6; border-left: 5px solid #3b82f6; margin-top: 15px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# Título Principal
st.markdown("<h1 style='text-align: center; color: #38bdf8 !important;'>🚀 RUTA DIRECTA (BDV)</h1><hr style='margin-bottom: 15px; border-color: #334155;'>", unsafe_allow_html=True)

# ---------------------------------------------------------
# LÓGICA DE HISTORIAL Y FECHAS
# ---------------------------------------------------------
hoy_str = datetime.now().strftime("%Y-%m-%d")
mes_str = datetime.now().strftime("%Y-%m")
archivo_historial = "historial_directo.csv"

# Columnas extendidas para guardar más detalles
columnas_historial = ['Fecha', 'Día', 'Mes', 'Cuenta', 'Cap_Invertido_Bs', 'USD_Comprados', 'USDT_Vendidos', 'Tasa_Venta', 'Bs_Recibidos', 'Ganancia_Bs', 'ROI']

if os.path.exists(archivo_historial):
    df_h = pd.read_csv(archivo_historial)
    for col in columnas_historial:
        if col not in df_h.columns:
            df_h[col] = 0.0 # Rellenar columnas faltantes en historiales viejos
else:
    df_h = pd.DataFrame(columns=columnas_historial)

# ---------------------------------------------------------
# DASHBOARD DE CONTROL (Módulo Frontal)
# ---------------------------------------------------------
st.markdown("<div class='dashboard-panel'>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top: 0; text-align: center;'>🎛️ PANEL DE CONTROL MULTI-CUENTA</h3>", unsafe_allow_html=True)

col_d1, col_d2, col_d3 = st.columns([1, 1.5, 1.5])

with col_d1:
    cuentas_lista = [f"Cuenta {i}" for i in range(1, 7)]
    cuenta_activa = st.selectbox("💳 Seleccionar Cuenta:", cuentas_lista, label_visibility="collapsed")
    vueltas_hoy = len(df_h[(df_h['Cuenta'] == cuenta_activa) & (df_h['Día'] == hoy_str)])
    st.markdown(f"<p style='text-align:center; color:#10b981 !important; font-size:18px;'>Vueltas hoy: <b>{vueltas_hoy}</b></p>", unsafe_allow_html=True)

df_cuenta_hoy = df_h[(df_h['Cuenta'] == cuenta_activa) & (df_h['Día'] == hoy_str)]
df_cuenta_mes = df_h[(df_h['Cuenta'] == cuenta_activa) & (df_h['Mes'] == mes_str)]
cupo_dia_usado = df_cuenta_hoy['USD_Comprados'].sum() if not df_cuenta_hoy.empty else 0.0
cupo_mes_usado = df_cuenta_mes['USD_Comprados'].sum() if not df_cuenta_mes.empty else 0.0
cupo_diario_restante = max(0, 2000 - cupo_dia_usado)
cupo_mensual_restante = max(0, 10000 - cupo_mes_usado)

with col_d2:
    st.metric("Cupo Diario Libre ($2k)", f"$ {cupo_diario_restante:,.2f}")
    st.progress(min(cupo_dia_usado / 2000, 1.0))

with col_d3:
    ganancia_acumulada = df_cuenta_hoy['Ganancia_Bs'].sum() if not df_cuenta_hoy.empty else 0.0
    mejor_vuelta = df_cuenta_hoy['Ganancia_Bs'].max() if not df_cuenta_hoy.empty else 0.0
    
    st.markdown(f"**💰 Ganancia del Día:** <span style='color:#16a34a; font-size:20px;'>Bs. {ganancia_acumulada:,.2f}</span>", unsafe_allow_html=True)
    st.markdown(f"**🔥 Mejor Vuelta:** <span style='color:#38bdf8; font-size:18px;'>Bs. {mejor_vuelta:,.2f}</span>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# FLUJO OPERATIVO: PASO A PASO (CONFIRMACIÓN MANUAL)
# ---------------------------------------------------------

# Comisiones Fijas (BDV Fijo 0.5%)
c_asig = 0.005 
c_tarjeta = 0.025 # 2.5%
c_binance = 0.033 # 3.3%

col_t1, col_t2 = st.columns(2)
with col_t1:
    tasa_c = st.number_input("📉 Tasa Compra BDV (Base)", value=570.75, format="%.2f", step=0.01)
with col_t2:
    tasa_v = st.number_input("📈 Tasa Venta P2P", value=648.00, format="%.2f", step=0.01)

tasa_real_b = tasa_c * (1 + c_asig)

st.markdown("---")

# PASO 1: FONDEO
st.markdown("<div class='step-box'>", unsafe_allow_html=True)
st.markdown("### 1️⃣ Fondeo de Capital (BDV)")
tipo_ingreso = st.radio("Ingresar monto en:", ["Bolívares (Bs)", "Dólares (USD)"], horizontal=True, label_visibility="collapsed")

if tipo_ingreso == "Bolívares (Bs)":
    cap_bs = st.number_input("Monto Invertido (Bs.)", value=57360.00, format="%.2f", step=100.0)
    usd_en_banco = cap_bs / tasa_real_b if tasa_real_b > 0 else 0
    st.info(f"💵 Se comprarán: **$ {usd_en_banco:,.2f}** (Aprox)")
else:
    usd_en_banco = st.number_input("Monto a Comprar (USD)", value=100.00, format="%.2f", step=10.0)
    cap_bs = usd_en_banco * tasa_real_b
    st.info(f"🇻🇪 Necesitas fondear: **Bs. {cap_bs:,.2f}** (Aprox)")
st.markdown("</div>", unsafe_allow_html=True)


# PASO 2: RECARGA BINANCE (TARJETA)
st.markdown("<div class='step-box'>", unsafe_allow_html=True)
st.markdown("### 2️⃣ Recarga por Tarjeta")
dejar_dolar = st.checkbox("Dejar $1 de holgura por seguridad", value=True)
usd_base = max(0.0, (usd_en_banco - 1.0) if dejar_dolar else usd_en_banco)

# Sugerencia matemática
sugerido_tarjeta = usd_base * (1 - c_tarjeta)

st.markdown(f"<div class='highlight-action'>⚠️ MONTO EXACTO A TECLEAR EN LA APP:<br><span style='font-size: 28px;'>$ {sugerido_tarjeta:,.2f}</span></div>", unsafe_allow_html=True)

# CONFIRMACIÓN MANUAL
confirmado_tarjeta = st.number_input("👉 Confirma el monto que escribiste (Sin redondear céntimos si no quieres):", value=float(f"{sugerido_tarjeta:.2f}"), step=1.0)
st.markdown("</div>", unsafe_allow_html=True)


# PASO 3: LLEGADA A BINANCE (USDT)
st.markdown("<div class='step-box'>", unsafe_allow_html=True)
st.markdown("### 3️⃣ USDT Recibidos en Binance")
sugerido_binance = confirmado_tarjeta * (1 - c_binance)

st.markdown(f"Deberían llegarte aproximadamente: **₮ {sugerido_binance:,.2f}**")
confirmado_usdt_recibido = st.number_input("👉 Confirma cuántos USDT reales te acreditaron:", value=float(f"{sugerido_binance:.2f}"), step=1.0)
st.markdown("</div>", unsafe_allow_html=True)


# PASO 4: VENTA P2P
st.markdown("<div class='step-box'>", unsafe_allow_html=True)
st.markdown("### 4️⃣ Venta en el P2P")

col_v1, col_v2 = st.columns(2)
with col_v1:
    usdt_a_vender = st.number_input("USDT a Vender en esta vuelta:", value=float(confirmado_usdt_recibido), step=1.0)
with col_v2:
    sugerido_bs_recibir = usdt_a_vender * tasa_v
    confirmado_bs_recibidos = st.number_input("👉 Confirma Bs. Totales Recibidos en Cuenta:", value=float(f"{sugerido_bs_recibir:.2f}"), step=100.0)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# RESULTADOS EXACTOS Y ALERTAS (Basado en confirmaciones)
# ---------------------------------------------------------

gan_bs = confirmado_bs_recibidos - cap_bs
roi = (gan_bs / cap_bs) * 100 if cap_bs > 0 else 0
brecha = ((tasa_v / tasa_real_b) - 1) * 100 if tasa_real_b > 0 else 0

# Alerta de Punto de Equilibrio (Dinámica)
tasa_minima_venta = cap_bs / usdt_a_vender if usdt_a_vender > 0 else 0

if tasa_v <= tasa_minima_venta:
    st.error(f"🚨 **¡ALERTA DE PÉRDIDA!** Para recuperar tu inversión debes vender a **MÁS de Bs. {tasa_minima_venta:,.2f}**.")
elif tasa_v < (tasa_minima_venta * 1.015): 
    st.warning(f"⚠️ **¡CUIDADO!** Tu margen es ajustado. Tasa mínima sin pérdidas es **Bs. {tasa_minima_venta:,.2f}**.")
else:
    st.success(f"💡 **ÓPTIMO:** Tu punto de equilibrio es vendiendo a **Bs. {tasa_minima_venta:,.2f}**.")

# Radar de Interés Compuesto
if usd_en_banco > 0 and roi > 0:
    capital_simulado = usd_en_banco
    cupo_disponible_sim = cupo_diario_restante
    vueltas_posibles = 0
    
    while capital_simulado <= cupo_disponible_sim:
        vueltas_posibles += 1
        cupo_disponible_sim -= capital_simulado
        capital_simulado = capital_simulado * (1 + (roi/100))
    
    excedente = capital_simulado - cupo_disponible_sim
    
    html_radar = f"""
    <div class="radar-box">
        <h4 style="margin-top:0; color:#3b82f6;">🔄 Radar de Interés Compuesto ({cuenta_activa})</h4>
        <p style="margin:5px 0;">Con el cupo libre actual y tu ROI real del <b>{roi:.2f}%</b>:</p>
        <ul style="margin-bottom:0;">
            <li>Puedes dar <b>{vueltas_posibles} vueltas completas más</b> re-invirtiendo todo.</li>
            <li>En la última vuelta solo pasarán <b>$ {cupo_disponible_sim:,.2f}</b> por esta cuenta.</li>
            <li>Tendrás un excedente de <b style="color:#f59e0b;">$ {excedente:,.2f}</b> para la próxima cuenta.</li>
        </ul>
    </div>
    """
    st.markdown(html_radar, unsafe_allow_html=True)

# ---------------------------------------------------------
# MÉTRICAS Y TICKET FINAL
# ---------------------------------------------------------
st.markdown("### 📊 Rendimiento de esta Vuelta (Exacto)")
res1, res2, res3 = st.columns(3)

gan_usdt = gan_bs / tasa_v if tasa_v != 0 else 0

with res1:
    st.markdown(f"""
    <div data-testid="stMetric" style="background-color: #1e293b !important; padding: 10px; border-radius: 12px; border: 1px solid #334155 !important;">
        <p style="font-weight: 800 !important; color: #94a3b8 !important; font-size: 14px !important; text-transform: uppercase; margin: 0;">GANANCIA NETA REAL</p>
        <div style="display: flex; align-items: baseline; flex-wrap: wrap; gap: 8px; margin-top: 5px;">
            <span style="font-weight: 900 !important; color: #38bdf8 !important; font-size: 26px !important; line-height: 1;">Bs. {gan_bs:,.2f}</span>
            <span style="color: #16a34a !important; font-weight: 800 !important; font-size: 16px !important; line-height: 1;">≈ ₮ {gan_usdt:,.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

res2.metric("ROI REAL", f"{roi:.2f}%")
res3.metric("BRECHA", f"{brecha:.2f}%")

# Ticket Estilo WhatsApp
ticket_html = f"""
<div class="ticket-wrapper">
    <div class="whatsapp-ticket">
        <div class="ticket-header">📋 REPORTE DIRECTO - BDV</div>
        <div class="ticket-row"><span class="ticket-label">💵 Cap. Invertido:</span><span class="ticket-value">Bs. {cap_bs:,.2f}</span></div>
        <div class="ticket-row"><span class="ticket-label">📉 Tasa Compra:</span><span class="ticket-value">Bs. {tasa_real_b:,.2f}</span></div>
        <div class="ticket-row"><span class="ticket-label">📈 Tasa Venta:</span><span class="ticket-value">Bs. {tasa_v:,.2f}</span></div>
        <div class="ticket-row"><span class="ticket-label">💰 Bs Recibidos:</span><span class="ticket-value">Bs. {confirmado_bs_recibidos:,.2f}</span></div>
        <div class="ticket-row" style="border:none;"><span class="ticket-label">🟢 Ganancia:</span><span class="ticket-value" style="color:#16a34a;">Bs. {gan_bs:,.2f}</span></div>
        <div class="ticket-roi-box">🚀 ROI REAL: {roi:.2f}%</div>
    </div>
</div>
"""
st.write(ticket_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# GUARDADO Y VISUALIZACIÓN DE HISTORIAL
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
if st.button("💾 GUARDAR VUELTA EXACTA", use_container_width=True):
    if usd_en_banco > cupo_diario_restante:
        st.error(f"❌ No puedes guardar. Supera el límite diario de la {cuenta_activa}.")
    else:
        nuevo_registro = {
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), 
            "Día": hoy_str,
            "Mes": mes_str,
            "Cuenta": cuenta_activa,
            "Cap_Invertido_Bs": cap_bs,
            "USD_Comprados": usd_en_banco, 
            "USDT_Vendidos": usdt_a_vender,
            "Tasa_Venta": tasa_v,
            "Bs_Recibidos": confirmado_bs_recibidos,
            "Ganancia_Bs": gan_bs, 
            "ROI": roi
        }
        pd.DataFrame([nuevo_registro]).to_csv(
            archivo_historial, 
            mode='a', 
            header=not os.path.exists(archivo_historial), 
            index=False
        )
        st.success(f"¡Vuelta registrada en {cuenta_activa} con éxito! Actualiza la página.")
        st.balloons()

st.markdown("---")
st.markdown("### 📂 REGISTRO DE MOVIMIENTOS")
with st.expander("Haz clic aquí para ver todos tus movimientos registrados"):
    if not df_h.empty:
        # Mostrar el dataframe filtrando las columnas más importantes para no saturar la pantalla móvil
        df_mostrar = df_h[['Día', 'Cuenta', 'USD_Comprados', 'USDT_Vendidos', 'Tasa_Venta', 'Ganancia_Bs', 'ROI']].tail(10).sort_index(ascending=False)
        st.dataframe(df_mostrar, use_container_width=True)
    else:
        st.info("Aún no hay operaciones registradas.")
