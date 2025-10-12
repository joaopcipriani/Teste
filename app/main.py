from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dateutil import parser
import pandas as pd
from io import StringIO
import os

app = FastAPI()

# Diretórios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# CORS liberado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Página inicial
@app.get("/")
async def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path)

# Variável global para armazenar logs
logs_df = None


def parse_datetime_safe(date_str, time_str):
    """Combina data e hora, ignorando formatos ruins."""
    try:
        return parser.isoparse(f"{date_str} {time_str}")
    except Exception:
        return pd.NaT


@app.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    """Recebe e processa o arquivo de log IIS."""
    global logs_df
    try:
        content = await file.read()
        content_str = content.decode("utf-8", errors="ignore")

        # Captura o cabeçalho de colunas do IIS
        lines = content_str.splitlines()
        field_line = next((line for line in lines if line.startswith("#Fields:")), None)
        if not field_line:
            return {"error": "Linha '#Fields:' não encontrada no log IIS."}

        # Extrai os nomes das colunas
        columns = field_line.replace("#Fields:", "").strip().split()

        # Remove comentários antes do conteúdo
        data_lines = [line for line in lines if not line.startswith("#")]
        data = "\n".join(data_lines)

        # Cria o DataFrame dinamicamente
        logs_df = pd.read_csv(
            StringIO(data),
            sep=r"\s+",
            header=None,
            names=columns,
            on_bad_lines="skip"
        )

        # Cria coluna datetime (caso exista date/time)
        if "date" in logs_df.columns and "time" in logs_df.columns:
            logs_df["datetime"] = logs_df.apply(
                lambda row: parse_datetime_safe(row["date"], row["time"]),
                axis=1
            )
            logs_df = logs_df.dropna(subset=["datetime"])

        return {
            "message": f"Arquivo {file.filename} carregado com sucesso.",
            "rows": len(logs_df),
            "columns": list(logs_df.columns)
        }

    except Exception as e:
        print(f"[ERRO UPLOAD] {e}")
        return {"error": f"Falha ao processar arquivo: {e}"}


@app.get("/logs")
def get_logs(start: str = None, end: str = None, code: int = None):
    """Retorna logs filtrados."""
    global logs_df
    if logs_df is None:
        return {"error": "Nenhum log carregado"}

    df = logs_df.copy()

    if "datetime" in df.columns:
        if start:
            df = df[df["datetime"] >= pd.to_datetime(start, errors="coerce")]
        if end:
            df = df[df["datetime"] <= pd.to_datetime(end, errors="coerce")]

    if code and "sc-status" in df.columns:
        df = df[df["sc-status"] == code]

    # Remove valores NaN para não quebrar o JSON
    df = df.fillna("")

    return df.to_dict(orient="records")
