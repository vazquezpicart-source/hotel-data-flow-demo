# -*- coding: utf-8 -*-
import streamlit as st

def modulo_inicio():

    st.title("🏨 Hotel Data Flow – Inicio")
    st.write("")

    # MENÚ SUPERIOR NATIVO
    menu = st.columns(6)

    with menu[0]:
        if st.button("🏠 Inicio", key="menu_inicio", use_container_width=True):
            st.session_state.pagina = "inicio"
            st.rerun()

    with menu[1]:
        if st.button("📊 Reservas", key="menu_reservas", use_container_width=True):
            st.session_state.pagina = "reservas"
            st.rerun()

    with menu[2]:
        if st.button("👤 Clientes", key="menu_clientes", use_container_width=True):
            st.session_state.pagina = "clientes"
            st.rerun()

    with menu[3]:
        st.button("🛏️ Habitaciones", key="menu_habitaciones", disabled=True, use_container_width=True)

    with menu[4]:
        if st.button("📦 Almacén", key="menu_almacen", use_container_width=True):
            st.session_state.pagina = "almacen"
            st.rerun()

    with menu[5]:
        if st.button("📈 Marketing", key="menu_marketing", use_container_width=True):
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
        if st.button("📊 Reservas", key="inicio_reservas", use_container_width=True):
            st.session_state.pagina = "reservas"
            st.rerun()

        if st.button("👤 Clientes", key="inicio_clientes", use_container_width=True):
            st.session_state.pagina = "clientes"
            st.rerun()

    with col2:
        st.button("🛏️ Habitaciones (En construcción)", disabled=True, use_container_width=True)
        if st.button("📦 Almacén", key="inicio_almacen", use_container_width=True):
            st.session_state.pagina = "almacen"
            st.rerun()

    with col3:
        if st.button("📈 Marketing", key="inicio_marketing", use_container_width=True):
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
