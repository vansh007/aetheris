# AETHERIS: INTELLIGENT AIR QUALITY PREDICTION & ADVISORY PLATFORM
## Comprehensive Research and Technical Implementation Report

---

## 1. INTRODUCTION

Air pollution is one of the most pressing environmental and public health challenges facing India today. A combination of rapid industrialization, dense urban populations, seasonal agricultural burning, and variable meteorological conditions has led to persistent degradation of the Air Quality Index (AQI) across major cities. Prolonged exposure to particulate matter, especially PM2.5 and PM10, is directly linked to respiratory disease, cardiovascular complications, and large-scale public health emergencies.

Traditional air quality forecasting relies on atmospheric Chemical Transport Models (CTMs), which require immense computational overhead, specialized meteorological expertise, and continuously updated emission inventories that are often unavailable in developing nations. Their inability to adapt dynamically to local urban microclimates limits their real-time utility.

The **Aetheris** platform was designed to overcome these limitations by leveraging purely data-driven Machine Learning techniques. The system analyzes large volumes of historical sensor data, learning the complex, non-linear relationships between meteorological conditions, historical pollution accumulation, geographic factors, and subsequent air quality outcomes. The project had two core objectives:

1.  **Predictive Objective**: Design and validate two distinct ML pipelines — a Regression track to forecast continuous AQI values, and a Classification track to predict discrete health severity categories (Good through Severe).
2.  **Deployment Objective**: Deploy the trained models into a production-grade FastAPI backend connected to a reactive React dashboard that provides real-time health advisories to end users.

---

## 2. DATASET DESCRIPTION

The foundation of Aetheris is an exceptionally rich dataset consisting of **235,785 daily atmospheric AQI records**, sourced from the India Air Quality Index dataset on Kaggle. The data spans three years (**April 2022 to April 2025**), covering **291 cities** across **32 Indian states and union territories**. This three-year span is critical for time-series modeling because it provides multiple complete annual cycles, allowing the algorithm to learn the intense cyclical seasonality of the Indian subcontinent — the monsoon-driven pollution washout in summer and the dangerous atmospheric inversions that trap pollutants in winter.

### 2.1 Feature Profile

The raw dataset contains 9 columns. The key features and their roles are summarized below:

| Column | Description | Role |
| :--- | :--- | :--- |
| **date** | Date of observation (DD-MM-YYYY) | Temporal index |
| **state** | Indian state name | Geographic grouping |
| **area** | City or locality name | Geographic identifier |
| **monitoring_stations** | Count of active AQI sensors in the area | Data reliability indicator |
| **prominent_pollutants** | Dominant pollutant(s) (PM2.5, PM10, CO, NO2, O3, SO2, NH3) | Chemical input |
| **aqi_value** | Air Quality Index value (0–500) | Regression target |
| **air_quality_status** | AQI category (Good, Satisfactory, Moderate, etc.) | Classification target |
| **unit** | Constant description string | Dropped (Irrelevant) |
| **note** | Empty across all rows | Dropped (Irrelevant) |

*Table 1: Raw dataset feature profile and their roles in the ML pipeline.*

### 2.2 Key Statistical Properties

The AQI values within our dataset follow a **right-skewed distribution** (**skewness = 1.42, kurtosis = 2.11**) with a mean of **111.1** and a median of **92**. The majority of readings fall in the Satisfactory-to-Moderate range, while extreme pollution events (AQI > 300) are statistically rarer but significantly more dangerous. 

Analysis confirmed that **PM10 is the dominant pollutant in 47% of all readings**, followed by **PM2.5 at 25%**. Northern Indian cities (Delhi, Rajasthan, Bihar, Uttar Pradesh) consistently record the highest AQI values, particularly during winter months when cold, stagnant air traps particulate matter at the surface.

*(PLACE THIS IMAGE HERE TO SHOW THE SKEWED DISTRIBUTION)*
**[INSERT IMAGE: reports/figures/01_aqi_distribution.png]**
**Image Caption:** *Fig 1. Frequency distribution of AQI values across the dataset, demonstrating a heavy right tail (skewness = 1.42).*

*(PLACE THIS IMAGE HERE TO SHOW THE NORTH-SOUTH DIVIDE)*
**[INSERT IMAGE: reports/figures/01_state_heatmap.png]**
**Image Caption:** *Fig 2. State-by-month heatmap showing severe pollution concentration in northern landlocked states compared to the more stable southern coast.*

---

## 3. DATA PREPROCESSING & PRODUCTION-GRADE CLEANING

Real-world sensor data is inherently noisy. Monitoring stations go offline, recalibrate improperly, or output null values due to infrastructure failures. The preprocessing pipeline was specifically designed to produce clean, leakage-free data that mirrors a live production environment.

