import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
    roc_auc_score
)

from sklearn.tree import plot_tree
from imblearn.over_sampling import SMOTE

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import joblib
import os

os.makedirs("models", exist_ok=True)

import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("titanic_cleaned.csv")

print(df.head())
print(df.shape)

print("=" * 80)
print("CLASS DISTRIBUTION")
print("=" * 80)

class_counts = df["survived"].value_counts()

print(class_counts)

print("\nClass Percentage")

class_percentage = (
    df["survived"]
      .value_counts(normalize=True)
      .mul(100)
      .round(2)
)

print(class_percentage)

X = df[
    [
        "pclass",
        "sex",
        "age",
        "sibsp",
        "parch",
        "fare",
        "embarked"
    ]
]

y = df["survived"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training Set Distribution")

print(
    y_train.value_counts(normalize=True)
)

print("\nTesting Set Distribution")

print(
    y_test.value_counts(normalize=True)
)

print("=" * 80)

print("Training Shape")

print(X_train.shape)

print("Testing Shape")

print(X_test.shape)

numeric_features = [
    "age",
    "fare",
    "sibsp",
    "parch",
    "pclass"
]

categorical_features = [
    "sex",
    "embarked"
]

numeric_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "scaler",
            StandardScaler()
        )
    ]
)

categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(handle_unknown="ignore")
        )
    ]
)

preprocessor = ColumnTransformer(

    transformers=[

        (
            "num",
            numeric_transformer,
            numeric_features
        ),

        (
            "cat",
            categorical_transformer,
            categorical_features
        )

    ]

)


logistic_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(
            random_state=42,
            max_iter=1000
        ))
    ]
)

decision_tree_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", DecisionTreeClassifier(
            random_state=42
        ))
    ]
)

random_forest_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            random_state=42
        ))
    ]
)

logistic_pipeline.fit(X_train, y_train)

decision_tree_pipeline.fit(X_train, y_train)

random_forest_pipeline.fit(X_train, y_train)

models = {
    "Logistic Regression": logistic_pipeline,
    "Decision Tree": decision_tree_pipeline,
    "Random Forest": random_forest_pipeline
}

results = []

for model_name, model in models.items():

    y_pred = model.predict(X_test)

    y_prob = model.predict_proba(X_test)[:,1]

    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(y_test, y_pred)

    recall = recall_score(y_test, y_pred)

    f1 = f1_score(y_test, y_pred)

    auc = roc_auc_score(y_test, y_prob)

    results.append({

        "Model": model_name,

        "Accuracy": accuracy,

        "Precision": precision,

        "Recall": recall,

        "F1 Score": f1,

        "AUC": auc

    })

    print("="*80)

    print(model_name)

    print("="*80)

    print("Accuracy :", accuracy)

    print("Precision:", precision)

    print("Recall   :", recall)

    print("F1 Score :", f1)

    print("AUC      :", auc)


    cm = confusion_matrix(
        y_test,
        y_pred
    )

    ConfusionMatrixDisplay(
        confusion_matrix=cm
    ).plot()

    plt.title(model_name)

    plt.show()


fpr, tpr, _ = roc_curve(
    y_test,
    y_prob
)

plt.figure(figsize=(6,5))

plt.plot(
    fpr,
    tpr,
    label=f"AUC = {auc:.3f}"
)

plt.plot(
    [0,1],
    [0,1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")

plt.ylabel("True Positive Rate")

plt.title(f"ROC Curve - {model_name}")

plt.legend()

plt.show()

plt.figure(figsize=(20,10))

tree_model = decision_tree_pipeline.named_steps[
    "classifier"
]

fitted_preprocessor = decision_tree_pipeline.named_steps["preprocessor"]

feature_names = fitted_preprocessor.get_feature_names_out()

plot_tree(

    tree_model,

    feature_names=feature_names,

    class_names=["Not Survived","Survived"],

    filled=True,

    rounded=True,

    fontsize=8

)

plt.title("Decision Tree")

plt.show()

comparison_df = pd.DataFrame(results)

comparison_df = comparison_df.round(4)

comparison_df

comparison_df.to_csv(
    "outputs/model_comparison.csv",
    index=False
)

baseline_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(
            random_state=42,
            max_iter=1000
        ))
    ]
)

