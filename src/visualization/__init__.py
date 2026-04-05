"""
Aetheris — Visualization
All EDA and analysis charts.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from src.utils import AQI_COLORS, AQI_CATEGORY_ORDER, SEASON_MAP

plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "font.size": 11})


def plot_aqi_distribution(df, save_path=None):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].hist(df["aqi_value"], bins=100, color="#4ECDC4", edgecolor="black", alpha=0.7)
    axes[0].axvline(df["aqi_value"].mean(), color="red", ls="--", label=f"Mean: {df['aqi_value'].mean():.0f}")
    axes[0].axvline(df["aqi_value"].median(), color="orange", ls="--", label=f"Median: {df['aqi_value'].median():.0f}")
    axes[0].set_title("AQI Value Distribution")
    axes[0].set_xlabel("AQI")
    axes[0].legend()
    axes[1].boxplot(df["aqi_value"].dropna(), vert=True, widths=0.5)
    axes[1].set_title("AQI Box Plot")
    axes[1].set_ylabel("AQI")
    plt.tight_layout()
    if save_path: fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"  Skewness: {df['aqi_value'].skew():.2f}, Kurtosis: {df['aqi_value'].kurt():.2f}")


def plot_category_counts(df, save_path=None):
    counts = df["air_quality_status"].value_counts().reindex(AQI_CATEGORY_ORDER).dropna()
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    colors = [AQI_COLORS.get(c, "#999") for c in counts.index]
    counts.plot(kind="bar", ax=axes[0], color=colors, edgecolor="black")
    axes[0].set_title("AQI Category Counts")
    axes[0].tick_params(axis="x", rotation=30)
    for i, v in enumerate(counts):
        axes[0].text(i, v + 500, f"{v:,}", ha="center", fontsize=9)
    axes[1].pie(counts, labels=counts.index, autopct="%1.1f%%", colors=colors, startangle=90)
    axes[1].set_title("AQI Category Proportions")
    plt.tight_layout()
    if save_path: fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"  Imbalance ratio (max/min): {counts.max()/counts.min():.1f}x")


def plot_monthly_trend(df, save_path=None):
    monthly = df.groupby(df["date"].dt.to_period("M"))["aqi_value"].mean()
    monthly.index = monthly.index.to_timestamp()
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(monthly.index, monthly.values, marker="o", markersize=4, color="#2C3E50", lw=1.5)
    ax.fill_between(monthly.index, monthly.values, alpha=0.15, color="#3498DB")
    ax.set_title("Monthly Average AQI Trend — India")
    ax.set_ylabel("Average AQI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    if save_path: fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_seasonality(df, save_path=None):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    df.groupby(df["date"].dt.month)["aqi_value"].mean().plot(kind="bar", ax=axes[0], color="#E74C3C", alpha=0.8)
    axes[0].set_title("Average AQI by Month")
    axes[0].set_xlabel("Month")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    dow = df.groupby(df["date"].dt.dayofweek)["aqi_value"].mean()
    dow.index = days
    dow.plot(kind="bar", ax=axes[1], color="#9B59B6", alpha=0.8)
    axes[1].set_title("Average AQI by Day of Week")
    plt.tight_layout()
    if save_path: fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_top_polluted_cities(df, n=20, save_path=None):
    city_avg = df.groupby("area")["aqi_value"].mean().nlargest(n).sort_values()
    fig, ax = plt.subplots(figsize=(10, 7))
    city_avg.plot(kind="barh", ax=ax, color=sns.color_palette("YlOrRd", n))
    ax.set_title(f"Top {n} Most Polluted Cities (Avg AQI)")
    ax.set_xlabel("Average AQI")
    plt.tight_layout()
    if save_path: fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_cleanest_cities(df, n=20, save_path=None):
    city_avg = df.groupby("area")["aqi_value"].mean().nsmallest(n).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 7))
    city_avg.plot(kind="barh", ax=ax, color=sns.color_palette("Greens", n))
    ax.set_title(f"Top {n} Cleanest Cities (Avg AQI)")
    ax.set_xlabel("Average AQI")
    plt.tight_layout()
    if save_path: fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_state_heatmap(df, save_path=None):
    month_col = df["date"].dt.month if "month" not in df.columns else df["month"]
    pivot = df.assign(month=month_col).pivot_table(values="aqi_value", index="state", columns="month", aggfunc="mean")
    top_states = pivot.mean(axis=1).nlargest(20).index
    pivot = pivot.loc[top_states]
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(pivot, cmap="YlOrRd", annot=True, fmt=".0f", linewidths=0.5, ax=ax)
    ax.set_title("Average AQI by State x Month (Top 20 States)")
    plt.tight_layout()
    if save_path: fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_pollutant_analysis(df, save_path=None):
    primary = df["prominent_pollutants"].str.split(",").str[0].str.strip()
    counts = primary.value_counts().head(8)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    counts.plot(kind="bar", ax=axes[0], color=sns.color_palette("Set2", 8))
    axes[0].set_title("Primary Pollutant Frequency")
    axes[0].tick_params(axis="x", rotation=30)
    df_temp = df.assign(_pp=primary)
    df_temp.boxplot(column="aqi_value", by="_pp", ax=axes[1], showfliers=False, grid=False)
    axes[1].set_title("AQI by Pollutant")
    axes[1].set_xlabel("Primary Pollutant")
    plt.suptitle("")
    plt.tight_layout()
    if save_path: fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_seasonal_boxplot(df, save_path=None):
    season_order = ["Winter", "Spring", "Monsoon", "Autumn"]
    df_temp = df.copy()
    if "season" not in df_temp.columns:
        df_temp["season"] = df_temp["date"].dt.month.map(SEASON_MAP)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df_temp, x="season", y="aqi_value", order=season_order, palette="coolwarm", showfliers=False, ax=ax)
    ax.set_title("AQI Distribution by Season")
    plt.tight_layout()
    if save_path: fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_outlier_analysis(df):
    Q1 = df["aqi_value"].quantile(0.25)
    Q3 = df["aqi_value"].quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    outliers = df[(df["aqi_value"] < lower) | (df["aqi_value"] > upper)]
    print(f"  IQR: {IQR:.1f}, Bounds: [{lower:.1f}, {upper:.1f}]")
    print(f"  Outliers: {len(outliers):,} ({len(outliers)/len(df)*100:.1f}%)")
    print(f"  Top outlier cities:")
    print(outliers["area"].value_counts().head(10).to_string())


def plot_correlation_with_target(X_train, y_train, top_n=25, save_path=None):
    corr = X_train.corrwith(y_train).abs().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 8))
    corr.head(top_n).sort_values().plot(kind="barh", ax=ax, color="#2C3E50")
    ax.set_title(f"Top {top_n} Features Correlated with AQI")
    ax.set_xlabel("|Correlation|")
    plt.tight_layout()
    if save_path: fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
