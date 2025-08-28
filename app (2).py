import streamlit as st
import pandas as pd
from openai import OpenAI
import os

# Configurar clave API de OpenAI
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Cargar CSV (ajustar nombre si es necesario)
@st.cache_data
def load_data():
    return pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTTfdT08aPWvHj4uX-0MEiDSwFcTTbN7aEd8Hb2nQX7Oqs-B_UWyIygFEI4KG-HXfeyznJ65b-VzQR-/pub?gid=987916598&single=true&output=csv")

df = load_data()

st.title("PadronizaPY - Consulta de Faenas 🐂🥩📊")
st.markdown("Haz preguntas en lenguaje natural sobre los datos y el modelo responderá.")

# Mostrar una muestra de los datos
if st.checkbox("Mostrar datos"):
    st.dataframe(df.head())

# Entrada de pregunta
pregunta = st.text_input("Escribe tu pregunta:", placeholder="¿Cuál fue el promedio de ventas en 2023?")

# Botón para enviar
if st.button("Preguntar") and pregunta:
    # Crear contexto desde los datos
    contexto = df.head(100).to_csv(index=False)

    prompt = f"""Tienes que responder preguntas del usuario usando este dataset como contexto:
---
{contexto}
---
Pregunta del usuario: {pregunta}
Respuesta:"""

    with st.spinner("Pensando..."):
        respuesta = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en análisis de datos, responde con precisión y claridad."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        st.success(respuesta.choices[0].message.content)
