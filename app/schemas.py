from pydantic import BaseModel
from typing import List, Optional

# Question poochne ke liye request body
class AskRequest(BaseModel):
    question: str

# Retrieve kiye gaye chunks (sources) ka structure
class SourceChunk(BaseModel):
    content: str
    metadata: dict
    score: float

# Final answer jo API return karegi
class AskResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]

# Document upload ka response
class UploadResponse(BaseModel):
    message: str
    filename: str
    total_chunks: int