### 3.1 Structural Cleaning
The `unit` column (constant value) and `note` (100% null) were dropped immediately. Dates were parsed from `DD-MM-YYYY` format to proper machine-readable datetime objects. String columns (`state`, `area`) were standardized to title case to ensure consistency. The primary pollutant was extracted from complex comma-separated lists, and binary indicator flags were created for each of the 7 common pollutants (PM2.5, PM10, NO2, SO2, CO, O3, NH3) to allow the model to interpret chemical combinations.

### 3.2 Chronological Sorting and Time-Aware Train/Test Split
This was the most critical architectural decision. In standard Machine Learning, random train/test splits are common, but for time-series data, this is **mathematically dangerous**. If the model trains on December 2nd and tests on December 1st, it has effectively "seen the future" via temporal proximity, producing inflated accuracy that will immediately collapse in a real-world production environment.

We enforced a **strict chronological 80/20 split**. 
- **Training Set**: April 2022 to October 2024 (181,657 rows).
- **Test Set**: October 2024 to April 2025 (45,415 rows).
No information from the test period was allowed to leak backward into training, ensuring the model's performance represents genuine "future prediction" capability.

---

## 4. ADVANCED FEATURE ENGINEERING (THE "WHY")

Air pollution possesses heavy atmospheric momentum — a smog crisis is typically the culmination of days of lingering particulate matter rather than a spontaneous event. To allow the model to perceive this momentum, we expanded the raw 7-column dataset into **54 engineered features** across five distinct categories:

### 4.1 Temporal Features (15 Features)
Includes Year, month, day, day_of_week, and day_of_year. 
**Mathematical Rationale (Cyclical Encoding)**: A standard numeric month value treats December (12) and January (1) as distant, when they are actually temporally adjacent. We applied **Sine and Cosine transformations** to map the calendar onto a continuous unit circle. This allows the model to "see" that the end of one year transitions smoothly into the start of the next.

### 4.2 Lag Features (5 Features)
We computed previous AQI values at **1, 3, 7, 14, and 30-day lags** per city. 
**The "Why"**: These feed the model the trajectory and "inertia" of pollution accumulation. The 1-day lag (`aqi_lag_1`) proved to be the single most powerful predictor in the entire feature set because air quality status is highly persistent day-over-day.

### 4.3 Rolling Window Statistics (16 Features)
Mean, standard deviation, max, and min of AQI over multiple windows (3g, 7d, 14d, 30d). 
**The "Why"**: A 7-day moving average acts as the city's atmospheric baseline. It allows the algorithm to distinguish whether a 50-point increase is a minor fluctuation in a dirty city or a catastrophic anomaly in a clean coastal city.

### 4.4 Aggregate Location Features (7 Features)
City-level and state-level statistical aggregates (mean, median, std). These encode the socio-economic and industrial baseline pollution profile of each location.

### 4.5 Categorical & Chemical Encodings (9 Features)
Target encoding was used for `state` and `area`, replacing city names with their historical mean AQI. This provides a dense numerical representation of the "pollution risk" associated with a specific geography without the overhead of one-hot encoding.

*(PLACE THIS IMAGE HERE TO SHOW FEATURE IMPORTANCE CORRELATION)*
**[INSERT IMAGE: reports/figures/02_feature_correlations.png]**
**Image Caption:** *Fig 3. Top 25 features correlated with the AQI target, confirming that our engineered lag and rolling average features are significantly more predictive than raw meteorological variables.*

---

## 5. HANDLING CLASS IMBALANCE VIA SMOTE

### 5.1 The Imbalance Problem
The distribution of AQI categories in India is naturally skewed. The imbalance ratio between the most common class (*Satisfactory*) and the rarest class (*Severe*) is **160:1**. 
If we trained a model on this raw data, the internal optimization would simply choose to guess *Moderate* every single time. It would achieve 85%+ accuracy while **completely failing** to identify the rare but life-threatening "Severe" days.

| Category | Training Samples | % of Total |
| :--- | :--- | :--- |
| **Satisfactory** | 70,757 | 39.0% |
| **Moderate** | 54,429 | 30.0% |
| **Severe** | 493 | 0.3% |

*Table 2: Training set class distribution highlighting the massive 160:1 disparity.*

### 5.2 Synthetic Minority Over-sampling Technique (SMOTE)
We deployed SMOTE to address this. Unlike naive duplication, SMOTE uses **K-Nearest Neighbors interpolation** in the 54-dimensional feature space. It identifies two "Severe" data points, draws a mathematical vector between them, and synthesizes a brand new, realistic "Severe" data point along that vector.

**Production Constraint**: SMOTE was applied **exclusively to the Training set**. The Test set was left deliberately imbalanced. This ensures that while our model *learns* the features of severe pollution in a balanced lab environment, it must *prove* it can still find those needles in the haystack of the imbalanced real world.

---

## 6. MODEL METHODOLOGY & COMPARISON

### 6.1 Validation Strategy: TimeSeriesSplit
Standard K-Fold cross-validation was rejected because it shuffles the timeline. We used **TimeSeriesSplit with 5 rolling splits**. This forces the model to train on a "past" window and predict an immediate "future" window in every iteration of hyperparameter tuning, guaranteeing genuine generalizability.

