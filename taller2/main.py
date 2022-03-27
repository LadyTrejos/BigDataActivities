import os
import pandas as pd
from pymongo import MongoClient

PATH = "/home/lady/Documentos/maestria/BigData/files/spain/"
COLUMNS = [
    "Div",
    "Date",
    "HomeTeam",
    "AwayTeam",
    "FTHG",
    "FTAG",
    "FTR",
    "HTHG",
    "HTAG",
    "HTR",
    "HS",
    "AS",
    "HST",
    "AST",
    "HC",
    "AC",
    "HF",
    "AF",
    "HY",
    "AY",
    "HR",
    "AR"
]


def get_columns_indexes(header):
    indexes = []
    for column in COLUMNS:
        indexes.append(header.index(column))
    return indexes


def load_data():
    collection = mongo_collection("infoligas", "spain")
    os.chdir(PATH)
    for file in os.listdir():
        df = pd.read_csv(file, usecols=COLUMNS, parse_dates=["Date"], dayfirst=True)
        df["Season"] = file.split("_")[1]
        collection.insert_many(df.to_dict("records"))


def mongo_collection(db, collection):
    client = MongoClient("localhost", 27017)
    db = client[db]
    col = db[collection]
    return col


load_data()
