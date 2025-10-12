from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

# Rota raiz serve o index.html
@app.get("/")
async def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html não encontrado."}

# Colunas esperadas do log IIS
columns = ["date", "time", "s-ip", "cs-method", "cs-uri-stem", "sc-status"]
logs_df = None

# Upload do log IIS
@app.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    global logs_df
    try:
        content = await file.read()
        content_str = content.decode("utf-8")

        # Ignora linhas de comentário
        lines = [line for line in content_str.splitlines() if not line.startswith("#")]
        data = "\n".join(lines)

        # Lê CSV do log, ignora linhas com colunas erradas
        logs_df = pd.read_csv(
            StringIO(data),
            delim_whitespace=True,
            header=None,
            names=columns,
            on_bad_lines="skip"
        )

        # Cria coluna datetime para filtro
        logs_df["datetime"] = pd.to_datetime(logs_df["date"] + " " + logs_df["time"])
        return {"message": f"Arquivo {file.filename} carregado com sucesso", "rows": len(logs_df)}
    except Exception as e:
        print(f"[ERRO UPLOAD] {e}")
        return {"error": f"Falha ao processar arquivo: {e}"}

# Filtrar logs
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
