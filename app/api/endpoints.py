import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas import AskRequest, AskResponse, UploadResponse, SourceChunk
from app.services.ingestion import process_and_store_document
from app.services.retrieval import answer_question
from app.core.config import settings

router = APIRouter()

# Ek temporary folder banate hain jisme hum uploaded PDF ko save kar sakein process karne se pehle
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-documents", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Yeh API endpoint user se PDF file leta hai, usko extract, chunk aur vectorize (embed) karke ChromaDB me save karta hai.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Sirf PDF files allowed hain.")
        
    # File ko temporarily server par save karna
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # Ingestion pipeline run karte hain
        total_chunks = process_and_store_document(file_path)
        
        # Cleanup: file process hone ke baad temporarily save ki gayi file hata dein
        os.remove(file_path)
        
        return UploadResponse(
            message="Document successfully processed aur database me store ho gaya hai.",
            filename=file.filename,
            total_chunks=total_chunks
        )
    except Exception as e:
        # Agar koi error aaye toh clearly show karna aur file delete kar dena
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    Yeh API endpoint user ka sawaal leta hai, similarity search karta hai aur AI se answer generate karwata hai.
    """
    if not settings.gemini_api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY set nahi hai. Kripya .env file check karein.")
        
    try:
        # Retrieval aur Generation pipeline run karte hain
        answer, sources_data = answer_question(request.question)
        
        # Response object banate hain
        sources = [SourceChunk(**src) for src in sources_data]
        
        return AskResponse(
            answer=answer,
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
