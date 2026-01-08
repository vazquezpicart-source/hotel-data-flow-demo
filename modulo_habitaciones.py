# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 17:57:05 2026

@author: manel
"""

import streamlit as st
import pandas as pd

def modulo_habitaciones():

    st.title("🛏️ Estado de Habitaciones")
    st.caption("Control visual de habitaciones limpias, sucias, bloqueadas y pendientes")

    st.divider()

    # -------------------------------
    # 📂 Cargar archivo
    # -------------------------------
    uploaded_file = st.file_uploader(
        "Cargar archivo habitaciones (CSV)",
        type=["csv"],
        key="habitaciones_uploader"
    )

    if uploaded_file is None:
        st.info("Sube un archivo CSV para comenzar.")
        return

    try:
        df = pd.read_csv(uploaded_file)
        st.success("Archivo cargado correctamente")
    except:
        st.error("Error al leer el archivo.")
        return

    # -------------------------------
    # 🔍 Validación
    # -------------------------------
    columnas_obligatorias = ["habitacion", "estado"]

    for col in columnas_obligatorias:
        if col not in df.columns:
            st.error(f"Falta la columna obligatoria: {col}")
            return

    # -------------------------------
    # 🎨 Colores por estado
    # -------------------------------
    colores = {
        "sucia": "#FF4C4C",       # rojo
        "limpia": "#4CAF50",      # verde
        "bloqueada": "#FFA500",   # naranja
        "pendiente": "#1E90FF"    # azul
    }

    st.subheader("📊 Estado actual")

    # -------------------------------
    # 🧱 Cuadrícula visual
    # -------------------------------
    cols = st.columns(4)

    for i, row in df.iterrows():
        habitacion = row["habitacion"]
        estado = row["estado"].lower()

        color = colores.get(estado, "#CCCCCC")

        with cols[i % 4]:
            st.markdown(
                f"""
                <div style="
                    background-color:{color};
                    padding:20px;
                    border-radius:10px;
                    text-align:center;
                    color:white;
                    font-size:20px;
                    margin-bottom:10px;
                ">
                    <b>{habitacion}</b><br>
                    {estado.upper()}
                </div>
                """,
                unsafe_allow_html=True
            )

    # -------------------------------
    # ✏️ Actualizar estado
    # -------------------------------
    st.subheader("✏️ Actualizar estado de una habitación")

    hab_sel = st.selectbox("Selecciona habitación", df["habitacion"])
    nuevo_estado = st.selectbox(
        "Nuevo estado",
        ["limpia", "sucia", "bloqueada", "pendiente"]
    )

    if st.button("Actualizar estado"):
        df.loc[df["habitacion"] == hab_sel, "estado"] = nuevo_estado
        st.success(f"Habitación {hab_sel} actualizada a {nuevo_estado.upper()}")

    # -------------------------------
    # 👀 Vista previa
    # -------------------------------
    with st.expander("👀 Vista previa del CSV"):
        st.dataframe(df)

    # -------------------------------
    # 📝 Logs
    # -------------------------------
    with st.expander("📝 Logs"):
        st.code(f"""
[OK] Habitaciones cargadas: {df.shape[0]}
[OK] Estados detectados: {df['estado'].unique()}
[OK] Actualización lista
        """)
