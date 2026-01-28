# 🚀 RAG Agent

This project implements a Retrieval-Augmented Generation (RAG) based document Question Answering system.
It follows a client–server architecture with clear separation between UI, backend logic, retrieval, and generation.

---

## 🖥️ How to Run the Project Locally

Follow the steps below to run the **RAG Agent** on your local machine.

---

## ✅ Prerequisites

Make sure you have the following installed:

- **Python 3.9+**
- **Git**
- **Gemini 1.5 Flash** or **Ollama** (for local LLM & embeddings)
- A stable terminal (**VS Code recommended**)

---

# 1️⃣ Clone the Repository
```bash
git clone <your-github-repo-url>
cd RAG
```

# 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

# 3️⃣ Install & Run Ollama Models
Make sure Ollama is running, then pull the required models:
```bash
ollama pull llama3
ollama pull nomic-embed-text
```

# 4️⃣ Project Structure:

```
rag-document-qna/
│
├── app.py                 # FastAPI backend (upload & QnA APIs)
├── streamlit_app.py       # Streamlit frontend for user interaction
│
├── embedder.py            # Ollama embedding logic (nomic-embed-text)
├── ingest.py              # Document chunking, embedding, and FAISS indexing
├── retriever.py           # Similarity search using FAISS
│
├── utils/
│   ├── loader.py          # PDF and TXT text extraction utilities
│
├── data/
│   ├── docs/              # Locally stored uploaded documents
│   ├── faiss.index        # FAISS vector index (generated)
│   └── metadata.pkl       # Chunk metadata (generated)
│
├── requirements.txt       # Project dependencies
├── .env                   # Environment configuration (ignored in Git)
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation

```

# 5️⃣ Run the Application:
```bash
ollama serve
uvicorn app:app --reload
streamlit run app.py
```
The app will open automatically in your browser at:
http://localhost:8501

# 6️⃣ Demo Flow (What to Test)

1. Upload a PDF/TXT file

2. Ask questions from the uploaded file.


# Architecture Explanation

The system uses a Streamlit frontend connected to a FastAPI backend, where documents are embedded using Ollama, stored in FAISS for semantic retrieval, and combined with an LLM to generate context-aware answers using a RAG pipeline.

```
User
 │
 ▼
Streamlit UI
 │  (upload documents / ask questions)
 ▼
FastAPI Backend
 │
 ├── Document Ingestion Pipeline
 │   ├─ PDF / TXT Loader
 │   ├─ Text Chunking
 │   ├─ Embedding Generation (Ollama – nomic-embed-text)
 │   ├─ Vector Storage (FAISS)
 │
 └── Query Pipeline
     ├─ Query Embedding
     ├─ Similarity Search (FAISS)
     ├─ Context Retrieval (Top-k chunks)
     ├─ Answer Generation (Ollama LLM)
     └─ Response to UI
```

The Streamlit frontend provides a simple interface for uploading PDF or TXT documents and asking questions. User requests are sent to a FastAPI backend, which acts as the central controller. FastAPI handles request validation, rate limiting, document ingestion, and query processing.

When a document is uploaded, the backend saves it locally and processes it through an ingestion pipeline that includes text extraction, chunking, and embedding generation using Ollama’s nomic-embed-text model. The resulting embeddings are stored in a FAISS vector index along with metadata, enabling efficient semantic retrieval.

For question answering, the user query is embedded and compared against stored document embeddings using FAISS similarity search. The most relevant chunks are retrieved and passed as context to an Ollama language model, which generates a grounded, document-aware response.

Overall, the architecture emphasizes:
Clear separation of frontend, backend, and retrieval layers
Fast semantic search using FAISS

## Architecture Flow 
 ![langgraph_model ss](graph.png)


## Chunk Size Selection

A chunk size of ~500 characters with 100-character overlap was chosen to balance contextual completeness and retrieval accuracy. Smaller chunks tend to lose important context needed for meaningful answers, while very large chunks reduce retrieval precision because unrelated information gets embedded together. The overlap ensures that information split across chunk boundaries is not lost, which improves recall during similarity search.

## Observed Retrieval Failure Case

One retrieval failure case was observed with scanned or image-based PDF documents where text could not be extracted properly. For this purpose, OCR is needed first to extract text and then converted into embeddings.

## Metric Tracked

The primary metric tracked was the FAISS cosine similarity score returned during retrieval. This metric was used to evaluate how closely the retrieved document chunks matched the user query, where lower distance values indicated higher semantic similarity. Monitoring this score helped in assessing retrieval quality.
