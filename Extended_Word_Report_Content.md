# AETHERIS: INTELLIGENT AIR QUALITY PREDICTION & ADVISORY SYSTEM
## Comprehensive Project Report

---

## 1. INTRODUCTION

Air pollution is one of the most critical environmental and public health challenges facing India today. Driven by a complex intersection of rapid industrialization, dense urban population centers, seasonal agricultural practices (such as stubble burning), and highly variable geographic and meteorological conditions, the Air Quality Index (AQI) in India fluctuates with dangerous volatility. Prolonged exposure to toxic particulate matter (PM2.5 and PM10) leads to severe respiratory and cardiovascular diseases, making early warning systems vital for public safety.

Traditionally, air quality forecasting has relied on resource-heavy atmospheric physics and chemical-transport models, which are often slow to compute and struggle to adapt to hyper-local urban microclimates. The **Aetheris** platform was conceived to bridge this gap by leveraging advanced, data-driven Machine Learning techniques. 

By analyzing massive volumes of historical pollution and meteorological data, Aetheris seeks to achieve two primary objectives:
1. **Accurate Forecasting**: To predict near-term continuous AQI values (Regression) and actionable severity brackets (Classification) with high accuracy across hundreds of Indian cities.
2. **Actionable Public Health Interface**: To deploy these predictions into a responsive, real-time web dashboard that issues dynamic health advisories, enabling citizens to make informed decisions about outdoor exposure.

This report details the end-to-end methodology utilized in developing Aetheris—from raw data ingestion, rigorous preprocessing, and feature engineering, to the deployment of advanced tree-based ensemble models validated via strict time-series protocols.

---

## 2. DATASET DETAIL

The validity of any machine learning model is inherently tied to the richness of its underlying dataset. The primary dataset compiled for Aetheris is exceptionally comprehensive, containing **235,785 daily records** spanning a 3-year period from **April 2022 to April 2025**. 

### Geographic & Temporal Scope
The geographical coverage of the dataset is vast, encompassing **291 individual cities** distributed across **32 Indian states and union territories**. This extensive coverage allows the model to learn localized pollution signatures—from the heavily industrialized northern plains to the coastal breeze ecosystems of the south. The three-year temporal span is critical because it captures multiple complete annual cycles, exposing the algorithms to the intense seasonality of the Indian subcontinent (e.g., monsoon smog clearance and winter inversion layers).

*(PLACE THIS IMAGE HERE TO SHOW THE GEOGRAPHIC DISTRIBUTION OF POLLUTION)*
**[INSERT IMAGE: reports/figures/01_state_heatmap.png]**
**Image Caption:** *Geospatial Heatmap demonstrating the severe baseline pollution density concentrated in the northern and central states of India.*

### Feature Profile
The raw dataset contains detailed feature vectors that can be categorized into three main distinct domains:
1. **Pollutant Concentrations**: The foundational data consisting of specific toxic gases and particulate matter, including PM2.5, PM10, Nitrogen Dioxide (NO2), Nitrogen Oxides (NOx), Ammonia (NH3), Sulfur Dioxide (SO2), Carbon Monoxide (CO), and Ground-level Ozone. PM2.5 and PM10 are the most significant drivers of AQI spikes in India.
2. **Meteorological Context**: Atmospheric conditions dictate whether pollution disperses or settles. The dataset includes Ambient Temperature, Relative Humidity, Wind Speed, and general weather categorizations.
3. **Target Variables**: 
   - `aqi_value`: The continuous numeric index representing absolute pollution concentration (used for the Regression track).
   - `aqi_category`: The bucketed severity status (Good, Satisfactory, Moderate, Poor, Very Poor, Severe) utilized by governmental bodies (used for the Classification track).

*(PLACE THIS IMAGE HERE TO SHOW HOW PM2.5 AND PM10 DOMINATE THE AQI)*
**[INSERT IMAGE: reports/figures/01_pollutant_breakdown.png]**
**Image Caption:** *A pie chart illustrating the proportional breakdown of pollutants, highlighting the dominance of PM10 and PM2.5 in driving hazardous air days.*

*(PLACE THIS IMAGE TO SHOW THE MACRO TREND OVER 3 YEARS)*
**[INSERT IMAGE: reports/figures/01_monthly_trend.png]**
**Image Caption:** *Historical line chart showing the cyclical nature of AQI peaks over the 3-year timeline.*

---

## 3. PREPROCESSING STEPS & FEATURE ENGINEERING

Raw sensor data is inherently messy; sensors drift, go offline, or report anomalous spikes. Furthermore, machine learning models do not inherently understand "time." Our preprocessing pipeline was designed to be extraordinarily rigorous, particularly concerning the prevention of **Data Leakage**—a fatal flaw in time-series machine learning where a model accidentally learns from "future" data during training.

