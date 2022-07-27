from fastapi import FastAPI

app = FastAPI()

@app.get("/car/{id}")
async def root(id):

    return {"car_id":id}


@app.get("/carh/{id}")
async def hinted_car_id(id:int):
   
    return {"car_id":id}
