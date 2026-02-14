# RAG FastAPI + pgvector

## Project Structure

app/
 ├── api/
 │    └── routes.py
 ├── core/
 │    └── config.py
 ├── db/
 │    └── pgvector.py
 ├── rag/
 │    ├── embed.py
 │    └── retrieve.py
 └── main.py

A minimal production-style Retrieval-Augmented Generation (RAG) backend built with:

- FastAPI
- PostgreSQL + pgvector
- SentenceTransformers embeddings
- Docker
- API key protection

---

## Architecture

User Query
    ↓
Embedding Model (SentenceTransformers)
    ↓
pgvector cosine similarity search
    ↓
Top-K chunks retrieved
    ↓
Answer constructed with citations

---

## Features

- Semantic search using cosine distance
- pgvector IVFFlat index
- Top-K configurable retrieval
- Chunk-based document ingestion
- API key protected endpoints
- Fully Dockerised environment

---

## Endpoints

### POST /v1/ingest

Ingest documents into the vector database.

### POST /v1/query

Query the system using semantic search.

Example:

```json
{
  "query": "mfa failing"
}

