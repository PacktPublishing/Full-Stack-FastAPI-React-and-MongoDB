from typing import List, Optional

from fastapi import APIRouter, Request, Body, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models import CarBase, CarDB, CarUpdate

from authentication import AuthHandler

router = APIRouter()

# instantiate the Auth Handler
auth_handler = AuthHandler()


@router.get("/", response_description="List all cars")
async def list_all_cars(
    request: Request,
    min_price: int = 0,
    max_price: int = 100000,
    brand: Optional[str] = None,
    page: int = 1,
    userId=Depends(auth_handler.auth_wrapper),
) -> List[CarDB]:

    RESULTS_PER_PAGE = 25
    skip = (page - 1) * RESULTS_PER_PAGE

    query = {"price": {"$lt": max_price, "$gt": min_price}}
    if brand:
        query["brand"] = brand

    full_query = (
        request.app.mongodb["cars2"]
        .find(query)
        .sort("_id", -1)
        .skip(skip)
        .limit(RESULTS_PER_PAGE)
    )

    results = [CarDB(**raw_car) async for raw_car in full_query]

    return results


# create new car
@router.post("/", response_description="Add new car")
async def create_car(
    request: Request,
    car: CarBase = Body(...),
    userId=Depends(auth_handler.auth_wrapper),
):

    car = jsonable_encoder(car)
    car["owner"] = userId

    new_car = await request.app.mongodb["cars2"].insert_one(car)
    created_car = await request.app.mongodb["cars2"].find_one(
        {"_id": new_car.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_car)


# get car by ID
@router.get("/{id}", response_description="Get a single car")
async def show_car(id: str, request: Request):
    if (car := await request.app.mongodb["cars2"].find_one({"_id": id})) is not None:
        return CarDB(**car)
    raise HTTPException(status_code=404, detail=f"Car with {id} not found")


@router.patch("/{id}", response_description="Update car")
async def update_task(
    id: str,
    request: Request,
    car: CarUpdate = Body(...),
    userId=Depends(auth_handler.auth_wrapper),
):

    # check if the user trying to modify is an admin:
    user = await request.app.mongodb["users"].find_one({"_id": userId})

    # check if the car is owned by the user trying to modify it
    findCar = await request.app.mongodb["cars2"].find_one({"_id": id})

    if (findCar["owner"] != userId) and user["role"] != "ADMIN":
        raise HTTPException(
            status_code=401, detail="Only the owner or an admin can update the car"
        )

    await request.app.mongodb["cars2"].update_one(
        {"_id": id}, {"$set": car.dict(exclude_unset=True)}
    )

    if (car := await request.app.mongodb["cars2"].find_one({"_id": id})) is not None:
        return CarDB(**car)

    raise HTTPException(status_code=404, detail=f"Car with {id} not found")


@router.delete("/{id}", response_description="Delete car")
async def delete_task(
    id: str, request: Request, userId=Depends(auth_handler.auth_wrapper)
):

    # check if the car is owned by the user trying to delete it
    findCar = await request.app.mongodb["cars2"].find_one({"_id": id})

    if findCar["owner"] != userId:
        raise HTTPException(status_code=401, detail="Only the owner can delete the car")

    delete_result = await request.app.mongodb["cars2"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

    raise HTTPException(status_code=404, detail=f"Car with {id} not found")


# optional
@router.get("/brand/{brand}", response_description="Get brand overview")
async def brand_price(brand: str, request: Request):

    query = [
        {"$match": {"brand": brand}},
        {"$project": {"_id": 0, "price": 1, "year": 1, "make": 1}},
        {
            "$group": {"_id": {"model": "$make"}, "avgPrice": {"$avg": "$price"}},
        },
        {"$sort": {"avgPrice": 1}},
    ]

    full_query = request.app.mongodb["cars2"].aggregate(query)

    results = [el async for el in full_query]

    return results
