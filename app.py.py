import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time # Import necesario para el timing del efecto

st.set_page_config(page_title="Team Arbitraje", layout="wide", initial_sidebar_state="collapsed")

# --- CSS Y JAVASCRIPT PARA EL EFECTO DE PARTÍCULAS (CANVAS) ---
st.markdown("""<style>.block-container{padding-top:3.5rem!important;padding-bottom:1rem!important}.main{background-color:#0f172a;color:#e2e8f0;font-family:sans-serif}h1,h2,h3,h4,p,label,.stMarkdown{color:#f8fafc!important;font-weight:700!important}h1{font-size:1.5rem!important;margin-bottom:0!important;padding-bottom:0!important}h3{font-size:1.1rem!important;margin-top:.5rem!important;margin-bottom:.1rem!important}hr{margin-top:.5rem!important;margin-bottom:.8rem!important;border-color:rgba(255,255,255,.05)!important}.stNumberInput div div input{color:#38bdf8!important;background-color:rgba(15,23,42,.8)!important;border:2px solid #334155!important;border-radius:8px;font-weight:900!important;font-size:15px!important;text-align:center;padding:4px!important;height:34px!important}.stNumberInput div div input:focus{border-color:#38bdf8!important;box-shadow:0 0 8px rgba(56,189,248,.2)!important}.dashboard-panel,.radar-box{background:linear-gradient(135deg,rgba(30,41,59,.8),rgba(15,23,42,.9));backdrop-filter:blur(12px);padding:12px 15px!important;border-radius:12px;border:1px solid rgba(255,255,255,.05);margin-bottom:10px!important;box-shadow:0 4px 15px rgba(0,0,0,.4)}div[data-testid="stMetric"]{background:linear-gradient(145deg,#1e293b,#0f172a)!important;padding:6px 10px!important;border-radius:10px;border:1px solid rgba(56,189,248,.2)!important;box-shadow:0 2px 10px rgba(0,0,0,.2)}div[data-testid="stMetricValue"]{font-size:1.2rem!important;font-weight:900!important;color:#38bdf8!important;text-shadow:0 0 5px rgba(56,189,248,.3)}div[data-testid="stMetricLabel"] p{font-weight:800!important;color:#94a3b8!important;font-size:11px!important;margin-bottom:0!important}.highlight-action{background:linear-gradient(135deg,#fef08a,#facc15);padding:6px;border-radius:8px;color:#000;text-align:center;font-size:15px;font-weight:900;margin-bottom:5px;border:1px dashed #854d0e}.summary-box{background:linear-gradient(135deg,rgba(15,23,42,.95),rgba(30,41,59,.98));border-radius:16px;padding:18px;border:1px solid rgba(56,189,248,.4);box-shadow:0 8px 25px rgba(0,0,0,.5);margin-top:20px;margin-bottom:15px}.summary-header{text-align:center;color:#facc15;font-size:16px;font-weight:900;border-bottom:1px dashed rgba(255,255,255,.2);padding-bottom:10px;margin-bottom:15px}.summary-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}.summary-item{background:rgba(0,0,0,.25);padding:12px;border-radius:10px;text-align:center;border:1px solid rgba(255,255,255,.05)}.summary-item-full{grid-column:span 2;background:linear-gradient(to right,rgba(16,185,129,.1),rgba(15,23,42,.5));border:1px solid rgba(16,185,129,.4);padding:15px;border-radius:12px;text-align:center}.sum-label{font-size:11px;color:#94a3b8;font-weight:800;margin-bottom:4px;display:block}.sum-val{font-size:15px;color:#e2e8f0;font-weight:900}.sum-val.highlight{color:#38bdf8;font-size:17px}.sum-val.success{color:#10b981;font-size:22px;text-shadow:0 0 10px rgba(16,185,129,.3)}
</style>
""", unsafe_allow_html=True)

# Placeholder para inyectar el efecto JavaScript
effect_placeholder = st.empty()

