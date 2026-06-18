from repodanta import config

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(config.embedding_model)
    return _model


def embed_chunks(chunks):
    model = _get_model()
    contents = [chunk.content for chunk in chunks]
    embeddings = model.encode(contents, show_progress_bar=True)
    return embeddings


def embed_query(query):
    model = _get_model()
    vec = model.encode([query])
    return vec.astype("float32")
