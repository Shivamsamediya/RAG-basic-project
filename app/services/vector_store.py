from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import settings

# 1. Embeddings Model Setup
# Yahan hum HuggingFace ka open-source model use kar rahe hain embeddings banane ke liye.
# "all-MiniLM-L6-v2" ek bahut popular aur fast model hai jo text ko numbers (vectors) mein convert karta hai.
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Vector Database Setup (ChromaDB)
# Hum ChromaDB use kar rahe hain kyunki ye local aur free hai.
# 'persist_directory' ka matlab hai ki data yahan save hoga taki server restart karne par data delete na ho.
def get_vector_store():
    # Yeh function ChromaDB ka instance return karega jisme humare embeddings model linked honge
    return Chroma(
        persist_directory=settings.chroma_persist_directory,
        embedding_function=embeddings
    )
