import faiss
import numpy as np
import pickle

def save_chunks(chunks, path=".repodanta/repodanta_chunks.pkl"):
    with open(path, "wb") as f:
        pickle.dump(chunks, f)

def load_chunks(path=".repodanta/repodanta_chunks.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)
    

# Build a FAISS index from the given embeddings
def build_index(embeddings):
    dim = embeddings.shape[1]
    
    index = faiss.IndexFlatL2(dim)
    faiss.normalize_L2(embeddings)

    index.add(embeddings)
    return index


# Search the FAISS index for the top_k most similar chunks to the query vector
def search_index(index, query_vec, top_k=5):
    faiss.normalize_L2(query_vec)

    scores, indices = index.search(query_vec, top_k)

    return scores, indices

def save_index(index, path=".repodanta/repodanta_index.faiss"):
    faiss.write_index(index, path)

def load_index(path=".repodanta/repodanta_index.faiss"):
    return faiss.read_index(path)


