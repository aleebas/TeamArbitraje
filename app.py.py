import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración inicial de la página
st.set_page_config(page_title="Team Arbitraje Directo", layout="wide", initial_sidebar_state="collapsed")

# Estilo Premium (Glassmorphism y Animaciones)
st.markdown("""
    <style>
    /* Fondo principal y textos */
    .main { background-color: #0f172a; color: #e2e8f0; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    h1, h2, h3, h4, p, label, .stMarkdown { color: #f8fafc !important; font-weight: 700 !important; }
    
    /* Cajas de Métricas Estilo Neón */
    div[data-testid="stMetric"] { 
        background: linear-gradient(145deg, #1e293b, #0f172a) !important; 
        padding: 15px; 
        border-radius: 16px; 
        border: 1px solid rgba(56, 189, 248, 0.2) !important; 
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stMetricValue"] { font-weight: 900 !important; color: #38bdf8 !important; text-shadow: 0 0 10px rgba(56,189,248,0.3); }
    div[data-testid="stMetricLabel"] p { font-weight: 800 !important; color: #94a3b8 !important; font-size: 13px !important; letter-spacing: 1px; }
    
    /* Inputs Modernos */
    .stNumberInput div div input { 
        color: #38bdf8 !important; 
        background-color: rgba(15, 23, 42, 0.8) !important; 
        border: 2px solid #334155 !important; 
        border-radius: 10px;
        font-weight: 900 !important; 
        font-size: 18px !important; 
        text-align: center;
        transition: all 0.3s ease;
    }
    .stNumberInput div div input:focus { border-color: #38bdf8 !important; box-shadow: 0 0 10px rgba(56,189,248,0.2) !important; }
    
    /* Dashboard Glassmorphism */
    .dashboard-panel { 
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        backdrop-filter: blur(12px);
        padding: 25px; 
        border-radius: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        margin-bottom: 30px; 
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4); 
    }
    
    /* Cajas de Pasos Animadas */
    .step-box { 
        background: linear-gradient(to right, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.4));
        padding: 18px 25px; 
        border-radius: 14px; 
        border: 1px solid rgba(255,255,255,0.05);
        border-left: 5px solid #38bdf8; 
        margin-bottom: 20px; 
        margin-top: 15px;
        transition: all 0.3s ease;
    }
    .step-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(0,0,0,0.5);
        border-left: 5px solid #10b981;
    }
    
    /* Alertas y Tickets */
    .highlight-action { background: linear-gradient(135deg, #fef08a, #facc15); padding: 15px; border-radius: 12px; color: #000; text-align: center; font-size: 18px; font-weight: 900; margin-bottom: 10px; border: 2px dashed #854d0e; box-shadow: 0 4px 15px rgba(250, 204, 21, 0.2); }
    .ticket-wrapper { display: flex; justify-content: center; padding: 15px; }
    .whatsapp-ticket { background: linear-gradient(to bottom, #ffffff, #f8fafc); border: 4px dashed #16a34a; border-radius: 24px; padding: 25px; width: 100%; max-width: 450px; color: #000000; box-shadow: 0 15px 35px rgba(0,0,0,0.3); margin-top: 20px;}
    .ticket-header { text-align: center; font-size: 20px; font-weight: 900; color: #16a34a; border-bottom: 3px solid #16a34a; padding-bottom: 12px; margin-bottom: 18px; }
    .ticket-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #cbd5e1; color: #000000; align-items: center; }
    .ticket-label { font-size: 16px; font-weight: 700; color: #334155; }
    .ticket-value { font-size: 16px; font-weight: 900; color: #000000; text-align: right; }
    .ticket-roi-box { text-align: center; font-size: 24px; font-weight: 900; color: #16a34a; background-color: #f0fdf4; padding: 15px; border-radius: 16px; margin-top: 20px; border: 2px solid #16a34a; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05); }
    .radar-box { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(5px); padding: 20px; border-radius: 14px; border: 1px solid rgba(59, 130, 246, 0.3); border-left: 5px solid #3b82f6; margin-top: 20px; margin-bottom: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.2); }
    </style>
    """, unsafe_allow_html=True)

