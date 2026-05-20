import logging

from fastapi import FastAPI, UploadFile, File

from backend.config import settings
from backend.schemas import HealthResponse, UploadResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    description="Backend API for LocalDoc AI",
)


@app.on_event("startup")
def startup_event():
    logger.info("Starting %s", settings.APP_NAME)
    logger.info("API version: %s", settings.API_VERSION)
    logger.info("Chroma DB path: %s", settings.CHROMA_DB_PATH)
    logger.info("LLM model: %s", settings.MODEL_NAME)
    logger.info("Embedding model: %s", settings.EMBEDDING_MODEL)


@app.get("/", response_model=HealthResponse)
def root():
    return HealthResponse(
        status="ok",
        message=f"Welcome to {settings.APP_NAME}",
    )


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        message=f"{settings.APP_NAME} running successfully",
    )

@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    return UploadResponse(
        filename=file.filename,
        content_type=file.content_type,
        message="File received successfully",
    )