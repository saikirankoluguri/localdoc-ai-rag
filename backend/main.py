from fastapi import FastAPI
from backend.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    description="Backend API for LocalDoc AI, a simple end-to-end RAG document assistant.",
)
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": f"{settings.APP_NAME} is running",
    }
