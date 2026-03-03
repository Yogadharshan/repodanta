import argparse
from src.function_service import extract_functions
from src.index_service import index_repo
from src.dependency_service import enrich_dependencies
from src.graph_service import analyze_structure
from src.chunker import chunk_repo


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to project")
    args = parser.parse_args()
    repo = index_repo(args.path)
    enrich_dependencies(repo)
    analyze_structure(repo)
    print(f"Root: {repo.root}")
    print(f"Total modules: {repo.total_modules}")
    print(f"Total lines: {repo.total_lines}")
    print("\nModules:")
    extract_functions(repo)

    for module_id, module in repo.modules.items():
        print(f"  {module_id} | {module.language} | {module.lines_of_code} LOC")
        print(module_id, "->", module.imports)
        print(repo.modules["src.index_service.py"].imports)

    top_modules = sorted(repo.modules.values(), key=lambda m: m.risk_score, reverse=True)[:5]

    print("\nTop 5 modules by risk score:")
    for m in top_modules:
        print(f"{m.module_id}: Fan-in={m.fan_in}, Fan-out={m.fan_out}, Risk Score={m.risk_score}")

    for m in repo.modules.values():
        print(m.module_id, len(m.functions))

        chunks = chunk_repo(repo)

    print("Total chunks:", len(chunks))

    for c in chunks[:5]:
        print(c.chunk_id)
    
if __name__ == "__main__":
    main()