import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
import os

# Configura tu clave de API
st.set_page_config(page_title="Agente IA - PadronizaPY", layout="wide")
st.title("🤖 Agente Inteligente - Pecuaria Smart")
st.markdown("Hazle preguntas sobre los datos de faena. Ejemplo: **¿Cuál fue el promedio de peso de carcasa?**")

# Lectura del CSV actualizado desde Google Sheets
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTTfdT08aPWvHj4uX-0MEiDSwFcTTbN7aEd8Hb2nQX7Oqs-B_UWyIygFEI4KG-HXfeyznJ65b-VzQR-/pub?gid=987916598&single=true&output=csv"

try:
    df = pd.read_csv(csv_url, sep=',')
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    st.success("Datos cargados correctamente.")
except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.stop()

# Muestra una parte del dataset si el usuario quiere
with st.expander("🔍 Ver datos cargados"):
    st.dataframe(df.head(10))

# Configura el LLM de OpenAI (reemplaza tu clave real)
openai_api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("Falta la clave de API de OpenAI. Defínela como variable de entorno o en Streamlit Secrets.")
    st.stop()

llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = create_pandas_dataframe_agent(llm, df, verbose=False)

# Input del usuario
question = st.text_input("📨 Escribe tu pregunta sobre los datos", placeholder="Ejemplo: ¿Cuál fue el promedio de peso de frigorífico en julio?")

if question:
    with st.spinner("Pensando..."):
        try:
            response = agent.run(question)
            st.markdown(f"**Respuesta:** {response}")
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

# Expander para gráficos rápidos
with st.expander("📊 Crear gráfico rápido"):
    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox("Variable en el eje X", df.columns)
    with col2:
        y_col = st.selectbox("Variable en el eje Y", df.columns)

    chart_type = st.radio("Tipo de gráfico", ["scatter", "line", "bar"], horizontal=True)

    if st.button("Generar gráfico"):
        plt.figure(figsize=(10, 5))
        if chart_type == "scatter":
            sns.scatterplot(data=df, x=x_col, y=y_col)
        elif chart_type == "line":
            sns.lineplot(data=df, x=x_col, y=y_col)
        elif chart_type == "bar":
            sns.barplot(data=df, x=x_col, y=y_col, ci=None)
        plt.xticks(rotation=45)
        st.pyplot(plt)
