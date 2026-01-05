import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

st.set_page_config(page_title="Movies Dashboard", layout="wide")

st.title("Movies Dashboard")

# Inicializar Firebase solo una vez
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["firebase"])
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Leer colección de películas
movies_ref = db.collection("movies")
docs = movies_ref.stream()

data = []
for doc in docs:
    movie = doc.to_dict()
    movie["id"] = doc.id
    data.append(movie)

if len(data) == 0:
    st.warning("No hay películas registradas.")
else:
    df = pd.DataFrame(data)

    st.subheader("Tabla de películas")
    st.dataframe(df, use_container_width=True)

    if "rating" in df.columns:
        st.subheader("Rating promedio")
        st.metric("Promedio", round(df["rating"].mean(), 2))
