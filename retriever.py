import faiss
import pickle
import numpy as np
from embedder import get_embedding

def retrieve_chunks(query, k=3):
    index = faiss.read_index("data/faiss.index")

    with open("data/metadata.pkl", "rb") as f:
        metadata = pickle.load(f)

    q_emb = get_embedding(query).reshape(1, -1)
    faiss.normalize_L2(q_emb)
    distances, indices = index.search(q_emb, k)

    results = []
    for idx in indices[0]:
        results.append(metadata[idx]["text"])

    return results, distances[0]
