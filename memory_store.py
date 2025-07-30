import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

BASE_DIR = "user_memory"

def get_user_paths(user_id):
    return (
        os.path.join(BASE_DIR, f"{user_id}_index.faiss"),
        os.path.join(BASE_DIR, f"{user_id}_texts.pkl")
    )

def store_user_message(user_id, message):
    os.makedirs(BASE_DIR, exist_ok=True)
    index_path, texts_path = get_user_paths(user_id)

    embedding = model.encode([message])
    
    # Load or create index
    if os.path.exists(index_path):
        index = faiss.read_index(index_path)
        with open(texts_path, "rb") as f:
            texts = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(embedding.shape[1])
        texts = []

    index.add(np.array(embedding))
    texts.append(message)

    faiss.write_index(index, index_path)
    with open(texts_path, "wb") as f:
        pickle.dump(texts, f)

def get_user_memory(user_id, query, k=3):
    index_path, texts_path = get_user_paths(user_id)
    if not os.path.exists(index_path):
        return []

    index = faiss.read_index(index_path)
    with open(texts_path, "rb") as f:
        texts = pickle.load(f)

    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k)
    return [texts[i] for i in I[0] if i < len(texts)]