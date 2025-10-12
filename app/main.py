from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dateutil import parser
import pandas as pd
from io import StringIO
import os

app = FastAPI()

# Pasta estática
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

# Serve index.html na raiz
@app.get("/")
async def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html não encontrado."}

# Colunas padrão do log IIS
columns = ["date", "time", "s-ip", "cs-method", "cs-uri-stem", "sc-status"]
logs_df = None

# Função segura para parse de datetime
def parse_datetime_safe(date_str, time_str):
    try:
        clean_str = f"{date_str} {time_str}".split()[0]  # ignora qualquer texto extra
        return parser.isoparse(clean_str)
    except Exception:
        return pd.NaT

# Upload de log IIS
@app.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    global logs_df
    try:
        content = await file.read()
        content_str = content.decode("utf-8")

        # Remove linhas de comentário e vazias
        lines = [line.strip() for line in content_str.splitlines() if line.strip() and not line.startswith("#")]

        # Detecta colunas pelo #Fields: se existir
        columns_detected = None
        for line in content_str.splitlines():
            if line.startswith("#Fields:"):
                columns_detected = line[len("#Fields:"):].strip().split()
                break

        # Usa colunas detectadas ou padrão
        cols = columns_detected if columns_detected else columns

        # Lê CSV da memória
        logs_df = pd.read_csv(
            StringIO("\n".join(lines)),
            sep=r'\s+',
            header=None,
            names=cols,
            on_bad_lines="skip",
            engine="python"
        )

        # Cria coluna datetime
        if "date" in logs_df.columns and "time" in logs_df.columns:
            logs_df["datetime"] = logs_df.apply(lambda row: parse_datetime_safe(row["date"], row["time"]), axis=1)
            logs_df = logs_df.dropna(subset=["datetime"])
        else:
            logs_df["datetime"] = pd.NaT

        # Converte NaN para None para JSON
        result = logs_df.where(pd.notnull(logs_df), None).to_dict(orient="records")

        return {"message": f"Arquivo {file.filename} carregado com sucesso", "rows": len(result), "data": result}

    except Exception as e:
        print(f"[ERRO UPLOAD] {e}")
        return {"error": f"Falha ao processar arquivo: {e}"}

# Endpoint para filtrar logs
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

    # Converte NaN para None para JSON
    result = df.where(pd.notnull(df), None).to_dict(orient="records")
    return {"rows": len(result), "data": result}
