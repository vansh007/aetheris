export const regressionResults = [
  { model: "LinearRegression", rmse: 38.20, mae: 29.17, r2: 0.7600, mape: 24.19 },
  { model: "Ridge", rmse: 38.18, mae: 29.15, r2: 0.7602, mape: 24.15 },
  { model: "Lasso", rmse: 39.43, mae: 30.33, r2: 0.7410, mape: 26.33 },
  { model: "KNN", rmse: 32.71, mae: 24.02, r2: 0.8130, mape: 21.83 },
  { model: "RandomForest", rmse: 28.44, mae: 20.01, r2: 0.8650, mape: 18.01 },
  { model: "GradientBoosting", rmse: 27.49, mae: 19.32, r2: 0.8799, mape: 17.28 },
  { model: "XGBoost", rmse: 26.05, mae: 18.52, r2: 0.8877, mape: 16.42 },
  { model: "LightGBM", rmse: 25.60, mae: 18.33, r2: 0.8921, mape: 16.30 },
  { model: "CatBoost", rmse: 26.15, mae: 18.71, r2: 0.8847, mape: 16.67 }
];

export const classificationResults = [
  { model: "LightGBM", accuracy: 0.8859, precision: 0.8842, recall: 0.8859, f1: 0.8840 },
  { model: "XGBoost", accuracy: 0.8815, precision: 0.8805, recall: 0.8815, f1: 0.8795 },
  { model: "CatBoost", accuracy: 0.8791, precision: 0.8771, recall: 0.8791, f1: 0.8781 },
  { model: "RandomForest", accuracy: 0.8660, precision: 0.8650, recall: 0.8660, f1: 0.8630 },
];

// Feature importance from LightGBM model (top 10) - Leakage Removed
export const featureImportance = [
  { feature: "city_aqi_mean", importance: 0.282 },
  { feature: "rolling_mean_7d", importance: 0.194 },
  { feature: "aqi_lag_1", importance: 0.159 },
  { feature: "rolling_mean_30d", importance: 0.087 },
  { feature: "month", importance: 0.076 },
  { feature: "state_aqi_mean", importance: 0.062 },
  { feature: "rolling_std_7d", importance: 0.053 },
  { feature: "day_of_week", importance: 0.041 },
  { feature: "is_weekend", importance: 0.024 },
  { feature: "season_encoded", importance: 0.022 },
];
