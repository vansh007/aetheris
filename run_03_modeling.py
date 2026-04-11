"""
Aetheris — Step 3: Model Training, Comparison & Hyperparameter Tuning
Run: python run_03_modeling.py
"""
"""
Load Data
   ↓
Train Multiple Models
   ↓
Evaluate & Compare
   ↓
Hyperparameter Tuning
   ↓
Handle Class Imbalance (SMOTE)
   ↓
Select Best Models
   ↓
Save for Deployment
"""
import pandas as pd
import numpy as np
import os
from sklearn.metrics import classification_report
from src.utils import ensure_dirs
from src.models import (
    get_regression_models, get_classification_models, get_tuning_grids,
    train_all_models, tune_model, apply_smote, save_model
)
from src.evaluation import (
    plot_model_comparison, plot_confusion_matrix, plot_actual_vs_predicted,
    plot_residuals, plot_feature_importance, print_report, regression_metrics
)

FIG = "reports/figures"
PROCESSED = "data/processed"


def main():
    ensure_dirs()
    os.makedirs("models", exist_ok=True)
    print("=" * 60)
    print("  AETHERIS — Step 3: Model Training & Comparison")
    print("=" * 60)

    # ── Load data ──
    print("\n--- Loading processed data ---")
    X_train = pd.read_csv(f"{PROCESSED}/X_train.csv")
    X_test = pd.read_csv(f"{PROCESSED}/X_test.csv")
    y_train_reg = pd.read_csv(f"{PROCESSED}/y_train_reg.csv").squeeze()
    y_test_reg = pd.read_csv(f"{PROCESSED}/y_test_reg.csv").squeeze()
    y_train_clf = pd.read_csv(f"{PROCESSED}/y_train_clf.csv").squeeze()
    y_test_clf = pd.read_csv(f"{PROCESSED}/y_test_clf.csv").squeeze()
    print(f"  Train: {X_train.shape}, Test: {X_test.shape}")

    # ═══════════════════════════════════════════════════════════
    # PART A: REGRESSION (Predict AQI Value)
    # ═══════════════════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("  PART A: REGRESSION — Predicting AQI Value")
    print("=" * 60)

    reg_models = get_regression_models()
    reg_results, reg_trained = train_all_models(
        reg_models, X_train, y_train_reg, X_test, y_test_reg, task="regression"
    )
    print_report(reg_results, "regression")

    # Comparison chart
    plot_model_comparison(reg_results, ["rmse", "r2", "mae"],
                          title="Regression Model Comparison",
                          save_path=f"{FIG}/03_regression_comparison.png")

    # Best model deep-dive
    best_reg_name = reg_results["rmse"].idxmin()
    best_reg = reg_trained[best_reg_name]
    y_pred_reg = best_reg.predict(X_test)

    print(f"\n--- Best Regression Model: {best_reg_name} ---")
    plot_actual_vs_predicted(y_test_reg, y_pred_reg,
                             title=f"{best_reg_name} — Actual vs Predicted",
                             save_path=f"{FIG}/03_actual_vs_predicted.png")
    plot_residuals(y_test_reg, y_pred_reg,
                   title=f"{best_reg_name} — Residuals",
                   save_path=f"{FIG}/03_residuals.png")
    plot_feature_importance(best_reg, X_train.columns, top_n=20,
                            title=f"{best_reg_name} — Feature Importance",
                            save_path=f"{FIG}/03_feature_importance.png")

    # ── Hyperparameter tuning (top 2 models) ──
    print("\n--- Hyperparameter Tuning ---")
    grids = get_tuning_grids()
    top_2 = reg_results["rmse"].nsmallest(2).index.tolist()
    tuned_models = {}

    for name in top_2:
        if name in grids:
            print(f"\n  Tuning {name}...")
            base = get_regression_models()[name]
            best_model, best_params = tune_model(base, grids[name], X_train, y_train_reg)
            tuned_models[name] = best_model

            y_pred_tuned = best_model.predict(X_test)
            tuned_m = regression_metrics(y_test_reg, y_pred_tuned)
            print(f"  TUNED RMSE: {tuned_m['rmse']:.2f} (was {reg_results.loc[name, 'rmse']:.2f})")
            print(f"  TUNED R²:   {tuned_m['r2']:.4f} (was {reg_results.loc[name, 'r2']:.4f})")

    # Save best regression model
    final_reg = tuned_models.get(best_reg_name, reg_trained[best_reg_name])
    save_model(final_reg, f"models/best_regression_{best_reg_name}.pkl")
    save_model(final_reg, "models/best_model.pkl")

    # ═══════════════════════════════════════════════════════════
    # PART B: CLASSIFICATION (Predict AQI Category)
    # ═══════════════════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("  PART B: CLASSIFICATION — Predicting AQI Category")
    print("=" * 60)

    print("\n--- Applying SMOTE for class imbalance ---")
    X_train_smote, y_train_smote = apply_smote(X_train, y_train_clf)

    clf_models = get_classification_models()
    clf_results, clf_trained = train_all_models(
        clf_models, X_train_smote, y_train_smote, X_test, y_test_clf, task="classification"
    )
    print_report(clf_results, "classification")

    # Comparison chart
    plot_model_comparison(clf_results, ["f1", "accuracy", "precision"],
                          title="Classification Model Comparison",
                          save_path=f"{FIG}/03_classification_comparison.png")

    # Best classifier deep-dive
    best_clf_name = clf_results["f1"].idxmax()
    best_clf = clf_trained[best_clf_name]
    y_pred_clf = best_clf.predict(X_test)

    labels = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
    print(f"\n--- Best Classifier: {best_clf_name} ---")
    plot_confusion_matrix(y_test_clf, y_pred_clf, labels=range(6),
                          title=f"{best_clf_name} — Confusion Matrix",
                          save_path=f"{FIG}/03_confusion_matrix.png")
    print("\nClassification Report:")
    print(classification_report(y_test_clf, y_pred_clf, target_names=labels, zero_division=0))

    # Save
    save_model(best_clf, f"models/best_classification_{best_clf_name}.pkl")
    reg_results.to_csv("reports/regression_results.csv")
    clf_results.to_csv("reports/classification_results.csv")

    print("\n" + "=" * 60)
    print("  MODELING COMPLETE")
    print("=" * 60)
    print(f"\n  Best Regression:     {best_reg_name} (RMSE={reg_results.loc[best_reg_name, 'rmse']:.2f})")
    print(f"  Best Classification: {best_clf_name} (F1={clf_results.loc[best_clf_name, 'f1']:.4f})")
    print("\nNext: python run_04_timeseries.py")


if __name__ == "__main__":
    main()
