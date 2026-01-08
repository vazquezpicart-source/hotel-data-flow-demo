# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 17:26:07 2026

@author: manel
"""

import streamlit as st
import pandas as pd

def modulo_marketing():

    # -------------------------------
    # 🏷️ HEADER
    # -------------------------------
    st.title("📈 Módulo de Marketing & Comercial")
    st.caption("Análisis de canales, tarifas, segmentos, mercados y campañas")

    st.divider()

    # -------------------------------
    # 📂 SUBIDA DE ARCHIVO
    # -------------------------------
    with st.expander("📂 Cargar archivo de marketing (CSV)", expanded=True):
        uploaded_file = st.file_uploader(
            "Selecciona un archivo CSV de marketing",
            type=["csv"],
            key="marketing_uploader"
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
    columnas_obligatorias = [
        "fecha", "canal", "tarifa", "precio",
        "segmento", "pais", "mercado",
        "campaña", "coste_campaña", "conversiones"
    ]

    with st.expander("🔍 Validación de columnas", expanded=True):
        columnas_faltantes = [col for col in columnas_obligatorias if col not in df.columns]

        if columnas_faltantes:
            st.error("❌ Faltan columnas obligatorias")
            st.write(columnas_faltantes)
            return
        else:
            st.success("✔ Todas las columnas obligatorias están presentes")
            st.code("[OK] Validación completada")

    # -------------------------------
    # 📊 KPIs COMERCIALES
    # -------------------------------
    with st.expander("📊 KPIs Comerciales", expanded=True):

        col1, col2, col3 = st.columns(3)

        revenue_total = df["precio"].sum()
        col1.metric("💰 Revenue total", f"{revenue_total:.2f} €")

        adr_global = df["precio"].mean()
        col2.metric("💵 ADR global", f"{adr_global:.2f} €")

        reservas_total = df.shape[0]
        col3.metric("📘 Nº de reservas", reservas_total)

    # -------------------------------
    # 📊 MIX DE DISTRIBUCIÓN
    # -------------------------------
    with st.expander("📊 Mix de distribución (canales)", expanded=True):

        mix = df.groupby("canal")["precio"].sum().reset_index()
        mix.columns = ["canal", "revenue"]

        st.bar_chart(mix, x="canal", y="revenue")

        st.write("### Tabla del mix de distribución")
        st.dataframe(mix)

    # -------------------------------
    # 📊 ANÁLISIS POR TARIFA
    # -------------------------------
    with st.expander("📊 Análisis por tarifa", expanded=True):

        tarifa_stats = df.groupby("tarifa")["precio"].agg(["count", "mean", "sum"])
        tarifa_stats.columns = ["Reservas", "ADR", "Revenue"]

        st.dataframe(tarifa_stats)

    # -------------------------------
    # 📅 ANÁLISIS TEMPORAL
    # -------------------------------
    with st.expander("📅 Análisis temporal", expanded=True):

        df["fecha"] = pd.to_datetime(df["fecha"])
        temporal = df.groupby("fecha")["precio"].sum().reset_index()

        st.line_chart(temporal, x="fecha", y="precio")

    # -------------------------------
    # 🌍 SEGMENTACIÓN
    # -------------------------------
    with st.expander("🌍 Segmentación comercial", expanded=True):

        seg_stats = df.groupby("segmento")["precio"].sum()
        st.write("### Revenue por segmento")
        st.dataframe(seg_stats)

        pais_stats = df.groupby("pais")["precio"].sum()
        st.write("### Revenue por país")
        st.dataframe(pais_stats)

        mercado_stats = df.groupby("mercado")["precio"].sum()
        st.write("### Revenue por mercado")
        st.dataframe(mercado_stats)

    # -------------------------------
    # 🎯 CAMPAÑAS DE MARKETING
    # -------------------------------
    with st.expander("🎯 Campañas de marketing (ROI)", expanded=True):

        df["coste_campaña"] = df["coste_campaña"].fillna(0)
        df["conversiones"] = df["conversiones"].fillna(0)

        campañas = df.groupby("campaña").agg({
            "precio": "sum",
            "coste_campaña": "sum",
            "conversiones": "sum"
        }).reset_index()

        campañas["ROI"] = campañas["precio"] - campañas["coste_campaña"]
        campañas["Coste por reserva"] = campañas["coste_campaña"] / campañas["conversiones"].replace(0, 1)

        st.dataframe(campañas)

    # -------------------------------
    # 👀 VISTA PREVIA
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
[OK] Validación completada
[OK] KPIs generados
[OK] Mix de distribución generado
[OK] Análisis por tarifa generado
[OK] Análisis temporal generado
[OK] Segmentación generada
[OK] Campañas analizadas
        """)
