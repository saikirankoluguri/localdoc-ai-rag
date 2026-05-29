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

python -c "from backend.vector_store import search_similar_chunks; print(search_similar_chunks('What is nationalism?', 2))"

One important note:

relevance_score here is a distance score, not always “higher is better”.

For Chroma/LangChain similarity_search_with_score, lower score usually means closer/better match. So:

0.5143 is slightly better than 0.5476

1. Question is specific, but top_k=3 may not be enough
2. Chunking includes textbook exercise/map/table noise
3. We indexed the whole history book, so unrelated chunks compete
4. We are using only semantic search, not keyword filtering
5. Chroma score is distance, not confidence

Finish End-to-End RAG first
Then create "Retrieval Improvements" feature later

## Vector Store and Semantic Search

### Index document chunks

Endpoint:

POST /documents/{filename}/index

Example:

POST /documents/NCERT-Class-10-History.pdf/index

Expected response:

{
  "source_document": "NCERT-Class-10-History.pdf",
  "total_chunks_indexed": 579,
  "collection_name": "documents",
  "message": "Document chunks indexed successfully"
}

If the document is already indexed:

{
  "source_document": "NCERT-Class-10-History.pdf",
  "total_chunks_indexed": 0,
  "collection_name": "documents",
  "message": "Document already indexed"
}

### Semantic Search

Endpoint:

POST /search

Request body:

{
  "query": "What is nationalism?",
  "top_k": 3
}

Description:

Searches ChromaDB and returns the most semantically relevant chunks.

Note:

The current score is a distance score. Lower score usually means a closer match.

### Required local services

Before testing:

ollama list

Make sure these models exist:

- nomic-embed-text
- llama3.1

Run backend:

uvicorn backend.main:app --reload

Swagger:

http://127.0.0.1:8000/docs
