import logging
from pathlib import Path
import shutil

from fastapi import FastAPI, UploadFile, File,HTTPException

from backend.config import settings
from backend.schemas import HealthResponse, UploadResponse, DocumentInfo,ChunkingResponse, ChunkInfo
from backend.document_loader import extract_text_from_pdf
from backend.text_chunker import chunk_text_file, save_chunks_to_json, load_chunks_from_json


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
@app.post("/documents/{filename}/chunks", response_model=ChunkingResponse)
def create_document_chunks(filename: str):
    source_path = Path(filename)
    extracted_file_path = Path("data/extracted") / f"{source_path.stem}.txt"

    if not extracted_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Extracted text not found for document: {filename}",
        )

    chunks_data = chunk_text_file(
        file_path=str(extracted_file_path),
        source_document=filename,
    )

    chunks_file_path = save_chunks_to_json(
    chunks=chunks_data,
    source_document=filename,
    )

    chunks = [ChunkInfo(**chunk) for chunk in chunks_data]

    return ChunkingResponse(
    source_document=filename,
    total_chunks=len(chunks),
    chunks_file_path=chunks_file_path,
    chunks=chunks,
    message="Document chunks generated and saved successfully",
    )

@app.get("/documents/{filename}/chunks", response_model=ChunkingResponse)
def get_document_chunks(filename: str):
    try:
        chunks_data = load_chunks_from_json(source_document=filename)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Chunks not found for document: {filename}. Generate chunks first.",
        )

    chunks = [ChunkInfo(**chunk) for chunk in chunks_data]

    chunks_file_path = str(
        Path("data/chunks") / f"{Path(filename).stem}_chunks.json"
    )

    return ChunkingResponse(
        source_document=filename,
        total_chunks=len(chunks),
        chunks_file_path=chunks_file_path,
        chunks=chunks,
        message="Document chunks loaded successfully",
    )