# Función JavaScript para el efecto de Canvas (Partículas de Éxito)
js_particle_effect = """
<div id="arb-effect-container" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:999999;">
    <canvas id="arb-canvas"></canvas>
</div>
<script>
(function() {
    const canvas = document.getElementById('arb-canvas');
    const ctx = canvas.getContext('2d');
    const container = document.getElementById('arb-effect-container');
    
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;
    
    const particles = [];
    # Usamos colores dorados y cianes de nuestro tema
    const colors = ['#facc15', '#38bdf8', '#10b981', '#ffffff']; 

    class Particle {
        constructor() {
            this.x = width / 2;
            this.y = height / 2; // Empieza en el centro
            this.vx = (Math.random() - 0.5) * 15; // Velocidad explosiva
            this.vy = (Math.random() - 0.5) * 15;
            this.gravity = 0.15;
            this.radius = Math.random() * 4 + 2;
            this.color = colors[Math.floor(Math.random() * colors.length)];
            this.alpha = 1;
            this.decay = Math.random() * 0.015 + 0.005;
        }
        update() {
            this.vx *= 0.99; // Fricción aire
            this.vy += this.gravity;
            this.x += this.vx;
            this.y += this.vy;
            this.alpha -= this.decay;
        }
        draw() {
            ctx.globalAlpha = this.alpha;
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    for (let i = 0; i < 70; i++) { // Cantidad de partículas
        particles.push(new Particle());
    }

    function animate() {
        requestAnimationFrame(animate);
        ctx.clearRect(0, 0, width, height); // Limpiar canvas transparente
        
        particles.forEach((p, index) => {
            if (p.alpha > 0) {
                p.update();
                p.draw();
            } else {
                particles.splice(index, 1);
            }
        });
        
        // Auto-destruir el contenedor si no hay partículas
        if (particles.length === 0) {
            container.remove();
        }
    }
    animate();
})();
</script>
"""

