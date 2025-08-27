import pandas as pd
import openai
import plotly.express as px
import os

# Configurar tu API Key desde variable de entorno o secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

# URL del CSV de Google Sheets
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTTfdT08aPWvHj4uX-0MEiDSwFcTTbN7aEd8Hb2nQX7Oqs-B_UWyIygFEI4KG-HXfeyznJ65b-VzQR-/pub?gid=987916598&single=true&output=csv"

# Cargar los datos desde el CSV online
def cargar_datos():
    df = pd.read_csv(CSV_URL, sep=';', encoding='utf-8', on_bad_lines='skip')
    return df

# Limpiar nombres de columnas
def limpiar_datos(df):
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df

# Preguntar a OpenAI e interpretar si hay que graficar
def responder_pregunta_con_grafico(pregunta, df):
    prompt = f"""
Sos un analista experto en faenas ganaderas. Tenés una tabla con estas columnas:
{list(df.columns)}

Te paso una pregunta del usuario: "{pregunta}"

Quiero que respondas lo siguiente:
1. RESPUESTA: texto claro y directo basado en los datos.
2. GRAFICO: si se puede graficar algo relacionado, indicá las columnas para eje X e Y en este formato:
GRAFICO: x=columna_x, y=columna_y, tipo=tipo_de_grafico
Si no se puede graficar, escribí GRAFICO: NO

Ejemplo de salida:
RESPUESTA: El frigorífico con más animales fue...
GRAFICO: x=ciudad, y=precio_del_gordo, tipo=barras

Usá solo columnas presentes en los datos. No inventes nada.
Primeras filas de la tabla:
{df.head(5).to_string()}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    contenido = response['choices'][0]['message']['content']
    partes = contenido.split("GRAFICO:")
    texto = partes[0].replace("RESPUESTA:", "").strip()
    grafico = partes[1].strip() if len(partes) > 1 else "NO"

    return texto, grafico

# Generar gráfico con Plotly
def mostrar_grafico(df, grafico):
    try:
        if "NO" in grafico:
            return None

        # Extraer info
        partes = grafico.replace(" ", "").split(",")
        x = partes[0].split("=")[1]
        y = partes[1].split("=")[1]
        tipo = partes[2].split("=")[1]

        df[y] = pd.to_numeric(df[y], errors="coerce")

        if tipo == "barras":
            fig = px.bar(df, x=x, y=y, title=f"{y} por {x}")
        elif tipo == "linea":
            fig = px.line(df, x=x, y=y, title=f"{y} en el tiempo")
        elif tipo == "dispersión":
            fig = px.scatter(df, x=x, y=y, title=f"{x} vs {y}")
        else:
            return None

        fig.show()
    except Exception as e:
        print("No se pudo generar el gráfico:", e)

# Ejecución principal
if __name__ == "__main__":
    pregunta = input("¿Qué querés saber sobre los datos? ➜ ")

    df = cargar_datos()
    df = limpiar_datos(df)

    respuesta, grafico = responder_pregunta_con_grafico(pregunta, df)

    print("\n🧠 Respuesta basada en datos:")
    print(respuesta)

    if "NO" not in grafico:
        print("\n📊 Generando gráfico sugerido por IA...")
        mostrar_grafico(df, grafico)
