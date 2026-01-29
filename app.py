import os
from fastapi import FastAPI, UploadFile
from retriever import retrieve_chunks
from ingest import ingest_document
from utils.loaders import load_txt, load_pdf
import requests
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request
# from slowapi.errors import RateLimitExceeded
# from fastapi.responses import JSONResponse
from dotenv import load_dotenv
load_dotenv()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter

DOCS_DIR = "data/docs"
os.makedirs(DOCS_DIR, exist_ok=True) 
OLLAMA_CHAT_URL = os.getenv("OLLAMA_CHAT_URL")
LLM_MODEL = os.getenv("LLM_MODEL")

app = FastAPI()

@app.post("/upload")
async def upload_doc(file: UploadFile):
    file_bytes = await file.read()

    file_path = os.path.join(DOCS_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    if file.filename.endswith(".txt"):
        text = load_txt(file_bytes)
    elif file.filename.endswith(".pdf"):
        text = load_pdf(file_bytes)
    else:
        return {"error": "Unsupported file type"}

    ingest_document(text, source=file.filename)

    return {
        "message": f"{file.filename} uploaded and indexed successfully",
        "saved_path": file_path
    }


@app.post("/ask")
@limiter.limit("5/minute")
async def ask(request: Request, question: str):
    chunks, scores = retrieve_chunks(question)

    context = "\n\n".join(chunks)

    prompt = f"""
Use the following context to answer the question.
If the answer is not present, say "No context found".

Context:
{context}

Question:
{question}
"""

    response = requests.post(
        OLLAMA_CHAT_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    answer = response.json()["response"]
    return {
        "answer": answer,
        "similarity_scores": scores.tolist()
    }
