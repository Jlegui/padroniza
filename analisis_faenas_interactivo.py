
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import requests
from io import StringIO

# Cargar los datos desde el CSV público
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTTfdT08aPWvHj4uX-0MEiDSwFcTTbN7aEd8Hb2nQX7Oqs-B_UWyIygFEI4KG-HXfeyznJ65b-VzQR-/pub?gid=987916598&single=true&output=csv"

def cargar_datos():
    try:
        response = requests.get(URL_CSV)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            return df
        else:
            print("No se pudo cargar el archivo CSV.")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return pd.DataFrame()

def responder_pregunta(pregunta, df):
    pregunta = pregunta.lower()

    if "total" in pregunta and "animales" in pregunta:
        total = df["Cantidad de animales"].sum()
        print(f"Total de animales faenados: {total}")
    elif "promedio" in pregunta and "carcasa" in pregunta:
        promedio = df["Peso de carcasa promedio"].mean()
        print(f"Peso promedio de carcasa: {promedio:.2f} kg")
    elif "grafico" in pregunta or "gráfico" in pregunta:
        if "por ciudad" in pregunta:
            fig = px.bar(df, x="Ciudad", y="Cantidad de animales", title="Faena por ciudad")
            fig.show()
        elif "por frigorífico" in pregunta:
            fig = px.pie(df, names="Frigorífico", values="Cantidad de animales", title="Distribución por frigorífico")
            fig.show()
        elif "por clasificación" in pregunta:
            fig = px.bar(df, x="Clasificación", y="Cantidad de animales", title="Cantidad por clasificación")
            fig.show()
        else:
            print("No se pudo identificar el gráfico solicitado.")
    else:
        print("No entiendo la pregunta. Intenta con: total de animales, promedio de carcasa, gráfico por ciudad...")

def main():
    df = cargar_datos()
    if df.empty:
        return
    while True:
        pregunta = input("\nHaz tu pregunta sobre los datos (o escribe 'salir'): ")
        if pregunta.lower() == "salir":
            break
        responder_pregunta(pregunta, df)

if __name__ == "__main__":
    main()