# Título Principal
st.markdown("<h1 style='text-align: center; color: #38bdf8 !important; text-shadow: 0 2px 10px rgba(56,189,248,0.2);'>🚀 RUTA DIRECTA (BDV)</h1><hr style='border-color: rgba(255,255,255,0.1); margin-bottom: 25px;'>", unsafe_allow_html=True)

# ---------------------------------------------------------
# LÓGICA DE HISTORIAL BLINDADA (SESSION STATE + CSV)
# ---------------------------------------------------------
hoy_str = datetime.now().strftime("%Y-%m-%d")
mes_str = datetime.now().strftime("%Y-%m")
archivo_historial = "historial_directo.csv"

columnas_historial = ['Fecha', 'Día', 'Mes', 'Cuenta', 'Cap_Invertido_Bs', 'USD_Comprados', 'USDT_Vendidos', 'Tasa_Venta', 'Bs_Recibidos', 'Ganancia_Bs', 'ROI']

# Proteger la caché guardando los datos en la memoria de la sesión
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
# DASHBOARD DE CONTROL (Módulo Frontal)
# ---------------------------------------------------------
st.markdown("<div class='dashboard-panel'>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top: 0; text-align: center; letter-spacing: 1px;'>🎛️ PANEL DE CONTROL MULTI-CUENTA</h3>", unsafe_allow_html=True)

col_d1, col_d2, col_d3 = st.columns([1, 1.5, 1.5])

