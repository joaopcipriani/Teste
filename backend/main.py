from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from analyzer import analyze_dump

app = FastAPI(title="Dump Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_dump(file: UploadFile = File(...)):
    content = await file.read()
    result = analyze_dump(content)
    return {"result": result}

@app.get("/")
def root():
    return {"status": "ok"}
