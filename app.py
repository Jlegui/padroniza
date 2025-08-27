
import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Título de la app
st.title("Pecuaria Smart Predict 🐄")

# Autenticación con Google Sheets usando st.secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(credentials)

# Leer el CSV desde URL pública
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTTfdT08aPWvHj4uX-0MEiDSwFcTTbN7aEd8Hb2nQX7Oqs-B_UWyIygFEI4KG-HXfeyznJ65b-VzQR-/pub?gid=987916598&single=true&output=csv"
try:
    df = pd.read_csv(csv_url, delimiter=",")
    st.success("✅ Datos cargados correctamente desde Google Sheets.")
except Exception as e:
    st.error(f"Error al cargar CSV: {e}")
    st.stop()

# Mostrar tabla
st.subheader("Vista previa de los datos")
st.dataframe(df.head())

# Limpieza simple de nombres de columnas
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Verificación de columnas para graficar
if "ciudad" in df.columns and "precio_del_gordo" in df.columns:
    st.subheader("Precio del gordo por ciudad")
    fig = px.box(df, x="ciudad", y="precio_del_gordo", title="Distribución del precio del gordo")
    st.plotly_chart(fig)
else:
    st.warning("No se encuentran las columnas 'ciudad' y 'precio_del_gordo' necesarias para graficar.")
