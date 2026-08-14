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

---

## Notes

This module is a demonstration pipeline for analytics and ML workflows using tabular data. It is structured so it can be reused and extended for other datasets or capstone projects.