from pydantic import BaseModel
from typing import List


class HealthResponse(BaseModel):
    status: str
    message: str


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    answer: str
    sources: List[str]

class UploadResponse(BaseModel):
    filename: str
    content_type: str
    saved_path: str
    extracted_text_path: str
    page_count: int
    text_length: int
    message: str

class DocumentInfo(BaseModel):
    filename: str
    file_path: str
    file_size_kb: float

class ChunkInfo(BaseModel):
    chunk_index: int
    text: str
    source_document: str
    character_count: int


class ChunkingResponse(BaseModel):
    source_document: str
    total_chunks: int
    chunks_file_path: str
    chunks: List[ChunkInfo]
    message: str