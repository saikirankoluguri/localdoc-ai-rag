from fastapi import FastAPI
from backend.config import settings
from backend.schemas import HealthResponse

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    description="Backend API for LocalDoc AI, a simple end-to-end RAG document assistant.",
)
@app.get("/health",response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        message=f"{settings.APP_NAME} is running Successfully",
    )
