import streamlit as st
import pandas as pd

# Título de la app
st.title("Visualización de datos desde Google Sheets")

# URL del CSV público de Google Sheets
url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTTfdT08aPWvHj4uX-0MEiDSwFcTTbN7aEd8Hb2nQX7Oqs-B_UWyIygFEI4KG-HXfeyznJ65b-VzQR-/pub?gid=987916598&single=true&output=csv"

# Leer el archivo CSV directamente (sin autenticación)
try:
    df = pd.read_csv(url_csv)
    st.success("Datos cargados correctamente")
    st.dataframe(df)
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
