import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Clasificador Metamórfico", layout="wide")

st.title("🔬 Clasificador Metamórfico")
st.write("Identificación de metapelitas AKFM y metabasitas ACF")

# =====================================================
# METAPELITAS
# =====================================================

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

alias_metapelitas = {
    "biotita":"bt",
    "granate":"grt",
    "estaurolita":"st",
    "clorita":"chl",
    "cloritoide":"cld",
    "cianita":"ky",
    "sillimanita":"sil",
    "cordierita":"crd",
    "muscovita":"ms",
    "moscovita":"ms",
    "feldespato":"kfs",
    "feldespato_potasico":"kfs",
    "ortopiroxeno":"opx",

    "bt":"bt",
    "grt":"grt",
    "st":"st",
    "chl":"chl",
    "cld":"cld",
    "ky":"ky",
    "sil":"sil",
    "crd":"crd",
    "ms":"ms",
    "kfs":"kfs",
    "opx":"opx"
}

pesos_metapelitas = {
    "chl":1,
    "ms":1,
    "bt":2,
    "cld":4,
    "grt":4,
    "st":5,
    "ky":6,
    "sil":6,
    "crd":7,
    "kfs":8,
    "opx":10
}

grado = {
    "A":"Muy bajo",
    "B":"Muy bajo",
    "C":"Muy bajo",
    "D":"Bajo",
    "E":"Bajo",
    "F":"Bajo",
    "G":"Medio",
    "H":"Medio",
    "I":"Medio",
    "J":"Medio",
    "K":"Medio-Alto",
    "L":"Medio-Alto",
    "M":"Alto",
    "N":"Alto",
    "O":"Alto",
    "P":"Alto",
    "Q":"Muy alto",
    "R":"Muy alto",
    "S":"Muy alto",
    "T":"Muy alto",
    "U":"Extremo"
}

# =====================================================
# METABASITAS
# =====================================================

facies_metabasitas = {
    "zeolita": {
        "heulandita","laumontita","wairakita",
        "clorita","calcita","cianita",
        "albita","cuarzo"
    },

    "pp_inferior": {
        "prehnita","epidota","zoisita",
        "calcita","clorita",
        "albita","cuarzo","cianita"
    },

    "pp_superior": {
        "prehnita","epidota","actinolita",
        "zoisita","clorita",
        "cuarzo","albita","calcita"
    },

    "esquisto_verde": {
        "actinolita","clorita","epidota",
        "zoisita","calcita",
        "talco","cloritoide",
        "cuarzo","albita"
    },

    "anfibolita": {
        "hornblenda","plagioclasa","granate",
        "cuarzo","calcita",
        "clinopiroxeno","biotita",
        "sillimanita","muscovita"
    },

    "granulita": {
        "ortopiroxeno","clinopiroxeno",
        "plagioclasa","andalucita",
        "sillimanita","muscovita",
        "cordierita","cuarzo",
        "calcita"
    }
}

# =====================================================
# INTERFAZ
# =====================================================

tipo = st.selectbox(
    "Tipo de roca",
    ["Metapelita (AKFM)", "Metabasita (ACF)"]
)

entrada = st.text_input(
    "Minerales observados",
    placeholder="Ej: bt grt st ky"
)

if st.button("Buscar"):

    # =================================================
    # METAPELITAS
    # =================================================

    if tipo == "Metapelita (AKFM)":

        minerales_usuario = set()

        for t in entrada.lower().split():
            if t in alias_metapelitas:
                minerales_usuario.add(alias_metapelitas[t])

        resultados = []

        for nombre, minerales in triangulos.items():

            coincidencias = minerales_usuario.intersection(minerales)

            puntaje = sum(
                pesos_metapelitas.get(m,1)
                for m in coincidencias
            )

            faltantes = len(
                minerales_usuario - minerales
            )

            resultados.append(
                (
                    nombre,
                    puntaje,
                    len(coincidencias),
                    faltantes
                )
            )

        resultados.sort(
            key=lambda x:(x[1],x[2],-x[3]),
            reverse=True
        )

        st.subheader("Top 5 triángulos más probables")

        cols = st.columns(5)

        for col, r in zip(cols, resultados[:5]):

            nombre = r[0]

            with col:

                st.write(
                    f"**{nombre}**"
                )

                st.write(
                    grado[nombre]
                )

                ruta = f"triangulos_N3/{nombre}.jpg"

                if os.path.exists(ruta):
                    st.image(ruta)

    # =================================================
    # METABASITAS
    # =================================================

    else:

        minerales_usuario = set(
            entrada.lower().split()
        )

        resultados = []

        for facies, minerales in facies_metabasitas.items():

            coincidencias = minerales_usuario.intersection(minerales)

            resultados.append(
                (
                    facies,
                    len(coincidencias)
                )
            )

        resultados.sort(
            key=lambda x:x[1],
            reverse=True
        )

        mejor = resultados[0][0]

        st.subheader(
            f"Facies más probable: {mejor}"
        )

        ruta = f"metabasitas/{mejor}.jpg"

        if os.path.exists(ruta):
            st.image(ruta)

        st.subheader("Ranking")

        for nombre, puntaje in resultados:
            st.write(
                f"{nombre}: {puntaje} coincidencias"
            )
