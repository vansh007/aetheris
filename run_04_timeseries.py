"""
Aetheris — Step 4: Time Series Forecasting
Run: python run_04_timeseries.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error, mean_absolute_error
from src.utils import ensure_dirs, load_config
import warnings
warnings.filterwarnings("ignore")

FIG = "reports/figures"


def main():
    ensure_dirs()
    cfg = load_config()
    CITY = cfg["timeseries"]["default_city"]
    FORECAST_DAYS = cfg["timeseries"]["forecast_days"]
    TEST_DAYS = cfg["timeseries"]["test_days"]
    ARIMA_ORDER = tuple(cfg["timeseries"]["arima_order"])

    print("=" * 60)
    print("  AETHERIS — Step 4: Time Series Forecasting")
    print("=" * 60)

    # ── Load ──
    df = pd.read_csv("data/processed/aqi_processed.csv")
    df["date"] = pd.to_datetime(df["date"])

    # Check if city exists, fallback to most-data city
    if CITY not in df["area"].values:
        CITY = df["area"].value_counts().index[0]
        print(f"  Default city not found, using: {CITY}")

    city_df = df[df["area"] == CITY].set_index("date")["aqi_value"].sort_index()
    city_daily = city_df.resample("D").mean().interpolate(method="linear")
    print(f"\n  City: {CITY}")
    print(f"  Daily records: {len(city_daily)}")
    print(f"  Date range: {city_daily.index.min().date()} → {city_daily.index.max().date()}")

    # ── 1. Decomposition ──
    print("\n--- 1. Time Series Decomposition ---")
    decomposition = seasonal_decompose(city_daily, model="additive", period=30)
    fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)
    decomposition.observed.plot(ax=axes[0], title="Observed")
    decomposition.trend.plot(ax=axes[1], title="Trend")
    decomposition.seasonal.plot(ax=axes[2], title="Seasonal")
    decomposition.resid.plot(ax=axes[3], title="Residual")
    plt.tight_layout()
    fig.savefig(f"{FIG}/04_decomposition.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("  Decomposition saved.")

    # ── 2. Stationarity ──
    print("\n--- 2. Stationarity Test (ADF) ---")
    result = adfuller(city_daily.dropna())
    print(f"  ADF Statistic: {result[0]:.4f}")
    print(f"  p-value: {result[1]:.6f}")
    print(f"  Stationary: {'Yes' if result[1] < 0.05 else 'No — differencing needed'}")

    # ── 3. ARIMA ──
    print(f"\n--- 3. ARIMA{ARIMA_ORDER} Forecasting ---")
    train_ts = city_daily[:-TEST_DAYS]
    test_ts = city_daily[-TEST_DAYS:]

    model_arima = ARIMA(train_ts, order=ARIMA_ORDER)
    fit_arima = model_arima.fit()

    forecast_arima = fit_arima.forecast(steps=TEST_DAYS)
    rmse_arima = np.sqrt(mean_squared_error(test_ts, forecast_arima))
    mae_arima = mean_absolute_error(test_ts, forecast_arima)
    print(f"  ARIMA RMSE: {rmse_arima:.2f}")
    print(f"  ARIMA MAE:  {mae_arima:.2f}")

    # Plot
    fig, ax = plt.subplots(figsize=(14, 5))
    train_ts[-60:].plot(ax=ax, label="Train", color="#2C3E50")
    test_ts.plot(ax=ax, label="Actual", color="#E74C3C")
    forecast_arima.plot(ax=ax, label="ARIMA Forecast", color="#3498DB", linestyle="--")
    ax.set_title(f"ARIMA Forecast — {CITY}")
    ax.legend()
    plt.tight_layout()
    fig.savefig(f"{FIG}/04_arima_forecast.png", dpi=150, bbox_inches="tight")
    plt.show()

    # ── 4. Prophet ──
    print("\n--- 4. Prophet Forecasting ---")
    rmse_prophet = None
    try:
        from prophet import Prophet

        prophet_df = train_ts.reset_index()
        prophet_df.columns = ["ds", "y"]

        m = Prophet(daily_seasonality=False, yearly_seasonality=True, weekly_seasonality=True)
        m.fit(prophet_df)

        future = m.make_future_dataframe(periods=TEST_DAYS)
        forecast = m.predict(future)

        prophet_pred = forecast.set_index("ds")["yhat"][-TEST_DAYS:]
        rmse_prophet = np.sqrt(mean_squared_error(test_ts, prophet_pred.values))
        mae_prophet = mean_absolute_error(test_ts, prophet_pred.values)
        print(f"  Prophet RMSE: {rmse_prophet:.2f}")
        print(f"  Prophet MAE:  {mae_prophet:.2f}")

        fig = m.plot(forecast)
        plt.title(f"Prophet Forecast — {CITY}")
        plt.tight_layout()
        fig.savefig(f"{FIG}/04_prophet_forecast.png", dpi=150, bbox_inches="tight")
        plt.show()

        fig2 = m.plot_components(forecast)
        plt.tight_layout()
        plt.show()

    except ImportError:
        print("  Prophet not installed. Install with: pip install prophet")

    # ── 5. Comparison ──
    print("\n--- 5. Comparison ---")
    print(f"  {'Model':<10} {'RMSE':>8} {'MAE':>8}")
    print(f"  {'ARIMA':<10} {rmse_arima:>8.2f} {mae_arima:>8.2f}")
    if rmse_prophet:
        print(f"  {'Prophet':<10} {rmse_prophet:>8.2f} {mae_prophet:>8.2f}")

    # ── 6. 7-day forecast ──
    print(f"\n--- 6. {FORECAST_DAYS}-Day Forecast for {CITY} ---")
    model_full = ARIMA(city_daily, order=ARIMA_ORDER)
    fit_full = model_full.fit()
    next_days = fit_full.forecast(steps=FORECAST_DAYS)

    for date, val in next_days.items():
        val = max(0, min(500, val))
        cat = ("Good" if val <= 50 else "Satisfactory" if val <= 100 else
               "Moderate" if val <= 200 else "Poor" if val <= 300 else
               "Very Poor" if val <= 400 else "Severe")
        print(f"  {date.date()}: AQI {val:.0f} ({cat})")

    print("\n" + "=" * 60)
    print("  TIME SERIES COMPLETE")
    print("=" * 60)
    print("\nNext: python run_05_clustering.py")


if __name__ == "__main__":
    main()
