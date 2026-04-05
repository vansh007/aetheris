"""
Aetheris — Feature Engineering
Temporal, lag, rolling, aggregate, and derived features.

IMPORTANT: Aggregate and encoding features are computed from training data
only to prevent data leakage. Pass `split_idx` to `full_feature_pipeline()`
to define the train/test boundary.
"""

import pandas as pd
import numpy as np
from src.utils import SEASON_MAP


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["day_of_week"] = df["date"].dt.dayofweek
    df["day_of_year"] = df["date"].dt.dayofyear
    df["quarter"] = df["date"].dt.quarter
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
    df["season"] = df["month"].map(SEASON_MAP)

    # Cyclical encoding
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
    df["dow_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
    df["dow_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)
    return df


def add_aqi_categories(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    bins = [0, 50, 100, 200, 300, 400, 500]
    labels = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
    df["aqi_category"] = pd.cut(df["aqi_value"], bins=bins, labels=labels, include_lowest=True)
    cat_map = {label: i for i, label in enumerate(labels)}
    df["aqi_category_num"] = df["aqi_category"].map(cat_map)
    return df


def add_lag_features(df: pd.DataFrame, lags=None) -> pd.DataFrame:
    if lags is None:
        lags = [1, 3, 7, 14, 30]
    df = df.copy().sort_values(["area", "date"])
    for lag in lags:
        df[f"aqi_lag_{lag}"] = df.groupby("area")["aqi_value"].shift(lag)
    return df


def add_rolling_features(df: pd.DataFrame, windows=None) -> pd.DataFrame:
    if windows is None:
        windows = [3, 7, 14, 30]
    df = df.copy().sort_values(["area", "date"])
    for w in windows:
        grp = df.groupby("area")["aqi_value"]
        df[f"aqi_roll_mean_{w}"] = grp.transform(lambda x: x.rolling(w, min_periods=1).mean())
        df[f"aqi_roll_std_{w}"] = grp.transform(lambda x: x.rolling(w, min_periods=1).std())
        df[f"aqi_roll_max_{w}"] = grp.transform(lambda x: x.rolling(w, min_periods=1).max())
        df[f"aqi_roll_min_{w}"] = grp.transform(lambda x: x.rolling(w, min_periods=1).min())
    return df


def add_city_state_stats(df: pd.DataFrame, split_idx: int) -> pd.DataFrame:
    """Compute city/state aggregate stats using ONLY training data (rows before split_idx).

    This prevents data leakage — test-set AQI values never influence these features.
    """
    df = df.copy()
    train_df = df.iloc[:split_idx]

    # City-level (computed from train only, mapped to all rows)
    city_stats = train_df.groupby("area")["aqi_value"].agg(
        city_aqi_mean="mean", city_aqi_median="median",
        city_aqi_std="std", city_record_count="count"
    ).reset_index()
    df = df.drop(columns=[c for c in ["city_aqi_mean", "city_aqi_median", "city_aqi_std", "city_record_count"]
                           if c in df.columns], errors="ignore")
    df = df.merge(city_stats, on="area", how="left")

    # State-level (computed from train only, mapped to all rows)
    state_stats = train_df.groupby("state")["aqi_value"].agg(
        state_aqi_mean="mean", state_aqi_median="median", state_aqi_std="std"
    ).reset_index()
    df = df.drop(columns=[c for c in ["state_aqi_mean", "state_aqi_median", "state_aqi_std"]
                           if c in df.columns], errors="ignore")
    df = df.merge(state_stats, on="state", how="left")

    # Fill NaN for any test cities/states not seen in training
    for col in ["city_aqi_mean", "city_aqi_median", "city_aqi_std", "city_record_count",
                "state_aqi_mean", "state_aqi_median", "state_aqi_std"]:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    return df


def encode_categoricals(df: pd.DataFrame, split_idx: int) -> pd.DataFrame:
    """Target-encode high-cardinality columns using ONLY training data.
    Label-encode low-cardinality columns normally.
    """
    from sklearn.preprocessing import LabelEncoder
    df = df.copy()
    train_df = df.iloc[:split_idx]

    # Label encode primary_pollutant and season (no leakage — not target-dependent)
    for col in ["primary_pollutant", "season"]:
        le = LabelEncoder()
        df[f"{col}_enc"] = le.fit_transform(df[col].astype(str))

    # Target encode state and area using TRAIN-ONLY mean AQI
    for col in ["state", "area"]:
        train_means = train_df.groupby(col)["aqi_value"].mean()
        df[f"{col}_enc"] = df[col].map(train_means)
        # Fill NaN for unseen categories with overall train mean
        df[f"{col}_enc"] = df[f"{col}_enc"].fillna(train_df["aqi_value"].mean())

    return df


# NOTE: pollution_risk_score has been REMOVED — it was computed directly from
# aqi_value (the target), causing perfect data leakage.


def full_feature_pipeline(df: pd.DataFrame, include_lags: bool = True,
                          split_idx: int = None) -> pd.DataFrame:
    """Run complete feature engineering.

    Args:
        df: Cleaned DataFrame with 'date', 'area', 'state', 'aqi_value' columns.
        include_lags: Whether to add lag and rolling features.
        split_idx: Index of the train/test boundary. Required to prevent leakage
                   in aggregate stats and target encoding. If None, uses 80% of data.
    """
    if split_idx is None:
        split_idx = int(len(df) * 0.8)
        print(f"[FEATURES] WARNING: No split_idx provided, defaulting to 80% ({split_idx:,})")

    print("[FEATURES] Adding date features...")
    df = add_date_features(df)

    print("[FEATURES] Adding AQI categories...")
    df = add_aqi_categories(df)

    print("[FEATURES] Adding city & state stats (train-only)...")
    df = add_city_state_stats(df, split_idx)

    # pollution_risk_score REMOVED — it contained aqi_value directly

    if include_lags:
        print("[FEATURES] Adding lag features...")
        df = add_lag_features(df)
        print("[FEATURES] Adding rolling features...")
        df = add_rolling_features(df)

    print("[FEATURES] Encoding categoricals (train-only target encoding)...")
    df = encode_categoricals(df, split_idx)

    print(f"[FEATURES] Done: {len(df.columns)} columns total")
    return df
