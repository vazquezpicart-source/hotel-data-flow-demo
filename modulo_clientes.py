# -*- coding: utf-8 -*-
"""
Módulo de Clientes – usando df_global y modo popup
"""

import streamlit as st
import pandas as pd
from datetime import datetime

COLUMNAS = [
    "localizador","nombre","apellido1","apellido2","email","telefono",
    "pais","idioma","habitacion","estado","llegada","salida","noches",
    "adultos","niños","tarifa","precio","segmento","canal","comentarios"
]

# ---------------------------------------------------------
# GENERADOR DE LOCALIZADOR
# ---------------------------------------------------------
def generar_localizador(df, fecha_llegada):
    fecha_str = fecha_llegada.strftime("%Y%m%d")
    mismos_dia = df[df["localizador"].str.contains(fecha_str, na=False)]

    if mismos_dia.empty:
        nuevo_num = 1
    else:
        ult = mismos_dia["localizador"].iloc[-1]
        try:
            num = int(ult.split("/")[-1])
        except:
            num = 0
        nuevo_num = num + 1

    return f"VIC/{fecha_str}/{nuevo_num:06d}"


# ---------------------------------------------------------
# MÓDULO PRINCIPAL
# ---------------------------------------------------------
def modulo_clientes(modo_popup=False):

    df = st.session_state.df_global

    # LIMPIEZA NUMÉRICA
    columnas_numericas = ["noches", "adultos", "niños", "precio"]
    for col in columnas_numericas:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    st.title("👤 Módulo de Clientes")

    # ---------------------------------------------------------
    # MODO POPUP (desde reservas)
    # ---------------------------------------------------------
    if modo_popup:

        localizador = st.session_state.cliente_seleccionado
        cliente = df[df["localizador"] == localizador].iloc[0]
        idx = df[df["localizador"] == localizador].index[0]

        st.subheader(f"📋 Ficha de {cliente['nombre']}")

        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input("Nombre", cliente["nombre"])
            apellido1 = st.text_input("Apellido 1", cliente["apellido1"])
            apellido2 = st.text_input("Apellido 2", cliente["apellido2"])
            email = st.text_input("Email", cliente["email"])
            telefono = st.text_input("Teléfono", cliente["telefono"])
            pais = st.text_input("País", cliente["pais"])
            idioma = st.text_input("Idioma", cliente["idioma"])

        with col2:
            habitacion = st.text_input("Habitación", cliente["habitacion"])
            estado = st.text_input("Estado", cliente["estado"])
            llegada = st.date_input("Llegada", pd.to_datetime(cliente["llegada"]))
            salida = st.date_input("Salida", pd.to_datetime(cliente["salida"]))
            noches = st.number_input("Noches", int(cliente["noches"]), step=1)
            adultos = st.number_input("Adultos", int(cliente["adultos"]), step=1)
            niños = st.number_input("Niños", int(cliente["niños"]), step=1)

        tarifa = st.text_input("Tarifa", cliente["tarifa"])
        precio = st.number_input("Precio", float(cliente["precio"]), step=1.0)
        segmento = st.text_input("Segmento", cliente["segmento"])
        canal = st.text_input("Canal", cliente["canal"])
        comentarios = st.text_area("Comentarios", cliente["comentarios"])

        if st.button("Actualizar cliente"):
            df.loc[idx] = [
                localizador, nombre, apellido1, apellido2, email, telefono,
                pais, idioma, habitacion, estado, llegada, salida, noches,
                adultos, niños, tarifa, precio, segmento, canal, comentarios
            ]
            df.to_csv("clientes_reservas.csv", index=False)
            st.session_state.df_global = df
            st.success("Cliente actualizado correctamente")

        if st.button("Cerrar ficha"):
            st.session_state.cliente_seleccionado = None
            st.rerun()

        return  # ← ESTE RETURN AHORA ESTÁ DENTRO DE LA FUNCIÓN

    # ---------------------------------------------------------
    # CREAR NUEVO CLIENTE
    # ---------------------------------------------------------
    st.subheader("➕ Crear nuevo cliente")

    with st.expander("Añadir cliente nuevo", expanded=False):

        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input("Nombre")
            apellido1 = st.text_input("Apellido 1")
            apellido2 = st.text_input("Apellido 2")
            email = st.text_input("Email")
            telefono = st.text_input("Teléfono")
            pais = st.text_input("País")
            idioma = st.text_input("Idioma")

        with col2:
            habitacion = st.text_input("Habitación")
            estado = st.text_input("Estado")
            llegada = st.date_input("Llegada")
            salida = st.date_input("Salida")

        noches = st.number_input("Noches", step=1)
        adultos = st.number_input("Adultos", step=1)
        niños = st.number_input("Niños", step=1)
        tarifa = st.text_input("Tarifa")
        precio = st.number_input("Precio", step=1.0)
        segmento = st.text_input("Segmento")
        canal = st.text_input("Canal")
        comentarios = st.text_area("Comentarios")

        localizador = generar_localizador(df, llegada)
        st.text_input("Localizador (automático)", localizador, disabled=True)

        if st.button("Guardar nuevo cliente"):
            nuevo = {
                "localizador": localizador,
                "nombre": nombre,
                "apellido1": apellido1,
                "apellido2": apellido2,
                "email": email,
                "telefono": telefono,
                "pais": pais,
                "idioma": idioma,
                "habitacion": habitacion,
                "estado": estado,
                "llegada": llegada,
                "salida": salida,
                "noches": noches,
                "adultos": adultos,
                "niños": niños,
                "tarifa": tarifa,
                "precio": precio,
                "segmento": segmento,
                "canal": canal,
                "comentarios": comentarios
            }

            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            df.to_csv("clientes_reservas.csv", index=False)
            st.session_state.df_global = df

            st.success("Cliente creado correctamente")

    # ---------------------------------------------------------
    # BUSCAR CLIENTE
    # ---------------------------------------------------------
    st.subheader("🔍 Buscar cliente")

    busqueda = st.text_input("Nombre o localizador")

    if busqueda:
        resultados = df[
            df["nombre"].str.contains(busqueda, case=False) |
            df["localizador"].str.contains(busqueda, case=False)
        ]

        if resultados.empty:
            st.warning("No se encontraron clientes.")
        else:
            st.dataframe(resultados)
