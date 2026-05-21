import logging
from pathlib import Path
import shutil

from fastapi import FastAPI, UploadFile, File,HTTPException

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
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    upload_dir = Path("data/raw")
    upload_dir.mkdir(parents=True, exist_ok=True)

    saved_path = upload_dir / file.filename

    with saved_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return UploadResponse(
        filename=file.filename,
        content_type=file.content_type,
        saved_path=str(saved_path),
        message="File uploaded and saved successfully",
    )