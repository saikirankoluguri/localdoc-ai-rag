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

class ChunkingSummaryResponse(BaseModel):
    source_document: str
    total_chunks: int
    chunks_file_path: str
    message: str

class ChunkPreviewResponse(BaseModel):
    source_document: str
    total_chunks: int
    preview_count: int
    chunks: List[ChunkInfo]
    message: str

class IndexResponse(BaseModel):
    # Original document name that was indexed
    source_document: str

    # Number of text chunks stored in the vector database
    total_chunks_indexed: int

    # ChromaDB collection where chunks are stored
    collection_name: str

    # Human-readable status message
    message: str


class SearchRequest(BaseModel):
    # User question or search query
    query: str

    # Number of most relevant chunks to return
    top_k: int = 3

#This represents one matching chunk.
class SearchResult(BaseModel):
    # Position of the chunk in the original chunk list
    chunk_index: int
    # Actual chunk text retrieved from vector database
    text: str
    # Original document where this chunk came from
    source_document: str
    # Length of this chunk in characters
    character_count: int
    # Similarity/relevance score from vector search
    relevance_score: float | None = None

#This represents the full API response for one search request. It contains multiple SearchResult objects.
class SearchResponse(BaseModel):
    # Original user query
    query: str
    # Number of search results returned
    total_results: int
    # List of matching chunks
    results: List[SearchResult]
    # Human-readable status message
    message: str

# Insert this code directly at the bottom of backend/schemas.py

class SourceChunk(BaseModel):
    chunk_index: int
    text: str
    source_document: str
    relevance_score: float

class AskRequest(BaseModel):
    question: str
    top_k: int = 3

class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceChunk]

