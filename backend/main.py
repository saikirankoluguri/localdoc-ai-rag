import logging
from pathlib import Path
import shutil

from fastapi import FastAPI, UploadFile, File,HTTPException

from backend.config import settings
from backend.schemas import HealthResponse, UploadResponse, DocumentInfo
from backend.document_loader import extract_text_from_pdf


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

    extracted_data = extract_text_from_pdf(str(saved_path))

   
    return UploadResponse(
    filename=file.filename,
    content_type=file.content_type,
    saved_path=str(saved_path),
    extracted_text_path=extracted_data["extracted_text_path"],
    page_count=extracted_data["page_count"],
    text_length=extracted_data["text_length"],
    message="File uploaded, saved, and text extracted successfully",
    )

@app.get("/documents", response_model=list[DocumentInfo])
def list_documents():
    upload_dir = Path("data/raw")
    upload_dir.mkdir(parents=True, exist_ok=True)

    documents = []

    for file_path in upload_dir.glob("*.pdf"):
        file_size_kb = round(file_path.stat().st_size / 1024, 2)

        documents.append(
            DocumentInfo(
                filename=file_path.name,
                file_path=str(file_path),
                file_size_kb=file_size_kb,
            )
        )

    return documents