### Stage 1: Data Cleaning and Chronological Ordering
The dataset was first stripped of redundant columns and explicitly sorted by date. Missing numerical values (NaNs) caused by sensor downtime were handled via sequential forward-filling. This mimics exactly how a live production system operates: if today's sensor is broken, we assume the pollution level remains equivalent to yesterday's last known reading.

### Stage 2: Time-Aware Train/Test Splitting
**Why we did it:** If we applied a random split to time-series data, we would train the model on data from December 2024 and ask it to predict data from January 2023. This is scientifically invalid. 
**How we did it:** We executed a strict **chronological 80/20 split**. The first 80% of the timeline became the Training Set, and the final 20% became the completely sequestered Test Set. Crucially, this split was performed *before* complex features were engineered.

### Stage 3: Feature Engineering
Pollution doesn't happen in a vacuum; today's smog is heavily influenced by yesterday's stagnant air. To teach the model this "momentum," we engineered 53 specific features strictly using past data:

1. **Temporal Deconstruction**: Dates were converted into mathematical signals. We extracted `month`, `day_of_week`, and `day_of_year`. To help the model understand that December 31st is right next to January 1st, we applied Sine and Cosine cyclical transformations.
2. **Lagged Variables**: We generated `aqi_lag_1` through `aqi_lag_7`. This feeds the model the exact AQI values of the prior 7 days.
3. **Rolling Statistics**: We computed 7-day and 30-day moving averages (`rolling_mean`) and standard deviations (`rolling_std`). This captures whether a city is currently in a prolonged pollution wave or a clearing phase.
4. **Target Encoding**: We converted text-based city and state names into numeric values by mapping them to their historical average AQI (`city_aqi_mean`). **Crucially, this mean was calculated ONLY using the training data.** If we used the whole dataset, information from the future test set would "leak" into the training set, artificially inflating our accuracy.
5. **Purging Leaky Features**: Upon auditing, we discovered a raw column named `pollution_risk_score` which was mathematically derived directly from the target AQI. It was immediately dropped to prevent the model from simply reverse-engineering the answer key.

*(PLACE THIS IMAGE HERE TO PROVE THE NEW FEATURES MATTERED TO THE TARGET)*
**[INSERT IMAGE: reports/figures/02_feature_correlations.png]**
**Image Caption:** *Correlation matrix proving that our engineered temporal features (like rolling means and lags) correlate significantly better to the target AQI than isolated weather metrics.*

---

## 4. HANDLING CLASS IMBALANCE

### The Problem
When predicting the specific `aqi_category` (Good vs. Severe), we encountered massive class imbalance. In India, a vast majority of the days fall within the *Satisfactory (50-100)* or *Moderate (100-200)* range. Conversely, extremely hazardous *Severe (400+)* days represent a tiny statistical minority of the dataset.
If we train a classification algorithm on this skewed data, the model will simply "guess" Moderate every single time to achieve a high general accuracy, failing completely to identify the rare but life-threatening severe pollution days.

*(PLACE THIS IMAGE HERE TO VISUALLY PROVE THE IMBALANCE TO THE READER)*
**[INSERT IMAGE: reports/figures/01_category_counts.png]**
**Image Caption:** *Histogram displaying the highly skewed distribution of historical AQI status categories, heavily biased toward Moderate and Satisfactory days.*

### The Solution: SMOTE
To solve this, we applied **SMOTE (Synthetic Minority Over-sampling Technique)**. 
**Why we did it:** SMOTE does not just duplicate existing data (which causes overfitting). Instead, it analyzes the minority class vectors in n-dimensional space and uses a K-Nearest Neighbors mathematical algorithm to artificially synthesize brand new, realistic data points that look exactly like "Severe" pollution days. 

**Application Rule:** We applied SMOTE *exclusively* to the Training set. The test set was left entirely untouched and imbalanced. Why? Because the test set must perfectly mirror the messy, imbalanced reality of the real world. By SMOTE-ing the training data, we forced the model to learn the mathematical boundaries of extreme pollution without cheating the final exam.

---

## 5. MODEL USED DESCRIPTION

Aetheris utilizes two distinct machine learning tracks to accomplish its goals, evaluated with highly customized validation strategies.

### Validation Strategy: TimeSeriesSplit
Standard Cross-Validation involves randomly slicing the training data into 5 chunks and intermingling them. As established, randomized data destroys the fabric of time-series causality. 
**Why we did it:** To tune our models, we implemented `TimeSeriesSplit(n_splits=5)`. This rolling-origin technique trains the model on Chunk 1, tests on Chunk 2. Then it trains on Chunks 1+2, and tests on Chunk 3. This mathematically guarantees that the algorithms learn to forward-predict, rather than simply memorizing randomized static patterns.

