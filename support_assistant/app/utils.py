from pathlib import Path
from app.config import DOCS_DIR

DOCS_PATH = DOCS_DIR


def get_document_paths():

    files = sorted(
        DOCS_PATH.glob("*.txt")
    )

    return files


if __name__ == "__main__":

    docs = get_document_paths()

    print(f"Documents Found: {len(docs)}")

    for doc in docs:
        print(doc.name)