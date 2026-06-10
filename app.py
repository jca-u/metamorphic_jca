import streamlit as st
from PIL import Image
import os

st.title("Clasificador de Metapelitas AKFM")

triangulos = {
    "A": {"chl", "kfs", "py"},
    "B": {"bt", "chl", "cld", "kfs"},
    "C": {"bt", "chl", "cld", "kfs"},
    "D": {"bt", "chl", "cld", "ky", "kfs"},
    "E": {"bt", "st", "cld", "chl", "ky"},
    "F": {"bt", "st", "cld", "chl", "kfs", "ky"},
    "G": {"bt", "grt", "st", "cld", "chl", "ky"},
    "H": {"bt", "grt", "st", "chl", "cld", "ky"},
    "I": {"bt", "grt", "st", "chl", "cld", "ky"},
    "J": {"bt", "grt", "st", "chl", "ky"},
    "K": {"bt", "grt", "st", "chl", "ky"},
    "L": {"bt", "grt", "st", "chl", "ky"},
    "M": {"bt", "grt", "st", "ky"},
    "N": {"bt", "grt", "st", "sil"},
    "O": {"bt", "grt", "st", "sil"},
    "P": {"bt", "grt", "sil"},
    "Q": {"bt", "grt", "crd", "sil"},
    "R": {"bt", "grt", "crd", "sil"},
    "S": {"bt", "grt", "crd", "sil"},
    "T": {"bt", "grt", "crd", "sil"},
    "U": {"bt", "grt", "crd", "sil", "opx"}
}

alias = {
    "biotita":"bt","granate":"grt","estaurolita":"st",
    "clorita":"chl","cloritoide":"cld","cianita":"ky",
    "sillimanita":"sil","cordierita":"crd",
    "feldespato":"kfs","ortopiroxeno":"opx",
    "bt":"bt","grt":"grt","st":"st","chl":"chl",
    "cld":"cld","ky":"ky","sil":"sil",
    "crd":"crd","kfs":"kfs","opx":"opx"
}

pesos = {
    "chl":1,"ms":1,"bt":2,"cld":4,"grt":4,
    "st":5,"ky":6,"sil":6,"crd":7,"kfs":8,"opx":10
}

grado = {
    "A":"Muy bajo","B":"Muy bajo","C":"Muy bajo",
    "D":"Bajo","E":"Bajo","F":"Bajo",
    "G":"Medio","H":"Medio","I":"Medio","J":"Medio",
    "K":"Medio-Alto","L":"Medio-Alto",
    "M":"Alto","N":"Alto","O":"Alto","P":"Alto",
    "Q":"Muy alto","R":"Muy alto",
    "S":"Muy alto","T":"Muy alto",
    "U":"Extremo"
}

entrada = st.text_input(
    "Ingrese minerales separados por espacios",
    "bt grt st ky"
)

if st.button("Buscar"):

    minerales_usuario = set()

    for t in entrada.lower().split():
        if t in alias:
            minerales_usuario.add(alias[t])

    resultados = []

    for nombre, minerales in triangulos.items():

        coincidencias = minerales_usuario.intersection(minerales)

        puntaje = sum(
            pesos.get(m,1)
            for m in coincidencias
        )

        faltantes = len(
            minerales_usuario - minerales
        )

        resultados.append(
            (nombre,puntaje,len(coincidencias),faltantes)
        )

    resultados.sort(
        key=lambda x:(x[1],x[2],-x[3]),
        reverse=True
    )

    st.subheader("Top 5 resultados")

    for r in resultados[:5]:

        letra = r[0]

        st.write(
            f"Triángulo {letra} | "
            f"Grado: {grado[letra]}"
        )

        ruta = f"triangulos_N3/{letra}.jpg"

        if os.path.exists(ruta):
            st.image(ruta, width=250)
