# a function that returns a sample of N cars
from pymongo import MongoClient
from decouple import config

import pandas as pd

# connect to mongodb
DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)

client = MongoClient(DB_URL)
db = client[DB_NAME]
cars = db["cars"]


def make_query(cars_number: int):

    query = [
        {"$match": {"year": {"$gt": 2010}}},
        {
            "$project": {
                "_id": 0,
            }
        },
        {"$sample": {"size": cars_number}},
        {"$sort": {"brand": 1, "make": 1, "year": 1}},
    ]

    full_query = cars.aggregate(query)
    results = [el for el in full_query]

    HTML = pd.DataFrame(results).to_html(index=False)

    return HTML
