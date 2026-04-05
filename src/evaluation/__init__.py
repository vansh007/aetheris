"""
Aetheris — Evaluation
Metrics, comparison plots, residual analysis, feature importance.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)


def regression_metrics(y_true, y_pred) -> dict:
    return {
        "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
        "mae": mean_absolute_error(y_true, y_pred),
        "r2": r2_score(y_true, y_pred),
        "mape": mean_absolute_percentage_error(y_true, y_pred) * 100,
    }


def classification_metrics(y_true, y_pred) -> dict:
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average="weighted", zero_division=0),
        "recall": recall_score(y_true, y_pred, average="weighted", zero_division=0),
        "f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
    }


def plot_model_comparison(results_df, metrics_list, title, save_path=None):
    n = len(metrics_list)
    fig, axes = plt.subplots(1, n, figsize=(6 * n, 5))
    if n == 1:
        axes = [axes]

    for ax, metric in zip(axes, metrics_list):
        ascending = metric not in ("r2", "accuracy", "precision", "recall", "f1")
        vals = results_df[metric].sort_values(ascending=ascending)
        colors = sns.color_palette("viridis", len(vals))
        vals.plot(kind="barh", ax=ax, color=colors)
        ax.set_title(metric.upper())
        ax.set_xlabel(metric)

    plt.suptitle(title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_confusion_matrix(y_true, y_pred, labels=None, title="Confusion Matrix", save_path=None):
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                xticklabels=labels, yticklabels=labels)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(title)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_actual_vs_predicted(y_true, y_pred, title="Actual vs Predicted", save_path=None):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(y_true, y_pred, alpha=0.3, s=5)
    ax.plot([0, 500], [0, 500], "r--", label="Perfect prediction")
    ax.set_xlabel("Actual AQI")
    ax.set_ylabel("Predicted AQI")
    ax.set_title(title)
    ax.legend()
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 500)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_residuals(y_true, y_pred, title="Residuals", save_path=None):
    residuals = np.array(y_true) - np.array(y_pred)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].scatter(y_pred, residuals, alpha=0.3, s=5)
    axes[0].axhline(0, color="red", linestyle="--")
    axes[0].set_xlabel("Predicted")
    axes[0].set_ylabel("Residual")
    axes[0].set_title("Residuals vs Predicted")

    axes[1].hist(residuals, bins=50, edgecolor="black", alpha=0.7)
    axes[1].axvline(0, color="red", linestyle="--")
    axes[1].set_xlabel("Residual")
    axes[1].set_title("Residual Distribution")

    plt.suptitle(title)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_feature_importance(model, feature_names, top_n=20, title="Feature Importance", save_path=None):
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_)
    else:
        print("Model has no feature importance attribute.")
        return

    feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False)
    top = feat_imp.head(top_n)

    fig, ax = plt.subplots(figsize=(10, 6))
    top.sort_values().plot(kind="barh", ax=ax, color=sns.color_palette("mako", top_n))
    ax.set_xlabel("Importance")
    ax.set_title(title)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def print_report(results_df, task="regression"):
    print(f"\n{'='*60}")
    print(f"  AETHERIS — {task.upper()} Model Comparison")
    print(f"{'='*60}")

    if task == "regression":
        best_rmse = results_df["rmse"].idxmin()
        best_r2 = results_df["r2"].idxmax()
        print(f"  Best RMSE: {best_rmse} ({results_df.loc[best_rmse, 'rmse']:.2f})")
        print(f"  Best R²:   {best_r2} ({results_df.loc[best_r2, 'r2']:.4f})")
    else:
        best_f1 = results_df["f1"].idxmax()
        best_acc = results_df["accuracy"].idxmax()
        print(f"  Best F1:       {best_f1} ({results_df.loc[best_f1, 'f1']:.4f})")
        print(f"  Best Accuracy: {best_acc} ({results_df.loc[best_acc, 'accuracy']:.4f})")

    print(f"\n{results_df.round(4).to_string()}")
    print(f"{'='*60}\n")
