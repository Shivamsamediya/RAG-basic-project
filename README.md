# 🚀 Complete Beginner's Guide to RAG (Retrieval-Augmented Generation)

Welcome! You are an AI Engineer now. This project is a production-style, but beginner-friendly RAG pipeline using FastAPI, LangChain, ChromaDB, and Gemini.

Is project me hum step-by-step seekhenge ki RAG kya hota hai aur kaise kaam karta hai.

---

## 📚 1. Core Concepts (Dimag ki Batti Jalao 💡)

### RAG Kya Hai? (What is RAG?)
LLMs (jaise ChatGPT ya Gemini) bahot smart hote hain, par unhe aapke **private data** (jaise aapki company ki PDF, aapka resume, ya kisi nayi book) ke baare me kuch nahi pata hota. 
Agar aap unse aapke document ke baare me kuch puchenge, toh woh galat answer de sakte hain jise **Hallucination** kehte hain.

**RAG (Retrieval-Augmented Generation)** iska solution hai:
1. **Retrieval**: Sabse pehle hum user ka sawal lete hain, aur apne document me se sirf wahi hissa (chunk) dhoondh ke nikalte hain jo sawal ka jawab de sake.
2. **Augmented**: Us dhoondhe gaye document ke hisse (context) ko hum user ke sawal ke sath jod (augment) dete hain.
3. **Generation**: Ye combined chiz (Question + Context) hum LLM ko dete hain aur bolte hain "Iss context ko padh kar answer do".

### Embeddings Kya Hoti Hain?
Computers ko English ya Hindi samajh nahi aati, unhe sirf numbers (0s aur 1s) samajh aate hain.
**Embeddings** kisi bhi text (word ya sentence) ka ek numerical representation (array of numbers) hota hai.
Maan lijiye "Dog" aur "Puppy" alag words hain, par unka meaning same hai. Embeddings in dono words ko aise numbers me convert karta hai jo maths (geometry) me ek doosre ke bohot paas (similar) hote hain. Hum yahan `SentenceTransformers` use kar rahe hain text ko embed karne ke liye.

### Vector Databases (ChromaDB) Kya Hai?
Normal databases (SQL) me hum exact text search karte hain (`WHERE text="dog"`). 
Par vectors ko hum SQL me save nahi kar sakte aur na hi unme mathematical similarity search kar sakte hain asaani se.
**Vector Databases (jaise ChromaDB)** specially inhi numbers (embeddings) ko store karne aur fast search karne ke liye banaye gaye hain.

### Chunking Aur Overlap Kyun Chahiye?
Aapki PDF me 100 pages ho sakte hain. Hum poori PDF ek baar me LLM ko nahi bhej sakte kyunki LLMs ki **Token Limit** (padhne ki capacity) hoti hai, aur ye mehenga bhi padega.
Isliye hum document ko chhote chhote tukdo (chunks) me todte hain (e.g., 1000 characters). 
**Overlap (e.g., 200 chars)** isliye dete hain taaki ek sentence aadha ek chunk me aur aadha doosre me tut na jaye. Overlap context ko jod ke rakhta hai.

### Semantic Search & Cosine Similarity
Jab aap "puppy" search karte hain aur document me "small dog" likha hai, toh exact keyword search fail ho jayega.
Par Semantic search meaning samjhta hai. Yeh user ke sawal ka bhi vector banata hai, aur ChromaDB me stored sabhi chunks ke vectors ke sath match karta hai. 
**Cosine Similarity** ek math formula hai jo measure karta hai ki do vectors (arrows) ke beech ka angle kitna kam hai. Jitna kam angle, utna similar meaning!

---

## ⚙️ 2. The Pipelines (Kaam Kaise Ho Raha Hai Internally)

### A. Ingestion Pipeline (Data Andar Daalna)
Jab aap `/upload-documents` par PDF bhejte hain:
1. `PyPDFLoader` PDF se saara text nikalta hai.
2. `RecursiveCharacterTextSplitter` usko 1000-character chunks me todta hai.
3. `HuggingFaceEmbeddings` har chunk ko numbers (vectors) me badalta hai.
4. Ye sab `ChromaDB` me permanently (local folder me) save ho jata hai.

### B. Retrieval Pipeline (Data Dhoondhna)
Jab aap `/ask` par question bhejte hain:
1. Aapka sawaal pehle vector me convert hota hai.
2. `ChromaDB` me us vector ki **Cosine Similarity** check hoti hai aur top 4 sabse related chunks nikal ke aate hain.

### C. Generation Pipeline (Answer Banana)
1. Jo chunks mile, unko mila kar ek **Prompt** (instruction) banaya jata hai.
2. **Prompt Engineering:** Hum AI ko strictly bolte hain "Apne man se kuch mat bolo, sirf diye gaye context se answer do". (Ye Hallucination rokti hai).
3. Ye prompt **Gemini API** ke paas jata hai, aur woh exact, sahi answer (aur source chunks) wapas bhejta hai.

---

## 🛠 3. Setup Instructions

### Step 1: Python Virtual Environment Banayein
Virtual Environment (venv) ek isolated space hota hai taaki is project ke packages aapke system ko affect na karein.

Terminal (Command Prompt / PowerShell) kholein aur project folder (`c:\Users\DELL\NextJs\rag-simple`) me jaayein:
```bash
python -m venv venv
```

### Step 2: Virtual Environment Activate Karein
**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```
*(Agar execution policy error aaye, toh ye run karein: `Set-ExecutionPolicy Unrestricted -Scope CurrentUser`)*

**Windows (Command Prompt):**
```bash
.\venv\Scripts\activate.bat
```

### Step 3: Dependencies Install Karein
```bash
pip install -r requirements.txt
```

### Step 4: Environment Variables Set Karein
1. `.env.example` file ko copy karein aur usko rename karke `.env` banayein.
2. Apni Gemini API key `GEMINI_API_KEY` me daalein.
*(Gemini API key free me Google AI Studio se mil jayegi)*

### Step 5: Server Run Karein
```bash
uvicorn app.main:app --reload
```
Aapka server ab `http://localhost:8000` par chal raha hai!
- Swagger UI (Test karne ke liye): `http://localhost:8000/docs`

---

## 🧪 4. Testing With Postman

Humne ek `postman_collection.json` file di hai. Isko aap Postman app me Import karein:
1. Postman kholein -> **Import** par click karein.
2. `postman_collection.json` file select karein.
3. Collection me aapko do API milengi:
   - **Upload Document:** Body tab me form-data me ek PDF file upload karein aur Send dabayein.
   - **Ask Question:** Body tab me raw JSON me apna question likhein aur Send dabayein.

### Sample Request/Response

**POST /api/upload-documents**
*Request:* FormData (file="sample.pdf")
*Response:*
```json
{
  "message": "Document successfully processed aur database me store ho gaya hai.",
  "filename": "sample.pdf",
  "total_chunks": 15
}
```

**POST /api/ask**
*Request:*
```json
{
  "question": "What are the main features mentioned in the document?"
}
```
*Response:*
```json
{
  "answer": "The main features mentioned are data ingestion, vector search, and LLM generation.",
  "sources": [
    {
      "content": "...(extracted chunk text)...",
      "metadata": {"source": "temp_uploads/sample.pdf", "page": 2},
      "score": 0.5432
    }
  ]
}
```

*(Note: Score jitna kam hota hai L2 distance me, utna related hota hai. ChromaDB by default L2 distance deta hai.)*

---
**Happy Coding! Aap ab ek fully functional AI RAG app bana chuke hain.** 🚀
