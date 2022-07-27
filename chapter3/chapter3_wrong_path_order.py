from fastapi import FastAPI

app = FastAPI()

@app.get("/user/{id}")
async def user(id:int):    
    return {"User_id":id}
    
@app.get("/user/me")
async def user():    
    return {"User_id":"This is me!"}
