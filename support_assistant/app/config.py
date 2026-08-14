"""
Application configuration.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ---------------------------------------------------
# Base Paths
# ---------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

APP_DIR = BASE_DIR / "app"

DOCS_DIR = BASE_DIR / "docs"

CHROMA_DB_DIR = BASE_DIR / "chroma_db"

MODELS_DIR = BASE_DIR / "models"

# ---------------------------------------------------
# Chroma Configuration
# ---------------------------------------------------

COLLECTION_NAME = "zepto_policies"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ---------------------------------------------------
# Environment
# ---------------------------------------------------

MOCK_LLM = os.getenv("MOCK_LLM", "1") == "1"

TOP_K = 3

CHUNK_SIZE = 500

CHUNK_OVERLAP = 100