from typing import List, Optional

from fastapi import (
    APIRouter,
    Request,
    Body,
    UploadFile,
    File,
    status,
    HTTPException,
    Depends,
    Form,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from io import BytesIO

from decouple import config

from PIL import Image, ImageOps

import cloudinary
import cloudinary.uploader

from models import CarBase, CarDB, CarUpdate

from authentication import AuthHandler

CLOUD_NAME = config("CLOUD_NAME", cast=str)
API_KEY = config("API_KEY", cast=str)
API_SECRET = config("API_SECRET", cast=str)

# configure Cloudinary
cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET,
)

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
    # userId=Depends(auth_handler.auth_wrapper),
) -> List[CarDB]:

    headers = {
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
    }

    RESULTS_PER_PAGE = 25
    skip = (page - 1) * RESULTS_PER_PAGE

    query = {"price": {"$lt": max_price, "$gt": min_price}}
    if brand:
        query["brand"] = brand

    full_query = (
        request.app.mongodb["cars"]
        .find(query)
        .sort("_id", -1)
        .skip(skip)
        .limit(RESULTS_PER_PAGE)
    )

    results = [CarDB(**raw_car) async for raw_car in full_query]

    return results


# create new car with FORM DATA
@router.post("/", response_description="Add new car with picture")
async def create_car_form(
    request: Request,
    brand: str = Form("brand"),
    make: str = Form("make"),
    year: int = Form("year"),
    cm3: int = Form("cm3"),
    price: int = Form("price"),
    km: int = Form("km"),
    picture: UploadFile = File(...),
    userId=Depends(auth_handler.auth_wrapper),
):

    # intercept with Pillow
    original_image = Image.open(picture.file)
    gray_image = ImageOps.posterize(original_image, 2)
    out_image = BytesIO()
    gray_image.save(out_image, "JPEG")
    out_image.seek(0)

    # upload to cloudinary
    result = cloudinary.uploader.upload(
        out_image,
        folder="FARM",
        crop="scale",
        width=800,
    )

    url = result.get("url")

    # go through Pydantic
    car = CarDB(
        brand=brand,
        price=price,
        cm3=cm3,
        km=km,
        make=make,
        year=year,
        picture=url,
        owner=userId,
    )

    car = jsonable_encoder(car)

    new_car = await request.app.mongodb["cars"].insert_one(car)
    created_car = await request.app.mongodb["cars"].find_one(
        {"_id": new_car.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_car)


# get car by ID
@router.get("/{id}", response_description="Get a single car")
async def show_car(id: str, request: Request):
    if (car := await request.app.mongodb["cars"].find_one({"_id": id})) is not None:
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
    findCar = await request.app.mongodb["cars"].find_one({"_id": id})

    if (findCar["owner"] != userId) and user["role"] != "ADMIN":
        raise HTTPException(
            status_code=401, detail="Only the owner or an admin can update the car"
        )

    await request.app.mongodb["cars"].update_one(
        {"_id": id}, {"$set": car.dict(exclude_unset=True)}
    )

    if (car := await request.app.mongodb["cars"].find_one({"_id": id})) is not None:
        return CarDB(**car)

    raise HTTPException(status_code=404, detail=f"Car with {id} not found")


@router.delete("/{id}", response_description="Delete car")
async def delete_task(
    id: str, request: Request, userId=Depends(auth_handler.auth_wrapper)
):

    # check if the car is owned by the user trying to delete it
    try:
        findCar = await request.app.mongodb["cars"].find_one({"_id": id})
        if findCar["owner"] != userId:
            raise HTTPException(
                status_code=401, detail="Only the owner can delete the car"
            )

        delete_result = await request.app.mongodb["cars"].delete_one({"_id": id})

        if delete_result.deleted_count == 1:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

    except TypeError:
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

    full_query = request.app.mongodb["cars"].aggregate(query)
    results = [el async for el in full_query]
    return results
