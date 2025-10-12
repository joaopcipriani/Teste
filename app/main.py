from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pandas as pd
from datetime import datetime
from io import StringIO
import os

app = FastAPI()

# Configura pasta estática corretamente
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

# Permite requests do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logs_df = None
columns = ["date", "time", "s-ip", "cs-method", "cs-uri-stem", "sc-status"]

@app.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    global logs_df
    content = await file.read()
    content_str = content.decode("utf-8")
    logs_df = pd.read_csv(StringIO(content_str), sep=" ", header=None, names=columns)
    logs_df["datetime"] = pd.to_datetime(logs_df["date"] + " " + logs_df["time"])
    return {"message": f"Arquivo {file.filename} carregado com sucesso", "rows": len(logs_df)}

@app.get("/logs")
def get_logs(start: str = None, end: str = None, code: int = None):
    global logs_df
    if logs_df is None:
        return {"error": "Nenhum log carregado"}

    df = logs_df.copy()
    if start:
        df = df[df["datetime"] >= pd.to_datetime(start)]
    if end:
        df = df[df["datetime"] <= pd.to_datetime(end)]
    if code:
        df = df[df["sc-status"] == code]

    return df.to_dict(orient="records")
