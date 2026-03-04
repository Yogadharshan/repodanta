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
from src.graph_builder import build_graphs
from src.function_search import find_functions_calling
from src.call_tracer import trace_call_chain

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to repo")
    parser.add_argument("--query", help="question about repo")

    args = parser.parse_args()

    repo = index_repo(args.path)

    enrich_dependencies(repo)
    analyze_structure(repo)
    extract_functions(repo)
    build_graphs(repo)

    print("\nmodule graph:")
    for k, v in repo.module_graph.items():
        print(k, "->", v)

    print("\nfunction graph:")
    for k, v in repo.function_graph.items():
        print(k, "->", v)

    chunks = chunk_repo(repo)

    embeddings = embed_chunks(chunks)

    index = build_index(embeddings)

    answer = answer_query(args.query, repo, index, chunks)

    results = find_functions_calling(repo, "read_text")

    print("\nfunctions calling read_text:\n")

    for r in results:
        print(f"{r['module']}:{r['function']} (line {r['line']})")

    print("\nanswer:\n")
    print(answer)

    chain = trace_call_chain(repo, "read_text")

    print("\ncall chain to read_text:\n")
    
    for caller, callee in chain:
        print(f"{caller} → {callee}")
if __name__ == "__main__":
    main()