# -*- coding: utf-8 -*-
"""
Hotel Data Flow – App principal
"""

import streamlit as st
import pandas as pd

from modulo_inicio import modulo_inicio
from modulo_reservas import modulo_reservas
from modulo_clientes import modulo_clientes
from modulo_almacen import modulo_almacen
from modulo_marketing import modulo_marketing
from modulo_habitaciones import modulo_habitaciones

# ---------------------------------------------------------
# CONFIGURACIÓN BÁSICA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Hotel Data Flow",
    layout="wide",
    page_icon="🏨"
)

# ---------------------------------------------------------
# CARGA DEL CSV UNIFICADO
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

if "df_global" not in st.session_state:
    try:
        df = pd.read_csv("clientes_reservas.csv")
        df = reparar_csv(df)
        st.session_state.df_global = df
    except Exception as e:
        st.error(f"❌ Error al cargar clientes_reservas.csv: {e}")
        st.stop()

# ---------------------------------------------------------
# CONTROL DE NAVEGACIÓN
# ---------------------------------------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

# 🔵 Nueva API: leer parámetros desde la barra superior
params = st.query_params

if "pagina" in params:
    st.session_state.pagina = params["pagina"]

# Estado de ficha cliente
if "cliente_seleccionado" not in st.session_state:
    st.session_state.cliente_seleccionado = None

# ---------------------------------------------------------
# RUTEO ENTRE MÓDULOS
# ---------------------------------------------------------
pagina = st.session_state.pagina

if pagina == "inicio":
    modulo_inicio()

elif pagina == "reservas":
    modulo_reservas()

elif pagina == "clientes":
    if st.session_state.cliente_seleccionado:
        modulo_clientes(modo_popup=True)
    else:
        modulo_clientes(modo_popup=False)

elif pagina == "almacen":
    modulo_almacen()

elif pagina == "marketing":
    modulo_marketing()

elif pagina == "habitaciones":
    modulo_habitaciones()
