# -*- coding: utf-8 -*-
"""
Módulo de Reservas – usando df_global
"""

import streamlit as st
import pandas as pd

def modulo_reservas():

    st.title("📊 Módulo de Reservas")
    st.caption("Análisis y gestión de reservas desde el CSV unificado")

    df = st.session_state.df_global

    # ---------------------------------------------------------
    # LIMPIEZA DE DATOS: convertir columnas numéricas
    # ---------------------------------------------------------
    df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
    df["noches"] = pd.to_numeric(df["noches"], errors="coerce")
    df["adultos"] = pd.to_numeric(df["adultos"], errors="coerce")
    df["niños"] = pd.to_numeric(df["niños"], errors="coerce")

    df["precio"].fillna(0, inplace=True)
    df["noches"].fillna(0, inplace=True)
    df["adultos"].fillna(0, inplace=True)
    df["niños"].fillna(0, inplace=True)

    st.divider()

    # ---------------------------------------------------------
    # LISTADO DE RESERVAS
    # ---------------------------------------------------------
    st.subheader("🔎 Listado de reservas")

    for i, fila in df.iterrows():
        with st.container(border=True):
            st.write(f"📅 **Llegada:** {fila['llegada']}")
            st.write(f"🏨 **Habitación:** {fila['habitacion']}")
            st.write(f"💶 **Tarifa:** {fila['tarifa']} — {fila['precio']} €")
            st.write(f"🌐 **Canal:** {fila['canal']}")
            st.write(f"🧾 **Localizador:** {fila['localizador']}")

            if st.button(f"👤 Ver ficha del cliente ({fila['localizador']})", key=f"cliente_{i}"):
                st.session_state.cliente_seleccionado = fila["localizador"]
                st.rerun()

    # ---------------------------------------------------------
    # ESTADÍSTICAS
    # ---------------------------------------------------------
    st.subheader("📈 Estadísticas")

    col1, col2, col3 = st.columns(3)

    col1.metric("ADR", f"{df['precio'].mean():.2f} €")
    col2.metric("Noches totales", int(df["noches"].sum()))
    col3.metric("Adultos totales", int(df["adultos"].sum()))

    st.bar_chart(df.groupby("canal")["precio"].sum())
