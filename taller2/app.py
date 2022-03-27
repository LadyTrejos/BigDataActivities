# streamlit run app.py

import pandas as pd
import streamlit as st
from pymongo import MongoClient

from queries import (
    result_table_agg,
    goals_avg_agg,
    bookings_avg_agg,
    shots_on_target_avg_agg,
    shots_on_target_agg,
    bookings_agg,
)


def no_teams_above_avg():
    return st.markdown("**Ningún equipo superó el promedio** 😟")


def get_result_table(season, team, teams):
    st.title("Tabla de resultados")
    if team == "TODOS":
        result_table = []
        for team in teams:
            result_table.extend(col.aggregate(result_table_agg(season, team)))
    else:
        result_table = col.aggregate(result_table_agg(season, team))
    st.write(
        pd.DataFrame(
            result_table, columns=["EQUIPO", "PJ", "PG", "PP", "GF", "GC", "PTOS"]
        ).sort_values(by="PTOS", ascending=False)
    )


def get_goals_avg(season):
    st.title("Promedio de goles ⚽")
    goals_avg = list(col.aggregate(goals_avg_agg(season)))[0]
    st.markdown(f"**Promedio de goles** ⟶ {round(goals_avg['pg'],2)}")
    st.markdown(f"**Promedio de goles locales** ⟶ {round(goals_avg['pl'],2)}")
    st.markdown(f"**Promedio de goles visitantes** ⟶ {round(goals_avg['pv'],2)}")


def get_bookings_avg(season):
    st.title("Promedio de amonestaciones")
    bookings_avg = list(col.aggregate(bookings_avg_agg(season)))[0]
    st.markdown(
        f"**Promedio de tarjetas amarillas** ⟶ {round(bookings_avg['pta'], 2)} 😐"
    )
    st.markdown(
        f"**Promedio de tarjetas amarillas para locales** ⟶ {round(bookings_avg['ptal'], 2)} 😐"
    )
    st.markdown(
        f"**Promedio de tarjetas amarillas para visitantes** ⟶ {round(bookings_avg['ptav'], 2)} 😐"
    )
    st.markdown(f"**Promedio de tarjetas rojas** ⟶ {round(bookings_avg['ptr'], 2)} 😡")
    st.markdown(
        f"**Promedio de tarjetas rojas para locales** ⟶ {round(bookings_avg['ptrl'], 2)} 😡"
    )
    st.markdown(
        f"**Promedio de tarjetas rojas para visitantes** ⟶ {round(bookings_avg['ptrv'], 2)} 😡"
    )


def _get_top_k_goals(season, teams, goals_avg, mayor=True):
    result_table = []
    for team in teams:
        result_table.extend(col.aggregate(result_table_agg(season, team)))
    df = pd.DataFrame(
        result_table, columns=["EQUIPO", "PJ", "PG", "PP", "GF", "GC", "PTOS"]
    )
    df["G_PROM"] = df["GF"] / df["PJ"]
    if mayor:
        top_k = df[df["G_PROM"] > goals_avg["pg"]]
    else:
        top_k = df[df["G_PROM"] < goals_avg["pg"]]
    top_k.drop(columns=["PG", "PP", "PTOS", "GC"], inplace=True)
    if top_k.shape[0]:
        st.write(top_k.sort_values(by="G_PROM", ascending=False))
    else:
        no_teams_above_avg()


def get_top_k_goals(season, teams):
    st.title("Equipos por encima del promedio de goles ⚽")
    goals_avg = list(col.aggregate(goals_avg_agg(season)))[0]
    st.markdown(f"**Promedio de goles**: {round(goals_avg['pg'], 2)}")

    show_minors_ta = st.checkbox("Mostrar resultados por debajo del promedio ")
    if show_minors_ta:
        _get_top_k_goals(season, teams, goals_avg, mayor=False)
    else:
        _get_top_k_goals(season, teams, goals_avg)


