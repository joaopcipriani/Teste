from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from datetime import datetime
import json

app = FastAPI(title="IIS Log Analyzer API")

# allow frontend (dev) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")
ANALYSES_DIR = os.path.join(BASE_DIR, "data", "analyses")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(ANALYSES_DIR, exist_ok=True)

# crude parser for typical IIS W3C logs (space separated, header lines start with '#')
def parse_iis_log(filepath):
    # Read header to infer fields if present
    fields = [
        "date", "time", "s-ip", "cs-method", "cs-uri-stem",
        "cs-uri-query", "s-port", "cs-username", "c-ip",
        "cs(User-Agent)", "sc-status", "sc-substatus",
        "sc-win32-status", "time-taken"
    ]
    try:
        df = pd.read_csv(
            filepath,
            sep=r"\s+",
            comment="#",
            names=fields,
            engine="python",
            header=None,
            dtype=str,
            na_values=['-']
        )
        # convert types
        if 'time-taken' in df.columns:
            df['time-taken'] = pd.to_numeric(df['time-taken'], errors='coerce').fillna(0)
        if 'sc-status' in df.columns:
            df['sc-status'] = pd.to_numeric(df['sc-status'], errors='coerce').fillna(0).astype(int)
        # combine date and time into timestamp if possible
        try:
            df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        except Exception:
            df['timestamp'] = pd.NaT
        return df
    except Exception as e:
        raise

def analyze_dataframe(df):
    total_requests = len(df)
    avg_time = float(df['time-taken'].mean()) if total_requests else 0
    status_counts = df['sc-status'].value_counts().to_dict()
    top_urls = (
        df.groupby('cs-uri-stem')['time-taken']
          .agg(['count','mean'])
          .sort_values('count', ascending=False)
          .reset_index()
          .rename(columns={'count':'hits','mean':'avg_time_ms'})
          .to_dict(orient='records')
    )
    return {
        "total_requests": total_requests,
        "avg_response_time_ms": round(avg_time, 2),
        "status_counts": status_counts,
        "top_urls": top_urls
    }

@app.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    # Save file
    filename = file.filename
    safe_name = filename.replace('..', '_')
    filepath = os.path.join(UPLOAD_DIR, safe_name)
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)

    # Parse and analyze
    try:
        df = parse_iis_log(filepath)
    except Exception as e:
        return {"error": "failed to parse log", "detail": str(e)}

    analysis = analyze_dataframe(df)

    # Save analysis per-file
    analysis_record = {
        "filename": safe_name,
        "processed_at": datetime.utcnow().isoformat() + "Z",
        "analysis": analysis
    }
    out_path = os.path.join(ANALYSES_DIR, safe_name + ".json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(analysis_record, fh, indent=2, ensure_ascii=False)

    return analysis_record

@app.get("/analyze")
def analyze_logs(
    start: datetime = Query(None),
    end: datetime = Query(None),
    status: int = Query(None),
    url_contains: str = Query(None)
):
    # read all analyzed JSON files and filter
    records = []
    for fname in os.listdir(ANALYSES_DIR):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(ANALYSES_DIR, fname), "r", encoding="utf-8") as fh:
            try:
                rec = json.load(fh)
                records.append(rec)
            except Exception:
                continue

    # flatten into a dataframe by reopening original uploads for filtering on timestamps / status / url if requested
    all_rows = []
    for rec in records:
        upload_name = rec['filename']
        upload_path = os.path.join(UPLOAD_DIR, upload_name)
        try:
            df = parse_iis_log(upload_path)
            df['__source_file'] = upload_name
            all_rows.append(df)
        except Exception:
            continue

    if not all_rows:
        return {"message": "no logs processed yet", "results": []}

    df_all = pd.concat(all_rows, ignore_index=True)

    if start:
        df_all = df_all[df_all['timestamp'] >= start]
    if end:
        df_all = df_all[df_all['timestamp'] <= end]
    if status is not None:
        df_all = df_all[df_all['sc-status'] == status]
    if url_contains:
        df_all = df_all[df_all['cs-uri-stem'].str.contains(url_contains, na=False)]

    summary_by_url = (
        df_all.groupby('cs-uri-stem')['time-taken']
              .agg(['count','mean'])
              .reset_index()
              .rename(columns={'count':'hits','mean':'avg_time_ms'})
              .sort_values('hits', ascending=False)
              .to_dict(orient='records')
    )

    overall = {
        "total_requests": len(df_all),
        "summary_by_url": summary_by_url,
        "status_counts": df_all['sc-status'].value_counts().to_dict()
    }
    return overall
