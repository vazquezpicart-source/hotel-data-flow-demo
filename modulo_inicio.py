# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

def modulo_inicio():

    st.title("🏨 Hotel Data Flow – Inicio")
    st.write("")

    # ============================================================
    # MENÚ SUPERIOR
    # ============================================================
    menu = st.columns(6)

    with menu[0]:
        if st.button("🏠 Inicio", key="menu_inicio", use_container_width=True):
            st.session_state.pagina = "inicio"
            st.rerun()

    with menu[1]:
        if st.button("📊 Reservas", key="menu_reservas", use_container_width=True):
            st.session_state.pagina = "reservas"
            st.rerun()

    with menu[2]:
        if st.button("👤 Clientes", key="menu_clientes", use_container_width=True):
            st.session_state.pagina = "clientes"
            st.rerun()

    with menu[3]:
        st.button("🛏️ Habitaciones", key="menu_habitaciones", disabled=True, use_container_width=True)

    with menu[4]:
        if st.button("📦 Almacén", key="menu_almacen", use_container_width=True):
            st.session_state.pagina = "almacen"
            st.rerun()

    with menu[5]:
        if st.button("📈 Marketing", key="menu_marketing", use_container_width=True):
            st.session_state.pagina = "marketing"
            st.rerun()

    st.divider()

    # ============================================================
    # 2. HERO BANNER PROFESIONAL
    # ============================================================

    st.markdown("""
<div style='text-align:center; padding: 20px 0 10px 0;'>

<h1 style='margin-bottom: 0; font-size: 42px;'>
    🏨 Hotel Data Flow
</h1>

<h3 style='margin-top: 5px; color: #4A4A4A; font-weight: 400;'>
    El PMS modular para hoteles pequeños y medianos
</h3>

<p style='font-size: 18px; color: #6A6A6A; max-width: 700px; margin: 10px auto;'>
    Gestión de reservas, clientes, operaciones y análisis en un solo lugar.
    Ligero, escalable y diseñado para el día a día real de un hotel.
</p>

</div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin-top: 0;'>", unsafe_allow_html=True)
    st.divider()

    # ============================================================
    # 1. DASHBOARD AVANZADO
    # ============================================================
    st.header("📊 Dashboard avanzado")

    df = st.session_state.df_global.copy()

    # Conversión de fechas
    df["llegada"] = pd.to_datetime(df["llegada"], errors="coerce")
    df["salida"] = pd.to_datetime(df["salida"], errors="coerce")

    hoy = pd.Timestamp.today().normalize()

    # -----------------------------
    # KPIs principales
    # -----------------------------
    ocupadas = df[df["estado"].str.contains("ocupada", case=False, na=False)]
    total_habitaciones = df["habitacion"].nunique() or 1
    ocupacion = len(ocupadas) / total_habitaciones * 100

    adr = df["precio"].mean()
    revpar = adr * (ocupacion / 100)
    pickup_hoy = len(df[df["llegada"] == hoy])
    estancia_media = df["noches"].mean()
    ingresos_totales = df["precio"].sum()

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric("🏨 Ocupación", f"{ocupacion:.1f}%")
    col2.metric("💶 ADR", f"{adr:.2f} €")
    col3.metric("📈 RevPAR", f"{revpar:.2f} €")
    col4.metric("🟦 Pick‑up hoy", pickup_hoy)
    col5.metric("🛌 Estancia media", f"{estancia_media:.1f} noches")
    col6.metric("💰 Ingresos totales", f"{ingresos_totales:.2f} €")

    # ============================================================
    # 3. ÚLTIMAS RESERVAS
    # ============================================================
    st.header("🧾 Últimas reservas")

    # Ordenar por llegada descendente
    ultimas = df.sort_values("llegada", ascending=False).head(5)

    if ultimas.empty:
        st.info("No hay reservas registradas todavía.")
    else:
        for _, fila in ultimas.iterrows():
            with st.container(border=True):
                st.markdown(f"""
                **{fila['nombre']} {fila['apellido1']}**  
                🛏️ Habitación: **{fila['habitacion']}**  
                📅 {fila['llegada'].date()} → {fila['salida'].date()}  
                💶 {fila['precio']} € — {fila['tarifa']}  
                🌐 Canal: {fila['canal']}
                """)

    # ============================================================
    # 4. TAREAS PENDIENTES
    # ============================================================
    st.header("📝 Tareas pendientes")

    tareas = [
        {"texto": "Revisar habitaciones pendientes de limpieza", "icono": "🧹"},
        {"texto": "Confirmar llegadas de hoy", "icono": "🟦"},
        {"texto": "Enviar emails de pre‑check‑in", "icono": "📧"},
        {"texto": "Actualizar precios del fin de semana", "icono": "💶"},
        {"texto": "Revisar disponibilidad para OTA", "icono": "🌐"},
    ]

    for i, tarea in enumerate(tareas):
        with st.container(border=True):
            st.checkbox(f"{tarea['icono']} {tarea['texto']}", key=f"tarea_{i}")

    # ============================================================
    # 5. RESUMEN DEL DÍA
    # ============================================================
    st.header("📅 Resumen del día")

    # Filtrar check‑ins y check‑outs
    checkins = df[df["llegada"] == hoy]
    checkouts = df[df["salida"] == hoy]

    # Habitaciones sucias (si existe la columna estado)
    if "estado" in df.columns:
        sucias = df[df["estado"].str.contains("sucia", case=False, na=False)]
    else:
        sucias = pd.DataFrame()

    colA, colB, colC = st.columns(3)

    # -----------------------------
    # Check‑ins
    # -----------------------------
    with colA:
        st.subheader("🟦 Check‑ins de hoy")
        if checkins.empty:
            st.info("No hay check‑ins programados.")
        else:
            for _, fila in checkins.iterrows():
                with st.container(border=True):
                    st.write(f"**{fila['nombre']} {fila['apellido1']}**")
                    st.write(f"Hab. {fila['habitacion']} — {fila['tarifa']}")

    # -----------------------------
    # Check‑outs
    # -----------------------------
    with colB:
        st.subheader("🟥 Check‑outs de hoy")
        if checkouts.empty:
            st.info("No hay check‑outs programados.")
        else:
            for _, fila in checkouts.iterrows():
                with st.container(border=True):
                    st.write(f"**{fila['nombre']} {fila['apellido1']}**")
                    st.write(f"Hab. {fila['habitacion']} — {fila['tarifa']}")

    # -----------------------------
    # Habitaciones sucias
    # -----------------------------
    with colC:
        st.subheader("🧹 Habitaciones sucias")
        if sucias.empty:
            st.success("No hay habitaciones sucias.")
        else:
            for _, fila in sucias.iterrows():
                with st.container(border=True):
                    st.write(f"Hab. **{fila['habitacion']}**")
                    st.write("Pendiente de limpieza")


    st.divider()

    # -----------------------------
    # Ingresos por canal
    # -----------------------------
    st.subheader("🌐 Ingresos por canal")
    canales = df.groupby("canal")["precio"].sum()
    st.bar_chart(canales)

    st.divider()

    # -----------------------------
    # Ocupación por tipo de habitación
    # -----------------------------
    st.subheader("🛏️ Ocupación por tipo de habitación")
    ocupacion_tipo = df.groupby("habitacion")["estado"].apply(
        lambda x: (x.str.contains("ocupada", case=False, na=False).sum() / len(x)) * 100
    )
    st.bar_chart(ocupacion_tipo)

    st.divider()

    # -----------------------------
    # Forecast 7 días
    # -----------------------------
    st.subheader("📅 Forecast próximos 7 días")
    forecast_7 = df[df["llegada"].between(hoy, hoy + pd.Timedelta(days=7))]
    st.line_chart(forecast_7.groupby("llegada")["localizador"].count())

    st.divider()

    # -----------------------------
    # Forecast 30 días
    # -----------------------------
    st.subheader("📅 Forecast próximos 30 días")
    forecast_30 = df[df["llegada"].between(hoy, hoy + pd.Timedelta(days=30))]
    st.line_chart(forecast_30.groupby("llegada")["localizador"].count())

    st.divider()

    # -----------------------------
    # Pick‑up por día
    # -----------------------------
    st.subheader("📈 Pick‑up por día")
    pickup_diario = df.groupby("llegada")["localizador"].count()
    st.area_chart(pickup_diario)

    st.divider()

    # -----------------------------
    # Gráfico de tarifas
    # -----------------------------
    st.subheader("💶 Distribución de tarifas")
    st.bar_chart(df.groupby("tarifa")["precio"].mean())

    st.divider()

    # -----------------------------
    # Comparativa año anterior
    # -----------------------------
    st.subheader("📊 Comparativa con el año anterior")
    df["año"] = df["llegada"].dt.year

    if df["año"].nunique() > 1:
        st.line_chart(df.groupby("año")["precio"].mean())
    else:
        st.info("No hay datos suficientes para comparar con el año anterior.")

    st.divider()

    # ============================================================
    # FOOTER
    # ============================================================
    st.caption("Hotel Data Flow · Proyecto en desarrollo · Creado por Manel Vázquez Picart")
