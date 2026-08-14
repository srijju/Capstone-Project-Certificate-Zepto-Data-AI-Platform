import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

import warnings
warnings.filterwarnings("ignore")

# Load Titanic dataset
df = sns.load_dataset("titanic")

# Save offline copy immediately
df.to_csv("titanic.csv", index=False)

print("Dataset saved as titanic.csv")

print("=" * 60)
print("Dataset Shape")
print("=" * 60)

print(df.shape)

print("=" * 60)
print("Dataset Information")
print("=" * 60)

df.info()

print("=" * 60)
print("Statistical Summary")
print("=" * 60)

print(df.describe(include="all"))

print("=" * 60)
print("First Five Records")
print("=" * 60)

print(df.head())

print("=" * 60)
print("Missing Values")
print("=" * 60)

print(df.isnull().sum())

missing_percentage = (
    df.isnull()
      .mean()
      .mul(100)
      .round(2)
)

missing_percentage = (
    missing_percentage[
        missing_percentage > 0
    ]
    .sort_values(ascending=False)
)

print("=" * 60)
print("Missing Value Percentage")
print("=" * 60)

print(missing_percentage)

missing_percentage.to_csv(
    "outputs/missing_percentage.csv",
    header=["Missing Percentage"]
)

# ==========================================================
# Missing Value Analysis
# ==========================================================

print("=" * 80)
print("MISSING VALUE ANALYSIS")
print("=" * 80)

missing_percentage = (
    df.isnull()
      .mean()
      .mul(100)
      .round(2)
)

missing_columns = missing_percentage[missing_percentage > 0]

print(missing_columns)

print("\nCleaning Strategy\n")

for column, percentage in missing_columns.items():

    if percentage < 5:
        print(f"{column}: {percentage:.2f}% missing → Drop rows")

    elif percentage <= 30:
        print(f"{column}: {percentage:.2f}% missing → Imputation")

    else:
        print(f"{column}: {percentage:.2f}% missing → Drop column")


 # Make a copy so original dataset is preserved
clean_df = df.copy()

low_missing_columns = [
    column
    for column, percentage in missing_columns.items()
    if percentage < 5
]

print("Columns with <5% missing:")
print(low_missing_columns)

clean_df = clean_df.dropna(
    subset=low_missing_columns
)

moderate_missing_columns = [
    column
    for column, percentage in missing_columns.items()
    if 5 <= percentage <= 30
]

print("\nColumns requiring imputation:")
print(moderate_missing_columns)

for column in moderate_missing_columns:

    if pd.api.types.is_numeric_dtype(clean_df[column]):

        median_value = clean_df[column].median()

        clean_df[column] = clean_df[column].fillna(
            median_value
        )

        print(f"{column} imputed using median ({median_value:.2f})")

    else:

        mode_value = clean_df[column].mode()[0]

        clean_df[column] = clean_df[column].fillna(
            mode_value
        )

        print(f"{column} imputed using mode ({mode_value})")


high_missing_columns = [
    column
    for column, percentage in missing_columns.items()
    if percentage > 30
]

print("\nColumns dropped:")

for column in high_missing_columns:

    clean_df.drop(columns=column, inplace=True)

    print(column)

print("=" * 80)
print("Missing Values After Cleaning")
print("=" * 80)

print(clean_df.isnull().sum())

clean_df.to_csv(
    "titanic_cleaned.csv",
    index=False
)

print("Clean dataset saved successfully.")



plt.figure(figsize=(8,5))

sns.histplot(
    clean_df["age"],
    bins=30,
    kde=True,
    color="skyblue"
)

plt.title("Distribution of Passenger Age")
plt.xlabel("Age")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig("plots/age_histogram.png")

plt.show()

plt.figure(figsize=(8,2))

sns.boxplot(
    x=clean_df["age"],
    color="lightgreen"
)

plt.title("Age Box Plot")

plt.tight_layout()

plt.savefig("plots/age_boxplot.png")

plt.show()

plt.figure(figsize=(8,5))

sns.histplot(
    clean_df["fare"],
    bins=30,
    kde=True,
    color="orange"
)

