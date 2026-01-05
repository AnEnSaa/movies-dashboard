import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

st.set_page_config(page_title="Movies Dashboard", layout="wide")
st.title("Movies Dashboard")

# Inicializar Firebase solo una vez
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

# -------- FUNCIÓN REQUERIDA POR LA RÚBRICA --------
def cargar_peliculas():
    docs = db.collection("movies").stream()
    data = []
    for doc in docs:
        movie = doc.to_dict()
        movie["id"] = doc.id
        data.append(movie)
    return pd.DataFrame(data)

# -------- SIDEBAR --------
st.sidebar.header("Opciones")
mostrar_todo = st.sidebar.checkbox("Mostrar todos los filmes")

# -------- LÓGICA PRINCIPAL --------
df = cargar_peliculas()

if df.empty:
    st.warning("No hay películas registradas.")
else:
    if mostrar_todo:
        st.subheader("Tabla de películas")
        st.dataframe(df, use_container_width=True)

        if "rating" in df.columns:
            st.subheader("Rating promedio")
            st.metric("Promedio", round(df["rating"].mean(), 2))
