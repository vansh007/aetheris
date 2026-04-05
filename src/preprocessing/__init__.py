"""
Aetheris — Data Loading & Cleaning
"""

import pandas as pd
import numpy as np


def load_raw_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    print(f"[LOAD] {len(df):,} rows x {len(df.columns)} columns")
    return df


def initial_clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Drop useless columns
    drop_cols = [c for c in ["unit", "note"] if c in df.columns]
    df.drop(columns=drop_cols, inplace=True)
    print(f"[CLEAN] Dropped columns: {drop_cols}")

    # Strip whitespace
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Parse dates
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    bad_dates = df["date"].isna().sum()
    if bad_dates > 0:
        print(f"[CLEAN] Dropping {bad_dates} rows with bad dates")
        df.dropna(subset=["date"], inplace=True)

    # Drop missing AQI
    missing_aqi = df["aqi_value"].isna().sum()
    if missing_aqi > 0:
        print(f"[CLEAN] Dropping {missing_aqi} rows with missing AQI")
        df.dropna(subset=["aqi_value"], inplace=True)

    # Clip AQI to valid range
    invalid = ((df["aqi_value"] < 0) | (df["aqi_value"] > 500)).sum()
    if invalid > 0:
        print(f"[CLEAN] Clipping {invalid} AQI values to [0, 500]")
        df["aqi_value"] = df["aqi_value"].clip(0, 500)

    # Standardize names
    df["state"] = df["state"].str.title()
    df["area"] = df["area"].str.title()

    # Sort and reset
    df.sort_values("date", inplace=True)
    df.reset_index(drop=True, inplace=True)

    print(f"[CLEAN] Result: {len(df):,} rows x {len(df.columns)} columns")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    dropped = before - len(df)
    if dropped > 0:
        print(f"[CLEAN] Removed {dropped:,} duplicate rows")
    return df


def fix_pollutants(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["prominent_pollutants"] = df["prominent_pollutants"].fillna("Unknown")

    # Primary pollutant (first listed)
    df["primary_pollutant"] = df["prominent_pollutants"].str.split(",").str[0].str.strip()

    # Count of pollutants
    df["n_pollutants"] = df["prominent_pollutants"].apply(
        lambda x: len(x.split(",")) if x != "Unknown" else 0
    )

    # Binary flags
    for p in ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "NH3"]:
        col_name = f"has_{p.replace('.', '')}"
        df[col_name] = df["prominent_pollutants"].str.contains(p, case=False, na=False).astype(int)

    return df


def full_clean_pipeline(filepath: str) -> pd.DataFrame:
    """Run complete cleaning: load -> clean -> dedup -> fix pollutants."""
    df = load_raw_data(filepath)
    df = initial_clean(df)
    df = remove_duplicates(df)
    df = fix_pollutants(df)

    print(f"\n[VALIDATION]")
    print(f"  Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"  States: {df['state'].nunique()}, Cities: {df['area'].nunique()}")
    print(f"  AQI: mean={df['aqi_value'].mean():.1f}, std={df['aqi_value'].std():.1f}, "
          f"min={df['aqi_value'].min():.0f}, max={df['aqi_value'].max():.0f}")

    return df
