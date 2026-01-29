import faiss
import pickle
import numpy as np
from embedder import get_embedding

CHUNK_SIZE = 500
OVERLAP = 100

def chunk_text(text):
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start += CHUNK_SIZE - OVERLAP
    return chunks

def ingest_document(text: str, source: str):
    chunks = chunk_text(text)

    embeddings = []
    metadata = []

    for i, chunk in enumerate(chunks):
        emb = get_embedding(chunk)
        embeddings.append(emb)
        metadata.append({
            "source": source,
            "chunk_id": i,
            "text": chunk
        })

    vectors = np.array(embeddings).astype("float32")
    faiss.normalize_L2(vectors)
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    faiss.write_index(index, "data/faiss.index")
    with open("data/metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)