st.markdown("<h1 style='text-align:center;color:#38bdf8!important;'>🚀 RUTA DIRECTA (BDV)</h1><div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

hoy_str, mes_str = datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m")
archivo_historial = "historial_directo.csv"
cols_h = ['Fecha','Día','Mes','Cuenta','Cap_Invertido_Bs','USD_Comprados','USDT_Vendidos','Tasa_Venta','Bs_Recibidos','Ganancia_Bs','ROI']

if 'historial_df' not in st.session_state:
    if os.path.exists(archivo_historial):
        df_t = pd.read_csv(archivo_historial)
        for c in cols_h:
            if c not in df_t.columns: df_t[c] = 0.0
        st.session_state.historial_df = df_t
    else:
        st.session_state.historial_df = pd.DataFrame(columns=cols_h)

df_h = st.session_state.historial_df
cuentas_lista = [f"Cuenta {i}" for i in range(1, 7)]
cuenta_activa = st.session_state.get('cuenta_activa', cuentas_lista[0])

# Inicializar flag de animación si no existe
if 'ejecutar_animacion' not in st.session_state:
    st.session_state.ejecutar_animacion = False

# --- Lógica de inyección del efecto ---
if st.session_state.ejecutar_animacion:
    effect_placeholder.markdown(js_particle_effect, unsafe_allow_html=True)
    st.session_state.ejecutar_animacion = False # Resetear flag inmediatamente
    # No hacemos rerun aquí para dejar que la animación corra en JS 
    # mientras el resto de la página carga.

df_hoy = df_h[(df_h['Cuenta']==cuenta_activa)&(df_h['Día']==hoy_str)]
df_mes = df_h[(df_h['Cuenta']==cuenta_activa)&(df_h['Mes']==mes_str)]
c_dia = max(0, 2000 - (df_hoy['USD_Comprados'].sum() if not df_hoy.empty else 0))
c_mes = max(0, 10000 - (df_mes['USD_Comprados'].sum() if not df_mes.empty else 0))
vueltas = len(df_hoy)
gan_acum = df_hoy['Ganancia_Bs'].sum() if not df_hoy.empty else 0
gan_tot = df_h[df_h['Día']==hoy_str]['Ganancia_Bs'].sum() if not df_h.empty else 0

st.markdown(f"<div class='dashboard-panel'><p style='text-align:center;margin:0;font-size:13px;color:#94a3b8;'>🎛️ PANEL DE CONTROL</p><p style='text-align:center;font-size:12px;margin:4px 0;'>Vueltas Hoy: <b style='color:#10b981;'>{vueltas}</b> | Día: <span style='color:#38bdf8;'>${c_dia:,.0f}</span> | Mes: <span style='color:#38bdf8;'>${c_mes:,.0f}</span></p><p style='text-align:center;font-size:13px;margin:0;'>Ganancia: <span style='color:#16a34a;'>Bs.{gan_acum:,.2f}</span> | 🌍 GLOBAL: <span style='color:#facc15;'>Bs.{gan_tot:,.2f}</span></p></div>", unsafe_allow_html=True)
st.session_state.cuenta_activa = st.selectbox("💳 Cuenta:", cuentas_lista, index=cuentas_lista.index(cuenta_activa), label_visibility="collapsed")

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
        st.info(f"💵 Compraste: **${usd_banco:,.2f}**")
    else:
        usd_banco = st.number_input("Monto (USD)", value=100.00, step=10.0)
        cap_bs = usd_banco*tasa_real_b
        st.info(f"🇻🇪 Fondeo: **Bs.{cap_bs:,.2f}**")

    st.markdown("<h3 style='margin:0;'>2️⃣ Recarga Tarjeta</h3>", unsafe_allow_html=True)
    dej_usd = st.checkbox("Dejar $1 holgura", value=True)
    usd_base = max(0.0, (usd_banco-1) if dej_usd else usd_banco)
    sug_tarj = usd_base * 0.975
    st.markdown(f"<div class='highlight-action'>⚠️ TECLEAR EN APP:<br><span style='font-size:22px;'>${sug_tarj:,.2f}</span></div>", unsafe_allow_html=True)
    conf_tarj = st.number_input("👉 Confirma monto app:", value=float(f"{sug_tarj:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;'>3️⃣ Recibido Binance</h3>", unsafe_allow_html=True)
    sug_bin = conf_tarj * 0.967
    conf_usdt = st.number_input(f"👉 USDT acreditados (≈₮{sug_bin:,.2f}):", value=float(f"{sug_bin:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;'>4️⃣ Venta P2P</h3>", unsafe_allow_html=True)
    usdt_vend = st.number_input("USDT a Vender:", value=float(conf_usdt), step=1.0)
    sug_bs_rec = usdt_vend * tasa_v
    conf_bs_rec = st.number_input(f"👉 Bs. Recibidos (≈Bs.{sug_bs_rec:,.2f}):", value=float(f"{sug_bs_rec:.2f}"), step=100.0)

    g_bs = conf_bs_rec - cap_bs
    g_usdt = g_bs/tasa_v if tasa_v>0 else 0
    roi = (g_bs/cap_bs)*100 if cap_bs>0 else 0
    brecha = ((tasa_v/tasa_real_b)-1)*100 if tasa_real_b>0 else 0
    h_cap, h_usd, h_usdt, h_bs = cap_bs, usd_banco, usdt_vend, conf_bs_rec
else:
    st.markdown("<h3 style='margin:0;'>1️⃣ Venta Inicial P2P</h3>", unsafe_allow_html=True)
    usdt_ini = st.number_input("USDT Iniciales:", value=100.00, step=1.0)
    sug_bs_inv = usdt_ini * tasa_v
    conf_bs_inv = st.number_input(f"👉 Bs. Recibidos (≈Bs.{sug_bs_inv:,.2f}):", value=float(f"{sug_bs_inv:.2f}"), step=100.0)

    st.markdown("<h3 style='margin:0;'>2️⃣ Fondeo BDV (Re-inversión)</h3>", unsafe_allow_html=True)
    bs_inv = st.number_input("Bs. para comprar USD:", value=float(conf_bs_inv), step=100.0)
    usd_banco_inv = bs_inv/tasa_real_b if tasa_real_b>0 else 0
    st.info(f"💵 Compraste: **${usd_banco_inv:,.2f}**")

    st.markdown("<h3 style='margin:0;'>3️⃣ Recarga Tarjeta</h3>", unsafe_allow_html=True)
    dej_usd = st.checkbox("Dejar $1 holgura", value=True)
    usd_base_inv = max(0.0, (usd_banco_inv-1) if dej_usd else usd_banco_inv)
    sug_tarj_inv = usd_base_inv * 0.975
    st.markdown(f"<div class='highlight-action'>⚠️ TECLEAR EN APP:<br><span style='font-size:22px;'>${sug_tarj_inv:,.2f}</span></div>", unsafe_allow_html=True)
    conf_tarj_inv = st.number_input("👉 Confirma monto app:", value=float(f"{sug_tarj_inv:.2f}"), step=1.0)

    st.markdown("<h3 style='margin:0;'>4️⃣ USDT Recuperados</h3>", unsafe_allow_html=True)
    sug_bin_inv = conf_tarj_inv * 0.967
    usdt_fin = st.number_input(f"👉 USDT recuperados (≈₮{sug_bin_inv:,.2f}):", value=float(f"{sug_bin_inv:.2f}"), step=1.0)

    g_usdt = usdt_fin - usdt_ini
    g_bs = g_usdt * tasa_v
    roi = (g_usdt/usdt_ini)*100 if usdt_ini>0 else 0
    brecha = ((tasa_v/tasa_real_b)-1)*100 if tasa_real_b>0 else 0
    h_cap, h_usd, h_usdt, h_bs = bs_inv, usd_banco_inv, usdt_ini, conf_bs_inv
    usd_banco = usd_banco_inv

c_bs_teo = h_cap
u_base_teo = max(0.0, (usd_banco-1) if dej_usd else usd_banco)
u_fin_teo = u_base_teo * 0.975 * 0.967
t_sug = (c_bs_teo*1.02)/u_fin_teo if u_fin_teo>0 else 0
bs_rec_teo = u_fin_teo * tasa_v
g_bs_teo = bs_rec_teo - c_bs_teo
g_u_teo = g_bs_teo/tasa_v if tasa_v>0 else 0
roi_teo = (g_bs_teo/c_bs_teo)*100 if c_bs_teo>0 else 0
c_roi = '#ef4444' if roi_teo<2 else '#10b981'

radar_placeholder.markdown(f"<div style='background:linear-gradient(135deg,rgba(16,185,129,.1),rgba(15,23,42,.6));border:1px solid rgba(16,185,129,.3);padding:12px;border-radius:12px;margin:5px 0 15px;'><p style='margin:0;font-size:11px;color:#94a3b8;'>🔍 PROYECCIÓN P2P (Basado en ${usd_banco:,.2f})</p><div style='display:flex;justify-content:space-between;margin-top:5px;'><div><p style='margin:0;font-size:13px;color:#e2e8f0;'>🎯 Sugerida(2%): <b style='color:#facc15;'>Bs.{t_sug:,.2f}</b></p><p style='margin:0;font-size:13px;'>📊 ROI: <b style='color:{c_roi};'>{roi_teo:,.2f}%</b></p></div><div style='text-align:right;'><p style='margin:0;font-size:10px;color:#94a3b8;'>GANANCIA</p><p style='margin:0;font-size:16px;font-weight:900;color:#38bdf8;'>Bs.{g_bs_teo:,.2f}</p><p style='margin:0;font-size:13px;color:#10b981;'>≈₮{g_u_teo:,.2f}</p></div></div></div>", unsafe_allow_html=True)

st.markdown("<hr style='margin-bottom:8px;'>", unsafe_allow_html=True)
r1, r2, r3 = st.columns(3)
r1.markdown(f"<div data-testid='stMetric'><p style='font-size:11px;color:#94a3b8;margin:0;font-weight:800;'>GANANCIA NETA</p><div style='display:flex;gap:6px;margin-top:2px;'><span style='font-size:18px;color:#38bdf8;font-weight:900;'>Bs.{g_bs:,.2f}</span><span style='font-size:13px;color:#10b981;font-weight:800;'>₮{g_usdt:,.2f}</span></div></div>", unsafe_allow_html=True)
r2.metric("ROI REAL", f"{roi:.2f}%")
r3.metric("BRECHA", f"{brecha:.2f}%")

df_h_g = df_h[df_h['Día']==hoy_str].copy()
if not df_h_g.empty:
    v_tot, c_us = len(df_h_g), df_h_g['Cuenta'].nunique()
    n_c = ", ".join(df_h_g['Cuenta'].str.replace('Cuenta','#').unique())
    p_t, p_roi, g_tot_bs = df_h_g['Tasa_Venta'].mean(), df_h_g['ROI'].mean(), df_h_g['Ganancia_Bs'].sum()
    g_tot_u = (df_h_g['Ganancia_Bs']/df_h_g['Tasa_Venta']).sum()
    v_usd = df_h_g['USD_Comprados'].sum()
else:
    v_tot, c_us, n_c, p_t, p_roi, g_tot_bs, g_tot_u, v_usd = 0,0,"N/A",0,0,0,0,0

st.markdown(f"<div class='summary-box'><div class='summary-header'>🏆 RESUMEN GLOBAL DEL DÍA</div><div class='summary-grid'><div class='summary-item'><span class='sum-label'>🔄 Vueltas</span><span class='sum-val'>{v_tot} <span style='font-size:11px;'>({n_c})</span></span></div><div class='summary-item'><span class='sum-label'>💸 Volumen Movido</span><span class='sum-val highlight'>${v_usd:,.2f}</span></div><div class='summary-item'><span class='sum-label'>📈 Tasa Promedio</span><span class='sum-val'>Bs.{p_t:,.2f}</span></div><div class='summary-item'><span class='sum-label'>🚀 ROI Promedio</span><span class='sum-val' style='color:{'#10b981' if p_roi>=2 else '#ef4444'};'>{p_roi:,.2f}%</span></div><div class='summary-item-full'><span class='sum-label' style='color:#38bdf8;'>💰 GANANCIA TOTAL HOY</span><div style='display:flex;justify-content:center;gap:10px;'><span class='sum-val success'>Bs.{g_tot_bs:,.2f}</span><span style='color:#e2e8f0;font-weight:900;'>≈₮{g_tot_u:,.2f}</span></div></div></div></div>", unsafe_allow_html=True)

if st.button("💾 GUARDAR VUELTA", use_container_width=True):
    if usd_banco>c_dia or usd_banco>c_mes: st.error(f"❌ Supera límites de {cuenta_activa}.")
    else:
        # 1. Preparar datos
        nr = pd.DataFrame([{"Fecha":datetime.now().strftime("%Y-%m-%d %H:%M"),"Día":hoy_str,"Mes":mes_str,"Cuenta":cuenta_activa,"Cap_Invertido_Bs":h_cap,"USD_Comprados":h_usd,"USDT_Vendidos":h_usdt,"Tasa_Venta":tasa_v,"Bs_Recibidos":h_bs,"Ganancia_Bs":g_bs,"ROI":roi}])
        
        # 2. Guardar persistentemente
        st.session_state.historial_df = pd.concat([st.session_state.historial_df, nr], ignore_index=True)
        st.session_state.historial_df.to_csv(archivo_historial, index=False)
        
        # 3. ACTIVAR FLAG DE ANIMACIÓN
        st.session_state.ejecutar_animacion = True
        
        # 4. Feedback y Rerun (El rerun activará la inyección del JS)
        st.success(f"¡Vuelta registrada en {cuenta_activa}!")
        time.sleep(0.5) # Pequeña pausa para que lean el éxito antes del refresh
        st.rerun()

with st.expander("📂 VER HISTORIAL"):
    if not st.session_state.historial_df.empty:
        st.dataframe(st.session_state.historial_df[['Día','Cuenta','USD_Comprados','Ganancia_Bs','ROI']].tail(10).sort_index(ascending=False), use_container_width=True)
        cd1, cd2 = st.columns(2)
        with cd1:
            if st.button("🗑️ Borrar Última", use_container_width=True):
                st.session_state.historial_df = st.session_state.historial_df.iloc[:-1]
                st.session_state.historial_df.to_csv(archivo_historial, index=False)
                st.rerun()
        with cd2:
            if st.button("🚨 Borrar TODO", use_container_width=True):
                st.session_state.historial_df = pd.DataFrame(columns=cols_h)
                if os.path.exists(archivo_historial): os.remove(archivo_historial)
                st.rerun()
    
