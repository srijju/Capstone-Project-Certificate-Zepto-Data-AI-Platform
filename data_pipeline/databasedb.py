import sqlite3
import pandas as pd

DATABASE_PATH = "data/books.db"
CSV_PATH = "data/cleaned_books.csv"


def create_tables(conn):
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Drop existing tables (optional, for reruns)
    cursor.execute("DROP TABLE IF EXISTS books")
    cursor.execute("DROP TABLE IF EXISTS categories")

    # Categories table
    cursor.execute("""
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE NOT NULL
        )
    """)

    # Books table
    cursor.execute("""
        CREATE TABLE books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price_gbp REAL,
            price_inr REAL,
            rating INTEGER,
            in_stock INTEGER,
            category_id INTEGER,
            FOREIGN KEY(category_id)
                REFERENCES categories(category_id)
        )
    """)

    conn.commit()


def insert_categories(conn, df):
    cursor = conn.cursor()

    categories = sorted(df["category"].unique())

    for category in categories:
        cursor.execute(
            """
            INSERT INTO categories(category_name)
            VALUES(?)
            """,
            (category,)
        )

    conn.commit()


def get_category_mapping(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category_id,
               category_name
        FROM categories
    """)

    rows = cursor.fetchall()

    return {
        name: category_id
        for category_id, name in rows
    }


def insert_books(conn, df):
    cursor = conn.cursor()

    category_map = get_category_mapping(conn)

    for _, row in df.iterrows():

        cursor.execute("""
            INSERT INTO books(
                title,
                price_gbp,
                price_inr,
                rating,
                in_stock,
                category_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row["title"],
            float(row["price_gbp"]),
            float(row["price_inr"]),
            int(row["rating"]),
            int(row["in_stock"]),
            category_map[row["category"]]
        ))

    conn.commit()


def main():

    df = pd.read_csv(CSV_PATH)

    conn = sqlite3.connect(DATABASE_PATH)

    create_tables(conn)

    insert_categories(conn, df)

    insert_books(conn, df)

    print("Database created successfully!")

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    print("Books:", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM categories")
    print("Categories:", cursor.fetchone()[0])

    conn.close()


if __name__ == "__main__":
    main()