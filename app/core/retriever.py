import os
import numpy as np
import faiss
import pickle
import yaml
from app.core.embedder import embed_texts
from datetime import datetime


with open("config/config.yaml") as f:
    cfg = yaml.safe_load(f)

def get_paths(session_id):
    base_dir = os.path.join("data", f"session_{session_id}", "backup")
    return {
        "INDEX_PATH": os.path.join(base_dir, "faiss.index"),
        "META_PATH": os.path.join(base_dir, "chunks.pkl")
    }


def normalize_embeddings(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / norms

def build_index(text_chunks,session_id,force_rebuild):
    paths = get_paths(session_id)
    INDEX_PATH = paths["INDEX_PATH"]
    META_PATH = paths["META_PATH"]
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)

    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH) and not force_rebuild:
        print("Index already exists.")
        return

    print("Building FAISS index...")

    vectors = embed_texts(text_chunks)
    vectors = normalize_embeddings(np.array(vectors).astype("float32"))

    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim) 

    index.add(vectors)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(text_chunks, f)

    print("FAISS index saved.")

def load_index(session_id):
    paths = get_paths(session_id)
    INDEX_PATH = paths["INDEX_PATH"]
    META_PATH = paths["META_PATH"]

    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError("FAISS index not found.")
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def retrieve_chunks(query,session_id, k=5):
    index, chunks = load_index(session_id)
    q_vec = embed_texts([query])
    q_vec = normalize_embeddings(np.array(q_vec).astype("float32"))
    _, I = index.search(q_vec, k)
    return [chunks[i] for i in I[0]]
