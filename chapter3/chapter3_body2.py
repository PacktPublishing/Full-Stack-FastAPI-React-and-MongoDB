from fastapi import FastAPI, Body
from pydantic import BaseModel

class InsertUser(BaseModel):
    username: str
    name: str

class InsertCar(BaseModel):
    brand: str
    model: str
    year: int

@app.post("/car/user")
async def new_car_model(
    car: InsertCar,
    user: InsertUser,
    code: int=Body(None) ):
    return {
        "car":car,
        "user":user,
        "code":code
    }
