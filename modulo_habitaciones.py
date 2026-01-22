# -*- coding: utf-8 -*-
import streamlit as st

def modulo_habitaciones():

    st.title("🛏️ Módulo de Habitaciones")
    st.write("")

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

    st.info("🛠️ Este módulo está actualmente en construcción.")
