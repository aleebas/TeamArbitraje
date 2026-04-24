import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time

st.set_page_config(page_title="Team Arbitraje", layout="wide", initial_sidebar_state="collapsed")

# --- CSS ADAPTATIVO (MODO BLANCO Y OSCURO) ---
st.markdown("""<style>
.block-container{padding-top:3.5rem!important;padding-bottom:1rem!important}
h1,h2,h3,h4,p,label,.stMarkdown{font-weight:700!important}
.dashboard-panel, .summary-box {
    background-color: var(--secondary-background-color);
    padding: 15px!important;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.2);
    margin-bottom: 10px!important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.stNumberInput div div input {
    background-color: var(--background-color)!important;
    color: var(--text-color)!important;
    border: 2px solid rgba(128,128,128,0.3)!important;
    border-radius: 8px;
    font-weight: 900!important;
    font-size: 15px!important;
    text-align: center;
    padding: 4px!important;
    height: 34px!important;
}
.stNumberInput div div input:focus { border-color: #0ea5e9!important; }
.highlight-action { background-color: #fef08a; padding:6px; border-radius:8px; color:#854d0e; text-align:center; font-size:15px; font-weight:900; margin-bottom:5px; border:1px dashed #ca8a04; }
.highlight-celeste { background-color: #e0f2fe; padding:6px; border-radius:8px; color:#0369a1; text-align:center; font-size:15px; font-weight:900; margin-bottom:5px; border:1px dashed #0284c7; }
.progress-bg { background-color: rgba(128,128,128,0.2); border-radius: 10px; width: 100%; height: 10px; margin-top: 4px; overflow: hidden; }
.progress-fill-day { background-color: #0ea5e9; height: 100%; }
.progress-fill-month { background-color: #a855f7; height: 100%; }
.summary-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.summary-item { background: rgba(128,128,128,0.05); padding: 12px; border-radius: 10px; text-align: center; border: 1px solid rgba(128,128,128,0.1); }
.summary-item-full { grid-column: span 2; background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.4); padding: 15px; border-radius: 12px; text-align: center; }
.breakdown-row { display:flex; justify-content:space-between; font-size:14px; margin-bottom:6px; padding: 4px 8px; background: rgba(128,128,128,0.05); border-radius: 6px; }
</style>""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;color:#0ea5e9!important;'>🚀 RUTA DIRECTA</h1><div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

# Lógica de Fechas y Ciclos
hoy = datetime.now()
hoy_str = hoy.strftime("%Y-%m-%d")

if hoy.day >= 6:
    inicio_ciclo = datetime(hoy.year, hoy.month, 6)
else:
    if hoy.month == 1: inicio_ciclo = datetime(hoy.year - 1, 12, 6)
    else: inicio_ciclo = datetime(hoy.year, hoy.month - 1, 6)
inicio_ciclo_str = inicio_ciclo.strftime("%Y-%m-%d")

archivo_historial = "historial_directo.csv"
carpeta_backups = "Backups_Diarios"
if not os.path.exists(carpeta_backups): os.makedirs(carpeta_backups)

cols_h = ['Fecha','Día','Mes_Ciclo','Cuenta','Cap_Invertido_Bs','USD_Comprados','USDT_Vendidos','Tasa_Venta','Bs_Recibidos','Ganancia_Bs','ROI']

# Lectura blindada
if 'historial_df' not in st.session_state:
    if os.path.exists(archivo_historial):
        try:
            df_t = pd.read_csv(archivo_historial, dtype=str)
            cols_num = ['Cap_Invertido_Bs','USD_Comprados','USDT_Vendidos','Tasa_Venta','Bs_Recibidos','Ganancia_Bs','ROI']
            for c in cols_h:
                if c not in df_t.columns: 
                    df_t[c] = '0.0' if c in cols_num else ''
            for c in cols_num:
                df_t[c] = pd.to_numeric(df_t[c], errors='coerce').fillna(0.0)
            st.session_state.historial_df = df_t
        except Exception:
            st.session_state.historial_df = pd.DataFrame(columns=cols_h)
    else:
        st.session_state.historial_df = pd.DataFrame(columns=cols_h)

df_h = st.session_state.historial_df
cuentas_lista = [f"Cuenta {i}" for i in range(1, 7)]

cuenta_activa_previa = st.session_state.get('cuenta_activa', cuentas_lista[0])
st.markdown("<p style='font-size:13px; color:#6b7280; margin:0 0 5px 5px; font-weight:800;'>💳 SELECCIONAR CUENTA:</p>", unsafe_allow_html=True)
cuenta_activa = st.selectbox("Cuenta", cuentas_lista, index=cuentas_lista.index(cuenta_activa_previa), label_visibility="collapsed")
st.session_state.cuenta_activa = cuenta_activa

# Cálculos
df_hoy = df_h[(df_h['Cuenta']==cuenta_activa) & (df_h['Día']==hoy_str)]
df_mes = df_h[(df_h['Cuenta']==cuenta_activa) & (df_h['Mes_Ciclo']==inicio_ciclo_str)]

consumo_dia = df_hoy['USD_Comprados'].sum() if not df_hoy.empty else 0
consumo_mes = df_mes['USD_Comprados'].sum() if not df_mes.empty else 0

c_dia = max(0, 7000 - consumo_dia)
c_mes = max(0, 10000 - consumo_mes)
pct_dia = min(100, (consumo_dia/7000)*100)
pct_mes = min(100, (consumo_mes/10000)*100)

vueltas = len(df_hoy)
gan_acum = df_hoy['Ganancia_Bs'].sum() if not df_hoy.empty else 0
gan_tot = df_h[df_h['Día']==hoy_str]['Ganancia_Bs'].sum() if not df_h.empty else 0

# --- PANEL DE CONTROL (Consumo / Disp) ---
st.markdown(f"""
<div class='dashboard-panel'>
    <p style='text-align:center;margin:0 0 10px 0;font-size:14px;color:#6b7280;font-weight:900;'>🎛️ PANEL DE CONTROL ({cuenta_activa})</p>
    <div style='display:flex;justify-content:space-between;margin-bottom:10px;'>
        <div style='width:48%;'>
            <p style='margin:0;font-size:12px;color:var(--text-color);'>Diario ($7K): <b style='color:#0ea5e9;'>${consumo_dia:,.0f} / Disp. ${c_dia:,.0f}</b></p>
            <div class='progress-bg'><div class='progress-fill-day' style='width:{pct_dia}%;'></div></div>
        </div>
        <div style='width:48%;'>
            <p style='margin:0;font-size:12px;color:var(--text-color);'>Ciclo ($10K): <b style='color:#a855f7;'>${consumo_mes:,.0f} / Disp. ${c_mes:,.0f}</b></p>
            <div class='progress-bg'><div class='progress-fill-month' style='width:{pct_mes}%;'></div></div>
        </div>
    </div>
    <p style='text-align:center;font-size:13px;margin:10px 0 0 0;color:var(--text-color);'>
        Vueltas: <b style='color:#10b981;'>{vueltas}</b> | 
        Ganancia Cta: <span style='color:#10b981;'>Bs.{gan_acum:,.2f}</span> | 
        🌍 GLOBAL: <span style='color:#f59e0b;'>Bs.{gan_tot:,.2f}</span>
    </p>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: tasa_c = st.number_input("📉 Tasa Compra BDV", value=570.75, step=0.01)
with c2: tasa_v = st.number_input("📈 Tasa Venta P2P", value=648.00, step=0.01)
tasa_real_b = tasa_c * 1.005

radar_placeholder = st.empty()
st.markdown("<hr>", unsafe_allow_html=True)

tipo_v = st.radio("🔄 Dirección:", ["➡️ Normal", "⬅️ Inversa"], horizontal=True)

if tipo_v == "➡️ Normal":
    st.markdown("<h3 style='margin:0;'>1️⃣ Fondeo BDV</h3>", unsafe_allow_html=True)
    t_ing = st.radio("Ingreso en:", ["Bs", "USD"], horizontal=True, label_visibility="collapsed")
    if t_ing == "Bs":
        cap_bs = st.number_input("Monto (Bs.)", value=57360.00, step=100.0)
        usd_banco = cap_bs/tasa_real_b if tasa_real_b>0 else 0
        st.markdown(f"<div class='highlight-celeste'>💵 COMPRASTE:<br><span style='font-size:22px;'>${usd_banco:,.2f}</span></div>", unsafe_allow_html=True)
    else:
        usd_banco = st.number_input("Monto (USD)", value=100.00, step=10.0)
        cap_bs = usd_banco*tasa_real_b
        st.markdown(f"<div class='highlight-celeste'>🇻🇪 FONDEO NECESARIO:<br><span style='font-size:22px;'>Bs.{cap_bs:,.2f}</span></div>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin:0;'>2️⃣ Recarga Tarjeta</h3>", unsafe_allow_html=True)
    dej_usd = st.checkbox("Dejar $0.30 holgura (Fallas)", value=True)
    usd_base = max(0.0, (usd_banco-0.30) if dej_usd else usd_banco)
    sug_tarj = usd_base * 0.975
    st.markdown(f"<div class='highlight-action'>⚠️ TECLEAR EN APP:<br><span style='font-size:22px;'>${sug_tarj:,.2f}</span></div>", unsafe_allow_html=True)
    conf_tarj = st.number_input("👉 Confirma monto app:", value=float(f"{sug_tarj:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;'>3️⃣ Recibido Binance</h3>", unsafe_allow_html=True)
    sug_bin = conf_tarj * 0.967
    conf_usdt = st.number_input(f"👉 USDT acreditados reales (≈₮{sug_bin:,.2f}):", value=float(f"{sug_bin:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;'>4️⃣ Venta P2P</h3>", unsafe_allow_html=True)
    usdt_vend = st.number_input("USDT a Vender:", value=float(conf_usdt), step=1.0)
    sug_bs_rec = usdt_vend * tasa_v
    conf_bs_rec = st.number_input(f"👉 Bs. Recibidos (≈Bs.{sug_bs_rec:,.2f}):", value=float(f"{sug_bs_rec:.2f}"), step=100.0)

    g_bs = conf_bs_rec - cap_bs
    g_usdt = g_bs/tasa_v if tasa_v>0 else 0
    roi = (g_bs/cap_bs)*100 if cap_bs>0 else 0
    h_cap, h_usd, h_usdt, h_bs = cap_bs, usd_banco, usdt_vend, conf_bs_rec
else:
    st.markdown("<h3 style='margin:0;'>1️⃣ Venta Inicial P2P</h3>", unsafe_allow_html=True)
    usdt_ini = st.number_input("USDT Iniciales:", value=100.00, step=1.0)
    sug_bs_inv = usdt_ini * tasa_v
    conf_bs_inv = st.number_input(f"👉 Bs. Recibidos (≈Bs.{sug_bs_inv:,.2f}):", value=float(f"{sug_bs_inv:.2f}"), step=100.0)

    st.markdown("<h3 style='margin:0;'>2️⃣ Fondeo BDV (Re-inversión)</h3>", unsafe_allow_html=True)
    bs_inv = st.number_input("Bs. para comprar USD:", value=float(conf_bs_inv), step=100.0)
    usd_banco_inv = bs_inv/tasa_real_b if tasa_real_b>0 else 0
    st.markdown(f"<div class='highlight-celeste'>💵 COMPRASTE:<br><span style='font-size:22px;'>${usd_banco_inv:,.2f}</span></div>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin:0;'>3️⃣ Recarga Tarjeta</h3>", unsafe_allow_html=True)
    dej_usd = st.checkbox("Dejar $0.30 holgura (Fallas)", value=True)
    usd_base_inv = max(0.0, (usd_banco_inv-0.30) if dej_usd else usd_banco_inv)
    sug_tarj_inv = usd_base_inv * 0.975
    st.markdown(f"<div class='highlight-action'>⚠️ TECLEAR EN APP:<br><span style='font-size:22px;'>${sug_tarj_inv:,.2f}</span></div>", unsafe_allow_html=True)
    conf_tarj_inv = st.number_input("👉 Confirma monto app:", value=float(f"{sug_tarj_inv:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;'>4️⃣ USDT Recuperados</h3>", unsafe_allow_html=True)
    sug_bin_inv = conf_tarj_inv * 0.967
    usdt_fin = st.number_input(f"👉 USDT recuperados (≈₮{sug_bin_inv:,.2f}):", value=float(f"{sug_bin_inv:.2f}"), step=1.0)

    g_usdt = usdt_fin - usdt_ini
    g_bs = g_usdt * tasa_v
    roi = (g_usdt/usdt_ini)*100 if usdt_ini>0 else 0
    h_cap, h_usd, h_usdt, h_bs = bs_inv, usd_banco_inv, usdt_ini, conf_bs_inv
    usd_banco = usd_banco_inv

c_bs_teo = h_cap
u_base_teo = max(0.0, (usd_banco-0.30) if dej_usd else usd_banco)
u_fin_teo = u_base_teo * 0.975 * 0.967
t_sug = (c_bs_teo*1.02)/u_fin_teo if u_fin_teo>0 else 0
bs_rec_teo = u_fin_teo * tasa_v
g_bs_teo = bs_rec_teo - c_bs_teo
g_u_teo = g_bs_teo/tasa_v if tasa_v>0 else 0
roi_teo = (g_bs_teo/c_bs_teo)*100 if c_bs_teo>0 else 0
c_roi = '#ef4444' if roi_teo<2 else '#10b981'

radar_placeholder.markdown(f"<div style='background:linear-gradient(135deg,rgba(16,185,129,.1),var(--secondary-background-color));border:1px solid rgba(16,185,129,.3);padding:12px;border-radius:12px;margin:5px 0 15px;'><p style='margin:0;font-size:11px;color:#6b7280;'>🔍 PROYECCIÓN P2P (Basado en ${usd_banco:,.2f})</p><div style='display:flex;justify-content:space-between;margin-top:5px;'><div><p style='margin:0;font-size:13px;color:var(--text-color);'>🎯 Sugerida(2%): <b style='color:#f59e0b;'>Bs.{t_sug:,.2f}</b></p><p style='margin:0;font-size:13px;color:var(--text-color);'>📊 ROI Teórico: <b style='color:{c_roi};'>{roi_teo:,.2f}%</b></p></div><div style='text-align:right;'><p style='margin:0;font-size:10px;color:#6b7280;'>GANANCIA</p><p style='margin:0;font-size:16px;font-weight:900;color:#0ea5e9;'>Bs.{g_bs_teo:,.2f}</p><p style='margin:0;font-size:13px;color:#10b981;'>≈₮{g_u_teo:,.2f}</p></div></div></div>", unsafe_allow_html=True)

# Lógica del Resumen Global (incluyendo el desglose por cuentas)
df_h_g = df_h[df_h['Día']==hoy_str].copy()

breakdown_html = ""
if not df_h_g.empty:
    v_tot = len(df_h_g)
    n_c = ", ".join(df_h_g['Cuenta'].str.replace('Cuenta','#').unique())
    p_t = df_h_g['Tasa_Venta'].mean()
    p_roi = df_h_g['ROI'].mean()
    g_tot_bs = df_h_g['Ganancia_Bs'].sum()
    g_tot_u = (df_h_g['Ganancia_Bs']/df_h_g['Tasa_Venta']).sum()
    v_usd = df_h_g['USD_Comprados'].sum()
    
    # Construcción del HTML para el desglose por cuentas
    breakdown_html += "<div style='margin-top:15px; border-top:1px dashed rgba(128,128,128,0.2); padding-top:12px;'>"
    breakdown_html += "<p style='text-align:center; font-size:11px; color:#6b7280; font-weight:800; margin-bottom:8px;'>📊 DESGLOSE POR CUENTA (HOY)</p>"
    
    agrupado = df_h_g.groupby('Cuenta')[['USD_Comprados', 'Ganancia_Bs']].sum().reset_index()
    for _, row in agrupado.iterrows():
        cta = row['Cuenta'].replace('Cuenta ', '#')
        vol = row['USD_Comprados']
        gan = row['Ganancia_Bs']
        breakdown_html += f"<div class='breakdown-row'><span style='color:var(--text-color); font-weight:800;'>Cta. {cta}</span><span style='color:#0ea5e9; font-weight:800;'>Vol: ${vol:,.0f}</span><span style='color:#10b981; font-weight:800;'>Gan: Bs.{gan:,.2f}</span></div>"
    breakdown_html += "</div>"
    
else:
    v_tot, n_c, p_t, p_roi, g_tot_bs, g_tot_u, v_usd = 0, "N/A", 0, 0, 0, 0, 0

# Inyección del Resumen Global
st.markdown(f"<div class='summary-box'><div class='summary-header'>🏆 RESUMEN GLOBAL DEL DÍA</div><div class='summary-grid'><div class='summary-item'><span style='font-size:11px;color:#6b7280;font-weight:800;display:block;'>🔄 Vueltas</span><span style='font-size:15px;color:var(--text-color);font-weight:900;'>{v_tot} <span style='font-size:11px;'>({n_c})</span></span></div><div class='summary-item'><span style='font-size:11px;color:#6b7280;font-weight:800;display:block;'>💸 Volumen Movido</span><span style='color:#0ea5e9;font-size:17px;font-weight:900;'>${v_usd:,.2f}</span></div><div class='summary-item'><span style='font-size:11px;color:#6b7280;font-weight:800;display:block;'>📈 Tasa Promedio</span><span style='font-size:15px;color:var(--text-color);font-weight:900;'>Bs.{p_t:,.2f}</span></div><div class='summary-item'><span style='font-size:11px;color:#6b7280;font-weight:800;display:block;'>🚀 ROI Promedio</span><span style='font-size:15px;font-weight:900;color:{'#10b981' if p_roi>=2 else '#ef4444'};'>{p_roi:,.2f}%</span></div><div class='summary-item-full'><span style='font-size:11px;color:#0ea5e9;font-weight:800;display:block;margin-bottom:4px;'>💰 GANANCIA TOTAL HOY</span><div style='display:flex;justify-content:center;gap:10px;'><span style='color:#10b981;font-size:22px;font-weight:900;'>Bs.{g_tot_bs:,.2f}</span><span style='color:var(--text-color);font-weight:900;font-size:15px;align-self:center;'>≈₮{g_tot_u:,.2f}</span></div></div></div>{breakdown_html}</div>", unsafe_allow_html=True)

if st.button("💾 GUARDAR VUELTA", use_container_width=True):
    if (consumo_dia + h_usd) > 7000: 
        st.error(f"❌ ¡ATENCIÓN! Esta operación excede tu límite diario de $7,000 para la {cuenta_activa}.")
    elif (consumo_mes + h_usd) > 10000:
        st.error(f"❌ ¡ATENCIÓN! Esta operación excede tu límite del ciclo mensual de $10,000 para la {cuenta_activa}.")
    else:
        nr = pd.DataFrame([{"Fecha":datetime.now().strftime("%Y-%m-%d %H:%M"),"Día":hoy_str,"Mes_Ciclo":inicio_ciclo_str,"Cuenta":cuenta_activa,"Cap_Invertido_Bs":h_cap,"USD_Comprados":h_usd,"USDT_Vendidos":h_usdt,"Tasa_Venta":tasa_v,"Bs_Recibidos":h_bs,"Ganancia_Bs":g_bs,"ROI":roi}])
        st.session_state.historial_df = pd.concat([st.session_state.historial_df, nr], ignore_index=True)
        st.session_state.historial_df.to_csv(archivo_historial, index=False)
        
        archivo_diario = os.path.join(carpeta_backups, f"historial_{hoy_str}.csv")
        df_diario = st.session_state.historial_df[st.session_state.historial_df['Día'] == hoy_str]
        df_diario.to_csv(archivo_diario, index=False)
        
        st.toast(f"¡Vuelta registrada en {cuenta_activa}! 💸", icon="✅")
        st.balloons() 
        time.sleep(2) 
        st.rerun()

with st.expander("📅 CENTRO DE RÉCORDS Y AUDITORÍA"):
    st.markdown("<p style='font-size:13px;color:#6b7280;'>Consulta tus movimientos históricos guardados.</p>", unsafe_allow_html=True)
    if not st.session_state.historial_df.empty:
        df_view = st.session_state.historial_df.copy()
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filtro_fecha = st.selectbox("Filtrar por Fecha:", ["Todas"] + list(df_view['Día'].unique())[::-1])
        with col_f2:
            filtro_cuenta = st.selectbox("Filtrar por Cuenta:", ["Todas"] + cuentas_lista)
            
        if filtro_fecha != "Todas": df_view = df_view[df_view['Día'] == filtro_fecha]
        if filtro_cuenta != "Todas": df_view = df_view[df_view['Cuenta'] == filtro_cuenta]
        
        st.dataframe(df_view[['Fecha','Cuenta','USD_Comprados','Ganancia_Bs','ROI']].sort_index(ascending=False), use_container_width=True)
        
        if not df_view.empty:
            t_usd_view = df_view['USD_Comprados'].sum()
            t_gan_view = df_view['Ganancia_Bs'].sum()
            p_roi_view = df_view['ROI'].mean()
            
            st.markdown(f"""
            <div style='display:flex; justify-content:space-around; background-color: var(--secondary-background-color); padding:15px; border-radius:12px; border:1px dashed #0ea5e9; margin-top:15px; margin-bottom:15px;'>
                <div style='text-align:center;'>
                    <span style='font-size:10px;color:#6b7280;font-weight:800;display:block;margin-bottom:2px;'>VOLUMEN (USD)</span>
                    <span style='font-size:18px;color:#0ea5e9;font-weight:900;'>${t_usd_view:,.2f}</span>
                </div>
                <div style='text-align:center; border-left:1px solid rgba(128,128,128,0.2); border-right:1px solid rgba(128,128,128,0.2); padding:0 15px;'>
                    <span style='font-size:10px;color:#6b7280;font-weight:800;display:block;margin-bottom:2px;'>GANANCIA NETA</span>
                    <span style='font-size:18px;color:#10b981;font-weight:900;'>Bs.{t_gan_view:,.2f}</span>
                </div>
                <div style='text-align:center;'>
                    <span style='font-size:10px;color:#6b7280;font-weight:800;display:block;margin-bottom:2px;'>ROI PROMEDIO</span>
                    <span style='font-size:18px;color:#f59e0b;font-weight:900;'>{p_roi_view:,.2f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color:rgba(128,128,128,0.2);'>", unsafe_allow_html=True)
        cd1, cd2 = st.columns(2)
        with cd1:
            if st.button("🗑️ Borrar Última Vuelta", use_container_width=True):
                st.session_state.historial_df = st.session_state.historial_df.iloc[:-1]
                st.session_state.historial_df.to_csv(archivo_historial, index=False)
                archivo_diario = os.path.join(carpeta_backups, f"historial_{hoy_str}.csv")
                df_diario = st.session_state.historial_df[st.session_state.historial_df['Día'] == hoy_str]
                if not df_diario.empty: 
                    df_diario.to_csv(archivo_diario, index=False)
                st.rerun()
        with cd2:
            if st.button("🚨 Reiniciar Base de Datos", use_container_width=True):
                st.session_state.historial_df = pd.DataFrame(columns=cols_h)
                if os.path.exists(archivo_historial): os.remove(archivo_historial)
                st.rerun()
    else:
        st.info("No hay registros en el historial todavía.")
