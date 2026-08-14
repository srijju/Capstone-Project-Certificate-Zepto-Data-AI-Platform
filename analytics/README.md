# Analytics Module

This folder contains the analytics and machine learning workflow for the Zepto Data & AI Platform project.

It uses the Titanic dataset to demonstrate a complete data science pipeline:

- exploratory data analysis (EDA)
- missing value treatment
- outlier and distribution checks
- feature preprocessing and scaling
- classification modeling
- class imbalance handling
- hyperparameter tuning
- regression modeling
- model saving and reuse

---

## Project Structure

```text
analytics/
├── README.md
├── requirements.txt
├── eda.py
├── modeling.py
├── titanic.csv
├── titanic_cleaned.csv
├── plots/
├── outputs/
├── models/
└── ...
```

---

## Dataset

The project uses the Titanic dataset from Seaborn.

`eda.py` loads the dataset and saves an offline copy as:

```text
titanic.csv
```

This keeps the workflow reproducible and avoids depending on a live source at runtime.

---

## Setup

```bash
cd analytics
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Required packages:

```text
pandas>=2.2.2
numpy>=2.1.0
matplotlib>=3.9.2
seaborn>=0.13.2
scikit-learn>=1.5.1
imbalanced-learn>=0.12.3
joblib>=1.4.2
```

---

## Run the Pipeline

Run EDA first:

```bash
python eda.py
```

This script:

- loads the Titanic dataset
- checks missing values and data quality
- performs outlier analysis
- computes survival patterns by sex and passenger class
- creates visualizations
- saves a cleaned dataset as `titanic_cleaned.csv`

Then run modeling:

```bash
python modeling.py
```

This script:

- splits data into train/test sets
- preprocesses numeric and categorical features
- trains multiple classifiers
- compares accuracy, precision, recall, F1, and AUC
- handles class imbalance using weighted Logistic Regression and SMOTE
- tunes a Random Forest model with `GridSearchCV`
- builds a regression model for fare prediction
- saves the best model to `models/best_pipeline.joblib`

---

## Main Analysis Areas

### EDA

- missing value percentage analysis
- age and fare distribution checks
- survival rate by sex and passenger class
- correlation analysis
- standardization comparison
- output plots saved under `plots/`

### Modeling

- Logistic Regression
- Decision Tree
- Random Forest
- Linear Regression (for fare prediction)
- GridSearchCV tuning
- model evaluation metrics

---

## Key Outputs

### Data outputs

- `titanic.csv` — raw offline dataset
- `titanic_cleaned.csv` — cleaned dataset

### Plot outputs

Saved under `plots/`:

- age and fare histograms
- box plots
- correlation heatmap
- survival visualizations
- pair plot
- regression plots

### Metrics outputs

Saved under `outputs/`:

- `missing_percentage.csv`
- `model_comparison.csv`
- `class_imbalance_results.csv`
- `gridsearch_results.csv`
- `regression_results.csv`
- `sample_prediction.csv`

### Model output

- `models/best_pipeline.joblib`



# Data Preprocessing Decisions

## Missing Value Handling

Missing values were analysed by calculating the percentage of missing data in every column.

The following strategy was applied throughout the project:

| Missing Percentage | Strategy |
|--------------------|----------|
| Less than 5% | Median (numeric) or Mode (categorical) |
| Between 5% and 30% | Statistical imputation |
| Greater than 30% | Consider dropping the feature if it provides little predictive value |

Median imputation was selected for numeric variables because it is less sensitive to skewed distributions and outliers than the mean.

Categorical variables were imputed using the mode.

---

## Outlier Analysis

Outliers were identified using the Interquartile Range (IQR) method.

The analysis focused on:

- Age
- Fare

Rather than removing all outliers automatically, the project reports their counts and evaluates whether they represent genuine passenger observations or data quality issues.

---

## Feature Scaling

The numerical features were standardized using `StandardScaler`.

To demonstrate the effect of scaling, the distributions of **Age** and **Fare** were compared before and after standardization.

---

## Train-Test Split

A stratified train-test split was performed before any preprocessing.

Stratification preserves the survival class distribution in both training and testing datasets, ensuring unbiased evaluation.

All preprocessing steps (imputation, encoding, and scaling) were fitted **only on the training dataset** and applied to the testing dataset using transform-only operations to prevent data leakage.

---

# Model Evaluation

Three classification algorithms were evaluated.

- Logistic Regression
- Decision Tree
- Random Forest

Each model was evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion Matrix

Random Forest hyperparameters were optimized using **GridSearchCV**, and the Out-of-Bag (OOB) score was reported.

---

# Class Imbalance

Three approaches were compared.

1. Baseline model
2. Class-weighted Logistic Regression
3. SMOTE oversampling

SMOTE was applied only to the training data to avoid introducing information from the test dataset.

---

# Regression Analysis

A Linear Regression model was trained to predict passenger fare.

The following evaluation metrics were reported:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

Residual plots were used to assess heteroscedasticity.

---

# Model Comparison

The generated file

```
outputs/model_comparison.csv
```

contains the performance comparison of all trained classification models.

Regression metrics are stored separately in

```
outputs/regression_results.csv
```

This separation avoids mixing classification and regression metrics into a single comparison.

---

# Final Recommendation

Based on the evaluation metrics, the Random Forest classifier achieved the strongest overall predictive performance while maintaining good robustness after hyperparameter tuning.

The complete preprocessing and modeling pipeline was serialized using Joblib and saved as:

```
models/best_pipeline.joblib
```

The saved pipeline includes both the preprocessing steps and the trained estimator, allowing new raw passenger records to be processed and predicted end-to-end without repeating the training workflow.

---

# Assignment Checklist

| Requirement | Status |
|-------------|--------|
| Offline Titanic dataset | ✅ |
| Missing-value percentage analysis | ✅ |
| Percentage-based imputation | ✅ |
| IQR outlier detection | ✅ |
| Univariate analysis | ✅ |
| Bivariate analysis | ✅ |
| Multivariate analysis | ✅ |
| Correlation heatmap | ✅ |
| Stratified train-test split | ✅ |
| No data leakage | ✅ |
| Three classifiers | ✅ |
| Decision Tree visualization | ✅ |
| Full evaluation metrics | ✅ |
| Class imbalance comparison | ✅ |
| SMOTE | ✅ |
| GridSearchCV | ✅ |
| OOB Score | ✅ |
| Regression analysis | ✅ |
| Saved Joblib pipeline | ✅ |
| Model comparison | ✅ |