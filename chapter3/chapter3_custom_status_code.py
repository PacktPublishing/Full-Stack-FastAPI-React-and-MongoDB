from fastapi import FastAPI, status

app = FastAPI()

@app.get("/", status_code=status.HTTP_208_ALREADY_REPORTED)
async def raw_fa_response():
    return {
        "message":"fastapi response"
    }


@app.post("/carsmodel")
async def new_car_model(car:InsertCar):
    if car.year>2022:
        raise HTTPException(
        status.HTTP_406_NOT_ACCEPTABLE,
        detail="The car doesn’t exist yet!"
    )
    return {
        "message":car
    }
