# -*- coding: utf-8 -*-
"""
Hotel Data Flow – Ecosistema con CSV unificado
"""

import streamlit as st
import pandas as pd

from modulo_reservas import modulo_reservas
from modulo_clientes import modulo_clientes
from modulo_almacen import modulo_almacen
from modulo_marketing import modulo_marketing
from modulo_habitaciones import modulo_habitaciones

# ---------------------------------------------------------
# 🧠 CARGA AUTOMÁTICA DEL CSV UNIFICADO + REPARACIÓN
# ---------------------------------------------------------
COLUMNAS_OBLIGATORIAS = [
    "localizador","nombre","apellido1","apellido2","email","telefono",
    "pais","idioma","habitacion","estado","llegada","salida","noches",
    "adultos","niños","tarifa","precio","segmento","canal","comentarios"
]

def reparar_csv(df):
    df = df.copy()
    for col in COLUMNAS_OBLIGATORIAS:
        if col not in df.columns:
            df[col] = ""
    return df[COLUMNAS_OBLIGATORIAS]

if "cliente_seleccionado" not in st.session_state:
    st.session_state.cliente_seleccionado = None

if "df_global" not in st.session_state:
    try:
        df = pd.read_csv("clientes_reservas.csv")
        df = reparar_csv(df)
        st.session_state.df_global = df
    except Exception as e:
        st.error(f"❌ Error al cargar clientes_reservas.csv: {e}")
        st.stop()

# ---------------------------------------------------------
# 🎨 CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Hotel Data Flow – Ecosistema",
    layout="wide",
    page_icon="🏨"
)

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

# ---------------------------------------------------------
# 🧭 MENÚ LATERAL
# ---------------------------------------------------------
st.sidebar.title("📌 Navegación")
opcion = st.sidebar.radio(
    "Selecciona un módulo:",
    ["📊 Reservas", "👤 Clientes", "📦 Almacén", "📈 Marketing & Comercial", "🛏️ Habitaciones"]
)

# ---------------------------------------------------------
# 🔀 SI VIENE DESDE RESERVAS → ABRIR FICHA CLIENTE
# ---------------------------------------------------------
if st.session_state.cliente_seleccionado:
    st.sidebar.warning("📌 Ficha del cliente abierta desde Reservas")
    modulo_clientes(modo_popup=True)
    st.stop()

# ---------------------------------------------------------
# 🔀 RUTEO ENTRE MÓDULOS
# ---------------------------------------------------------
if opcion == "📊 Reservas":
    modulo_reservas()

elif opcion == "👤 Clientes":
    modulo_clientes()

elif opcion == "📦 Almacén":
    modulo_almacen()

elif opcion == "📈 Marketing & Comercial":
    modulo_marketing()

elif opcion == "🛏️ Habitaciones":
    modulo_habitaciones()
