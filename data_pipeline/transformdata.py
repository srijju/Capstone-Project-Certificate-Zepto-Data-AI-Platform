import pandas as pd
import numpy as np
import re

GBP_TO_INR = 105.50

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def clean_price(price):
    """
    Converts:
        £51.77 -> 51.77

    Returns NaN if parsing fails.
    """
    try:
        return float(price.replace("£", "").strip())
    except Exception:
        return np.nan


def clean_rating(rating):
    """
    Converts:
        Three -> 3

    Returns NaN if parsing fails.
    """
    return RATING_MAP.get(rating, np.nan)


def clean_availability(text):
    """
    Converts:
        'In stock (19 available)' -> True
        'Out of stock' -> False
    """
    if isinstance(text, str):
        return "In stock" in text
    return False


def main():

    df = pd.read_csv("data/raw_books.csv")

    print("Rows before cleaning:", len(df))

    # -----------------------------
    # Clean price
    # -----------------------------
    df["price_gbp"] = df["price"].apply(clean_price)

    # -----------------------------
    # Clean rating
    # -----------------------------
    df["rating"] = df["star_rating"].apply(clean_rating)

    # -----------------------------
    # Clean availability
    # -----------------------------
    df["in_stock"] = df["availability"].apply(clean_availability)

    # -----------------------------
    # Handle missing numeric values
    # Median Imputation
    # -----------------------------
    df["price_gbp"] = df["price_gbp"].fillna(
        df["price_gbp"].median()
    )

    df["rating"] = df["rating"].fillna(
        int(df["rating"].median())
    )

    # -----------------------------
    # Convert GBP to INR
    # -----------------------------
    df["price_inr"] = (
        df["price_gbp"] * GBP_TO_INR
    ).round(2)

    # -----------------------------
    # Remove old columns
    # -----------------------------
    df.drop(
        columns=[
            "price",
            "star_rating",
            "availability"
        ],
        inplace=True
    )

    print("\nRows after cleaning:", len(df))

    print("\nData Types\n")
    print(df.dtypes)

    print("\nSample Data\n")
    print(df.head())

    df.to_csv(
        "data/cleaned_books.csv",
        index=False
    )

    print("\nCleaned data saved successfully!")


if __name__ == "__main__":
    main()