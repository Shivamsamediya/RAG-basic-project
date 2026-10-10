import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.vector_store import get_vector_store

def process_and_store_document(file_path: str) -> int:
    """
    Yeh function PDF ko read karega, uske chunks banayega aur ChromaDB mein store karega.
    (Ingestion Pipeline)
    """
    
    # 1. EXTRACT: PDF loader banate hain jo page-by-page text extract karega.
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # 2. CHUNKING: Text ko chhote tukdon (chunks) mein todna.
    # Kyun? Kyunki LLM aur Embedding models ki ek limit hoti hai (Token limit). 
    # Hum poori PDF ek sath nahi bhej sakte.
    # chunk_size=1000 ka matlab har chunk mein lagbhag 1000 characters honge.
    # chunk_overlap=200 ka matlab lagatar 2 chunks mein 200 characters common honge, 
    # taaki context break na ho (jaise aadhi line ek chunk me aur aadhi doosre me na chali jaye).
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    
    # Ab documents ko split karte hain chunks mein
    chunks = text_splitter.split_documents(documents)
    
    # 3. EMBED & STORE: Chunks ko vectors (numbers) mein convert karke database mein save karna
    vector_store = get_vector_store()
    
    # add_documents function automatically chunks ko embed karke database me save kar dega
    vector_store.add_documents(chunks)
    
    # total chunks kitne bane, return karte hain
    return len(chunks)
