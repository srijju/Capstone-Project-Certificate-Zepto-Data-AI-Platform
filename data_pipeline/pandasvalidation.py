import os
import sqlite3
import pandas as pd

DATABASE_PATH = "data/books.db"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DATABASE_PATH)

# ==========================================================
# Query 1 - Read using pd.read_sql()
# ==========================================================

query1 = """
SELECT
    title,
    price_gbp,
    rating
FROM books
WHERE rating >= 4;
"""

df_high_rating = pd.read_sql(query1, conn)

print("\nBooks with Rating >= 4")
print(df_high_rating.head())

# ==========================================================
# Query 2 - Read using pd.read_sql()
# ==========================================================

query2 = """
SELECT
    title,
    price_inr
FROM books
ORDER BY price_inr DESC;
"""

df_expensive = pd.read_sql(query2, conn)

print("\nMost Expensive Books")
print(df_expensive.head())

# ==========================================================
# JOIN Query using SQL
# ==========================================================

join_query = """
SELECT
    b.title,
    c.category_name,
    b.rating,
    b.price_inr,
    b.in_stock
FROM books b
INNER JOIN categories c
ON b.category_id = c.category_id
ORDER BY
    c.category_name,
    b.rating DESC,
    b.price_inr DESC;
"""

sql_join_df = pd.read_sql(join_query, conn)

# ==========================================================
# Read complete tables
# ==========================================================

books_df = pd.read_sql(
    "SELECT * FROM books;",
    conn
)

categories_df = pd.read_sql(
    "SELECT * FROM categories;",
    conn
)

conn.close()

# ==========================================================
# Reproduce JOIN using Pandas
# ==========================================================

merge_df = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)

merge_df = merge_df[
    [
        "title",
        "category_name",
        "rating",
        "price_inr",
        "in_stock"
    ]
]

merge_df = merge_df.sort_values(
    by=[
        "category_name",
        "rating",
        "price_inr"
    ],
    ascending=[True, False, False]
).reset_index(drop=True)

sql_join_df = sql_join_df.reset_index(drop=True)

# ==========================================================
# Compare Results
# ==========================================================

results_match = sql_join_df.equals(merge_df)

print("\nSQL JOIN and Pandas Merge produce identical results:")
print(results_match)

# ==========================================================
# Save Outputs
# ==========================================================

sql_join_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "sql_join_result.csv"
    ),
    index=False
)

merge_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "pandas_merge_result.csv"
    ),
    index=False
)

with open(
    os.path.join(
        OUTPUT_DIR,
        "validation_report.txt"
    ),
    "w",
    encoding="utf-8"
) as report:

    report.write("PANDAS VALIDATION REPORT\n")
    report.write("=" * 80 + "\n\n")

    report.write("Query 1 (Rating >= 4)\n")
    report.write(df_high_rating.to_string(index=False))
    report.write("\n\n")

    report.write("Query 2 (Highest Price in INR)\n")
    report.write(df_expensive.to_string(index=False))
    report.write("\n\n")

    report.write("SQL JOIN Result\n")
    report.write(sql_join_df.to_string(index=False))
    report.write("\n\n")

    report.write("Pandas Merge Result\n")
    report.write(merge_df.to_string(index=False))
    report.write("\n\n")

    report.write(f"Equivalent Output: {results_match}\n")

print("\nValidation completed successfully.")
print("Validation report saved in outputs/validation_report.txt")
print("SQL JOIN output saved as outputs/sql_join_result.csv")
print("Pandas Merge output saved as outputs/pandas_merge_result.csv")