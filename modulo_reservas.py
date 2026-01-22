# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

def modulo_reservas():

    st.title("📊 Módulo de Reservas")
    st.write("")

    # MENÚ SUPERIOR
    menu = st.columns(6)

    with menu[0]:
        if st.button("🏠 Inicio", use_container_width=True):
            st.session_state.pagina = "inicio"
            st.rerun()

    with menu[1]:
        if st.button("📊 Reservas", use_container_width=True):
            st.session_state.pagina = "reservas"
            st.rerun()

    with menu[2]:
        if st.button("👤 Clientes", use_container_width=True):
            st.session_state.pagina = "clientes"
            st.rerun()

    with menu[3]:
        st.button("🛏️ Habitaciones", disabled=True, use_container_width=True)

    with menu[4]:
        if st.button("📦 Almacén", use_container_width=True):
            st.session_state.pagina = "almacen"
            st.rerun()

    with menu[5]:
        if st.button("📈 Marketing", use_container_width=True):
            st.session_state.pagina = "marketing"
            st.rerun()

    st.divider()

    df = st.session_state.df_global

    # Limpieza numérica
    df["precio"] = pd.to_numeric(df["precio"], errors="coerce").fillna(0)
    df["noches"] = pd.to_numeric(df["noches"], errors="coerce").fillna(0)
    df["adultos"] = pd.to_numeric(df["adultos"], errors="coerce").fillna(0)
    df["niños"] = pd.to_numeric(df["niños"], errors="coerce").fillna(0)

    df = df[df["localizador"] != ""]

    st.subheader("🔎 Listado de reservas")

    for i, fila in df.iterrows():
        with st.container(border=True):
            st.write(f"📅 **Llegada:** {fila['llegada']}")
            st.write(f"🏨 **Habitación:** {fila['habitacion']}")
            st.write(f"💶 **Tarifa:** {fila['tarifa']} — {fila['precio']} €")
            st.write(f"🌐 **Canal:** {fila['canal']}")
            st.write(f"🧾 **Localizador:** {fila['localizador']}")

            if st.button(f"👤 Ver ficha del cliente ({fila['localizador']})", key=f"cliente_{i}", use_container_width=True):
                st.session_state.cliente_seleccionado = fila["localizador"]
                st.session_state.pagina = "clientes"
                st.rerun()

    st.subheader("📈 Estadísticas")

    col1, col2, col3 = st.columns(3)
    col1.metric("ADR", f"{df['precio'].mean():.2f} €")
    col2.metric("Noches totales", int(df["noches"].sum()))
    col3.metric("Adultos totales", int(df["adultos"].sum()))

    st.bar_chart(df.groupby("canal")["precio"].sum())
