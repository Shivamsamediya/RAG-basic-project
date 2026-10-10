from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.core.config import settings

# FastAPI application ka main instance banate hain
app = FastAPI(
    title="RAG Pipeline API",
    description="Beginner-friendly but production-style RAG application with FastAPI, LangChain, ChromaDB aur Gemini API.",
    version="1.0.0"
)

# CORS middleware add karte hain taaki koi bhi frontend app is API ko call kar sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Production me isko specific domains par set karna chahiye
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jo routes humne endpoints.py me banaye hain, unko yahan include/connect karte hain
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    """
    Ek simple health-check API endpoint.
    Check karne ke liye ki server running hai ya nahi.
    """
    return {"message": "Welcome to the RAG Pipeline API! Head over to /docs to test the endpoints."}
