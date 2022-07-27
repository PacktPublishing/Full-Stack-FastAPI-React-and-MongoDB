import csv
from fastapi.encoders import jsonable_encoder



# dotenv environment variables
from dotenv import dotenv_values

from models import CarBase

config = dotenv_values(".env")

# 

# read csv
with open("sample_data.csv",encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    name_records = list(csv_reader)



# Mongo db - we do not need Motor here
from pymongo import MongoClient
client = MongoClient()



client = MongoClient(config['DB_URL'])
db = client[config['DB_NAME']]
cars = db[config['COLLECTION_NAME']]


for rec in name_records[51:250]:
    
    try:
        rec['cm3'] = int(rec['cm3'])
        rec['price'] = int(rec['price'])
        rec['year'] = int(rec['year'])

        if rec['price']>1000:
            car = jsonable_encoder(CarBase(**rec))  
            print("Inserting:",car)
            cars.insert_one(car)

    except ValueError:
        pass
