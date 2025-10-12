from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dateutil import parser
import pandas as pd
from io import StringIO
import os
import re

app = FastAPI()

# Pasta estática
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve index.html
@app.get("/")
async def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path)

# Variável global
logs_df = None


# === Função segura para parse datetime ===
def parse_datetime_safe(date_str, time_str):
    try:
        dt_str = f"{date_str.strip()} {time_str.strip()}"
        return parser.parse(dt_str)
    except Exception:
        return pd.NaT


# === Upload e leitura do log IIS ===
@app.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    global logs_df
    try:
        content = await file.read()
        content_str = content.decode("utf-8", errors="ignore")

        # Remove comentários e detecta cabeçalho
        lines = [line.strip() for line in content_str.splitlines() if line.strip() and not line.startswith("#")]

        if not lines:
            return {"error": "Arquivo de log vazio ou inválido."}

        # Detectar colunas automaticamente (depois de #Fields: ou padrão)
        match = re.search(r"#Fields:\s*(.*)", content_str)
        if match:
            fields = match.group(1).split()
        else:
            print("⚠️ Linha '#Fields:' não encontrada — usando colunas padrão.")
            fields = ["date", "time", "s-ip", "cs-method", "cs-uri-stem", "sc-status"]

        # Ler log em DataFrame
        logs_df = pd.read_csv(
            StringIO("\n".join(lines)),
            sep=r"\s+",
            names=fields,
            engine="python",
            on_bad_lines="skip",
        )

        # Garantir que existam colunas de data e hora
        if "date" in logs_df.columns and "time" in logs_df.columns:
            logs_df["datetime"] = logs_df.apply(
                lambda r: parse_datetime_safe(r["date"], r["time"]), axis=1
            )
        else:
            logs_df["datetime"] = pd.NaT

        logs_df = logs_df.dropna(subset=["datetime"])

        return {"message": f"Arquivo {file.filename} processado com sucesso!", "rows": len(logs_df)}

    except Exception as e:
        print(f"[ERRO UPLOAD] {e}")
        return {"error": f"Falha ao processar arquivo: {e}"}


# === Endpoint de consulta de logs ===
@app.get("/logs")
def get_logs(start: str = None, end: str = None, code: int = None):
    global logs_df
    if logs_df is None or logs_df.empty:
        return {"error": "Nenhum log carregado."}

    df = logs_df.copy()

    if start:
        df = df[df["datetime"] >= pd.to_datetime(start)]
    if end:
        df = df[df["datetime"] <= pd.to_datetime(end)]
    if code:
        if "sc-status" in df.columns:
            df = df[df["sc-status"] == code]

    # Evita erro de NaN -> JSON
    df = df.replace({pd.NA: None})
    df = df.fillna("")

    return df.to_dict(orient="records")
