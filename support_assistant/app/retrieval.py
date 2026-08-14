"""
Retrieval module for the Zepto Support Assistant.

Responsibilities
----------------
1. Connect to ChromaDB.
2. Retrieve the top-k most relevant chunks.
3. Return:
   - retrieved documents
   - metadata
   - chunk IDs
"""

import logging

import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction,
)

from app.config import (
    CHROMA_DB_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    TOP_K,
)

# ======================================================
# Logging
# ======================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# ======================================================
# ChromaDB
# ======================================================

client = chromadb.PersistentClient(
    path=str(CHROMA_DB_DIR)
)

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)

# Create the collection if it doesn't already exist
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function,
)

# ======================================================
# Retrieval
# ======================================================

def retrieve_context(
    question: str,
    top_k: int = TOP_K,
):
    """
    Retrieve the most relevant chunks from ChromaDB.

    Parameters
    ----------
    question : str
        User query.

    top_k : int
        Number of chunks to retrieve.

    Returns
    -------
    tuple
        (
            documents,
            metadata,
            chunk_ids
        )
    """

    try:

        results = collection.query(

            query_texts=[question],

            n_results=top_k,

        )

        # No matching documents
        if (
            not results.get("documents")
            or not results["documents"]
            or not results["documents"][0]
        ):

            logger.warning(
                "No matching documents found."
            )

            return [], [], []

        documents = results["documents"][0]

        metadata = results["metadatas"][0]

        chunk_ids = results["ids"][0]

        logger.info(
            "Retrieved %d chunks.",
            len(documents),
        )

        return (

            documents,

            metadata,

            chunk_ids,

        )

    except Exception as ex:

        logger.exception(
            "Retrieval failed: %s",
            ex,
        )

        return (

            [],

            [],

            [],

        )

# ======================================================
# Local Test
# ======================================================

def main():

    question = "How do I track my delivery?"

    documents, metadata, chunk_ids = retrieve_context(
        question
    )

    print("\nQuestion")
    print("=" * 80)
    print(question)

    if not documents:

        print("\nNo matching documents found.")
        return

    print("\nRetrieved Chunks")
    print("=" * 80)

    for i in range(len(documents)):

        print(f"\nResult {i + 1}")

        print("-" * 80)

        print("Chunk ID :", chunk_ids[i])

        print("Source   :", metadata[i]["source"])

        print()

        print(documents[i][:300])

        print()

if __name__ == "__main__":
    main()