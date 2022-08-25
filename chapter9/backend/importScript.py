import csv
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from decouple import config
from models import CarBase

# connect to mongodb
DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)

client = MongoClient(DB_URL)
db = client[DB_NAME]
cars = db["cars"]


#

# read csv
with open("filteredCars.csv", encoding="utf-8") as f:
    csv_reader = csv.DictReader(f)
    name_records = list(csv_reader)


for rec in name_records:
    print(rec)

    try:
        rec["cm3"] = int(rec["cm3"])
        rec["price"] = int(rec["price"])
        rec["year"] = int(rec["year"])
        rec["km"] = int(rec["km"])
        rec["brand"] = str(rec["brand"])
        rec["make"] = str(rec["make"])

        car = jsonable_encoder(CarBase(**rec))
        print("Inserting:", car)
        cars.insert_one(car)

    except ValueError:
        pass
