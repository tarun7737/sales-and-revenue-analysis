
"""FastAPI backend for browser/mobile clients; CSV uploads are processed in memory."""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from src.data import clean_sales_data
from src.analytics import make_report
from src.sample_data import make_sample_data

app = FastAPI(title="Sales & Revenue Analytics API", version="1.0.0")
# Local React dev server origins. Replace with the exact deployed frontend origin in production.
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
                   allow_credentials=True, allow_methods=["GET","POST"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/analytics/demo")
def demo():
    df,warnings=clean_sales_data(make_sample_data())
    return make_report(df,warnings)

@app.post("/analytics/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(400,"Upload a CSV file.")
    try:
        raw=pd.read_csv(io.BytesIO(await file.read()))
        df,warnings=clean_sales_data(raw)
        return make_report(df,warnings)
    except Exception as exc:
        raise HTTPException(422,str(exc))
