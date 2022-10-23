from fastapi import FastAPI, Body
from pydantic import BaseModel

# the following is necessary for handling the Body, which comes in a dictionary
from typing import Dict


class InsertCar(BaseModel):
    brand: str
    model: str
    year: int


# the InsertCar model is NOT used here, so everything just flows through the endpoint

app = FastAPI()


@app.post("/cars")
async def new_car(data: Dict = Body(...)):
    print(data)
    return {"message": data}
