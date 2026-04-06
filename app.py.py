import streamlit as st
import pandas as pd
from datetime import datetime
import os

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
    .radar-box { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #3b82f6; border-left: 5px solid #3b82f6; margin-top: 15px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# Comienzo limpio directamente con el título y separador
st.markdown("<h2 style='text-align: center;'>🚀 RUTA DIRECTA</h2><hr style='margin-bottom: 15px;'>", unsafe_allow_html=True)

# Lógica de Cupo y Récords Diario MULTI-CUENTA
hoy_str = datetime.now().strftime("%Y-%m-%d")
mes_str = datetime.now().strftime("%Y-%m")
archivo_historial = "historial_directo.csv"

# Leer historial con compatibilidad para cuentas viejas
if os.path.exists(archivo_historial):
    df_h = pd.read_csv(archivo_historial)
    if 'Cuenta' not in df_h.columns:
        df_h['Cuenta'] = 'Cuenta 1'
    if 'Mes' not in df_h.columns:
        df_h['Mes'] = mes_str
else:
    df_h = pd.DataFrame(columns=['Fecha', 'Día', 'Mes', 'Cuenta', 'USD_Comprados', 'Ganancia_Bs', 'ROI'])

# SIDEBAR: Selector de Cuenta
cuentas_lista = [f"Cuenta {i}" for i in range(1, 7)]
st.sidebar.header("💳 GESTIÓN DE CUENTAS")
cuenta_activa = st.sidebar.selectbox("Seleccionar Cuenta Activa:", cuentas_lista)

# Filtrar datos de la cuenta seleccionada
df_cuenta_hoy = df_h[(df_h['Cuenta'] == cuenta_activa) & (df_h['Día'] == hoy_str)]
df_cuenta_mes = df_h[(df_h['Cuenta'] == cuenta_activa) & (df_h['Mes'] == mes_str)]

cupo_dia_usado = df_cuenta_hoy['USD_Comprados'].sum() if not df_cuenta_hoy.empty else 0.0
cupo_mes_usado = df_cuenta_mes['USD_Comprados'].sum() if not df_cuenta_mes.empty else 0.0

mejor_vuelta = df_cuenta_hoy['Ganancia_Bs'].max() if not df_cuenta_hoy.empty else 0.0
ganancia_acumulada = df_cuenta_hoy['Ganancia_Bs'].sum() if not df_cuenta_hoy.empty else 0.0
vueltas_hoy = len(df_cuenta_hoy)

cupo_diario_restante = 2000 - cupo_dia_usado
cupo_mensual_restante = 10000 - cupo_mes_usado

# SIDEBAR: Control de Cupo y Récord de la Cuenta Activa
st.sidebar.markdown(f"### 🛡️ LÍMITES - {cuenta_activa.upper()}")
st.sidebar.metric("Cupo Diario Libre", f"$ {cupo_diario_restante:,.2f}")
st.sidebar.progress(min(cupo_dia_usado / 2000, 1.0))

st.sidebar.metric("Cupo Mensual Libre", f"$ {cupo_mensual_restante:,.2f}")
st.sidebar.progress(min(cupo_mes_usado / 10000, 1.0))

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏆 RÉCORD DE HOY")
st.sidebar.metric("🔄 Vueltas Completadas", vueltas_hoy)
st.sidebar.metric("💰 Ganancia Acumulada", f"Bs. {ganancia_acumulada:,.2f}")
st.sidebar.metric("🔥 Mejor Vuelta", f"Bs. {mejor_vuelta:,.2f}")

# Comisiones Fijas
c_tarjeta = 0.025 # 2.5%
c_binance = 0.033 # 3.3%

# INPUTS: Banco y Tasas 
banco = st.selectbox("🏦 Banco Origen:", ["BDV", "BANCAMIGA"])
col_t1, col_t2 = st.columns(2)
with col_t1:
    tasa_c = st.number_input("📉 Tasa Compra (Base)", value=570.75, format="%.2f", step=0.01)
with col_t2:
    tasa_v = st.number_input("📈 Tasa Venta P2P", value=648.00, format="%.2f", step=0.01)

# Cálculo de tasa real de compra
c_asig = 0.005 if banco == "BDV" else 0.008
tasa_real_b = tasa_c * (1 + c_asig)

# Entrada de Capital Bidireccional
st.markdown("### 💱 Capital a Invertir")
tipo_ingreso = st.radio("Ingresar monto en:", ["Bolívares (Bs)", "Dólares (USD)"], horizontal=True, label_visibility="collapsed")

if tipo_ingreso == "Bolívares (Bs)":
    cap_bs = st.number_input("Monto Invertido (Bs.)", value=57360.00, format="%.2f", step=100.0)
    usd_en_banco = cap_bs / tasa_real_b if tasa_real_b > 0 else 0
    st.success(f"💵 Capital convertido: **$ {usd_en_banco:,.2f}** disponibles en {banco}.")
else:
    usd_en_banco = st.number_input("Monto Invertido (USD)", value=441.00, format="%.2f", step=10.0)
    cap_bs = usd_en_banco * tasa_real_b
    st.success(f"🇻🇪 Capital requerido: **Bs. {cap_bs:,.2f}** para fondear {banco}.")

# LÓGICA DE NEGOCIO EN CASCADA
st.markdown("### 🧮 Simulación en Cascada")
dejar_dolar = st.checkbox("Dejar $1 en la cuenta por seguridad", value=True)

# Matematicas
usd_base = (usd_en_banco - 1.0) if dejar_dolar else usd_en_banco
usd_base = max(0.0, usd_base)
usd_post_tarjeta = usd_base * (1 - c_tarjeta)
usdt_finales = usd_post_tarjeta * (1 - c_binance)

gan_bs = (usdt_finales * tasa_v) - cap_bs
roi = (gan_bs / cap_bs) * 100 if cap_bs > 0 else 0
brecha = ((tasa_v / tasa_real_b) - 1) * 100 if tasa_real_b > 0 else 0

# ALERTA DINÁMICA DE PUNTO DE EQUILIBRIO
tasa_minima_venta = cap_bs / usdt_finales if usdt_finales > 0 else 0

if tasa_v <= tasa_minima_venta:
    st.error(f"🚨 **¡ALERTA DE PÉRDIDA!** Estás trabajando para pagar comisiones. Para recuperar tu inversión debes vender a **MÁS de Bs. {tasa_minima_venta:,.2f}**.")
elif tasa_v < (tasa_minima_venta * 1.015): 
    st.warning(f"⚠️ **¡CUIDADO!** Tu margen de ganancia es muy ajustado. Recuerda que tu tasa mínima sin pérdidas es **Bs. {tasa_minima_venta:,.2f}**.")

# RADAR DE INTERÉS COMPUESTO (NUEVA FUNCIONALIDAD)
if usd_en_banco > 0 and roi > 0:
    capital_simulado = usd_en_banco
    cupo_disponible_sim = cupo_diario_restante
    vueltas_posibles = 0
    
    while capital_simulado <= cupo_disponible_sim:
        vueltas_posibles += 1
        cupo_disponible_sim -= capital_simulado
        capital_simulado = capital_simulado * (1 + (roi/100)) # Crece por el interés compuesto
    
    # Lo que queda para la "vuelta partida"
    excedente = capital_simulado - cupo_disponible_sim
    
    html_radar = f"""
    <div class="radar-box">
        <h4 style="margin-top:0; color:#3b82f6;">🔄 Radar de Interés Compuesto ({cuenta_activa})</h4>
        <p style="margin:5px 0;">Con tu cupo libre de <b>$ {cupo_diario_restante:,.2f}</b> y un margen del <b>{roi:.2f}%</b>:</p>
        <ul style="margin-bottom:0;">
            <li>Puedes dar <b>{vueltas_posibles} vueltas completas</b> re-invirtiendo todo el capital.</li>
            <li>En la vuelta #{vueltas_posibles + 1}, solo podrás pasar <b>$ {cupo_disponible_sim:,.2f}</b> por esta cuenta.</li>
            <li>Tendrás un excedente de <b style="color:#f59e0b;">$ {excedente:,.2f}</b> que deberás pasar a la siguiente cuenta para no frenar la bola de nieve.</li>
        </ul>
    </div>
    """
    st.markdown(html_radar, unsafe_allow_html=True)

# Panel visual del descuento
st.info(f"""
1️⃣ **Fondo Total Disponible:** $ {usd_en_banco:,.2f} \n
2️⃣ **Monto a pasar por Tarjeta:** $ {usd_base:,.2f} \n
3️⃣ **Neto tras Tarjeta (-2.5%):** $ {usd_post_tarjeta:,.2f} \n
4️⃣ **Final en Binance (-3.3%):** ₮ {usdt_finales:,.2f}
""")

st.markdown("### 📊 Rendimiento de esta Vuelta")
res1, res2, res3 = st.columns(3)

# Métrica inline preservada
gan_usdt = gan_bs / tasa_v if tasa_v != 0 else 0

with res1:
    st.markdown(f"""
    <div data-testid="stMetric" style="background-color: #1e293b !important; padding: 10px; border-radius: 12px; border: 1px solid #334155 !important;">
        <p style="font-weight: 800 !important; color: #94a3b8 !important; font-size: 14px !important; text-transform: uppercase; margin: 0;">GANANCIA NETA</p>
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

# Guardar en Historial
st.markdown("<br>", unsafe_allow_html=True)
if st.button("💾 GUARDAR VUELTA", use_container_width=True):
    if usd_en_banco > cupo_diario_restante:
        st.error(f"❌ No puedes guardar esta vuelta. Supera el límite diario de la {cuenta_activa}.")
    else:
        nuevo_registro = {
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), 
            "Día": hoy_str,
            "Mes": mes_str,
            "Cuenta": cuenta_activa,
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
        st.success(f"¡Vuelta registrada en {cuenta_activa} con éxito! Actualiza para ver el Récord.")
        st.balloons()
