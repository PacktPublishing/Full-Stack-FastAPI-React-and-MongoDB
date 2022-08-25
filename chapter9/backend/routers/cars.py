from json import load
from math import ceil

from typing import List, Optional

from fastapi import APIRouter, Request, Body, HTTPException, BackgroundTasks


from fastapi_cache.decorator import cache

from models import CarBase

from utils.report import report_pipeline

import joblib
import pandas as pd


router = APIRouter()


@router.get("/all", response_description="List all cars")
async def list_all_cars(
    request: Request,
    min_price: int = 0,
    max_price: int = 100000,
    brand: Optional[str] = None,
    page: int = 1,
) -> List[CarBase]:

    RESULTS_PER_PAGE = 25
    skip = (page - 1) * RESULTS_PER_PAGE

    query = {"price": {"$lt": max_price, "$gt": min_price}}
    if brand:
        query["brand"] = brand

    # count total docs
    pages = ceil(
        await request.app.mongodb["cars"].count_documents(query) / RESULTS_PER_PAGE
    )

    full_query = (
        request.app.mongodb["cars"]
        .find(query)
        .sort("km", -1)
        .skip(skip)
        .limit(RESULTS_PER_PAGE)
    )

    results = [CarBase(**raw_car) async for raw_car in full_query]

    return {"results": results, "pages": pages}


# sample of N cars
@router.get("/sample/{n}", response_description="Sample of N cars")
@cache(expire=60)
async def get_sample(n: int, request: Request):

    query = [
        {"$match": {"year": {"$gt": 2010}}},
        {
            "$project": {
                "_id": 0,
            }
        },
        {"$sample": {"size": n}},
        {"$sort": {"brand": 1, "make": 1, "year": 1}},
    ]

    full_query = request.app.mongodb["cars"].aggregate(query)
    results = [el async for el in full_query]
    return results


# aggregation by model / avg price
@router.get("/brand/{val}/{brand}", response_description="Get brand models by val")
async def brand_price(brand: str, val: str, request: Request):

    query = [
        {"$match": {"brand": brand}},
        {"$project": {"_id": 0}},
        {
            "$group": {"_id": {"model": "$make"}, f"avg_{val}": {"$avg": f"${val}"}},
        },
        {"$sort": {f"avg_{val}": 1}},
    ]

    full_query = request.app.mongodb["cars"].aggregate(query)
    return [el async for el in full_query]


# count cars by brand
@router.get("/brand/count", response_description="Count by brand")
async def brand_count(request: Request):

    query = [{"$group": {"_id": "$brand", "count": {"$sum": 1}}}]

    full_query = request.app.mongodb["cars"].aggregate(query)
    return [el async for el in full_query]


# count cars by make
@router.get("/make/count/{brand}", response_description="Count by brand")
async def brand_count(brand: str, request: Request):

    query = [
        {"$match": {"brand": brand}},
        {"$group": {"_id": "$make", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]

    full_query = request.app.mongodb["cars"].aggregate(query)
    results = [el async for el in full_query]
    return results


@router.post("/email", response_description="Send email")
async def send_mail(
    background_tasks: BackgroundTasks,
    cars_num: int = Body(...),
    email: str = Body(...),
):

    background_tasks.add_task(report_pipeline, email, cars_num)

    return {"Received": {"email": email, "cars_num": cars_num}}


@router.post("/predict", response_description="Predict price")
async def predict(
    brand: str = Body(...),
    make: str = Body(...),
    year: int = Body(...),
    cm3: int = Body(...),
    km: int = Body(...),
):

    print(brand, make, year, cm3, km)
    loaded_model = joblib.load("./random_forest_pipe.joblib")

    # = Body?
    input_data = {
        "brand": brand,
        "make": make,
        "year": year,
        "cm3": cm3,
        "km": km,
    }

    from_db_df = pd.DataFrame(input_data, index=[0])

    prediction = float(loaded_model.predict(from_db_df)[0])
    return {"prediction": prediction}
