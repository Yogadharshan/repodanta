import argparse

from src.index_service import index_repo
from src.dependency_service import enrich_dependencies
from src.graph_service import analyze_structure
from src.function_service import extract_functions
from src.chunker import chunk_repo
from src.embedder import embed_chunks, embed_query
from src.vector_store import build_index
from src.retriever import retrieve
from src.query_engine import answer_query


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to repo")
    parser.add_argument("--query", help="question about repo")

    args = parser.parse_args()

    repo = index_repo(args.path)

    enrich_dependencies(repo)
    analyze_structure(repo)
    extract_functions(repo)

    chunks = chunk_repo(repo)

    embeddings = embed_chunks(chunks)

    index = build_index(embeddings)

    answer = answer_query(args.query, repo, index, chunks)

    print("\nanswer:\n")
    print(answer)


if __name__ == "__main__":
    main()