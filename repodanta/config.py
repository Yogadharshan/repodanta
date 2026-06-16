supported_extensions = [".py"]
ignore_folders = {
    ".git",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    "build",
    "dist",
    ".repodanta",
    "assets"
}

ignored_extensions = {
    ".log",
    ".png",
    ".jpg",
    ".jpeg",
    ".mp4",
    ".pdf",
    ".zip",
    ".tar",
    ".gz"
}

# Embedding
embedding_model = "all-MiniLM-L6-v2"

# LLM
ollama_url = "http://localhost:11434/api/generate"
ollama_model = "qwen2.5:7b"

# Storage
storage_dir = ".repodanta"
index_file = ".repodanta/index.faiss"
chunks_file = ".repodanta/chunks.pkl"
hash_file = ".repodanta/repo_hash.txt"

# Retrieval
top_k = 5
chunk_size = 80
