from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/cars")
async def raw_request(request:Request):
    return {
        "message":request.base_url,
        "all":dir(request)
    }