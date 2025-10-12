from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dateutil import parser
import pandas as pd
from io import StringIO
import os

app = FastAPI()

# Configura pasta estática
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Permite CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

columns = ["date", "time", "s-ip", "cs-method", "cs-uri-stem", "sc-status"]
logs_df = None

# Função de parsing de datetime segura
def parse_datetime_safe(date_str, time_str):
    try:
        clean_str = f"{date_str} {time_str}".split()[0]
        return parser.isoparse(clean_str)
    except Exception:
        return pd.NaT

@app.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    global logs_df
    try:
        content = await file.read()
        content_str = content.decode("utf-8")
        lines = [line for line in content_str.splitlines() if not line.startswith("#")]
        data = "\n".join(lines)

        logs_df = pd.read_csv(
            StringIO(data),
            sep=r'\s+',
            header=None,
            names=columns,
            on_bad_lines="skip"
        )

        logs_df["datetime"] = logs_df.apply(lambda row: parse_datetime_safe(row["date"], row["time"]), axis=1)
        logs_df = logs_df.dropna(subset=["datetime"])

        return {"message": f"Arquivo {file.filename} carregado com sucesso", "rows": len(logs_df)}
    except Exception as e:
        print(f"[ERRO UPLOAD] {e}")
        return {"error": f"Falha ao processar arquivo: {e}"}
