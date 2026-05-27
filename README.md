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

python -c "from langchain_text_splitters import RecursiveCharacterTextSplitter; print('Text splitter working')"

ollama serve

ollama pull nomic-embed-text
ollama pull llama3.1

ollama list

1.0   → almost identical meaning
0.8   → very related
0.5   → somewhat related
0.2   → weak relation
0     → unrelated
-1    → opposite meaning

Real RAG FLOW:
User Question
      ↓
Embedding model
      ↓
Question vector

Question vector
      ↓
Compare against all chunk vectors
      ↓
Cosine similarity calculation
      ↓
Sort by highest score
      ↓
Return top K chunks