
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import requests
from io import StringIO
import matplotlib.pyplot as plt

# Imagen/logo superior
st.image("https://i.imgur.com/BQn3Vkb.png", width=150)
st.title("📊 Consulta de Faena - PadronizaPY")

# Leer credenciales desde st.secrets
service_account_info = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(service_account_info)
authed_session = AuthorizedSession(credentials)

# URL CSV pública de Google Sheets
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTTfdT08aPWvHj4uX-0MEiDSwFcTTbN7aEd8Hb2nQX7Oqs-B_UWyIygFEI4KG-HXfeyznJ65b-VzQR-/pub?gid=987916598&single=true&output=csv"

# Descargar datos
try:
    response = authed_session.get(csv_url)
    response.raise_for_status()
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)

    # Mostrar tabla
    st.subheader("Datos de faena")
    st.dataframe(df, use_container_width=True)

    # Zona de preguntas al estilo GPT
    st.subheader("🤖 Haz preguntas sobre la faena")

    import openai
    from langchain.agents import create_pandas_dataframe_agent
    from langchain.chat_models import ChatOpenAI

    openai.api_key = st.secrets["openai_api_key"]
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

    agent = create_pandas_dataframe_agent(llm, df, verbose=False)

    pregunta = st.text_input("Escribe tu pregunta:")
    if pregunta:
        with st.spinner("Analizando..."):
            respuesta = agent.run(pregunta)
            st.success(respuesta)

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
