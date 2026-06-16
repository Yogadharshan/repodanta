from sentence_transformers import SentenceTransformer
from repodanta import config

model = SentenceTransformer(config.embedding_model)

# Embed a list of code chunks into vectors
def embed_chunks(chunks):
    contents = [chunk.content for chunk in chunks]
    embeddings = model.encode(contents, show_progress_bar=True)
    return embeddings

# Embed a query string into a vector
def embed_query(query):
    vec = model.encode([query])
    return vec.astype("float32")