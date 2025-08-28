
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------- CONFIGURACIÓN DE LA APP ----------
st.set_page_config(page_title="PadronizaPY - Consulta de Faenas", layout="wide")
st.title("📋 PadronizaPY - Consulta de Faenas 🐂🥩📊")

# ---------- LOGO ----------
logo_url = "https://i.imgur.com/qxGEh0S.png"  # Reemplazar por tu logo si es necesario
st.image(logo_url, width=150)

# ---------- CARGA DE DATOS DESDE CSV PÚBLICO ----------
url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTTfdT08aPWvHj4uX-0MEiDSwFcTTbN7aEd8Hb2nQX7Oqs-B_UWyIygFEI4KG-HXfeyznJ65b-VzQR-/pub?gid=987916598&single=true&output=csv"

try:
    df = pd.read_csv(url_csv)
    st.success("✅ Datos cargados correctamente desde Google Sheets.")
    st.dataframe(df)

    # ---------- SECCIÓN GPT SIMULADO PARA CONSULTAS ----------
    st.subheader("Pregunta algo sobre los datos 🤠")

    pregunta = st.text_input("Escribe tu pregunta:")
    if pregunta:
        # Concatenar columnas de texto
        texto = df.astype(str).apply(" ".join, axis=1).tolist()
        texto.append(pregunta)

        # TF-IDF + similitud coseno para encontrar filas relevantes
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(texto)
        sims = cosine_similarity(X[-1], X[:-1]).flatten()

        top_idx = sims.argmax()
        st.write("📌 Resultado más relevante:")
        st.write(df.iloc[top_idx])

        # Opción de gráfico simple
        if st.checkbox("📈 Mostrar gráfico de la fila más relevante"):
            st.bar_chart(df.iloc[top_idx].select_dtypes(include='number'))

except Exception as e:
    st.error(f"❌ Error al cargar los datos: {e}")
