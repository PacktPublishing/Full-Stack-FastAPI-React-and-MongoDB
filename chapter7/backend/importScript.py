import csv
from fastapi.encoders import jsonable_encoder

import random



from decouple import config

from models import CarBase2



# 

# read csv
with open("sample_data.csv",encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    name_records = list(csv_reader)



# Mongo db - we do not need Motor here
from pymongo import MongoClient
client = MongoClient()

DB_URL = config('DB_URL', cast=str)
DB_NAME = config('DB_NAME', cast=str)


client = MongoClient(DB_URL)
db = client[DB_NAME]
cars = db['cars2']

users = db['users']


ids_list = []
all_users=users.find({})

for x in all_users:
    ids_list.append(x['_id'])

print(ids_list)
for rec in name_records[1:250]:
    
    try:
        rec['cm3'] = int(rec['cm3'])
        rec['price'] = int(rec['price'])
        rec['year'] = int(rec['year'])
        rec['owner'] = random.choice(ids_list)

        if rec['price']>1000:
            car = jsonable_encoder(CarBase2(**rec))  
            print("Inserting:",car)
            cars.insert_one(car)

    except ValueError:
        pass
