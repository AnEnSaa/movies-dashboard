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

# -------- FUNCIÓN --------
def cargar_peliculas():
    docs = db.collection("movies").stream()
    data = []
    for doc in docs:
        movie = doc.to_dict()
        movie["id"] = doc.id
        data.append(movie)
    return pd.DataFrame(data)

df = cargar_peliculas()

if df.empty:
    st.warning("No hay películas registradas.")
    df = pd.DataFrame(columns=["name", "genre", "director", "company"])

# -------- SIDEBAR --------
st.sidebar.header("Opciones")

mostrar_todo = st.sidebar.checkbox("Mostrar todos los filmes")

titulo_busqueda = st.sidebar.text_input("Buscar por título")
buscar_titulo = st.sidebar.button("Buscar por título")

directores = sorted(df["director"].dropna().unique())
director_seleccionado = st.sidebar.selectbox(
    "Selecciona un director", directores
)
buscar_director = st.sidebar.button("Filtrar por director")

# -------- MOSTRAR TODO --------
if mostrar_todo:
    st.subheader("Tabla de películas")
    st.dataframe(df, use_container_width=True)

# -------- BÚSQUEDA POR TÍTULO --------
if buscar_titulo and titulo_busqueda:
    resultado = df[
        df["name"].str.contains(titulo_busqueda, case=False, na=False)
    ]
    st.subheader("Resultado de búsqueda por título")
    st.dataframe(resultado, use_container_width=True)

# -------- FILTRO POR DIRECTOR --------
if buscar_director:
    filtrado = df[df["director"] == director_seleccionado]
    st.subheader(f"Películas dirigidas por {director_seleccionado}")
    st.dataframe(filtrado, use_container_width=True)

# -------- FORMULARIO DE INSERCIÓN --------
st.subheader("Agregar nueva película")

with st.form("form_pelicula"):
    name = st.text_input("Nombre de la película")
    genre = st.text_input("Género")
    director = st.text_input("Director")
    company = st.text_input("Compañía productora")

    submitted = st.form_submit_button("Guardar película")

    if submitted:
        if name and genre and director and company:
            db.collection("movies").add({
                "name": name,
                "genre": genre,
                "director": director,
                "company": company
            })
            st.success("🎉 Película guardada correctamente")
            st.rerun()
        else:
            st.error("Todos los campos son obligatorios")

# -------- MÉTRICA --------
if "rating" in df.columns:
    st.subheader("Rating promedio")
    st.metric("Promedio", round(df["rating"].mean(), 2))
