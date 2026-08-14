# Support Assistant – Zepto Data & AI Platform

## Overview

This module implements a Retrieval-Augmented Generation (RAG) support assistant for answering Zepto policy-related questions.

The assistant indexes Zepto policy documents into a vector database (ChromaDB), retrieves the most relevant document chunks using semantic search, and answers user queries through a LangGraph workflow exposed as a FastAPI application.

The project is designed to work completely offline using a deterministic mock mode (`MOCK_LLM=1` by default), while also providing an optional extension for integration with a real Large Language Model.

---

# Objectives

This module demonstrates:

- Document ingestion
- Text chunking
- Sentence-transformer embeddings
- ChromaDB vector storage
- Semantic retrieval
- LangGraph workflow orchestration
- Intent classification
- Retrieval-Augmented Generation (RAG)
- FastAPI REST API
- Docker deployment

---

# Project Structure

```text
support_assistant/

├── README.md
├── requirements.txt
├── Dockerfile
│
├── docs/
│   ├── doc_01.txt
│   ├── doc_02.txt
│   ├── ...
│   └── doc_08.txt
│
├── chroma_db/
│
└── app/
    ├── __init__.py
    ├── config.py
    ├── ingestion.py
    ├── retrieval.py
    ├── prompts.py
    ├── graph.py
    ├── schemas.py
    └── main.py
```

---

# Architecture

The Retrieval-Augmented Generation pipeline follows four stages.

```
Policy Documents
        │
        ▼
Ingestion
(app/ingestion.py)
        │
        ▼
Chunking & Embeddings
(app/ingestion.py)
        │
        ▼
ChromaDB Vector Store
(chroma_db/)
        │
        ▼
Semantic Retrieval
(app/retrieval.py)
        │
        ▼
LangGraph Workflow
(app/graph.py)
        │
 ┌──────┴─────────┐
 ▼                ▼
retrieve_and_answer
direct_answer
        │
        ▼
FastAPI
(app/main.py)
```

---

# RAG Pipeline

The Retrieval-Augmented Generation workflow consists of four stages.

## 1. Ingestion

Implemented in:

```
app/ingestion.py
```

Responsibilities:

- Read policy documents
- Split documents into chunks
- Generate embeddings
- Store chunks in ChromaDB

---

## 2. Embedding

The following embedding model is used:

```
all-MiniLM-L6-v2
```

Embeddings are generated locally using Sentence Transformers.

No external API key is required.

---

## 3. Retrieval

Implemented in:

```
app/retrieval.py
```

Responsibilities:

- Embed incoming user query
- Retrieve Top-3 most similar chunks
- Return:

  - retrieved documents
  - metadata
  - chunk IDs

Similarity search is performed using cosine similarity through ChromaDB.

---

## 4. Generation

Implemented in:

```
app/graph.py
```

The retrieved context is converted into a response.

The generation stage is the only stage affected by the `MOCK_LLM` configuration.

---

# MOCK_LLM Behaviour

The project supports two execution modes.

## MOCK_LLM = 1 (Default)

This is the required grading mode.

Characteristics:

- No network calls
- No external LLM
- Intent classification uses keyword matching
- Retrieval is real
- Response generation uses deterministic templates

Policy questions return

```
Based on the retrieved context:
...
```

General questions return

```
I can only answer questions about Zepto policies right now.
```

---

## MOCK_LLM = 0 (Optional Extension)

When enabled:

- Prompt template is used
- A real LLM can generate answers
- Pydantic validation is applied
- Invalid responses are retried up to two additional times

This mode is included as an optional extension and is not required for grading.

---

# Intent Classification

The LangGraph workflow classifies every incoming query as either:

```
policy_question
```

or

```
general_question
```

Keyword matching is performed using the following terms:

- delivery
- return
- refund
- membership
- tracking
- cancel
- gift card
- support hours

Queries containing one or more keywords are routed to:

```
retrieve_and_answer
```

All other queries are routed to:

```
direct_answer
```

---

# Prompt Template

The prompt template used for the optional LLM implementation contains:

- Role
- Context
- Task
- Output Format
- Length Constraint
- Negative Constraint
- Few-shot Example

The prompt is implemented in

```
app/prompts.py
```

---

# API

The assistant is exposed through FastAPI.

## Endpoint

```
POST /ask
```

Request

```json
{
  "query": "How do I track my delivery?"
}
```

Response

```json
{
  "answer": "...",
  "sources": [
    "chunk_001",
    "chunk_002",
    "chunk_003"
  ],
  "confidence": 1.0
}
```

The response is validated using a Pydantic model.

---

# Installation

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

macOS/Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Running the Project

## Step 1 – Build the Vector Database

```bash
python -m app.ingestion
```

This loads all policy documents into ChromaDB.

---

## Step 2 – Test Retrieval

```bash
python -m app.retrieval
```

Displays the retrieved chunks and chunk IDs.

---

## Step 3 – Test LangGraph

```bash
python -m app.graph
```

Demonstrates both routing paths:

- policy_question
- general_question

---

## Step 4 – Run FastAPI

```bash
uvicorn app.main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

to access the Swagger interface.

---

# Example API Calls

## Example 1 – Policy Question

Request

```json
{
  "query": "How do I track my delivery?"
}
```

Example Response

```json
{
  "answer": "Based on the retrieved context: Track your order using the tracking page provided after dispatch...",
  "sources": [
    "doc_04_chunk_0",
    "doc_04_chunk_1",
    "doc_02_chunk_0"
  ],
  "confidence": 1.0
}
```

---

## Example 2 – General Question

Request

```json
{
  "query": "Who won the IPL?"
}
```

Example Response

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

---

# Docker

Build the image.

```bash
docker build -t zepto-support-assistant .
```

Run the container.

```bash
docker run -p 8000:8000 zepto-support-assistant
```

Open

```
http://localhost:8000/docs
```

---

# Design Decisions

## ChromaDB

Chosen because it is lightweight, persistent, and easy to integrate with Sentence Transformers.

---

## Sentence Transformers

Used to generate embeddings locally without requiring an external API.

---

## LangGraph

Provides explicit workflow orchestration with conditional routing between retrieval-based and direct responses.

---

## FastAPI

Provides automatic request validation, OpenAPI documentation, and a lightweight REST interface.

---

## Pydantic

Ensures every API response conforms to the required schema.

---

## Deterministic Mock Mode

The default grading mode avoids external dependencies while still exercising the complete RAG pipeline.

---

# Assignment Checklist

| Requirement | Status |
|-------------|--------|
| 8 documents indexed | ✅ |
| ChromaDB vector store | ✅ |
| Prompt template | ✅ |
| Intent classification | ✅ |
| LangGraph workflow | ✅ |
| Conditional routing | ✅ |
| Semantic retrieval | ✅ |
| Mock generation | ✅ |
| Pydantic response validation | ✅ |
| FastAPI endpoint | ✅ |
| Docker support | ✅ |
| Architecture documentation | ✅ |

---

# Future Improvements

Possible extensions include:

- Integration with OpenAI or other hosted LLMs
- Streaming responses
- Conversation memory
- Authentication
- Hybrid search (keyword + vector)
- Reranking retrieved documents
- Multi-turn conversational support