baseline_pipeline.fit(X_train, y_train)

baseline_pred = baseline_pipeline.predict(X_test)

baseline_f1 = f1_score(
    y_test,
    baseline_pred
)

print(f"Baseline F1 Score: {baseline_f1:.4f}")

balanced_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(
            random_state=42,
            max_iter=1000,
            class_weight="balanced"
        ))
    ]
)

balanced_pipeline.fit(X_train, y_train)

balanced_pred = balanced_pipeline.predict(X_test)

balanced_f1 = f1_score(
    y_test,
    balanced_pred
)

print(f"Balanced F1 Score: {balanced_f1:.4f}")

X_train_preprocessed = preprocessor.fit_transform(X_train)

X_test_preprocessed = preprocessor.transform(X_test)

smote = SMOTE(
    random_state=42
)

X_smote, y_smote = smote.fit_resample(
    X_train_preprocessed,
    y_train
)

print(pd.Series(y_smote).value_counts())

smote_model = LogisticRegression(
    random_state=42,
    max_iter=1000
)

smote_model.fit(
    X_smote,
    y_smote
)

smote_pred = smote_model.predict(
    X_test_preprocessed
)

smote_f1 = f1_score(
    y_test,
    smote_pred
)

print(f"SMOTE F1 Score: {smote_f1:.4f}")

imbalance_results = pd.DataFrame({

    "Method":[
        "Baseline",
        "Class Weight",
        "SMOTE"
    ],

    "F1 Score":[
        baseline_f1,
        balanced_f1,
        smote_f1
    ]

})

imbalance_results = imbalance_results.round(4)

print(imbalance_results)

imbalance_results.to_csv(
    "outputs/class_imbalance_results.csv",
    index=False
)

rf_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            random_state=42,
            oob_score=True,
            bootstrap=True
        ))
    ]
)

param_grid = {

    "classifier__n_estimators": [
        100,
        200
    ],

    "classifier__max_depth": [
        None,
        5,
        10
    ],

    "classifier__min_samples_split": [
        2,
        5,
        10
    ]

}

grid_search = GridSearchCV(

    estimator=rf_pipeline,

    param_grid=param_grid,

    scoring="f1",

    cv=5,

    n_jobs=-1,

    verbose=1

)

grid_search.fit(
    X_train,
    y_train
)

print("=" * 80)
print("BEST PARAMETERS")
print("=" * 80)

print(grid_search.best_params_)

print("=" * 80)
print("BEST CV F1 SCORE")
print("=" * 80)

print(grid_search.best_score_)

best_model = grid_search.best_estimator_

y_pred = best_model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred
)

recall = recall_score(
    y_test,
    y_pred
)

f1 = f1_score(
    y_test,
    y_pred
)

print("=" * 80)
print("TEST PERFORMANCE")
print("=" * 80)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

rf_classifier = best_model.named_steps["classifier"]

print("=" * 80)
print("OUT OF BAG SCORE")
print("=" * 80)

print(rf_classifier.oob_score_)

grid_results = pd.DataFrame({

    "Metric":[
        "Best CV F1",
        "Test Accuracy",
        "Test Precision",
        "Test Recall",
        "Test F1",
        "OOB Score"
    ],

    "Value":[
        grid_search.best_score_,
        accuracy,
        precision,
        recall,
        f1,
        rf_classifier.oob_score_
    ]

})

grid_results.to_csv(
    "outputs/gridsearch_results.csv",
    index=False
)

print(grid_results)

regression_df = pd.read_csv("titanic_cleaned.csv")

X_reg = regression_df[
    [
        "pclass",
        "sex",
        "age",
        "sibsp",
        "parch",
        "embarked"
    ]
]

y_reg = regression_df["fare"]

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg,
    y_reg,
    test_size=0.2,
    random_state=42
)

numeric_features_reg = [
    "age",
    "sibsp",
    "parch",
    "pclass"
]

categorical_features_reg = [
    "sex",
    "embarked"
]

numeric_transformer_reg = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "scaler",
            StandardScaler()
        )
    ]
)

categorical_transformer_reg = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(handle_unknown="ignore")
        )
    ]
)

