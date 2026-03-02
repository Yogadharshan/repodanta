import argparse
from src.index_service import index_repo
from src.dependency_service import enrich_dependencies

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to project")
    args = parser.parse_args()

    repo = index_repo(args.path)
    enrich_dependencies(repo)
    print(f"Root: {repo.root}")
    print(f"Total modules: {repo.total_modules}")
    print(f"Total lines: {repo.total_lines}")
    print("\nModules:")
    for module_id, module in repo.modules.items():
        print(f"  {module_id} | {module.language} | {module.lines_of_code} LOC")
        print(module_id, "->", module.imports)

if __name__ == "__main__":
    main()