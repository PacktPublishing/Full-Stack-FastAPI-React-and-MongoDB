from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Success!"}

@app.post("/")
async def post_root():
    return {"message": "Post request success"}  



# uvicorn chapter3_first_endpoint:app --reload 
