"""
Aetheris — Step 2: Data Cleaning, Feature Engineering, Train/Test Split
Run: python run_02_preprocessing.py

NOTE: The train/test split index is computed BEFORE feature engineering
so that aggregate stats and target encodings use training data only,
preventing data leakage.
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import StandardScaler
from src.utils import ensure_dirs
from src.preprocessing import full_clean_pipeline
from src.preprocessing.feature_engineering import full_feature_pipeline
from src.visualization import plot_correlation_with_target

FIG = "reports/figures"
PROCESSED = "data/processed"


def main():
    ensure_dirs()
    print("=" * 60)
    print("  AETHERIS — Step 2: Preprocessing & Feature Engineering")
    print("=" * 60)

    # ── 1. Clean ──
    print("\n--- Stage 1: Cleaning ---")
    df = full_clean_pipeline("data/raw/aqi.csv")

    # ── 2. Sort by date for proper time-based splitting ──
    df = df.sort_values("date").reset_index(drop=True)

    # ── 3. Compute split index BEFORE feature engineering ──
    # This ensures aggregate features and target encodings use train data only
    split_idx = int(len(df) * 0.8)
    print(f"\n[SPLIT] Train/test boundary at row {split_idx:,} of {len(df):,}")
    print(f"  Train dates: {df.iloc[0]['date']} → {df.iloc[split_idx-1]['date']}")
    print(f"  Test dates:  {df.iloc[split_idx]['date']} → {df.iloc[-1]['date']}")

    # ── 4. Feature Engineering (with leakage-safe aggregates) ──
    print("\n--- Stage 2: Feature Engineering ---")
    df = full_feature_pipeline(df, include_lags=True, split_idx=split_idx)

    # ── 5. Handle NaN from lags ──
    lag_cols = [c for c in df.columns if "lag" in c or "roll" in c]
    n_before = len(df)
    df_model = df.dropna(subset=lag_cols).copy()
    print(f"\n[LAG CLEANUP] Dropped {n_before - len(df_model):,} rows with NaN lags "
          f"({len(df_model):,} remaining)")

    # ── 6. Define features & targets ──
    exclude = ["date", "state", "area", "prominent_pollutants", "primary_pollutant",
               "air_quality_status", "aqi_value", "aqi_category", "aqi_category_num",
               "season", "pollution_risk_score"]  # pollution_risk_score excluded as safety net
    feature_cols = [c for c in df_model.columns if c not in exclude]
    print(f"\n[FEATURES] {len(feature_cols)} features selected:")
    for i in range(0, len(feature_cols), 5):
        print(f"  {', '.join(feature_cols[i:i+5])}")

    X = df_model[feature_cols]
    y_reg = df_model["aqi_value"]
    y_clf = df_model["aqi_category_num"]

    # ── 7. Time-aware train/test split ──
    # Recompute split_idx after dropping NaN lag rows
    print("\n--- Stage 3: Train/Test Split (80/20 time-based) ---")
    df_model = df_model.sort_values("date")
    split_idx_model = int(len(df_model) * 0.8)

    X_train = df_model.iloc[:split_idx_model][feature_cols]
    X_test = df_model.iloc[split_idx_model:][feature_cols]
    y_train_reg = df_model.iloc[:split_idx_model]["aqi_value"]
    y_test_reg = df_model.iloc[split_idx_model:]["aqi_value"]
    y_train_clf = df_model.iloc[:split_idx_model]["aqi_category_num"]
    y_test_clf = df_model.iloc[split_idx_model:]["aqi_category_num"]

    print(f"  Train: {len(X_train):,} rows")
    print(f"  Test:  {len(X_test):,} rows")
    print(f"  Train dates: {df_model.iloc[:split_idx_model]['date'].min().date()} → "
          f"{df_model.iloc[:split_idx_model]['date'].max().date()}")
    print(f"  Test dates:  {df_model.iloc[split_idx_model:]['date'].min().date()} → "
          f"{df_model.iloc[split_idx_model:]['date'].max().date()}")

    # ── 8. Scale ──
    print("\n--- Stage 4: Scaling ---")
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=feature_cols, index=X_train.index)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=feature_cols, index=X_test.index)
    print(f"  Train mean: {X_train_scaled.mean().mean():.6f} (should be ~0)")
    print(f"  Train std:  {X_train_scaled.std().mean():.6f} (should be ~1)")

    # ── 9. Save everything ──
    print("\n--- Stage 5: Saving ---")
    df_model.to_csv(f"{PROCESSED}/aqi_processed.csv", index=False)

    X_train.to_csv(f"{PROCESSED}/X_train.csv", index=False)
    X_test.to_csv(f"{PROCESSED}/X_test.csv", index=False)
    X_train_scaled.to_csv(f"{PROCESSED}/X_train_scaled.csv", index=False)
    X_test_scaled.to_csv(f"{PROCESSED}/X_test_scaled.csv", index=False)
    y_train_reg.to_csv(f"{PROCESSED}/y_train_reg.csv", index=False)
    y_test_reg.to_csv(f"{PROCESSED}/y_test_reg.csv", index=False)
    y_train_clf.to_csv(f"{PROCESSED}/y_train_clf.csv", index=False)
    y_test_clf.to_csv(f"{PROCESSED}/y_test_clf.csv", index=False)

    joblib.dump(scaler, f"{PROCESSED}/scaler.pkl")
    joblib.dump(feature_cols, f"{PROCESSED}/feature_cols.pkl")

    print("  Saved all files to data/processed/")

    # ── 10. Feature correlation plot ──
    print("\n--- Feature Correlations with AQI ---")
    plot_correlation_with_target(X_train, y_train_reg, top_n=25,
                                save_path=f"{FIG}/02_feature_correlations.png")

    # ── 11. Class distribution ──
    print("\n--- Classification Target Distribution ---")
    labels = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
    for i, label in enumerate(labels):
        train_count = (y_train_clf == i).sum()
        test_count = (y_test_clf == i).sum()
        print(f"  {label}: train={train_count:,} test={test_count:,}")

    # ── 12. Leakage sanity check ──
    print("\n--- Leakage Sanity Check ---")
    if "pollution_risk_score" in feature_cols:
        print("  ⚠️  WARNING: pollution_risk_score is still in features!")
    else:
        print("  ✅ pollution_risk_score NOT in features")

    leaky_cols = [c for c in feature_cols if c in ["pollution_risk_score"]]
    if leaky_cols:
        print(f"  ⚠️  Potentially leaky columns found: {leaky_cols}")
    else:
        print("  ✅ No known leaky columns detected")

    print("\n" + "=" * 60)
    print("  PREPROCESSING COMPLETE (leakage-free)")
    print("=" * 60)
    print("\nNext: python run_03_modeling.py")


if __name__ == "__main__":
    main()