with col_d1:
    cuentas_lista = [f"Cuenta {i}" for i in range(1, 7)]
    cuenta_activa = st.selectbox("💳 Seleccionar Cuenta:", cuentas_lista, label_visibility="collapsed")
    vueltas_hoy = len(df_h[(df_h['Cuenta'] == cuenta_activa) & (df_h['Día'] == hoy_str)])
    st.markdown(f"<p style='text-align:center; color:#10b981 !important; font-size:18px; margin-top:10px;'>Vueltas hoy: <b>{vueltas_hoy}</b></p>", unsafe_allow_html=True)

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
    ganancia_total_hoy = df_h[df_h['Día'] == hoy_str]['Ganancia_Bs'].sum() if not df_h.empty else 0.0
    
    st.markdown(f"<p style='margin-bottom:5px;'><b>💰 Ganancia ({cuenta_activa}):</b> <span style='color:#16a34a; font-size:18px;'>Bs. {ganancia_acumulada:,.2f}</span></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin-bottom:5px;'><b>🔥 Mejor Vuelta:</b> <span style='color:#38bdf8; font-size:16px;'>Bs. {mejor_vuelta:,.2f}</span></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin-bottom:0;'><b>🌍 Ganancia GLOBAL (Hoy):</b> <span style='color:#facc15; font-size:20px; font-weight:900;'>Bs. {ganancia_total_hoy:,.2f}</span></p>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# FLUJO OPERATIVO: PASO A PASO
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

st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

# PASO 1: FONDEO
st.markdown("<div class='step-box'><h3 style='margin:0;'>1️⃣ Fondeo de Capital (BDV)</h3></div>", unsafe_allow_html=True)
tipo_ingreso = st.radio("Ingresar monto en:", ["Bolívares (Bs)", "Dólares (USD)"], horizontal=True, label_visibility="collapsed")

if tipo_ingreso == "Bolívares (Bs)":
    cap_bs = st.number_input("Monto Invertido (Bs.)", value=57360.00, format="%.2f", step=100.0)
    usd_en_banco = cap_bs / tasa_real_b if tasa_real_b > 0 else 0
    st.info(f"💵 Se comprarán: **$ {usd_en_banco:,.2f}** (Aprox)")
else:
    usd_en_banco = st.number_input("Monto a Comprar (USD)", value=100.00, format="%.2f", step=10.0)
    cap_bs = usd_en_banco * tasa_real_b
    st.info(f"🇻🇪 Necesitas fondear: **Bs. {cap_bs:,.2f}** (Aprox)")


# PASO 2: RECARGA BINANCE (TARJETA)
st.markdown("<div class='step-box'><h3 style='margin:0;'>2️⃣ Recarga por Tarjeta</h3></div>", unsafe_allow_html=True)
dejar_dolar = st.checkbox("Dejar $1 de holgura por seguridad", value=True)
usd_base = max(0.0, (usd_en_banco - 1.0) if dejar_dolar else usd_en_banco)

sugerido_tarjeta = usd_base * (1 - c_tarjeta)

st.markdown(f"<div class='highlight-action'>⚠️ MONTO EXACTO A TECLEAR EN LA APP:<br><span style='font-size: 28px;'>$ {sugerido_tarjeta:,.2f}</span></div>", unsafe_allow_html=True)
confirmado_tarjeta = st.number_input("👉 Confirma el monto que escribiste (Sin redondear céntimos si no quieres):", value=float(f"{sugerido_tarjeta:.2f}"), step=1.0)


# PASO 3: LLEGADA A BINANCE (USDT)
st.markdown("<div class='step-box'><h3 style='margin:0;'>3️⃣ USDT Recibidos en Binance</h3></div>", unsafe_allow_html=True)
sugerido_binance = confirmado_tarjeta * (1 - c_binance)

st.markdown(f"Deberían llegarte aproximadamente: **₮ {sugerido_binance:,.2f}**")
confirmado_usdt_recibido = st.number_input("👉 Confirma cuántos USDT reales te acreditaron:", value=float(f"{sugerido_binance:.2f}"), step=1.0)


# PASO 4: VENTA P2P
st.markdown("<div class='step-box'><h3 style='margin:0;'>4️⃣ Venta en el P2P</h3></div>", unsafe_allow_html=True)

col_v1, col_v2 = st.columns(2)
with col_v1:
    usdt_a_vender = st.number_input("USDT a Vender en esta vuelta:", value=float(confirmado_usdt_recibido), step=1.0)
with col_v2:
    sugerido_bs_recibir = usdt_a_vender * tasa_v
    confirmado_bs_recibidos = st.number_input("👉 Confirma Bs. Totales Recibidos en Cuenta:", value=float(f"{sugerido_bs_recibir:.2f}"), step=100.0)

# ---------------------------------------------------------
# RESULTADOS EXACTOS Y ALERTAS 
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
            <span style="color: #10b981 !important; font-weight: 800 !important; font-size: 16px !important; line-height: 1;">≈ ₮ {gan_usdt:,.2f}</span>
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
# GUARDADO Y VISUALIZACIÓN DE HISTORIAL CON MEMORIA PROTEGIDA
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
        # Guardar en memoria Session State y en CSV al mismo tiempo
        df_nuevo = pd.DataFrame([nuevo_registro])
        st.session_state.historial_df = pd.concat([st.session_state.historial_df, df_nuevo], ignore_index=True)
        st.session_state.historial_df.to_csv(archivo_historial, index=False)
        
        st.success(f"¡Vuelta registrada en {cuenta_activa} con éxito! Actualiza la página.")
        st.balloons()

st.markdown("---")
st.markdown("### 📂 REGISTRO DE MOVIMIENTOS")
with st.expander("Haz clic aquí para ver o eliminar tus movimientos registrados"):
    if not st.session_state.historial_df.empty:
        df_mostrar = st.session_state.historial_df[['Día', 'Cuenta', 'USD_Comprados', 'USDT_Vendidos', 'Tasa_Venta', 'Ganancia_Bs', 'ROI']].tail(10).sort_index(ascending=False)
        st.dataframe(df_mostrar, use_container_width=True)
        
        st.markdown("#### ⚙️ Gestión de Datos")
        col_del1, col_del2 = st.columns(2)
        with col_del1:
            if st.button("🗑️ Borrar Última Vuelta", use_container_width=True):
                # Elimina de la memoria y rescribe el CSV
                st.session_state.historial_df = st.session_state.historial_df.iloc[:-1]
                st.session_state.historial_df.to_csv(archivo_historial, index=False)
                st.success("Última vuelta eliminada. ¡Actualiza la página para ver los cambios!")
        with col_del2:
            if st.button("🚨 Borrar TODO el Historial", use_container_width=True):
                # Limpia la memoria y borra el archivo
                st.session_state.historial_df = pd.DataFrame(columns=columnas_historial)
                if os.path.exists(archivo_historial):
                    os.remove(archivo_historial)
                st.success("Historial reseteado por completo. ¡Actualiza la página!")
    else:
        st.info("Aún no hay operaciones registradas.")
        