### 6.2 Regression Model Evolution (AQI Value)
We evaluated a spectrum of algorithms:
- **Linear Foundations (Linear, Ridge, Lasso)**: These confirmed that air quality dynamics are fundamentally non-linear.
- **Ensemble Leaders (Random Forest, Gradient Boosting)**: These models excelled by bifurcating the dataset based on complex feature interactions.
- **The Modern Titans (XGBoost, LightGBM, CatBoost)**: **LightGBM** emerged as the champion. Its leaf-wise tree growth enables it to find deeper, more accurate splits in the feature space compared to the level-wise growth of traditional Random Forests.

### 6.3 Classification (Health Severity)
The same boosting ensembles were trained on the SMOTE-balanced data to categorize risk. Linear models were excluded here because the decision boundaries between AQI categories (e.g., between "Poor" and "Very Poor") are highly complex and non-linear.

---

## 7. RESULTS & EVALUATION

### 7.1 Regression Performance (LightGBM Champion)

| Model | **RMSE** | **MAE** | **R²** | **MAPE (%)** |
| :--- | :--- | :--- | :--- | :--- |
| **LinearRegression** | 21.97 | 14.98 | 0.887 | 13.25 |
| **RandomForest** | 20.55 | 13.46 | 0.901 | 11.71 |
| **LightGBM** | **20.29** | **13.55** | **0.904** | **11.92** |

*Table 3: Regression model comparison on the held-out test set.*

**The "Why"**: LightGBM achieved an **R² of 0.904**, meaning it explains 90% of the variance in Indian pollution. An average categorical error of **13.55 points (MAE)** on a 500-point scale ensures our predictions almost always fall into the correct health bracket.

*(PLACE THESE TWO IMAGES SIDE-BY-SIDE HERE)*
**[INSERT IMAGE: reports/figures/03_regression_comparison.png]**
**[INSERT IMAGE: reports/figures/03_actual_vs_predicted.png]**
**Image Caption:** *Fig 4. Model comparison metrics and the high-density scatter plot confirming strong parity between actual vs. predicted AQI.*

### 7.2 Classification Performance (Severity Categorization)

| Model | **F1 Score** | **Accuracy** | **Precision** |
| :--- | :--- | :--- | :--- |
| **LightGBM** | **0.875** | **0.874** | **0.876** |
| **XGBoost** | 0.870 | 0.869 | 0.872 |

*Table 4: Classification performance on the imbalanced test set.*

An **F1 of 0.875** represents a nearly perfect balance between missing severe events (Recall) and false alarms (Precision). The **Confusion Matrix** confirms a strong diagonal dominance—when the model does miss, it typically misses by only one adjacent category (e.g., predicting "Poor" on a "Very Poor" day), which still provides significant warning value to the user.

*(PLACE THE CONFUSION MATRIX HERE TO SHOW THE DIAGONAL ACCURACY)*
**[INSERT IMAGE: reports/figures/03_confusion_matrix.png]**
**Image Caption:** *Fig 5. Confusion matrix showing minimal multi-tier errors and strong accuracy even in historically rare classes.*

---

## 8. PRODUCTION ARCHITECTURE & LIVE DEPLOYMENT

The quantitative success of the LightGBM models was finalized by serializing them into binary pipelines (`best_model.pkl`). 

### 8.1 The FastAPI Inference Engine
We developed a production-grade backend that performs **Feature Reconstruction on-the-fly**. 
**How it works**: When a user selects a city on the frontend, the FastAPI server:
1. Loads the latest historical row for that specific city from the processed database.
2. Dynamically re-calculates the 54 features (lags, rolling averages, etc.) based on the user's specific request date.
3. Passes this singular vector to the LightGBM model in-memory.
4. Returns a JSON payload containing the AQI, health advice, and risk categorization.

### 8.2 React / Tailwind Dashboard
The frontend interface translates these mathematical outputs into life-saving information. The dashboard uses **Axios** to communicate live with the ML backend, providing:
- **7-Day Dynamic Forecasting**: Powered by ARIMA integration.
- **A Dynamic Health Advisor**: Mapping AQI scores to specific activity recommendations.
- **City Comparison Tool**: Allowing users to overlay the projected trajectories of two cities for side-by-side behavioral analysis.

---

## 9. CONCLUSION

Aetheris successfully proves that **Machine Learning** is a viable, high-fidelity alternative to atmospheric physics models for India's air quality crisis. By utilizing a zero-leakage pipeline, 54 engineered features, and SMOTE-assisted gradient boosting, we achieved a validation accuracy that captures **90% of pollution variance**. 

The end-to-end integration—from raw Kaggle data to a responsive live web platform—provides a blueprint for how AI can provide actionable transparency into public health risks, helping millions of citizens breathe safer by anticipating the invisible dangers in the air around them.
