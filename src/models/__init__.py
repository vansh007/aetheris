"""
Aetheris — Model Definitions & Training
Regression, classification, tuning, SMOTE.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV, cross_val_score, TimeSeriesSplit
from xgboost import XGBRegressor, XGBClassifier
from lightgbm import LGBMRegressor, LGBMClassifier
from catboost import CatBoostRegressor, CatBoostClassifier
from imblearn.over_sampling import SMOTE
import joblib
import warnings
warnings.filterwarnings("ignore")


def get_regression_models():
    return {
        "LinearRegression": LinearRegression(),
        "Ridge": Ridge(alpha=1.0),
        "Lasso": Lasso(alpha=0.1),
        "KNN": KNeighborsRegressor(n_neighbors=5),
        "RandomForest": RandomForestRegressor(n_estimators=200, max_depth=20, random_state=42, n_jobs=-1),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42),
        "XGBoost": XGBRegressor(n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42, verbosity=0, n_jobs=-1),
        "LightGBM": LGBMRegressor(n_estimators=200, max_depth=10, learning_rate=0.1, random_state=42, verbose=-1, n_jobs=-1),
        "CatBoost": CatBoostRegressor(iterations=300, depth=6, learning_rate=0.1, random_seed=42, verbose=0),
    }


def get_classification_models():
    return {
        "RandomForest": RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42, n_jobs=-1),
        "XGBoost": XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42, verbosity=0, n_jobs=-1, eval_metric="mlogloss"),
        "LightGBM": LGBMClassifier(n_estimators=200, max_depth=10, learning_rate=0.1, random_state=42, verbose=-1, n_jobs=-1),
        "CatBoost": CatBoostClassifier(iterations=300, depth=6, learning_rate=0.1, random_seed=42, verbose=0),
    }


def get_tuning_grids():
    return {
        "Ridge": {"alpha": [0.01, 0.1, 1.0, 10.0, 100.0]},
        "RandomForest": {
            "n_estimators": [100, 200, 300],
            "max_depth": [10, 20, 30, None],
            "min_samples_split": [2, 5, 10],
        },
        "XGBoost": {
            "n_estimators": [100, 200, 300],
            "max_depth": [3, 5, 7],
            "learning_rate": [0.01, 0.05, 0.1],
            "subsample": [0.8, 1.0],
        },
        "LightGBM": {
            "n_estimators": [100, 200, 300],
            "max_depth": [5, 10, -1],
            "learning_rate": [0.01, 0.05, 0.1],
            "num_leaves": [31, 50, 100],
        },
    }


def train_all_models(models, X_train, y_train, X_test, y_test, task, cv=5):
    """Train all models and return results DataFrame + trained model dict."""
    from src.evaluation import regression_metrics, classification_metrics

    results = []
    trained = {}

    for name, model in models.items():
        print(f"  Training {name}...", end=" ", flush=True)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        if task == "regression":
            metrics = regression_metrics(y_test, y_pred)
            scoring = "neg_root_mean_squared_error"
        else:
            metrics = classification_metrics(y_test, y_pred)
            scoring = "f1_weighted"

        tscv = TimeSeriesSplit(n_splits=cv)
        cv_scores = cross_val_score(model, X_train, y_train, cv=tscv, scoring=scoring, n_jobs=-1)
        metrics["cv_mean"] = abs(cv_scores.mean())
        metrics["cv_std"] = cv_scores.std()
        metrics["model"] = name

        results.append(metrics)
        trained[name] = model
        print("done")

    results_df = pd.DataFrame(results).set_index("model")
    return results_df, trained


def tune_model(model, param_grid, X_train, y_train, scoring="neg_root_mean_squared_error", cv=5):
    tscv = TimeSeriesSplit(n_splits=cv)
    search = GridSearchCV(model, param_grid, scoring=scoring, cv=tscv, n_jobs=-1, verbose=0, refit=True)
    search.fit(X_train, y_train)
    print(f"  Best params: {search.best_params_}")
    print(f"  Best CV score: {abs(search.best_score_):.4f}")
    return search.best_estimator_, search.best_params_


def apply_smote(X_train, y_train, random_state=42):
    smote = SMOTE(random_state=random_state)
    X_res, y_res = smote.fit_resample(X_train, y_train)
    print(f"[SMOTE] {len(X_train):,} -> {len(X_res):,} samples")
    return X_res, y_res


def save_model(model, filepath):
    joblib.dump(model, filepath)
    print(f"[SAVE] Model saved to {filepath}")


def load_model(filepath):
    return joblib.load(filepath)
