import streamlit as st
import pandas as pd
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.PQR_salud

MESES = {
    "ENERO": 1,
    "FEBRERO": 2,
    "MARZO": 3,
    "ABRIL": 4,
    "MAYO": 5,
    "JUNIO": 6,
    "JULIO": 7,
    "AGOSTO": 8,
    "SEPTIEMBRE": 9,
    "OCTUBRE": 10,
    "NOVIEMBRE": 11,
    "DICIEMBRE": 12,
}
mes = st.sidebar.selectbox("Mes: ", MESES.keys())
pet_dpto = st.sidebar.selectbox("Departamento: ", db.quejas.distinct("pet_dpto"))
pet_mpio = st.sidebar.selectbox(
    "Municipio: ", db.quejas.find({"pet_dpto": pet_dpto}).distinct("pet_mpio")
)
quejas = db.quejas.find(
    {"mes": MESES[mes], "pet_dpto": pet_dpto.upper(), "pet_mpio": pet_mpio.upper()},
    {"_id": 0, "mes": 1, "pet_dpto": 1, "pet_mpio": 1, "macromotivo": 1},
)
quejas_df = pd.DataFrame(quejas)

if quejas_df.shape[0]:
    st.bar_chart(quejas_df["macromotivo"].value_counts(), height=500)
    st.write(quejas_df)
else:
    st.write("No hay datos.")
