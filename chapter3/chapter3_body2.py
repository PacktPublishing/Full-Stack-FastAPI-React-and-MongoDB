from fastapi import FastAPI, Body
from pydantic import BaseModel


class InsertUser(BaseModel):
    username: str
    name: str


class InsertCar(BaseModel):
    brand: str
    model: str
    year: int


app = FastAPI()


@app.post("/car/user")
async def new_car_model(car: InsertCar, user: InsertUser, code: int = Body(None)):
    return {"car": car, "user": user, "code": code}


""" 
Example of input for REST client - Insomnia, HTTPie

{
	"car":{
		"brand":"some brand",
		"model":"some model",
		"year":2002
	},
	"user":{
		"username":"Mike",
		"name":"Michael Jones"
	}
}
 """
