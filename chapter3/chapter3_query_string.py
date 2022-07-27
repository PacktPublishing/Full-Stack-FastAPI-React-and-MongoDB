from fastapi import FastAPI

app = FastAPI()

@app.get("/cars/price")
async def cars_by_price(min_price:int=0, max_price:int=100000):
    return{"Message":f"Listing cars with prices between {min_price} and {max_price}"}
