# -*- coding: utf-8 -*-
"""
Created on Thu Jan  1 18:39:15 2026

@author: manel
"""

import streamlit as st
from modulo_reservas import modulo_reservas
from modulo_almacen import modulo_almacen

# -------------------------------
# 🎨 CONFIGURACIÓN DE LA PÁGINA
# -------------------------------
st.set_page_config(
    page_title="Hotel Data Flow – Ecosistema",
    layout="wide",
    page_icon="🏨"
)

# -------------------------------
# 🎨 ESTILOS PERSONALIZADOS
# -------------------------------
st.markdown("""
<style>
.main {
    background-color: #F7F9FC;
}
h1, h2, h3 {
    color: #1A3C57;
}
div[data-testid="metric-container"] {
    background-color: #FFFFFF;
    border: 1px solid #E0E6ED;
    padding: 15px;
    border-radius: 10px;
}
.streamlit-expanderHeader {
    font-size: 18px;
    color: #1A3C57;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🧭 MENÚ LATERAL
# -------------------------------
st.sidebar.title("📌 Navegación")
opcion = st.sidebar.radio(
    "Selecciona un módulo:",
    ["📊 Reservas", "📦 Almacén", "📈 Marketing & Comercial"
]
)

# -------------------------------
# 🔀 RUTEO ENTRE MÓDULOS
# -------------------------------
if opcion == "📊 Reservas":
    modulo_reservas()

elif opcion == "📦 Almacén":
    modulo_almacen()
elif opcion == "📈 Marketing & Comercial":
    modulo_marketing()
