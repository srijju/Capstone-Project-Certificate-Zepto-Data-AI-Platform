
# Zepto Data & AI Platform

## Overview

This repository contains the complete solution for the **Zepto Data & AI Platform Capstone Project**. The project demonstrates an end-to-end AI/ML engineering workflow consisting of three independent but related modules:

1. **Data Pipeline** – Web scraping, data cleaning, transformation, and relational storage.
2. **Analytics** – Exploratory Data Analysis (EDA), machine learning, evaluation, and model persistence.
3. **Support Assistant** – Retrieval-Augmented Generation (RAG) application using ChromaDB, LangGraph, FastAPI, and Docker.

Each module is self-contained, but together they represent a complete data engineering, analytics, and AI application.

---

# Repository Structure

```text
Capstone-Project-Certificate-Zepto-Data-AI-Platform/
│
├── README.md
├── data_pipeline/
├── analytics/
├── support_assistant/
└── .gitignore
```

Each module contains its own `README.md` and `requirements.txt`.

---

# Technologies Used

- Python 3.11+
- Requests
- BeautifulSoup
- SQLite
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- imbalanced-learn
- Joblib
- Sentence Transformers
- ChromaDB
- LangGraph
- FastAPI
- Pydantic
- Docker

---

# Project Setup

This project uses **separate `requirements.txt` files** for each module.

Clone the repository:

```bash
git clone <repository-url>
cd Capstone-Project-Certificate-Zepto-Data-AI-Platform
```

---

# Module 1 – Data Pipeline

Folder:

```text
data_pipeline/
```

## Objective

Build an ETL pipeline that:

- Scrapes book information from books.toscrape.com
- Cleans and transforms data
- Converts GBP to INR using the fixed exchange rate (1 GBP = 105.50 INR)
- Stores data in a normalized SQLite database
- Demonstrates SQL and pandas queries

## Setup

```bash
cd data_pipeline
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python scrape_books.py
python queries.py
```

## Outputs

- books.db
- books.csv
- SQL query outputs
- pandas query outputs

For detailed documentation, see `data_pipeline/README.md`.

---

# Module 2 – Analytics

Folder:

```text
analytics/
```

## Objective

Perform an end-to-end analytics workflow using the Titanic dataset.

The module includes:

- Data cleaning
- Missing-value handling
- Outlier detection
- Exploratory Data Analysis
- Feature engineering
- Classification
- Regression
- Model evaluation
- Model persistence

## Setup

```bash
cd analytics
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python eda.py
python modeling.py
```

## Outputs

- titanic.csv
- titanic_cleaned.csv
- plots/
- outputs/
- models/best_pipeline.joblib

For detailed methodology, interpretations, and model comparison, see `analytics/README.md`.

---

# Module 3 – Support Assistant

Folder:

```text
support_assistant/
```

## Objective

Develop a Retrieval-Augmented Generation (RAG) support assistant capable of answering Zepto policy questions.

The workflow includes:

- Document ingestion
- Chunking
- Embedding
- ChromaDB indexing
- Semantic retrieval
- LangGraph workflow
- FastAPI API
- Docker deployment

## Setup

```bash
cd support_assistant
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Build the vector database:

```bash
python -m app.ingestion
```

Test retrieval:

```bash
python -m app.retrieval
```

Run the LangGraph workflow:

```bash
python -m app.graph
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Docker:

```bash
docker build -t zepto-support-assistant .
docker run -p 8000:8000 zepto-support-assistant
```

For implementation details, architecture, and API examples, see `support_assistant/README.md`.

---

# Design Decisions

## Data Pipeline

- BeautifulSoup + Requests for web scraping
- SQLite as a lightweight relational database
- Normalized Books/Categories schema
- Fixed currency conversion as required by the assignment

## Analytics

- Offline Titanic dataset for reproducibility
- Stratified train/test split
- Pipeline-based preprocessing
- Comparison of multiple ML models
- Complete pipeline serialization using Joblib

## Support Assistant

- ChromaDB vector database
- Sentence Transformer embeddings
- LangGraph workflow
- FastAPI REST API
- Deterministic mock mode (`MOCK_LLM=1`)
- Docker support

---

# Running the Entire Project

1. Run the Data Pipeline module to build the relational dataset.
2. Run the Analytics module to perform EDA and train the machine learning models.
3. Run the Support Assistant module to build the vector database and launch the API.

Each module is independent and may be executed separately.

---

# Assignment Deliverables

- One public GitHub repository
- Root README
- `data_pipeline/`
- `analytics/`
- `support_assistant/`
- Individual `requirements.txt` for each module
- Individual module README files
- SQLite database (or regeneration script)
- Offline Titanic dataset
- Saved model pipeline
- ChromaDB database (or regeneration through ingestion)
- Dockerfile
- Git history with feature branch and merge

---

# Future Improvements

- PostgreSQL support for the data pipeline
- Experiment tracking using MLflow
- Advanced explainability using SHAP
- Hybrid retrieval (keyword + vector search)
- Real LLM integration
- CI/CD automation
- Cloud deployment

---

# Author

Developed as part of the **Zepto Data & AI Platform Capstone Project**.
