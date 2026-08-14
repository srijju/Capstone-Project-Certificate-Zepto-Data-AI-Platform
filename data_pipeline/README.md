# Data Pipeline – Zepto Data & AI Platform

## Overview

This folder contains a complete data engineering workflow for scraping, cleaning, validating, and storing book catalog data from `books.toscrape.com`.

The pipeline demonstrates a realistic ETL process:

- scrape raw records from a public website
- clean and normalize the extracted data
- convert values to a consistent schema
- store the dataset in SQLite
- run SQL queries and compare them against pandas logic
- save outputs for validation and reporting

This is a sample project that mirrors how raw product/catalog data can be prepared for analytics and downstream applications.

---

## Objectives

The pipeline performs the following tasks:

- scrape book information from `books.toscrape.com`
- collect records across multiple categories
- clean prices, ratings, and stock values
- convert GBP prices to INR
- save the cleaned data to CSV
- create a normalized SQLite database
- run SQL queries such as `SELECT`, `ORDER BY`, `LIMIT`, `DISTINCT`, `BETWEEN`, and `JOIN`
- validate SQL results against pandas merge logic

---

## Project Structure

```text
data_pipeline/
├── README.md
├── requirements.txt
├── scrapedata.py
├── transformdata.py
├── databasedb.py
├── queriesdata.py
├── pandasvalidation.py
├── data/
│   ├── raw_books.csv
│   ├── cleaned_books.csv
│   └── books.db
├── outputs/
│   ├── Query_1_SELECT_WHERE.csv
│   ├── Query_2_ORDER_BY.csv
│   ├── Query_3_LIMIT.csv
│   ├── Query_4_DISTINCT.csv
│   ├── Query_5_BETWEEN.csv
│   ├── Query_6_JOIN.csv
│   ├── sql_join_result.csv
│   ├── pandas_merge_result.csv
│   ├── sql_query_results.txt
│   └── validation_report.txt
└── .DS_Store
```

---

## Setup

Create and activate a virtual environment:

```bash
cd data_pipeline
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Current requirements:

```text
requests>=2.32.0
beautifulsoup4>=4.12.3
pandas>=2.2.2
numpy>=1.26.4
lxml>=5.2.2
```

---

## Run the Pipeline

Run the scripts in this order:

```bash
python scrapedata.py
python transformdata.py
python databasedb.py
python queriesdata.py
python pandasvalidation.py
```

### What each script does

1. `scrapedata.py`
   - fetches category links from the website
   - scrapes book records
   - saves raw output to `data/raw_books.csv`

2. `transformdata.py`
   - cleans price, rating, and availability values
   - handles missing values with median imputation
   - converts GBP to INR using a fixed exchange rate
   - saves cleaned data to `data/cleaned_books.csv`

3. `databasedb.py`
   - creates SQLite tables for categories and books
   - loads cleaned data into `data/books.db`

4. `queriesdata.py`
   - runs SQL queries and exports results to `outputs/`

5. `pandasvalidation.py`
   - checks whether the SQL join result matches a pandas merge result
   - saves a validation report in `outputs/validation_report.txt`

---

## Data Fields

### Raw scraped fields

- `title`
- `price`
- `star_rating`
- `availability`
- `category`

### Cleaned fields

- `title`
- `category`
- `price_gbp`
- `price_inr`
- `rating`
- `in_stock`

---

## Data Cleaning and Transformations

The pipeline applies the following cleaning rules:

- price strings like `£51.77` are converted to numeric values
- rating labels like `Three`, `Four`, `Five` are mapped to `3`, `4`, `5`
- availability strings are converted to a boolean-style stock flag
- missing numeric values are filled using median imputation
- GBP values are converted to INR using:

```text
1 GBP = 105.50 INR
```

The final price is calculated as:

```text
price_inr = price_gbp × 105.50
```

---

## Database Design

The SQLite database is normalized into two tables.

### `categories`

- `category_id` (PRIMARY KEY)
- `category_name`

### `books`

- `book_id` (PRIMARY KEY)
- `title`
- `price_gbp`
- `price_inr`
- `rating`
- `in_stock`
- `category_id` (FOREIGN KEY)

---

## Output Files

### Data files

- `data/raw_books.csv` — raw scraped records
- `data/cleaned_books.csv` — cleaned transformed dataset
- `data/books.db` — SQLite database

### Query outputs

- `outputs/Query_1_SELECT_WHERE.csv`
- `outputs/Query_2_ORDER_BY.csv`
- `outputs/Query_3_LIMIT.csv`
- `outputs/Query_4_DISTINCT.csv`
- `outputs/Query_5_BETWEEN.csv`
- `outputs/Query_6_JOIN.csv`
- `outputs/sql_query_results.txt`
- `outputs/sql_join_result.csv`
- `outputs/pandas_merge_result.csv`
- `outputs/validation_report.txt`

---

## Notes

- The source site used here is `books.toscrape.com`, which is a common scraping practice dataset.
- This project is intended as a learning/demo pipeline and is intentionally simple.
- It can be extended to real product catalogs, cloud storage, automated ETL jobs, and analytics pipelines.

---

## Example Use Case

This pipeline is useful for:

- e-commerce catalog ingestion
- product dataset preparation
- SQL and pandas comparison exercises
- data quality validation
- analytics-ready data generation