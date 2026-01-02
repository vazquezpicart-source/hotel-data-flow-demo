# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 17:46:59 2026

@author: manel
"""

import streamlit as st
import pandas as pd

def modulo_reservas():

    # -------------------------------
    # 🏨 HEADER
    # -------------------------------
    st.title("📊 Módulo de Reservas")
    st.caption("Carga, validación y análisis básico de reservas hoteleras")

    st.divider()

    # -------------------------------
    # 📂 SUBIDA DE ARCHIVO
    # -------------------------------
    with st.expander("📂 Cargar archivo de reservas (CSV)", expanded=True):
        uploaded_file = st.file_uploader(
            "Selecciona un archivo CSV de reservas",
            type=["csv"],
            key="reservas_uploader"
        )

    if uploaded_file is None:
        st.info("Sube un archivo CSV para comenzar.")
        return

    # -------------------------------
    # 📥 LECTURA DEL ARCHIVO
    # -------------------------------
    try:
        df = pd.read_csv(uploaded_file)
        st.success("Archivo cargado correctamente")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return

    # -------------------------------
    # 🔍 VALIDACIÓN DE COLUMNAS
    # -------------------------------
    with st.expander("🔍 Validación de columnas", expanded=True):

        columnas_obligatorias = ["fecha", "habitacion", "tarifa", "precio", "canal"]
        columnas_faltantes = [col for col in columnas_obligatorias if col not in df.columns]

        if columnas_faltantes:
            st.error("❌ El archivo no contiene todas las columnas obligatorias.")
            st.write("Columnas faltantes:")
            st.write(columnas_faltantes)

            st.code(f"""
[ERROR] Columnas obligatorias faltantes: {columnas_faltantes}
[STOP] Proceso detenido por falta de estructura mínima.
            """)
            return
        else:
            st.success("✔ Todas las columnas obligatorias están presentes.")
            st.code("[OK] Columnas obligatorias validadas correctamente.")

    # -------------------------------
    # 📊 ESTADÍSTICAS BÁSICAS
    # -------------------------------
    with st.expander("📈 Estadísticas del dataset", expanded=True):

        colA, colB, colC = st.columns(3)

        # Precio medio global (ADR)
        precio_medio = df["precio"].mean()
        colA.metric("💵 Precio medio global (ADR)", f"{precio_medio:.2f} €")

        # ADR por tarifa
        adr_por_tarifa = df.groupby("tarifa")["precio"].mean().round(2)
        colB.write("**ADR por tarifa**")
        colB.dataframe(adr_por_tarifa)

        # Revenue por canal
        revenue_por_canal = df.groupby("canal")["precio"].sum()
        colC.write("**Revenue por canal**")
        colC.dataframe(revenue_por_canal)

    # -------------------------------
    # 📊 GRÁFICO: REVENUE POR CANAL
    # -------------------------------
    with st.expander("📊 Gráfico: Revenue por canal", expanded=True):

        chart_data = revenue_por_canal.reset_index()
        chart_data.columns = ["canal", "revenue"]

        st.bar_chart(chart_data, x="canal", y="revenue")

    # -------------------------------
    # 👀 VISTA PREVIA DEL DATASET
    # -------------------------------
    with st.expander("👀 Vista previa del dataset", expanded=False):
        st.dataframe(df, height=500)

    # -------------------------------
    # 📝 LOGS
    # -------------------------------
    with st.expander("📝 Logs del proceso", expanded=False):
        st.code(f"""
[OK] Archivo cargado: {uploaded_file.name}
[OK] Filas detectadas: {df.shape[0]}
[OK] Columnas detectadas: {df.shape[1]}
[OK] Validación de columnas completada
[OK] Estadísticas calculadas correctamente
[OK] Gráfico generado correctamente
[OK] Vista previa generada correctamente
        """)
