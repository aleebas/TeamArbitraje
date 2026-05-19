import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Team Arbitraje", layout="wide", initial_sidebar_state="collapsed")

# --- CSS APLANADO (Cero errores) ---
st.markdown("<style>.block-container{padding-top:2rem!important;padding-bottom:1rem!important} h1,h2,h3,h4,p,label,.stMarkdown{font-weight:700!important} .dashboard-panel, .summary-box {background-color: var(--secondary-background-color); padding: 15px!important; border-radius: 12px; border: 1px solid rgba(128,128,128,0.2); margin-bottom: 10px!important; box-shadow: 0 4px 15px rgba(0,0,0,0.05);} .stNumberInput div div input {background-color: var(--background-color)!important; color: var(--text-color)!important; border: 2px solid rgba(128,128,128,0.3)!important; border-radius: 8px; font-weight: 900!important; font-size: 15px!important; text-align: center; padding: 4px!important; height: 34px!important;} .stNumberInput div div input:focus { border-color: #0ea5e9!important; } .highlight-action { background-color: #fef08a; padding:6px; border-radius:8px; color:#854d0e; text-align:center; font-size:15px; font-weight:900; margin-bottom:5px; border:1px dashed #ca8a04; } .highlight-celeste { background-color: #e0f2fe; padding:6px; border-radius:8px; color:#0369a1; text-align:center; font-size:15px; font-weight:900; margin-bottom:5px; border:1px dashed #0284c7; } div[data-testid='stMetric']{background-color: var(--secondary-background-color); padding: 6px 10px!important; border-radius: 10px; border: 1px solid rgba(128,128,128,0.2)!important;}</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;color:#0ea5e9!important;'>🚀 RUTA DIRECTA V2</h1><div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

# --- INICIALIZAR REGISTRO DIARIO (Sin Historial CSV) ---
if 'registro_diario' not in st.session_state:
    st.session_state.registro_diario = pd.DataFrame(columns=['Ruta', 'Capital_Inicial', 'USDT_Recibidos', 'Tasa_Venta', 'Ganancia_Bs', 'Ganancia_USDT', 'ROI'])

# --- PANEL DE CONFIGURACIÓN GLOBAL ---
c1, c2 = st.columns(2)
with c1: tasa_c = st.number_input("📉 Tasa Compra BCV/Banco", value=611.00, step=0.01)
with c2: tasa_v = st.number_input("📈 Tasa Venta P2P", value=648.00, step=0.01)

st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)

# --- SELECTORES DE RUTA Y COMISIONES ---
col_b, col_t, col_p = st.columns(3)
with col_b:
    banco = st.radio("🏦 Banco Origen:", ["BDV (0.5%)", "Bancamiga (0.8%)"])
    tasa_asignacion = 1.005 if "BDV" in banco else 1.008

with col_t:
    if "BDV" in banco:
        tarjeta = st.radio("💳 Tarjeta Uso:", ["Física (1.5%) - $1K", "Digital (2.5%) - $2K"])
        factor_tarjeta = 0.985 if "Física" in tarjeta else 0.975
        limite_tarj = 1000 if "Física" in tarjeta else 2000
    else:
        tarjeta = st.radio("💳 Tarjeta Uso:", ["Única (5.0%) - $2.5K"])
        factor_tarjeta = 0.950
        limite_tarj = 2500

with col_p:
    plataforma = st.radio("🌐 Plataforma Destino:", ["Binance (3.6%)", "KONTIGO (Prueba 1%)"])
    factor_plat = 0.964 if "Binance" in plataforma else 0.990

tasa_real_b = tasa_c * tasa_asignacion

if "KONTIGO" in plataforma:
    st.warning("⚠️ KONTIGO está en fase de pruebas. El cálculo es una estimación del 1% sin fijo.")

radar_placeholder = st.empty()
st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)

# --- FLUJO DE CÁLCULO ---
tipo_v = st.radio("🔄 Dirección de los Fondos:", ["➡️ Normal (Bs a USDT)", "⬅️ Inversa (USDT a Bs)"], horizontal=True)