plt.title("Distribution of Fare")
plt.xlabel("Fare")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig("plots/fare_histogram.png")

plt.show()

plt.figure(figsize=(8,2))

sns.boxplot(
    x=clean_df["fare"],
    color="tomato"
)

plt.title("Fare Box Plot")

plt.tight_layout()

plt.savefig("plots/fare_boxplot.png")

plt.show()

def count_outliers_iqr(series):

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = series[
        (series < lower) |
        (series > upper)
    ]

    return (
        len(outliers),
        lower,
        upper
    )

age_outliers, age_lower, age_upper = count_outliers_iqr(
    clean_df["age"]
)

print("Age Outliers")
print("----------------------")
print(f"Lower Limit : {age_lower:.2f}")
print(f"Upper Limit : {age_upper:.2f}")
print(f"Outliers    : {age_outliers}")

fare_outliers, fare_lower, fare_upper = count_outliers_iqr(
    clean_df["fare"]
)

print("\nFare Outliers")
print("----------------------")
print(f"Lower Limit : {fare_lower:.2f}")
print(f"Upper Limit : {fare_upper:.2f}")
print(f"Outliers    : {fare_outliers}")

fare_mean = clean_df["fare"].mean()
fare_median = clean_df["fare"].median()
fare_mode = clean_df["fare"].mode()[0]

print("=" * 60)

print(f"Mean   : {fare_mean:.2f}")
print(f"Median : {fare_median:.2f}")
print(f"Mode   : {fare_mode:.2f}")

print("=" * 60)

if fare_mean > fare_median > fare_mode:
    skewness = "Right-Skewed"

elif fare_mean < fare_median < fare_mode:
    skewness = "Left-Skewed"

else:
    skewness = "Approximately Symmetric"

print(f"Fare Distribution : {skewness}")

summary = {
    "Column": ["Age", "Fare"],
    "Outliers": [age_outliers, fare_outliers]
}

summary_df = pd.DataFrame(summary)

print(summary_df)

print("=" * 80)
print("SURVIVAL RATE BY SEX")
print("=" * 80)

survival_by_sex = (
    clean_df
    .groupby("sex")["survived"]
    .mean()
    .mul(100)
    .round(2)
)

print(survival_by_sex)

print("=" * 80)
print("SURVIVAL RATE BY PASSENGER CLASS")
print("=" * 80)

survival_by_class = (
    clean_df
    .groupby("pclass")["survived"]
    .mean()
    .mul(100)
    .round(2)
)

print(survival_by_class)

print("=" * 80)
print("SURVIVAL RATE BY SEX AND PASSENGER CLASS")
print("=" * 80)

survival_by_both = (
    clean_df
    .groupby(["sex", "pclass"])["survived"]
    .mean()
    .mul(100)
    .round(2)
)

print(survival_by_both)

female_first = clean_df[
    (clean_df["sex"] == "female") &
    (clean_df["pclass"] == 1)
]

rate = female_first["survived"].mean() * 100

print(f"Female First Class Survival Rate: {rate:.2f}%")

male_third = clean_df[
    (clean_df["sex"] == "male") &
    (clean_df["pclass"] == 3)
]

rate = male_third["survived"].mean() * 100

print(f"Male Third Class Survival Rate: {rate:.2f}%")

first_or_second = clean_df[
    (clean_df["pclass"] == 1) |
    (clean_df["pclass"] == 2)
]

print(
    "Passengers in First or Second Class:",
    len(first_or_second)
)

correlation_columns = [
    "survived",
    "pclass",
    "age",
    "sibsp",
    "parch",
    "fare"
]

correlation_matrix = (
    clean_df[
        correlation_columns
    ]
    .corr()
)

print(correlation_matrix)