preprocessor_reg = ColumnTransformer(

    transformers=[

        (
            "num",
            numeric_transformer_reg,
            numeric_features_reg
        ),

        (
            "cat",
            categorical_transformer_reg,
            categorical_features_reg
        )

    ]

)

regression_pipeline = Pipeline(
    steps=[

        (
            "preprocessor",
            preprocessor_reg
        ),

        (
            "regressor",
            LinearRegression()
        )

    ]
)

regression_pipeline.fit(
    X_train_reg,
    y_train_reg
)

y_pred_reg = regression_pipeline.predict(
    X_test_reg
)

mae = mean_absolute_error(
    y_test_reg,
    y_pred_reg
)

mse = mean_squared_error(
    y_test_reg,
    y_pred_reg
)

rmse = np.sqrt(
    mean_squared_error(
        y_test_reg,
        y_pred_reg
    )
)

r2 = r2_score(
    y_test_reg,
    y_pred_reg
)

print("=" * 80)
print("LINEAR REGRESSION RESULTS")
print("=" * 80)

print(f"MAE : {mae:.2f}")
print(f"MSE : {mse:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R²  : {r2:.4f}")

plt.figure(figsize=(7,6))

plt.scatter(
    y_test_reg,
    y_pred_reg,
    alpha=0.6
)

plt.plot(
    [
        y_test_reg.min(),
        y_test_reg.max()
    ],
    [
        y_test_reg.min(),
        y_test_reg.max()
    ],
    color="red",
    linestyle="--"
)

plt.xlabel("Actual Fare")
plt.ylabel("Predicted Fare")

plt.title("Actual vs Predicted Fare")

plt.tight_layout()

plt.savefig("plots/regression_actual_vs_predicted.png")

plt.show()

residuals = y_test_reg - y_pred_reg

plt.figure(figsize=(8,5))

plt.scatter(
    y_pred_reg,
    residuals,
    alpha=0.6
)

plt.axhline(
    y=0,
    color="red",
    linestyle="--"
)

plt.xlabel("Predicted Fare")

plt.ylabel("Residuals")

plt.title("Residual Plot")

plt.tight_layout()

plt.savefig(
    "plots/residual_plot.png"
)

plt.show()

regression_results = pd.DataFrame({

    "Metric":[
        "MAE",
        "MSE",
        "RMSE",
        "R2 Score"
    ],

    "Value":[
        mae,
        mse,
        rmse,
        r2
    ]

})

regression_results.to_csv(
    "outputs/regression_results.csv",
    index=False
)

print(regression_results)

best_pipeline = grid_search.best_estimator_

MODEL_PATH = "models/best_pipeline.joblib"

joblib.dump(
    best_pipeline,
    MODEL_PATH
)

print(f"Pipeline saved to {MODEL_PATH}")

loaded_pipeline = joblib.load(
    MODEL_PATH
)

print("Pipeline loaded successfully.")

original_predictions = best_pipeline.predict(
    X_test
)

loaded_predictions = loaded_pipeline.predict(
    X_test
)

import numpy as np

identical = np.array_equal(
    original_predictions,
    loaded_predictions
)

print("=" * 80)
print("MODEL PERSISTENCE CHECK")
print("=" * 80)

print("Predictions Match:", identical)

loaded_accuracy = accuracy_score(
    y_test,
    loaded_predictions
)

print(f"Accuracy of Loaded Model: {loaded_accuracy:.4f}")

new_passenger = pd.DataFrame({

    "pclass": [1],

    "sex": ["female"],

    "age": [28],

    "sibsp": [0],

    "parch": [0],

    "fare": [80.0],

    "embarked": ["S"]

})

prediction = loaded_pipeline.predict(
    new_passenger
)

probability = loaded_pipeline.predict_proba(
    new_passenger
)

print("=" * 80)
print("NEW PASSENGER PREDICTION")
print("=" * 80)

print(
    "Predicted Survival:",
    prediction[0]
)

print(
    "Probability:",
    probability[0]
)

prediction_df = pd.DataFrame({

    "Predicted Survival": prediction,

    "Probability of Not Surviving":
        probability[:,0],

    "Probability of Surviving":
        probability[:,1]

})

prediction_df.to_csv(
    "outputs/sample_prediction.csv",
    index=False
)

prediction_df