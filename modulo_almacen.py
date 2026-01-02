# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 17:36:05 2026

@author: manel
"""

import streamlit as st
import pandas as pd

def modulo_almacen():

    # -------------------------------
    # 🏷️ HEADER
    # -------------------------------
    st.title("📦 Módulo de Almacén")
    st.caption("Control de inventario, existencias, entradas, salidas y merma")

    st.divider()

    # -------------------------------
    # 📂 SUBIDA DE ARCHIVO
    # -------------------------------
    with st.expander("📂 Cargar inventario (CSV)", expanded=True):
        uploaded_file = st.file_uploader(
            "Selecciona un archivo CSV de inventario",
            type=["csv"],
            key="almacen_uploader"
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

        columnas_obligatorias = [
            "producto", "categoria", "stock_inicial", "stock_actual",
            "unidad", "precio_unitario"
        ]

        columnas_faltantes = [col for col in columnas_obligatorias if col not in df.columns]

        if columnas_faltantes:
            st.error("❌ Faltan columnas obligatorias")
            st.write(columnas_faltantes)
            return
        else:
            st.success("✔ Todas las columnas obligatorias están presentes")
            st.code("[OK] Validación completada")

    # -------------------------------
    # 📊 ESTADÍSTICAS DEL INVENTARIO
    # -------------------------------
    with st.expander("📊 Estadísticas del inventario", expanded=True):

        col1, col2, col3 = st.columns(3)

        # Valor total del inventario
        df["valor_total"] = df["stock_actual"] * df["precio_unitario"]
        valor_total = df["valor_total"].sum()
        col1.metric("💰 Valor total del inventario", f"{valor_total:.2f} €")

        # Productos con stock bajo
        stock_bajo = df[df["stock_actual"] <= 5]["producto"].count()
        col2.metric("⚠ Productos con stock bajo", stock_bajo)

        # Número total de productos
        total_productos = df["producto"].count()
        col3.metric("📦 Total de productos", total_productos)

        # Tabla: stock por categoría
        st.write("### 📦 Stock por categoría")
        st.dataframe(df.groupby("categoria")["stock_actual"].sum())

    # -------------------------------
    # ➕➖ REGISTRO DE MOVIMIENTOS
    # -------------------------------
    with st.expander("➕➖ Registrar movimientos (entradas, salidas, merma)", expanded=True):

        producto_sel = st.selectbox("Selecciona un producto", df["producto"].unique())
        movimiento = st.selectbox("Tipo de movimiento", ["Entrada", "Salida", "Merma"])
        cantidad = st.number_input("Cantidad", min_value=1, step=1)

        if st.button("Registrar movimiento"):

            idx = df[df["producto"] == producto_sel].index[0]

            if movimiento == "Entrada":
                df.loc[idx, "stock_actual"] += cantidad

            elif movimiento == "Salida":
                if df.loc[idx, "stock_actual"] >= cantidad:
                    df.loc[idx, "stock_actual"] -= cantidad
                else:
                    st.error("❌ No hay suficiente stock para realizar la salida.")
                    return

            elif movimiento == "Merma":
                if df.loc[idx, "stock_actual"] >= cantidad:
                    df.loc[idx, "stock_actual"] -= cantidad
                else:
                    st.error("❌ No hay suficiente stock para registrar la merma.")
                    return

            st.success(f"Movimiento registrado: {movimiento} de {cantidad} unidades de {producto_sel}")

    # -------------------------------
    # 👀 VISTA PREVIA
    # -------------------------------
    with st.expander("👀 Vista previa del inventario", expanded=False):
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
[OK] Estadísticas generadas
[OK] Movimientos listos para registrar
        """)
