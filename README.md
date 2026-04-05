# 🌬️ Aetheris — Intelligent Air Quality Prediction & Advisory System

End-to-end ML system that predicts AQI for Indian cities, analyzes pollution trends, detects anomalies, and provides health recommendations.

## Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place dataset
# Download aqi.csv from Kaggle → put in data/raw/aqi.csv

# 4. Run scripts in order
python run_01_eda.py
python run_02_preprocessing.py
python run_03_modeling.py
python run_04_timeseries.py
python run_05_clustering.py
python run_06_evaluation.py
```

## Project Structure

```
aetheris/
├── data/raw/aqi.csv              ← PUT YOUR DATASET HERE
├── data/processed/               ← Auto-generated
├── src/
│   ├── preprocessing/            ← Cleaning & feature engineering
│   ├── models/                   ← Model definitions & training
│   ├── evaluation/               ← Metrics & plots
│   ├── visualization/            ← EDA & dashboard charts
│   ├── api/                      ← FastAPI backend
│   └── utils/                    ← Constants, config, helpers
├── reports/figures/              ← Saved plots
├── models/                       ← Saved .pkl models
├── config/config.yaml            ← All settings
├── run_01_eda.py                 ← Step 1: Explore data
├── run_02_preprocessing.py       ← Step 2: Clean & engineer features
├── run_03_modeling.py            ← Step 3: Train & compare models
├── run_04_timeseries.py          ← Step 4: ARIMA/Prophet forecasting
├── run_05_clustering.py          ← Step 5: Cluster cities & detect anomalies
├── run_06_evaluation.py          ← Step 6: Final report
└── requirements.txt
```

## Dataset
- **Source**: India AQI Dataset 2023-2025 (Kaggle)
- **Records**: 235,785 | **States**: 32 | **Cities**: 291

## Models Compared
**Regression** (predict AQI value): Linear, Ridge, Lasso, KNN, Random Forest, Gradient Boosting, XGBoost, LightGBM, CatBoost
**Classification** (predict AQI category): Random Forest, XGBoost, LightGBM, CatBoost — all with SMOTE
**Time Series**: ARIMA, Prophet
**Clustering**: K-Means, DBSCAN, Hierarchical
**Anomaly Detection**: Isolation Forest
