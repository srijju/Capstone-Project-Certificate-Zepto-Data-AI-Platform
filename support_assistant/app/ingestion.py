"""
Document ingestion for the Zepto Support Assistant.

Responsibilities:
1. Load policy documents.
2. Split into chunks.
3. Generate embeddings.
4. Store chunks in ChromaDB.
"""

from pathlib import Path
import logging

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import (
    DOCS_DIR,
    CHROMA_DB_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# Chroma Client
# --------------------------------------------------

client = chromadb.PersistentClient(
    path=str(CHROMA_DB_DIR)
)

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)

# --------------------------------------------------
# Text Splitter
# --------------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)


# --------------------------------------------------
# Load Documents
# --------------------------------------------------

def load_documents():
    """
    Load all text files from the docs directory.
    """

    documents = []

    for file in sorted(DOCS_DIR.glob("*.txt")):

        try:

            text = file.read_text(
                encoding="utf-8"
            )

            documents.append({

                "filename": file.name,

                "text": text

            })

        except Exception as ex:

            logger.error(
                f"Could not read {file.name}: {ex}"
            )

    logger.info(
        f"Loaded {len(documents)} documents."
    )

    return documents


# --------------------------------------------------
# Chunk Documents
# --------------------------------------------------

def chunk_documents(documents):
    """
    Split each document into chunks.
    """

    chunks = []

    for document in documents:

        split_chunks = text_splitter.split_text(
            document["text"]
        )

        for index, chunk in enumerate(split_chunks):

            chunks.append({

                "id":
                    f"{document['filename']}_{index}",

                "document":
                    chunk,

                "metadata": {

                    "source":
                        document["filename"]

                }

            })

    logger.info(
        f"Created {len(chunks)} chunks."
    )

    return chunks


# --------------------------------------------------
# Store Chunks
# --------------------------------------------------

def index_documents(chunks):
    """
    Store chunks inside ChromaDB.
    Safe to execute multiple times.
    """

    existing = collection.count()

    if existing > 0:

        logger.info(
            f"Collection already contains {existing} chunks."
        )

        return

    collection.add(

        ids=[
            chunk["id"]
            for chunk in chunks
        ],

        documents=[
            chunk["document"]
            for chunk in chunks
        ],

        metadatas=[
            chunk["metadata"]
            for chunk in chunks
        ]

    )

    logger.info(
        f"Indexed {len(chunks)} chunks."
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    documents = load_documents()

    chunks = chunk_documents(
        documents
    )

    index_documents(
        chunks
    )


if __name__ == "__main__":

    main()