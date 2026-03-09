import os
from repodanta.index_service import index_repo
from repodanta.dependency_service import enrich_dependencies
from repodanta.graph_service import analyze_structure
from repodanta.function_service import extract_functions
from repodanta.graph_builder import build_graphs
from repodanta.chunker import chunk_repo
from repodanta.embedder import embed_chunks
from repodanta.vector_store import build_index, save_index, load_index, save_chunks, load_chunks
from repodanta.repo_hash import check_repo_hash, save_repo_hash


def load_repo(path: str):
    repo = index_repo(path)
    enrich_dependencies(repo)
    analyze_structure(repo)
    extract_functions(repo)
    build_graphs(repo)
    return repo


def load_index_and_chunks(repo, path: str):
    os.makedirs(".repodanta", exist_ok=True)
    index_file = ".repodanta/index.faiss"
    chunks_file = ".repodanta/chunks.pkl"
    hash_file = ".repodanta/repo_hash.txt"

    if check_repo_hash(repo, hash_file) and os.path.exists(index_file) and os.path.exists(chunks_file):
        print("repo unchanged. loading index.")
        index = load_index(index_file)
        chunks = load_chunks(chunks_file)
        return index, chunks, None

    print("building repository index...")
    chunks = chunk_repo(repo)
    print(f"chunks created: {len(chunks)}")
    embeddings = embed_chunks(chunks)
    index = build_index(embeddings)
    save_index(index, index_file)
    save_chunks(chunks, chunks_file)
    save_repo_hash(repo, hash_file)
    return index, chunks, embeddings