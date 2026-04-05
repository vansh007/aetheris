"""
Aetheris — Step 1: Exploratory Data Analysis
Run: python run_01_eda.py
"""

import pandas as pd
import os
from src.utils import ensure_dirs
from src.visualization import (
    plot_aqi_distribution, plot_category_counts, plot_monthly_trend,
    plot_seasonality, plot_top_polluted_cities, plot_cleanest_cities,
    plot_state_heatmap, plot_pollutant_analysis, plot_seasonal_boxplot,
    plot_outlier_analysis
)

FIG = "reports/figures"


def main():
    ensure_dirs()
    print("=" * 60)
    print("  AETHERIS — Step 1: Exploratory Data Analysis")
    print("=" * 60)

    # Load raw data
    filepath = "data/raw/aqi.csv"
    if not os.path.exists(filepath):
        print(f"\nERROR: {filepath} not found!")
        print("Download aqi.csv from Kaggle and place it in data/raw/")
        return

    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    print(f"\nLoaded: {len(df):,} rows x {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")

    # ── Basic Info ──
    print("\n--- Basic Info ---")
    print(df.dtypes)
    print(f"\n--- Describe ---")
    print(df.describe())

    # ── Missing Values ──
    print("\n--- Missing Values ---")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    print(pd.DataFrame({"count": missing, "pct": missing_pct}).query("count > 0"))

    # ── Unique Values ──
    print("\n--- Unique Values ---")
    for col in df.columns:
        print(f"  {col}: {df[col].nunique()}")

    # ── Plots ──
    print("\n--- Generating plots ---")

    print("\n1. AQI Distribution")
    plot_aqi_distribution(df, save_path=f"{FIG}/01_aqi_distribution.png")

    print("\n2. AQI Category Counts")
    plot_category_counts(df, save_path=f"{FIG}/01_category_counts.png")

    print("\n3. Monthly Trend")
    plot_monthly_trend(df, save_path=f"{FIG}/01_monthly_trend.png")

    print("\n4. Seasonality (Month & Day of Week)")
    plot_seasonality(df, save_path=f"{FIG}/01_seasonality.png")

    print("\n5. Top 20 Most Polluted Cities")
    plot_top_polluted_cities(df, save_path=f"{FIG}/01_top_polluted.png")

    print("\n6. Top 20 Cleanest Cities")
    plot_cleanest_cities(df, save_path=f"{FIG}/01_cleanest.png")

    print("\n7. State x Month Heatmap")
    plot_state_heatmap(df, save_path=f"{FIG}/01_state_heatmap.png")

    print("\n8. Pollutant Analysis")
    plot_pollutant_analysis(df, save_path=f"{FIG}/01_pollutants.png")

    print("\n9. Seasonal Boxplot")
    plot_seasonal_boxplot(df, save_path=f"{FIG}/01_seasonal_boxplot.png")

    print("\n10. Outlier Analysis")
    plot_outlier_analysis(df)

    # ── Monitoring Stations ──
    print("\n11. Monitoring Stations vs AQI")
    corr = df["number_of_monitoring_stations"].corr(df["aqi_value"])
    print(f"  Correlation (stations vs AQI): {corr:.3f}")

    print("\n" + "=" * 60)
    print("  EDA COMPLETE — Figures saved to reports/figures/")
    print("=" * 60)
    print("\nKey insights to note:")
    print("  - AQI distribution is right-skewed (most readings are Satisfactory/Moderate)")
    print("  - Winter months show higher pollution")
    print("  - PM10 and PM2.5 are dominant pollutants")
    print("  - Northern cities (Delhi, Rajasthan) are most polluted")
    print("  - Class imbalance exists (Severe is rare) — will need SMOTE")
    print("\nNext: python run_02_preprocessing.py")


if __name__ == "__main__":
    main()
