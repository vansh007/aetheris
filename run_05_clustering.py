"""
Aetheris — Step 5: City Clustering & Anomaly Detection
Run: python run_05_clustering.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage
from src.utils import ensure_dirs, load_config, SEASON_MAP
import warnings
warnings.filterwarnings("ignore")

FIG = "reports/figures"


def main():
    ensure_dirs()
    cfg = load_config()
    print("=" * 60)
    print("  AETHERIS — Step 5: Clustering & Anomaly Detection")
    print("=" * 60)

    df = pd.read_csv("data/processed/aqi_processed.csv")
    df["date"] = pd.to_datetime(df["date"])

    # ═══════════════════════════════════════════════════════════
    # PART A: CITY CLUSTERING
    # ═══════════════════════════════════════════════════════════
    print("\n--- Part A: City Clustering ---")

    # Build city-level features
    city_feat = df.groupby("area").agg(
        aqi_mean=("aqi_value", "mean"), aqi_std=("aqi_value", "std"),
        aqi_max=("aqi_value", "max"), aqi_min=("aqi_value", "min"),
        aqi_median=("aqi_value", "median"), record_count=("aqi_value", "count"),
        n_stations=("number_of_monitoring_stations", "mean"),
    ).reset_index()

    # Add pollutant proportions if available
    poll_cols = [c for c in df.columns if c.startswith("has_")]
    if poll_cols:
        poll_agg = df.groupby("area")[poll_cols].mean().reset_index()
        city_feat = city_feat.merge(poll_agg, on="area")

    min_records = cfg["clustering"]["min_city_records"]
    city_feat = city_feat[city_feat["record_count"] >= min_records]
    print(f"  Cities with {min_records}+ records: {len(city_feat)}")

    feat_cols = [c for c in city_feat.columns if c != "area"]
    scaler = StandardScaler()
    X_cluster = scaler.fit_transform(city_feat[feat_cols])

    # ── Elbow + Silhouette ──
    K_range = cfg["clustering"]["n_clusters_range"]
    inertias, sils = [], []
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_cluster)
        inertias.append(km.inertia_)
        sils.append(silhouette_score(X_cluster, labels))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(K_range, inertias, "bo-")
    axes[0].set_title("Elbow Method")
    axes[0].set_xlabel("K")
    axes[0].set_ylabel("Inertia")
    axes[1].plot(K_range, sils, "ro-")
    axes[1].set_title("Silhouette Score")
    axes[1].set_xlabel("K")
    plt.tight_layout()
    fig.savefig(f"{FIG}/05_elbow_silhouette.png", dpi=150, bbox_inches="tight")
    plt.show()

    best_k = K_range[np.argmax(sils)]
    print(f"  Best K by silhouette: {best_k} (score: {max(sils):.3f})")

    # ── Final K-Means ──
    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    city_feat["cluster"] = kmeans.fit_predict(X_cluster)

    print(f"\n  Cluster Summary:")
    for c in range(best_k):
        subset = city_feat[city_feat["cluster"] == c]
        examples = ", ".join(subset["area"].head(5).tolist())
        print(f"    Cluster {c}: {len(subset)} cities, avg AQI={subset['aqi_mean'].mean():.0f} — {examples}")

    # Scatter
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(city_feat["aqi_mean"], city_feat["aqi_std"],
                         c=city_feat["cluster"], cmap="Set1", alpha=0.7, s=30)
    ax.set_xlabel("Mean AQI")
    ax.set_ylabel("AQI Std Dev")
    ax.set_title("City Clusters — Pollution Zones")
    plt.colorbar(scatter, label="Cluster")
    plt.tight_layout()
    fig.savefig(f"{FIG}/05_city_clusters.png", dpi=150, bbox_inches="tight")
    plt.show()

    # ── Hierarchical Dendrogram (top 50 cities) ──
    print("\n--- Hierarchical Clustering (Top 50 cities) ---")
    top_cities = city_feat.nlargest(50, "record_count")
    X_top = scaler.fit_transform(top_cities[feat_cols])
    linkage_matrix = linkage(X_top, method="ward")

    fig, ax = plt.subplots(figsize=(16, 7))
    dendrogram(linkage_matrix, labels=top_cities["area"].values, leaf_rotation=90, leaf_font_size=8, ax=ax)
    ax.set_title("Hierarchical Clustering — Top 50 Cities")
    plt.tight_layout()
    fig.savefig(f"{FIG}/05_dendrogram.png", dpi=150, bbox_inches="tight")
    plt.show()

    # ═══════════════════════════════════════════════════════════
    # PART B: ANOMALY DETECTION
    # ═══════════════════════════════════════════════════════════
    print("\n--- Part B: Anomaly Detection (Isolation Forest) ---")
    anomaly_features = ["aqi_value", "number_of_monitoring_stations"]
    if "n_pollutants" in df.columns:
        anomaly_features.append("n_pollutants")

    contam = cfg["clustering"]["anomaly_contamination"]
    iso = IsolationForest(contamination=contam, random_state=42, n_jobs=-1)
    df["is_anomaly"] = (iso.fit_predict(df[anomaly_features].fillna(0)) == -1).astype(int)

    anomalies = df[df["is_anomaly"] == 1]
    normals = df[df["is_anomaly"] == 0]
    print(f"  Anomalies: {len(anomalies):,} ({len(anomalies)/len(df)*100:.2f}%)")
    print(f"  Anomaly AQI range: {anomalies['aqi_value'].min():.0f} — {anomalies['aqi_value'].max():.0f}")
    print(f"  Normal AQI range:  {normals['aqi_value'].min():.0f} — {normals['aqi_value'].max():.0f}")
    print(f"\n  Top anomaly cities:")
    print(anomalies["area"].value_counts().head(10).to_string())

    # Plot
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.scatter(normals["date"], normals["aqi_value"], s=1, alpha=0.1, color="#2C3E50", label="Normal")
    ax.scatter(anomalies["date"], anomalies["aqi_value"], s=5, color="red", alpha=0.5, label="Anomaly")
    ax.set_title("AQI Anomaly Detection (Isolation Forest)")
    ax.set_ylabel("AQI")
    ax.legend()
    plt.tight_layout()
    fig.savefig(f"{FIG}/05_anomalies.png", dpi=150, bbox_inches="tight")
    plt.show()

    # ═══════════════════════════════════════════════════════════
    # PART C: SEASONAL ANALYSIS
    # ═══════════════════════════════════════════════════════════
    print("\n--- Part C: Seasonal Pattern Analysis ---")
    if "season" not in df.columns:
        df["season"] = df["date"].dt.month.map(SEASON_MAP)

    season_order = ["Winter", "Spring", "Monsoon", "Autumn"]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.boxplot(data=df, x="season", y="aqi_value", order=season_order,
                palette="coolwarm", showfliers=False, ax=axes[0])
    axes[0].set_title("AQI by Season")

    # Category proportions
    ct = df.groupby(["season", "air_quality_status"]).size().unstack(fill_value=0)
    ct = ct.reindex(season_order)
    cat_order = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
    ct = ct[[c for c in cat_order if c in ct.columns]]
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100
    ct_pct.plot(kind="bar", stacked=True, ax=axes[1])
    axes[1].set_title("AQI Category % by Season")
    axes[1].set_ylabel("Percentage")
    axes[1].legend(bbox_to_anchor=(1.05, 1), fontsize=8)
    plt.tight_layout()
    fig.savefig(f"{FIG}/05_seasonal_analysis.png", dpi=150, bbox_inches="tight")
    plt.show()

    # Save cluster data
    city_feat.to_csv("data/processed/city_clusters.csv", index=False)

    print("\n" + "=" * 60)
    print("  CLUSTERING & ANOMALY DETECTION COMPLETE")
    print("=" * 60)
    print("\nNext: python run_06_evaluation.py")


if __name__ == "__main__":
    main()
