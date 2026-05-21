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
    message: str