# -*- coding: utf-8 -*-
"""
Created on Thu Jan  1 18:39:15 2026

@author: manel
"""

import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Hotel Data Flow – Demo",
    layout="wide"
)

# Título principal
st.title("🏨 Hotel Data Flow – Demo")
st.subheader("Carga un archivo y visualiza tus datos hoteleros de forma sencilla")

st.write("Formatos aceptados: **CSV**")

# Subida de archivo
uploaded_file = st.file_uploader("📂 Sube tu archivo", type=["csv"])

if uploaded_file is not None:

    # Leer archivo
    try:
        df = pd.read_csv(uploaded_file)
        st.success("Archivo cargado correctamente")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        st.stop()

    # Información básica
    st.write("### 📊 Información del dataset")
    col1, col2 = st.columns(2)
    col1.metric("Filas", df.shape[0])
    col2.metric("Columnas", df.shape[1])

    # Vista previa con scroll
    st.write("### 👀 Vista previa del dataset")
    st.dataframe(df, height=500)

    # Logs del proceso
    st.write("### 📝 Logs del proceso")
    st.code(f"""
[OK] Archivo cargado: {uploaded_file.name}
[OK] Filas detectadas: {df.shape[0]}
[OK] Columnas detectadas: {df.shape[1]}
[OK] Vista previa generada correctamente
    """)
else:
    st.info("Sube un archivo CSV para comenzar.")
