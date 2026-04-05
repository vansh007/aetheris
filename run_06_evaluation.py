"""
Aetheris — Step 6: Final Evaluation & Summary Report
Run: python run_06_evaluation.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import ensure_dirs

FIG = "reports/figures"


def main():
    ensure_dirs()
    print("=" * 60)
    print("  AETHERIS — Step 6: Final Evaluation & Report")
    print("=" * 60)

    # ── Load results ──
    try:
        reg_results = pd.read_csv("reports/regression_results.csv", index_col=0)
        clf_results = pd.read_csv("reports/classification_results.csv", index_col=0)
    except FileNotFoundError:
        print("ERROR: Run run_03_modeling.py first!")
        return

    # ═══════════════════════════════════════════════════════════
    # 1. COMBINED DASHBOARD
    # ═══════════════════════════════════════════════════════════
    print("\n--- 1. Final Comparison Dashboard ---")
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    reg_results["rmse"].sort_values().plot(kind="barh", ax=axes[0, 0], color="#E74C3C")
    axes[0, 0].set_title("Regression — RMSE (lower = better)")

    reg_results["r2"].sort_values(ascending=False).plot(kind="barh", ax=axes[0, 1], color="#2ECC71")
    axes[0, 1].set_title("Regression — R² (higher = better)")

    clf_results["f1"].sort_values(ascending=False).plot(kind="barh", ax=axes[1, 0], color="#3498DB")
    axes[1, 0].set_title("Classification — F1 (higher = better)")

    clf_results["accuracy"].sort_values(ascending=False).plot(kind="barh", ax=axes[1, 1], color="#9B59B6")
    axes[1, 1].set_title("Classification — Accuracy (higher = better)")

    plt.suptitle("AETHERIS — Final Model Comparison", fontsize=16, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{FIG}/06_final_dashboard.png", dpi=150, bbox_inches="tight")
    plt.show()

    # ═══════════════════════════════════════════════════════════
    # 2. OVERFITTING CHECK
    # ═══════════════════════════════════════════════════════════
    if "cv_mean" in reg_results.columns:
        print("\n--- 2. Overfitting Check (Test RMSE vs CV RMSE) ---")
        fig, ax = plt.subplots(figsize=(10, 5))
        x = range(len(reg_results))
        width = 0.35
        ax.bar([i - width / 2 for i in x], reg_results["rmse"], width, label="Test RMSE", color="#E74C3C")
        ax.bar([i + width / 2 for i in x], reg_results["cv_mean"], width, label="CV RMSE", color="#3498DB")
        ax.set_xticks(list(x))
        ax.set_xticklabels(reg_results.index, rotation=45, ha="right")
        ax.set_title("Overfitting Check — Test vs CV RMSE")
        ax.legend()
        plt.tight_layout()
        fig.savefig(f"{FIG}/06_overfitting_check.png", dpi=150, bbox_inches="tight")
        plt.show()

        gap = abs(reg_results["rmse"] - reg_results["cv_mean"])
        overfit = gap[gap > 5]
        if len(overfit) > 0:
            print("  Potential overfit models (>5 RMSE gap):")
            for name in overfit.index:
                print(f"    {name}: test={reg_results.loc[name, 'rmse']:.2f}, "
                      f"cv={reg_results.loc[name, 'cv_mean']:.2f}")
        else:
            print("  No significant overfitting detected.")

    # ═══════════════════════════════════════════════════════════
    # 3. FINAL SUMMARY
    # ═══════════════════════════════════════════════════════════
    best_reg = reg_results["rmse"].idxmin()
    best_clf = clf_results["f1"].idxmax()

    print("\n" + "=" * 60)
    print("  AETHERIS — FINAL PROJECT SUMMARY")
    print("=" * 60)

    print(f"""
  REGRESSION (Predict AQI Value)
  ─────────────────────────────
  Best Model: {best_reg}
  RMSE:       {reg_results.loc[best_reg, 'rmse']:.2f}
  MAE:        {reg_results.loc[best_reg, 'mae']:.2f}
  R²:         {reg_results.loc[best_reg, 'r2']:.4f}
  MAPE:       {reg_results.loc[best_reg, 'mape']:.2f}%

  CLASSIFICATION (Predict AQI Category)
  ─────────────────────────────────────
  Best Model: {best_clf}
  Accuracy:   {clf_results.loc[best_clf, 'accuracy']:.4f}
  F1 Score:   {clf_results.loc[best_clf, 'f1']:.4f}
  Precision:  {clf_results.loc[best_clf, 'precision']:.4f}
  Recall:     {clf_results.loc[best_clf, 'recall']:.4f}

  MODELS COMPARED
  ──────────────
  Regression:     {', '.join(reg_results.index.tolist())}
  Classification: {', '.join(clf_results.index.tolist())}

  TECHNIQUES USED
  ──────────────
  - Feature Engineering: temporal, lag, rolling, cyclical, target encoding
  - Class Imbalance: SMOTE oversampling
  - Validation: 5-fold cross-validation + time-based train/test split
  - Hyperparameter Tuning: GridSearchCV
  - Time Series: ARIMA, Prophet (decomposition + forecasting)
  - Clustering: K-Means (elbow + silhouette), Hierarchical (dendrogram)
  - Anomaly Detection: Isolation Forest
  - Explainability: Feature importance analysis

  FIGURES SAVED
  ─────────────
  All plots saved to reports/figures/
""")

    print("=" * 60)
    print("  PROJECT COMPLETE")
    print("=" * 60)
    print("\n  Optional next steps:")
    print("  - Run the API: uvicorn src.api:app --reload")
    print("  - Build frontend dashboard")
    print("  - Deploy to cloud")


if __name__ == "__main__":
    main()
