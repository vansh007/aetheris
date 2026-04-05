# 🌬️ Aetheris — Intelligent Air Quality Prediction & Advisory System

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

**Aetheris** is a production-grade, end-to-end Machine Learning platform engineered to predict, analyze, and visualize Air Quality Index (AQI) dynamics across 291 Indian cities. By leveraging advanced tree-based ensemble learning and rigorous time-series preprocessing, Aetheris provides high-fidelity pollution forecasts and actionable health advisories.

---

## 🚀 Key Features

*   **Zero-Leakage ML Pipeline**: Strictly enforced `TimeSeriesSplit` cross-validation to prevent temporal data leakage and ensure real-world generalizability.
*   **54-Feature Intelligence engine**: Dynamic generation of 7-day lags, 30-day rolling averages, cyclical time encodings, and geographic target encodings.
*   **Synthetic Rebalancing (SMOTE)**: Addressed the massive 160:1 class imbalance between "Satisfactory" and "Severe" days to ensure the model never misses life-threatening pollution spikes.
*   **Live Inference Backend**: A high-performance FastAPI server that reconstructs complex feature vectors on-the-fly for real-time LightGBM predictions.
*   **Modern Analytics Dashboard**: A sleek, dark-themed React interface with interactive Recharts, city-to-city comparisons, and automated health recommendations.

---

## 📊 Performance Leaderboard

After evaluating 9+ algorithms, **LightGBM** (Gradient Boosting) emerged as the champion across both tracks:

### 📈 Regression (Exact AQI Value)
| Metric | Result | Interpretation |
| :--- | :--- | :--- |
| **R² Score** | **0.904** | Explains 90% of atmospheric variance |
| **RMSE** | **20.29** | Average error of only ~4% on the full scale |
| **MAE** | **13.55** | Extremely tight precision for categorical mapping |

### 🎯 Classification (Severity Categories)
| Metric | Result | Status |
| :--- | :--- | :--- |
| **Weighted F1** | **0.875** | Robust balance between Precision & Recall |
| **Recall (Severe)** | **High** | Successfully identifies hazardous days via SMOTE |

---

## 🏗️ System Architecture

```mermaid
graph TD
    A[Kaggle Dataset: 235k Records] --> B[Pipeline: run_02_preprocessing.py]
    B --> C{Feature Engine}
    C --> C1[7d/30d Lags & Rolling]
    C --> C2[Cyclical Time Encodings]
    C --> C3[Location Target Encoding]
    
    B --> D[TimeSeriesSplit & SMOTE]
    D --> E[Model: LightGBM / XGBoost]
    
    E --> F[Serialized best_model.pkl]
    F --> G[FastAPI Production Server]
    
    H[React Frontend] <--> G
    H --> I[Dynamic Dashboard]
    H --> J[City Comparison Tool]
    H --> K[Health Advisory Engine]
```

---

## 🛠️ Installation & Setup

### Backend (Python 3.9+)
```bash
# 1. Setup environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train models
python run_01_eda.py
python run_02_preprocessing.py
python run_03_modeling.py   # Generated best_model.pkl

# 4. Start API
uvicorn src.api:app --reload
```

### Frontend (Node 18+)
```bash
cd frontend
npm install
npm run dev
```

---

## 📁 Project Structure

```text
aetheris/
├── src/
│   ├── api/             # FastAPI Inference Engine
│   ├── models/          # Ensemble Definitions & Logic
│   ├── preprocessing/   # Zero-leakage Engineering
│   └── evaluation/      # Time-Series Validation Suites
├── frontend/            # React + Tailwind + Vite
├── data/                # Raw & Processed data stores
├── reports/figures/     # High-res performance plots
├── models/              # Serialized Production Binaries
└── run_*.py             # Orchestration scripts 01-06
```

---

## 📜 Research Reports
For a deep dive into the methodology, exploratory analysis, and mathematical rationale, please refer to the following documents in the root:
*   [Ultimate_Thesis_Aetheris_Report.md](./Ultimate_Thesis_Aetheris_Report.md) (Complete detailed breakdown)
*   [report.md](./report.md) (Quick summary)

---
**Author**: Project Aetheris (2025)