def _get_top_k_shots(season, teams, shots_on_target_avg, mayor=True):
    shots_teams = []
    for team in teams:
        team_shots = list(col.aggregate(shots_on_target_agg(season, team)))[0]
        if mayor and team_shots["TA_PROM"] > shots_on_target_avg:
            shots_teams.append(team_shots)
        if not mayor and team_shots["TA_PROM"] < shots_on_target_avg:
            shots_teams.append(team_shots)

    team_shots_df = pd.DataFrame(shots_teams, columns=["EQUIPO", "TA_PROM"])
    if team_shots_df.shape[0]:
        st.write(team_shots_df.sort_values(by="TA_PROM", ascending=False))
    else:
        no_teams_above_avg()


def get_top_k_shots(season, teams):
    st.title("Equipos por encima del promedio de tiros al arco")
    shots_on_target_avg = list(col.aggregate(shots_on_target_avg_agg(season)))[0]["pst"]
    st.markdown(f"**Promedio de tiros al arco**: {round(shots_on_target_avg, 2)}")

    show_minors_ta = st.checkbox("Mostrar resultados por debajo del promedio.")

    if show_minors_ta:
        _get_top_k_shots(season, teams, shots_on_target_avg, mayor=False)
    else:
        _get_top_k_shots(season, teams, shots_on_target_avg)


def _get_top_k_bookings(season, teams, bookings_avg, mayor=True):
    bookings = []
    for team in teams:
        team_bookings_avg = list(col.aggregate(bookings_agg(season, team)))[0]
        if mayor and team_bookings_avg["A_PROM"] > bookings_avg:
            bookings.append(team_bookings_avg)
        if not mayor and team_bookings_avg["A_PROM"] < bookings_avg:
            bookings.append(team_bookings_avg)

    bookings_df = pd.DataFrame(bookings, columns=["EQUIPO", "A_PROM"])
    if bookings_df.shape[0]:
        st.write(bookings_df.sort_values(by="A_PROM", ascending=False))
    else:
        no_teams_above_avg()


def get_top_k_bookings(season, teams):

    st.title("Equipos por encima del promedio de amonestaciones")
    bookings_avg_list = list(col.aggregate(bookings_avg_agg(season)))[0]
    bookings_avg = bookings_avg_list["pta"] + bookings_avg_list["ptr"]
    st.markdown(f"**Promedio de amonestaciones**: {round(bookings_avg, 2)}")

    show_minors = st.checkbox("Mostrar resultados por debajo del promedio")

    if show_minors:
        _get_top_k_bookings(season, teams, bookings_avg, mayor=False)
    else:
        _get_top_k_bookings(season, teams, bookings_avg)


if __name__ == "__main__":
    client = MongoClient("localhost", 27017)
    db = client.infoligas
    col = db.spain

    # SIDEBAR
    seasons = col.find().distinct("Season")
    season = st.sidebar.selectbox("Temporada: ", seasons)
    teams = col.find({"Season": season}).distinct("HomeTeam")
    team = st.sidebar.selectbox("Equipo: ", ["TODOS"] + teams)
    show_result_table = st.sidebar.checkbox("Tabla de resultados", value=True)
    show_mean_goals = st.sidebar.checkbox("Promedio de goles")
    show_mean_bookings = st.sidebar.checkbox("Promedio de amonestaciones")
    show_top_k_mean_goals = st.sidebar.checkbox(
        "Equipos por encima del promedio de goles"
    )
    show_top_k_mean_shots = st.sidebar.checkbox(
        "Equipos por encima del promedio de tiros al arco"
    )
    show_top_k_mean_bookings = st.sidebar.checkbox(
        "Equipos por encima del promedio de amonestaciones"
    )

    if show_result_table:
        get_result_table(season, team, teams)

    if show_mean_goals:
        get_goals_avg(season)

    if show_mean_bookings:
        get_bookings_avg(season)

    if show_top_k_mean_goals:
        get_top_k_goals(season, teams)

    if show_top_k_mean_shots:
        get_top_k_shots(season, teams)

    if show_top_k_mean_bookings:
        get_top_k_bookings(season, teams)
