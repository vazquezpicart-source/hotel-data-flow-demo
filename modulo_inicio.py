# -*- coding: utf-8 -*-
import streamlit as st

def modulo_inicio():

    st.title("🏨 Hotel Data Flow – Inicio")

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

    st.subheader("PMS modular · ligero · en evolución constante")

    st.write("""
    Bienvenido a la versión de desarrollo de **Hotel Data Flow**, un PMS diseñado para hoteles pequeños y medianos.
    """)

    st.header("🚀 Acceso rápido")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Reservas", use_container_width=True):
            st.session_state.pagina = "reservas"
            st.rerun()

        if st.button("👤 Clientes", use_container_width=True):
            st.session_state.pagina = "clientes"
            st.rerun()

    with col2:
        st.button("🛏️ Habitaciones (En construcción)", disabled=True, use_container_width=True)
        if st.button("📦 Almacén", use_container_width=True):
            st.session_state.pagina = "almacen"
            st.rerun()

    with col3:
        if st.button("📈 Marketing", use_container_width=True):
            st.session_state.pagina = "marketing"
            st.rerun()

    st.divider()

    st.header("🛠️ Estado del proyecto")
    st.write("""
    - 🟢 Módulos funcionales: Reservas, Clientes  
    - 🟡 En desarrollo: Habitaciones, Almacén, Marketing  
    - 🔵 Planificados: Check-in, Panel diario, Facturación, Dashboard avanzado  
    """)

    st.caption("Hotel Data Flow · Proyecto en desarrollo · Creado por Manel Vázquez Picart")