plt.figure(figsize=(8,6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig("plots/correlation_heatmap.png")

plt.show()

corr = correlation_matrix.abs()

# Convert matrix to long format
corr_pairs = (
    corr.stack()
        .reset_index()
)

corr_pairs.columns = [
    "Feature1",
    "Feature2",
    "Correlation"
]

# Remove self-correlations
corr_pairs = corr_pairs[
    corr_pairs["Feature1"] != corr_pairs["Feature2"]
]

# Remove duplicate pairs
corr_pairs["pair"] = corr_pairs.apply(
    lambda x: tuple(sorted([x["Feature1"], x["Feature2"]])),
    axis=1
)

corr_pairs = corr_pairs.drop_duplicates("pair")

# Top 2 strongest correlations
top_pairs = corr_pairs.sort_values(
    by="Correlation",
    ascending=False
).head(2)

print("\nTop Two Strongest Correlations")
print(top_pairs[["Feature1", "Feature2", "Correlation"]])

plt.figure(figsize=(7,5))

sns.barplot(
    data=clean_df,
    x="sex",
    y="survived",
    estimator="mean",
    palette="Set2"
)

plt.title("Survival Rate by Gender")
plt.ylabel("Survival Rate")

plt.tight_layout()

plt.savefig("plots/survival_by_gender.png")

plt.show()

plt.figure(figsize=(7,5))

sns.barplot(
    data=clean_df,
    x="pclass",
    y="survived",
    estimator="mean",
    palette="Blues"
)

plt.title("Survival Rate by Passenger Class")
plt.xlabel("Passenger Class")
plt.ylabel("Survival Rate")

plt.tight_layout()

plt.savefig("plots/survival_by_class.png")

plt.show()

plt.figure(figsize=(8,5))

sns.boxplot(
    data=clean_df,
    x="survived",
    y="age",
    palette="Pastel1"
)

plt.title("Age Distribution by Survival")
plt.xlabel("Survived")
plt.ylabel("Age")

plt.tight_layout()

plt.savefig("plots/age_vs_survival.png")

plt.show()

plt.figure(figsize=(8,5))

sns.boxplot(
    data=clean_df,
    x="survived",
    y="fare",
    palette="Set3"
)

plt.title("Fare Distribution by Survival")
plt.xlabel("Survived")
plt.ylabel("Fare")

plt.tight_layout()

plt.savefig("plots/fare_vs_survival.png")

plt.show()

sns.pairplot(
    clean_df[
        [
            "survived",
            "age",
            "fare",
            "pclass"
        ]
    ],
    hue="survived"
)

plt.savefig("plots/pairplot.png")

plt.show()

print("=" * 80)
print("BEFORE STANDARDIZATION")
print("=" * 80)

before_stats = clean_df[["age", "fare"]].agg(
    ["mean", "std"]
)

print(before_stats)

scaler = StandardScaler()

standardized_df = clean_df.copy()

standardized_df[["age", "fare"]] = scaler.fit_transform(
    clean_df[["age", "fare"]]
)

print("=" * 80)
print("AFTER STANDARDIZATION")
print("=" * 80)

after_stats = standardized_df[
    ["age", "fare"]
].agg(
    ["mean", "std"]
)

print(after_stats)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.histplot(
    clean_df["age"],
    bins=30,
    kde=True,
    ax=axes[0],
    color="skyblue"
)

axes[0].set_title("Age Before Standardization")

sns.histplot(
    standardized_df["age"],
    bins=30,
    kde=True,
    ax=axes[1],
    color="orange"
)

axes[1].set_title("Age After Standardization")

plt.tight_layout()

plt.savefig("plots/age_standardization.png")

plt.show()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.histplot(
    clean_df["fare"],
    bins=30,
    kde=True,
    ax=axes[0],
    color="green"
)

axes[0].set_title("Fare Before Standardization")

sns.histplot(
    standardized_df["fare"],
    bins=30,
    kde=True,
    ax=axes[1],
    color="red"
)

axes[1].set_title("Fare After Standardization")

plt.tight_layout()

plt.savefig("plots/fare_standardization.png")

plt.show()

print("=" * 80)
print("STANDARDIZATION VERIFICATION")
print("=" * 80)

verification = pd.DataFrame({

    "Mean": standardized_df[
        ["age", "fare"]
    ].mean(),

    "Standard Deviation": standardized_df[
        ["age", "fare"]
    ].std(ddof=0)

})

print(verification)

clean_df.to_csv(
    "titanic_cleaned.csv",
    index=False
)

print("Cleaned dataset saved successfully.")