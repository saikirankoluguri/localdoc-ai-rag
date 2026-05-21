# localdoc-ai-rag

# LocalDoc AI - RAG Document Assistant

A simple end-to-end RAG application that allows users to upload documents and ask questions based on their content.

## Tech Stack

- Python
- FastAPI
- LangChain
- ChromaDB
- Ollama
- Streamlit

## Project Status

Sprint 0: Project setup completed.

pip install -r requirements.txt
python -c "import fastapi; import uvicorn; print('FastAPI setup working')"

uvicorn backend.main:app

## Document Ingestion API

### Upload a PDF

Endpoint:

```http
POST /upload

### Step 2: Test final feature

Run:

```bash
uvicorn backend.main:app --reload