from fastapi import FastAPI

app = FastAPI(
    title="LocalDoc AI RAG API",
    description="Backend API for LocalDoc AI, a simple end-to-end RAG document assistant.",
    version="0.1.0",
)
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "LocalDoc AI RAG API is running",
    }
