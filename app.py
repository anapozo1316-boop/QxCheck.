

import streamlit as st
import pandas as pd

# ======================================
# CONFIGURACIÓN
# ======================================

st.set_page_config(
    page_title="QxCheck",
    layout="wide"
)

# ======================================
# FUNCIONES
# ======================================

def cargar_datos():

    equipos = pd.read_csv("equipos.csv")
    disponibles = pd.read_csv("disponibles.csv")

    equipos = equipos.drop_duplicates()
    disponibles = disponibles.drop_duplicates()

    return equipos, disponibles


def guardar_disponibles(df):

    df.to_csv(
        "disponibles.csv",
        index=False
    )


def guardar_equipos(df):

    df.to_csv(
        "equipos.csv",
        index=False
    )

# ======================================
# CARGAR DATOS
# ======================================

equipos_df, disponibles_df = cargar_datos()

# ======================================
# SIDEBAR
# ======================================

st.sidebar.title("QxCheck")

menu = st.sidebar.radio(

    "Menú",

    [
        "Dashboard",
        "Ver Equipos",
        "Editar Disponibles",
        "Editar Equipos"
    ]
)

# ======================================
# DASHBOARD
# ======================================

if menu == "Dashboard":

    st.title("Dashboard")

    total_equipos = equipos_df["equipo"].nunique()

    st.metric(
        "Total Equipos",
        total_equipos
    )

    st.metric(
        "Instrumentos registrados",
        len(disponibles_df)
    )

# ======================================
# VER EQUIPOS
# ======================================

elif menu == "Ver Equipos":

    st.title("Verificación de Equipos")

    equipos = equipos_df["equipo"].unique()

    equipo_seleccionado = st.selectbox(
        "Selecciona un equipo",
        equipos
    )

    equipo_df = equipos_df[
        equipos_df["equipo"] == equipo_seleccionado
    ]

    resultado = pd.merge(
        equipo_df,
        disponibles_df,
        on="instrumento",
        how="left"
    )

    resultado["cantidad_disponible"] = resultado[
        "cantidad_disponible"
    ].fillna(0)

    resultado["cantidad_disponible"] = resultado[
        "cantidad_disponible"
    ].astype(int)

    resultado["faltante"] = (
        resultado["cantidad_requerida"] -
        resultado["cantidad_disponible"]
    )

    resultado["estado"] = resultado["faltante"].apply(
        lambda x: "🟢 Completo" if x <= 0 else "🔴 Faltante"
    )

    st.dataframe(resultado)

    faltantes = resultado[
        resultado["faltante"] > 0
    ]

    if faltantes.empty:

        st.success("🟢 Equipo completo")

    else:

        st.error("⚠️ Equipo incompleto")

        for _, row in faltantes.iterrows():

            st.warning(
                f"Falta {row['faltante']} de {row['instrumento']}"
            )

# ======================================
# EDITAR DISPONIBLES
# ======================================

elif menu == "Editar Disponibles":

    st.title("Editar Disponibles")

    st.dataframe(disponibles_df)

    instrumento = st.selectbox(
        "Instrumento",
        disponibles_df["instrumento"]
    )

    nueva_cantidad = st.number_input(
        "Nueva cantidad",
        min_value=0,
        step=1
    )

    if st.button("Guardar Disponibles"):

        disponibles_df.loc[
            disponibles_df["instrumento"] == instrumento,
            "cantidad_disponible"
        ] = nueva_cantidad

        guardar_disponibles(disponibles_df)

        st.success("✅ Cantidad actualizada")

# ======================================
# EDITAR EQUIPOS
# ======================================

elif menu == "Editar Equipos":

    st.title("Editar Cantidades Requeridas")

    st.dataframe(equipos_df)

    equipo = st.selectbox(
        "Equipo",
        equipos_df["equipo"].unique()
    )

    instrumentos_equipo = equipos_df[
        equipos_df["equipo"] == equipo
    ]

    instrumento = st.selectbox(
        "Instrumento",
        instrumentos_equipo["instrumento"]
    )

    nueva_cantidad = st.number_input(
        "Nueva cantidad requerida",
        min_value=0,
        step=1
    )

    if st.button("Guardar Equipo"):

        equipos_df.loc[
            (
                equipos_df["equipo"] == equipo
            ) &
            (
                equipos_df["instrumento"] == instrumento
            ),
            "cantidad_requerida"
        ] = nueva_cantidad

        guardar_equipos(equipos_df)

        st.success("✅ Equipo actualizado")

