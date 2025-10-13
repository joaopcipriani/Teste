from fastapi import FastAPI, UploadFile, File
from analyzer import analyze_dump

app = FastAPI()

@app.post("/upload")
async def upload_dump(file: UploadFile = File(...)):
    content = await file.read()
    result = analyze_dump(content)
    return {"result": result}
