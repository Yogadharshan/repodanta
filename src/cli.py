import argparse

from index_service import index_repo
from dependency_service import enrich_dependencies
from graph_service import analyze_structure
from function_service import extract_functions
from chunker import chunk_repo
from embedder import embed_chunks, embed_query
from vector_store import build_index
from retriever import retrieve
from query_engine import answer_query
from duplicate_detector import find_duplicates
import os
from vector_store import save_index, load_index, save_chunks, load_chunks


def run():

    parser = argparse.ArgumentParser(prog="repodanta")

    subparsers = parser.add_subparsers(dest="command")

    query_cmd = subparsers.add_parser("query")
    query_cmd.add_argument("path")
    query_cmd.add_argument("question")

    inspect_cmd = subparsers.add_parser("inspect")
    inspect_cmd.add_argument("path")

    dup_cmd = subparsers.add_parser("duplicates")
    dup_cmd.add_argument("path")

    args = parser.parse_args()

    repo = index_repo(args.path)

    enrich_dependencies(repo)
    analyze_structure(repo)
    extract_functions(repo)

    chunks = chunk_repo(repo)

    os.makedirs(".repodanta", exist_ok=True)
    
    index_path = ".repodanta/index.faiss"
    chunks_path = ".repodanta/chunks.pkl"
    
    if os.path.exists(index_path) and os.path.exists(chunks_path):
        
        index = load_index()
        chunks = load_chunks()
    
    else:
    
        chunks = chunk_repo(repo)
        embeddings = embed_chunks(chunks)
        index = build_index(embeddings)
    
        save_index(index)
        save_chunks(chunks)

    embeddings = embed_chunks(chunks)
    index = build_index(embeddings)

    if args.command == "query":

        answer = answer_query(args.question, repo, index, chunks)
        print(answer)

    elif args.command == "inspect":

        total_loc = sum(m.lines_of_code for m in repo.modules.values())
        total_modules = len(repo.modules)
        total_functions = sum(len(m.functions) for m in repo.modules.values())

        print("\nrepository overview\n")

        print("-" * 40)

        print(f"modules           : {total_modules}")
        print(f"functions         : {total_functions}")
        print(f"lines of code     : {total_loc}")

        print("-" * 40)

        top_fan_out = sorted(
            repo.modules.values(),
            key=lambda m: m.fan_out,
            reverse=True
        )[:3]

        print("\norchestration modules:")
        for m in top_fan_out:
            print(f"  {m.module_id} (fan-out={m.fan_out})")


        top_fan_in = sorted(
            repo.modules.values(),
            key=lambda m: m.fan_in,
            reverse=True
        )[:3]

        print("-" * 40)

        print("\ncore infrastructure modules:")

        for m in top_fan_in:
            print(f"  {m.module_id} (fan-in={m.fan_in}) ")

        print("-" * 40)

        risk = m.fan_in * 2 + m.fan_out
        top_risk = sorted(
            repo.modules.values(),
            key=lambda m: risk,
            reverse=True
        )[:3]
        for m in top_risk: # Highlight modules that are both high fan-in and fan-out (potentially risky)
            print(f" top risk module: {m.module_id} (risk score={risk})")

        print("-" * 40)

        print("\n end of report")

        print("-" * 40)



    elif args.command == "duplicates":

        duplicates = find_duplicates(chunks, embeddings)

        for d in duplicates:
            print(
                d["chunk1"],
                "<->",
                d["chunk2"],
                "| similarity:",
                round(d["similarity"], 3)
            )