import os

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
        with open(file, "r") as current_file:
            header = current_file.readline().split(",")
            lines = current_file.readlines()
            column_indexes = get_columns_indexes(header)

            file_data = []
            for line in lines:
                line_list = line.split(",")
                useful_columns = [line_list[i] for i in column_indexes]
                data = dict(zip(COLUMNS, useful_columns))
                file_data.append(data)

            collection.insert_many(file_data)


def mongo_collection(db, collection):
    client = MongoClient("localhost", 27017)
    db = client[db]
    col = db[collection]
    return col


load_data()
