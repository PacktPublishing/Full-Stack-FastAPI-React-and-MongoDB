from fastapi import FastAPI, Form, File, UploadFile 
app = FastAPI()

@app.post("/upload")
async def upload(file:UploadFile=File(...), brand:str=Form(...), model:str=Form(...)):
    
    return {
        "brand": brand,
        "model": model,
        "file_name":file.filename}
