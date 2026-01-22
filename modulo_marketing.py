# -*- coding: utf-8 -*-
import streamlit as st

def modulo_marketing():

    st.title("📈 Módulo de Marketing & Comercial")

    # MENÚ SUPERIOR
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

    st.info("🛠️ Este módulo está actualmente en construcción.")
    st.write("""
    Aquí podrás gestionar campañas, segmentos, canales de venta, 
    análisis de rendimiento y estrategias comerciales.
    """)
