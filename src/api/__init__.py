"""
Aetheris — FastAPI Backend
Run with: uvicorn src.api:app --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Dict, Any
import os
import joblib
import pandas as pd
import numpy as np
from src.utils import AQI_HEALTH_ADVICE

app = FastAPI(title="Aetheris API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BEST_MODEL: Any = None
FEATURE_COLS: Optional[List[str]] = None
LATEST_DATA: Optional[Dict[str, Any]] = None

GLOBAL_STATE = {"loaded": False}

def ensure_loaded():
    global BEST_MODEL, FEATURE_COLS, LATEST_DATA
    if GLOBAL_STATE["loaded"]:
        return
    
    # Absolute paths for Vercel
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        model_path = os.path.join(base_dir, "models", "best_model.pkl")
        features_path = os.path.join(base_dir, "data", "processed", "feature_cols.pkl")
        data_path = os.path.join(base_dir, "data", "processed", "aqi_processed.csv")

        if os.path.exists(model_path):
            BEST_MODEL = joblib.load(model_path)
        if os.path.exists(features_path):
            FEATURE_COLS = joblib.load(features_path)
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            df["date"] = pd.to_datetime(df["date"])
            LATEST_DATA = dict(tuple(df.sort_values("date").groupby("area").last().reset_index().groupby("area")))
        
        GLOBAL_STATE["loaded"] = True
        print(f"Serverless state initialized at {base_dir}")
    except Exception as e:
        print(f"CRITICAL VERCEL LOAD ERROR: {e}")

@app.on_event("startup")
def startup():
    ensure_loaded()

class PredictRequest(BaseModel):
    city: str
    state: str
    date: date
    primary_pollutant: Optional[str] = "PM10"


class PredictResponse(BaseModel):
    city: str
    predicted_aqi: float
    category: str
    health_advice: str
    risk: str
    best_time_outside: str


@app.get("/")
def root():
    return {"status": "Aetheris API running", "version": "1.0.0"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    ensure_loaded()
    if BEST_MODEL is None or FEATURE_COLS is None or LATEST_DATA is None:
        raise HTTPException(503, "API is disconnected from ML storage — models not loaded.")

    city_key = req.city
    if city_key not in LATEST_DATA:
        # Fallback to Delhi if city entirely unknown to the ML dataset
        city_key = "Delhi"
        
    latest_row = LATEST_DATA[city_key].copy()
    
    # Update time-based deterministic features
    latest_row["month"] = req.date.month
    latest_row["day"] = req.date.day
    latest_row["day_of_week"] = req.date.weekday()
    latest_row["is_weekend"] = int(req.date.weekday() >= 5)
    
    # Extract only the exact columns the pipeline expects, in the exact order
    try:
        X = latest_row[FEATURE_COLS]
    except KeyError as e:
        raise HTTPException(500, f"Missing historical features to construct prediction: {e}")

    # Predict
    try:
        pred_val = BEST_MODEL.predict(X)[0]
    except Exception as e:
        raise HTTPException(500, f"Model inference failed: {e}")
        
    aqi = float(max(0, min(500, pred_val)))
    
    # Dynamic classification logic matching platform standards
    cat = "Good" if aqi <= 50 else "Satisfactory" if aqi <= 100 else "Moderate" if aqi <= 200 else "Poor" if aqi <= 300 else "Very Poor" if aqi <= 400 else "Severe"
    advice = AQI_HEALTH_ADVICE[cat]
    
    return PredictResponse(
        city=req.city, 
        predicted_aqi=round(aqi, 1), 
        category=cat,
        health_advice=advice["message"], 
        risk=advice["risk"],
        best_time_outside=advice["best_time"]
    )


@app.get("/health/{aqi_value}")
def health_advisory(aqi_value: float):
    cat = "Good" if aqi_value <= 50 else "Satisfactory" if aqi_value <= 100 else "Moderate" if aqi_value <= 200 else "Poor" if aqi_value <= 300 else "Very Poor" if aqi_value <= 400 else "Severe"
    return AQI_HEALTH_ADVICE[cat]
