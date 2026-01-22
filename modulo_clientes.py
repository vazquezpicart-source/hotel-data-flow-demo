# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

def modulo_clientes(modo_popup=False):

    st.title("👤 Módulo de Clientes")

    # ---------------------------------------------------------
    # MENÚ SUPERIOR NATIVO
    # ---------------------------------------------------------
    menu = st.columns(6)

    with menu[0]:
        if st.button("🏠 Inicio"):
            st.session_state.pagina = "inicio"
            st.rerun()

    with menu[1]:
        if st.button("📊 Reservas"):
            st.session_state.pagina = "reservas"
            st.rerun()

    with menu[2]:
        if st.button("👤 Clientes"):
            st.session_state.pagina = "clientes"
            st.rerun()

    with menu[3]:
        st.button("🛏️ Habitaciones", disabled=True)

    with menu[4]:
        if st.button("📦 Almacén"):
            st.session_state.pagina = "almacen"
            st.rerun()

    with menu[5]:
        if st.button("📈 Marketing"):
            st.session_state.pagina = "marketing"
            st.rerun()

    st.divider()

    # ---------------------------------------------------------
    # CARGA DEL DATAFRAME
    # ---------------------------------------------------------
    df = st.session_state.df_global

    # Limpieza numérica
    for col in ["noches", "adultos", "niños", "precio"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # ---------------------------------------------------------
    # MODO POPUP: FICHA CLIENTE
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

        return

    # ---------------------------------------------------------
    # CREAR NUEVO CLIENTE
    # ---------------------------------------------------------
    st.subheader("➕ Crear nuevo cliente")

    with st.form("form_nuevo_cliente"):
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
            llegada = st.date_input("Llegada")
            salida = st.date_input("Salida")
            noches = st.number_input("Noches", min_value=1, value=1)
            adultos = st.number_input("Adultos", min_value=1, value=2)
            niños = st.number_input("Niños", min_value=0, value=0)
            tarifa = st.text_input("Tarifa")
            precio = st.number_input("Precio", min_value=0.0, value=100.0)
            canal = st.text_input("Canal")

        habitacion = st.text_input("Habitación")
        estado = st.text_input("Estado")
        segmento = st.text_input("Segmento")
        comentarios = st.text_area("Comentarios")

        submitted = st.form_submit_button("Guardar cliente")

        if submitted:
            nuevo = {
                "localizador": f"CL-{len(df)+1:04d}",
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

            df.loc[len(df)] = nuevo
            df.to_csv("clientes_reservas.csv", index=False)
            st.session_state.df_global = df
            st.success("✅ Cliente guardado correctamente")

    # ---------------------------------------------------------
    # BUSCAR CLIENTE
    # ---------------------------------------------------------
    st.subheader("🔍 Buscar cliente")

    busqueda = st.text_input("Buscar por nombre, email o localizador")

    if busqueda:
        resultado = df[
            df["nombre"].str.contains(busqueda, case=False, na=False) |
            df["email"].str.contains(busqueda, case=False, na=False) |
            df["localizador"].str.contains(busqueda, case=False, na=False)
        ]

        if resultado.empty:
            st.warning("No se encontraron coincidencias.")
        else:
            for i, fila in resultado.iterrows():
                with st.container(border=True):
                    st.write(f"👤 **{fila['nombre']} {fila['apellido1']}**")
                    st.write(f"📧 {fila['email']} — 📞 {fila['telefono']}")
                    st.write(f"🧾 Localizador: {fila['localizador']} — 🏨 Habitación: {fila['habitacion']}")

                    if st.button(f"Ver ficha ({fila['localizador']})", key=f"ficha_{i}"):
                        st.session_state.cliente_seleccionado = fila["localizador"]
                        st.session_state.pagina = "clientes"
                        st.rerun()
