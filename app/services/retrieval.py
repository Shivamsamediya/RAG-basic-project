from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.services.vector_store import get_vector_store
from app.core.config import settings

# LLM Setup (Generation)
# Hum Gemini-2.5-flash use kar rahe hain kyunki ye fast aur smart hai.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=settings.gemini_api_key,
    temperature=0.2 # Temperature kam rakha hai taaki answers factual hon (hallucination kam ho)
)

# PROMPT ENGINEERING
# Yeh prompt design karta hai ki AI ko context aur question kaise dena hai.
# Hum usko strictly bol rahe hain ki sirf context ka use kare (Hallucination rokne ke liye).
RAG_PROMPT_TEMPLATE = """
Aap ek helpful AI assistant hain. 
Neeche diye gaye CONTEXT ka istemaal karke QUESTION ka answer dein.
Agar aapko answer context mein nahi milta, toh clearly bolein: "Sorry, I don't know the answer based on the provided document."
Apne man se answer (hallucinate) mat banayein.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
prompt = PromptTemplate(
    template=RAG_PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)

def answer_question(question: str):
    """
    Yeh function RAG pipeline ka Retrieval aur Generation part handle karta hai.
    """
    
    # 1. RETRIEVAL (Semantic Search)
    vector_store = get_vector_store()
    
    # ChromaDB me similarity_search_with_score() use kar rahe hain
    # k=4 matlab hum top 4 sabse closely related chunks nikalenge
    # Yeh internally pehle Question ko embed karega, phir Cosine Similarity se best chunks dhoondega.
    results = vector_store.similarity_search_with_score(question, k=4)
    
    # Chunks aur context text alag nikalte hain
    context_texts = []
    sources = []
    
    for doc, score in results:
        context_texts.append(doc.page_content)
        sources.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            # Distance/Score: Chroma default L2 distance return karta hai, chhota score matlab zyada similar
            "score": float(score) 
        })
        
    # Saare top chunks ko ek single string me combine karna prompt ke liye
    combined_context = "\n\n---\n\n".join(context_texts)
    
    # 2. GENERATION
    # Langchain Expression Language (LCEL) use kar ke pipeline banate hain:
    # Prompt me variables daalein -> LLM ko bhejein -> Output extract karein
    chain = prompt | llm | StrOutputParser()
    
    # Chain run karke final answer nikalna
    ai_answer = chain.invoke({
        "context": combined_context,
        "question": question
    })
    
    return ai_answer, sources