### Track A: Regression (Predicting Absolute AQI values)
We evaluated a vast array of algorithms, establishing baselines and pushing toward state-of-the-art:
1. **Linear Baselines (Linear, Ridge, Lasso)**: Simple models used to see if pollution behaves linearly. (It does not).
2. **K-Nearest Neighbors (KNN)**: Looks for similar weather/lag days in the past.
3. **Tree-Based Ensembles (Random Forest, Gradient Boosting)**: Decision trees excel at handling non-linear data bounded by complex thresholds (e.g., if Temp > 30 and Wind < 5 and Lag_AQI > 200). 
4. **Advanced Gradient Boosting (XGBoost, LightGBM, CatBoost)**: The industry standard for tabular data. These frameworks iteratively build trees, each new tree specifically targeting the errors made by the previous trees. LightGBM, utilizing leaf-wise tree growth, is particularly efficient on high-dimensional data consisting of 200k+ rows.

### Track B: Classification (Categorizing Health Risk)
Because SMOTE expanded our training data significantly, we relied exclusively on powerful, memory-efficient ensemble methods (Random Forest, XGBoost, CatBoost, LightGBM) to handle the multi-class prediction (distinguishing between 6 strict severity brackets).

### Track C: Decomposition Methodology
To fuel the frontend 7-day prediction UI independently, we juxtaposed the structural machine learning inputs against classical econometric forecasting tools (**ARIMA** and Facebook's **Prophet**). We decomposed the historical timeline into three components: Trend (macro long-term tracking), Seasonal (recurring annual smog cycles), and Residual (unpredictable noise).

*(PLACE THIS IMAGE HERE TO SHOW THE SEASONAL BREAKDOWN)*
**[INSERT IMAGE: reports/figures/04_decomposition.png]**
**Image Caption:** *Time series decomposition isolating the pure annual seasonal cycle from long-term macro trends.*

---

## 6. RESULTS & PLATFORM INTEGRATION

After comprehensive grid-search tuning via `TimeSeriesSplit`, the gradient boosting frameworks fundamentally outperformed legacy models.

### Regression Results
**LightGBM** emerged as the undisputed champion algorithm for predicting raw AQI figures:
*   **Root Mean Squared Error (RMSE)**: ~25.60
*   **Mean Absolute Error (MAE)**: ~18.33
*   **R² Score:** ~0.89 
This implies the model can explain nearly 90% of the variance in Indian air pollution. An RMSE of ~25 is remarkably tight given that the AQI scale physically stretches from 0 to 500, meaning our model is generally only off by a fraction of a category bracket.

*(PLACE THESE TWO IMAGES SIDE-BY-SIDE HERE TO SHOW MODEL COMPARISONS AND ACCURACY)*
**[INSERT IMAGE: reports/figures/03_regression_comparison.png]**
**[INSERT IMAGE: reports/figures/03_actual_vs_predicted.png]**
**Image Caption:** *Left: Model comparison charts highlighting Gradient Boosting dominance. Right: Scatter plot showing strong alignment between predicted AQI and actual AQI in the test set.*

Furthermore, the **Feature Importance** graph proved our engineering thesis correct. The model relied overwhelmingly on our engineered aggregates (`city_aqi_mean`, `rolling_mean_7d`, and `aqi_lag_1`) rather than raw daily temperature or humidity. 

*(PLACE THIS IMAGE HERE TO PROVE THE PIPELINE WORKED)*
**[INSERT IMAGE: reports/figures/03_feature_importance.png]**
**Image Caption:** *LightGBM internal Feature Importance rankings, proving historical rolling momentum is the primary scientific driver of future pollution.*

### Classification Results
On the Classification track, **LightGBM** and **XGBoost** shared the crown, achieving a macro **F1 Score of ~0.88**.
Thanks to SMOTE, the classifier successfully identified the dangerous `Severe` class days that previous iterations had missed. The confusion matrix below demonstrates a tight diagonal density, indicating that when the model did misclassify a day, it almost always missed by a single adjacent severity bracket (e.g., guessing Poor instead of Very Poor), rather than catastrophic misses.

*(PLACE THIS CONFUSION MATRIX HERE TO PROVE CLASSIFICATION ACCURACY)*
**[INSERT IMAGE: reports/figures/03_confusion_matrix.png]**
**Image Caption:** *Validation confusion matrix detailing high model recall across all 6 severely imbalanced pollutant brackets.*

### Final Production Conclusion
With the quantitative validity of the algorithms proven, the models (`best_model.pkl`) were frozen and integrated directly into a production-grade **FastAPI Backend**. When users select a city via the **React + Tailwind UI**, the platform instantaneously constructs a massive 53-variable feature vector containing the historical rolling context of that city, passes it to the LightGBM models in-memory, and dynamically generates actionable, mathematically-sound health advisories and comparative visualizations. 

Aetheris succeeds entirely as a comprehensive, strictly accurate, and highly modular Air Quality prediction framework.
