import streamlit as st
import pandas as pd
import plotly.express as px
import openai
import io

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="PadronizaPY - Consultoría de Faena", layout="wide")
st.image("logo_padronizapy.png", width=250)
st.title("Agente de IA - Consultoría de Faena")

# --- API KEY ---
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else ""

# --- CARGA DE DATOS ---
@st.cache_data
def cargar_datos():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTTfdT08aPWvHj4uX-0MEiDSwFcTTbN7aEd8Hb2nQX7Oqs-B_UWyIygFEI4KG-HXfeyznJ65b-VzQR-/pub?gid=987916598&single=true&output=csv"
    df = pd.read_csv(url, dtype=str)
    return df

df = cargar_datos()

st.subheader("📄 Vista previa de los datos")
st.dataframe(df.head(10), use_container_width=True)

# --- PREGUNTA DEL USUARIO ---
st.subheader("🤖 Hacé una pregunta sobre tus datos de faena")
pregunta = st.text_input("Ejemplo: ¿Cuál fue el frigorífico con más animales en julio 2024?")

# --- PROCESAR PREGUNTA ---
if pregunta and openai.api_key:
    with st.spinner("Procesando con inteligencia artificial..."):

        # Enviar datos + pregunta al modelo
        prompt = f"""
Sos un asistente experto en análisis de datos de faenas ganaderas.
Respondé la siguiente pregunta en español con base en los datos que te paso.

Pregunta: {pregunta}

Datos (formato tabla CSV):
{df.head(100).to_csv(index=False)}

Tu respuesta debe incluir:
- Un resumen claro y directo
- Si aplica, sugerí un gráfico que represente la respuesta
- Si aplica, indicá columnas que se podrían mostrar en una tabla

Respondé solo con texto, sin código.
"""

        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        mensaje = respuesta['choices'][0]['message']['content']
        st.markdown("### 📌 Respuesta:")
        st.markdown(mensaje)

        # Mostrar la tabla completa si el usuario lo desea
        if st.checkbox("Mostrar todos los datos (completos)"):
            st.dataframe(df, use_container_width=True)
else:
    st.info("Ingresá una pregunta arriba y asegurate de tener tu OpenAI API Key configurada.")

# --- FOOTER ---
st.markdown("---")
st.markdown("Desarrollado por **PadronizaPY** · Consultoría de Faena")
