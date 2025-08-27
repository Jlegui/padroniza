
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import requests

# Configurar título de la app
st.set_page_config(page_title="Pecuaria Smart Predict", layout="wide")
st.title("📈 Pecuaria Smart Predict")

# Leer credenciales del archivo JSON
with open("gcp_service_account.json", "r") as file:
    import json
    service_account_info = json.load(file)

credentials = service_account.Credentials.from_service_account_info(service_account_info)
authed_session = AuthorizedSession(credentials)

# URL CSV pública de Google Sheets
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTTfdT08aPWvHj4uX-0MEiDSwFcTTbN7aEd8Hb2nQX7Oqs-B_UWyIygFEI4KG-HXfeyznJ65b-VzQR-/pub?gid=987916598&single=true&output=csv"

# Cargar los datos
try:
    response = authed_session.get(csv_url)
    response.raise_for_status()
    data = pd.read_csv(pd.compat.StringIO(response.text))
    st.success("Datos cargados correctamente desde Google Sheets.")
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# Mostrar los datos
st.dataframe(data)