if "Normal" in tipo_v:
    st.markdown("<h3 style='margin:0;color:#0ea5e9;'>1️⃣ Fondeo de Cuenta</h3>", unsafe_allow_html=True)
    t_ing = st.radio("Disponibilidad Inicial en:", ["Bs", "USD"], horizontal=True, label_visibility="collapsed")
    
    if t_ing == "Bs":
        cap_bs = st.number_input("Monto Inicial (Bs.)", value=61100.00, step=100.0)
        usd_banco = cap_bs / tasa_real_b if tasa_real_b > 0 else 0
        st.markdown(f"<div class='highlight-celeste'>💵 SE COMPRAN:<br><span style='font-size:22px;'>${usd_banco:,.2f} USD</span></div>", unsafe_allow_html=True)
    else:
        usd_banco = st.number_input("Monto Inicial a Comprar (USD)", value=100.00, step=10.0)
        cap_bs = usd_banco * tasa_real_b
        st.markdown(f"<div class='highlight-celeste'>🇻🇪 REQUIERES FONDEAR:<br><span style='font-size:22px;'>Bs.{cap_bs:,.2f}</span></div>", unsafe_allow_html=True)

    if usd_banco > 0:
        vueltas_sug = math.ceil((limite_tarj * 0.98) / usd_banco) # Ajuste sutil para no rozar el límite exacto
        st.markdown(f"<p style='text-align:center; font-size:11.5px; color:#6b7280; margin-top:-3px; margin-bottom:12px;'>💡 <b>Sugerencia Límite:</b> {vueltas_sug} vueltas aprox. para agotar el cupo de ${limite_tarj}.</p>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin:0;color:#0ea5e9;'>2️⃣ Recarga y Consumo de Tarjeta</h3>", unsafe_allow_html=True)
    holgura = st.number_input("Dejar holgura (USD) - Recomendado $0.10 a $0.30", value=0.10, step=0.10)
    usd_base = max(0.0, usd_banco - holgura)
    
    sug_tarj = usd_base * factor_tarjeta
    st.markdown(f"<div class='highlight-action'>⚠️ TECLEAR EN APP (RASPAR):<br><span style='font-size:22px;'>${sug_tarj:,.2f}</span></div>", unsafe_allow_html=True)
    conf_tarj = st.number_input("👉 Confirma el monto exacto raspado:", value=float(f"{sug_tarj:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;color:#0ea5e9;'>3️⃣ Recibido en Plataforma P2P</h3>", unsafe_allow_html=True)
    sug_bin = conf_tarj * factor_plat
    conf_usdt = st.number_input(f"👉 Confirma USDT Reales Acreditados (Teórico: ₮{sug_bin:,.2f}):", value=float(f"{sug_bin:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;color:#0ea5e9;'>4️⃣ Venta P2P Final</h3>", unsafe_allow_html=True)
    usdt_vend = st.number_input("USDT exactos a Vender:", value=float(conf_usdt), step=1.0)
    sug_bs_rec = usdt_vend * tasa_v
    conf_bs_rec = st.number_input(f"👉 Confirma Bs. Reales Recibidos (Teórico: Bs.{sug_bs_rec:,.2f}):", value=float(f"{sug_bs_rec:.2f}"), step=100.0)

    g_bs = conf_bs_rec - cap_bs
    g_usdt = g_bs / tasa_v if tasa_v > 0 else 0
    roi = (g_bs / cap_bs) * 100 if cap_bs > 0 else 0
    h_cap = cap_bs

else:
    st.markdown("<h3 style='margin:0;color:#0ea5e9;'>1️⃣ Venta Inicial P2P (Punto de Partida)</h3>", unsafe_allow_html=True)
    usdt_ini = st.number_input("USDT Iniciales que vendes:", value=100.00, step=1.0)
    sug_bs_inv = usdt_ini * tasa_v
    conf_bs_inv = st.number_input(f"👉 Bs. Recibidos de la venta (Teórico: Bs.{sug_bs_inv:,.2f}):", value=float(f"{sug_bs_inv:.2f}"), step=100.0)

    st.markdown("<h3 style='margin:0;color:#0ea5e9;'>2️⃣ Fondeo y Compra en Banco</h3>", unsafe_allow_html=True)
    bs_inv = st.number_input("Bs. que usarás para comprar USD:", value=float(conf_bs_inv), step=100.0)
    usd_banco = bs_inv / tasa_real_b if tasa_real_b > 0 else 0
    st.markdown(f"<div class='highlight-celeste'>💵 SE COMPRAN:<br><span style='font-size:22px;'>${usd_banco:,.2f} USD</span></div>", unsafe_allow_html=True)
    
    if usd_banco > 0:
        vueltas_sug = math.ceil((limite_tarj * 0.98) / usd_banco)
        st.markdown(f"<p style='text-align:center; font-size:11.5px; color:#6b7280; margin-top:-3px; margin-bottom:12px;'>💡 <b>Sugerencia Límite:</b> {vueltas_sug} vueltas aprox. para agotar el cupo de ${limite_tarj}.</p>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin:0;color:#0ea5e9;'>3️⃣ Recarga y Consumo de Tarjeta</h3>", unsafe_allow_html=True)
    holgura = st.number_input("Dejar holgura (USD) - Recomendado $0.10 a $0.30", value=0.10, step=0.10)
    usd_base_inv = max(0.0, usd_banco - holgura)
    
    sug_tarj_inv = usd_base_inv * factor_tarjeta
    st.markdown(f"<div class='highlight-action'>⚠️ TECLEAR EN APP (RASPAR):<br><span style='font-size:22px;'>${sug_tarj_inv:,.2f}</span></div>", unsafe_allow_html=True)
    conf_tarj_inv = st.number_input("👉 Confirma el monto exacto raspado:", value=float(f"{sug_tarj_inv:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;color:#0ea5e9;'>4️⃣ Recuperación en Plataforma P2P</h3>", unsafe_allow_html=True)
    sug_bin_inv = conf_tarj_inv * factor_plat
    usdt_fin = st.number_input(f"👉 Confirma USDT Reales Recuperados (Teórico: ₮{sug_bin_inv:,.2f}):", value=float(f"{sug_bin_inv:.2f}"), step=1.0)

    g_usdt = usdt_fin - usdt_ini
    g_bs = g_usdt * tasa_v
    roi = (g_usdt / usdt_ini) * 100 if usdt_ini > 0 else 0
    h_cap = bs_inv

# --- RADAR DE PROYECCIÓN P2P DINÁMICO ---
u_base_teo = max(0.0, usd_banco - holgura)
u_fin_teo = u_base_teo * factor_tarjeta * factor_plat
t_sug = (h_cap * 1.02) / u_fin_teo if u_fin_teo > 0 else 0
bs_rec_teo = u_fin_teo * tasa_v
g_bs_teo = bs_rec_teo - h_cap
g_u_teo = g_bs_teo / tasa_v if tasa_v > 0 else 0
roi_teo = (g_bs_teo / h_cap) * 100 if h_cap > 0 else 0
c_roi = '#ef4444' if roi_teo < 2 else '#10b981'

ruta_detallada_radar = f"{banco} ➡️ {tarjeta.split(' -')[0]} ➡️ {plataforma}"

# AQUÍ SE INTEGRA LA TASA DE COMPRA Y VENTA DIRECTO EN EL RADAR
radar_html = f"<div style='background-color: var(--secondary-background-color); border:1px solid rgba(16,185,129,.3); padding:12px; border-radius:12px; margin:5px 0 15px;'><p style='margin:0;font-size:11px;color:#6b7280;'>🔍 RADAR PROYECTIVO (Monto Base: Bs. {h_cap:,.2f} | ${usd_banco:,.2f})</p><p style='margin:0;font-size:10px;color:#a855f7;font-weight:800;margin-bottom:8px;'>⚙️ MÉTODO: {ruta_detallada_radar}</p><div style='display:flex; justify-content:space-between; margin-bottom:8px; border-bottom:1px dashed rgba(128,128,128,0.2); padding-bottom:5px;'><span style='font-size:11px; color:#6b7280;'>📉 Compra: <b style='color:var(--text-color);'>Bs.{tasa_c:,.2f}</b></span><span style='font-size:11px; color:#6b7280;'>📈 Venta P2P: <b style='color:var(--text-color);'>Bs.{tasa_v:,.2f}</b></span></div><div style='display:flex;justify-content:space-between;margin-top:5px;'><div><p style='margin:0;font-size:13px;color:var(--text-color);'>🎯 Tasa sugerida (2%): <b style='color:#f59e0b;'>Bs.{t_sug:,.2f}</b></p><p style='margin:0;font-size:13px;color:var(--text-color);'>📊 ROI Teórico: <b style='color:{c_roi};'>{roi_teo:,.2f}%</b></p></div><div style='text-align:right;'><p style='margin:0;font-size:10px;color:#6b7280;'>GANANCIA PROYECTADA</p><p style='margin:0;font-size:16px;font-weight:900;color:#0ea5e9;'>Bs.{g_bs_teo:,.2f}</p><p style='margin:0;font-size:13px;color:#10b981;'>≈₮{g_u_teo:,.2f}</p></div></div></div>"
radar_placeholder.markdown(radar_html, unsafe_allow_html=True)

# --- MÉTRICAS FINALES REALES Y GUARDADO ---
st.markdown("<hr style='margin-bottom:8px; border-color:rgba(128,128,128,0.2);'>", unsafe_allow_html=True)
r1, r2 = st.columns(2)
r1.markdown(f"<div data-testid='stMetric'><p style='font-size:11px;color:#6b7280;margin:0;font-weight:800;'>GANANCIA NETA REAL CONFIRMADA</p><div style='display:flex;gap:6px;margin-top:2px;'><span style='font-size:18px;color:#0ea5e9;font-weight:900;'>Bs.{g_bs:,.2f}</span><span style='font-size:13px;color:#10b981;font-weight:800;'>₮{g_usdt:,.2f}</span></div></div>", unsafe_allow_html=True)
r2.metric("ROI REAL", f"{roi:.2f}%")

if st.button("💾 GUARDAR ESTA VUELTA EN EL RESUMEN DEL DÍA", use_container_width=True):
    etiqueta_ruta = f"{banco[:3]} + {tarjeta.split(' ')[0]} -> {plataforma.split(' ')[0]}"
    nueva_vuelta = pd.DataFrame([{
        'Ruta': etiqueta_ruta,
        'Capital_Inicial': h_cap,
        'USDT_Recibidos': conf_usdt if "Normal" in tipo_v else usdt_fin,
        'Tasa_Venta': tasa_v,
        'Ganancia_Bs': g_bs,
        'Ganancia_USDT': g_usdt,
        'ROI': roi
    }])
    st.session_state.registro_diario = pd.concat([st.session_state.registro_diario, nueva_vuelta], ignore_index=True)
    st.balloons()
    st.success("¡Vuelta agregada a la tabla de hoy!")

# --- RESUMEN DEL DÍA (PARA CAPTURA) ---
st.markdown("<div style='margin-top:30px;'></div><h2 style='text-align:center; color:#a855f7;'>📸 RESUMEN DEL DÍA</h2>", unsafe_allow_html=True)

df_resumen = st.session_state.registro_diario

if not df_resumen.empty:
    st.dataframe(df_resumen.style.format({
        'Capital_Inicial': 'Bs.{:,.2f}',
        'USDT_Recibidos': '₮{:,.2f}',
        'Tasa_Venta': 'Bs.{:,.2f}',
        'Ganancia_Bs': 'Bs.{:,.2f}',
        'Ganancia_USDT': '₮{:,.2f}',
        'ROI': '{:,.2f}%'
    }), use_container_width=True)
    
    tot_bs = df_resumen['Ganancia_Bs'].sum()
    tot_usdt = df_resumen['Ganancia_USDT'].sum()
    avg_roi = df_resumen['ROI'].mean()
    
    st.markdown(f"""
    <div style='display:flex; justify-content:space-around; background-color: var(--secondary-background-color); padding:15px; border-radius:12px; border:1px dashed #a855f7; margin-top:10px;'>
        <div style='text-align:center;'>
            <span style='font-size:10px;color:#6b7280;font-weight:800;display:block;'>TOTAL VUELTAS</span>
            <span style='font-size:18px;color:#e2e8f0;font-weight:900;'>{len(df_resumen)}</span>
        </div>
        <div style='text-align:center; border-left:1px solid rgba(128,128,128,0.2); border-right:1px solid rgba(128,128,128,0.2); padding:0 15px;'>
            <span style='font-size:10px;color:#6b7280;font-weight:800;display:block;'>GANANCIA TOTAL HOY</span>
            <span style='font-size:18px;color:#10b981;font-weight:900;'>Bs.{tot_bs:,.2f} <span style='font-size:14px;color:#0ea5e9;'> (≈₮{tot_usdt:,.2f})</span></span>
        </div>
        <div style='text-align:center;'>
            <span style='font-size:10px;color:#6b7280;font-weight:800;display:block;'>ROI PROMEDIO</span>
            <span style='font-size:18px;color:#f59e0b;font-weight:900;'>{avg_roi:,.2f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚨 BORRAR REGISTRO Y EMPEZAR NUEVO DÍA", use_container_width=True):
        st.session_state.registro_diario = pd.DataFrame(columns=['Ruta', 'Capital_Inicial', 'USDT_Recibidos', 'Tasa_Venta', 'Ganancia_Bs', 'Ganancia_USDT', 'ROI'])
        st.rerun()
else:
    st.info("Aún no has guardado ninguna vuelta hoy. Registra tus movimientos para generar la tabla.")
    
