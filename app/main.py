from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dateutil import parser
import pandas as pd
from io import StringIO
import os

app = FastAPI()

# === CONFIGURAÇÃO DE PASTAS ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# === CORS LIBERADO ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === SERVE FRONTEND ===
@app.get("/")
async def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        return {"error": "index.html não encontrado."}
    return FileResponse(index_path)


# === CONFIGURAÇÃO DO LOG ===
columns = ["date", "time", "s-ip", "cs-method", "cs-uri-stem", "sc-status"]
logs_df = None


# === PARSE SEGURO DE DATETIME ===
def parse_datetime_safe(date_str, time_str):
    try:
        clean_str = f"{date_str} {time_str}".strip()
        return parser.isoparse(clean_str)
    except Exception:
        return pd.NaT


# === UPLOAD DE LOG IIS ===
@app.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    global logs_df
    try:
        content = await file.read()
        content_str = content.decode("utf-8", errors="ignore")

        # Remove comentários do log
        lines = [line for line in content_str.splitlines() if not line.startswith("#")]
        data = "\n".join(lines)

        # Lê log em formato CSV simples
        df = pd.read_csv(
            StringIO(data),
            sep=r"\s+",
            header=None,
            names=columns,
            on_bad_lines="skip",
            engine="python"
        )

        # Gera coluna datetime e limpa inválidos
        df["datetime"] = df.apply(lambda row: parse_datetime_safe(row["date"], row["time"]), axis=1)
        df = df.dropna(subset=["datetime"])

        logs_df = df
        return {"message": f"Arquivo {file.filename} carregado com sucesso", "rows": len(df)}

    except Exception as e:
        print(f"[ERRO UPLOAD] {e}")
        return {"error": f"Falha ao processar arquivo: {e}"}


# === ENDPOINT DE LOGS FILTRADOS, PAGINADOS E ORDENADOS ===
@app.get("/logs")
def get_logs(
    start: str = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end: str = Query(None, description="Data final (YYYY-MM-DD)"),
    code: int = Query(None, description="Código de status HTTP (ex: 404)"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(100, ge=1, le=1000, description="Tamanho da página"),
    sort: str = Query("desc", pattern="^(asc|desc)$", description="Ordenação (asc ou desc)")
):
    global logs_df
    if logs_df is None:
        return {"error": "Nenhum log carregado"}

    df = logs_df.copy()

    # === FILTROS ===
    if start:
        df = df[df["datetime"] >= pd.to_datetime(start)]
    if end:
        df = df[df["datetime"] <= pd.to_datetime(end)]
    if code:
        df = df[df["sc-status"] == code]

    # === ORDENAÇÃO ===
    df = df.sort_values(by="datetime", ascending=(sort == "asc"))

    # === PAGINAÇÃO ===
    total = len(df)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    df_page = df.iloc[start_idx:end_idx]

    # === CONVERSÃO SEGURA PARA JSON ===
    df_page = df_page.replace({pd.NA: None, pd.NaT: None, float("nan"): None})
    df_page["datetime"] = df_page["datetime"].astype(str)

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total // page_size) + (1 if total % page_size else 0),
        "data": df_page.to_dict(orient="records")
    }
