from pathlib import Path
from config import ignore_folders, supported_extensions
from models import ModuleNode, FunctionNode, Repo



def index_repo(path):
    repo_root = Path(path).resolve()
    validate_path(repo_root)
    files = scan_files(repo_root)
    modules = build_modules(files, repo_root)
    repo = build_repo(repo_root, modules)
    return repo

def validate_path(repo_root: Path):
    if not repo_root.exists():
        raise ValueError(f"Path {repo_root} does not exist")
    if not repo_root.is_dir():
        raise ValueError(f"Path {repo_root} is not a directory")

def scan_files(repo_root: Path) -> list[Path]:
    # Placeholder for file scanning logic

    files = []

    for file in repo_root.rglob("*"):
        if file.is_file() and file.suffix in supported_extensions:
            if not any(ignored in file.parts for ignored in ignore_folders):
                files.append(file) # it is Path object, we can convert to string later if needed
    
    return files

def count_lines(file: Path) -> int:
    try:
        with file.open("r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def build_modules(files: list[Path], repo_root: Path) -> dict[str, ModuleNode]:
    # Placeholder for module building logic
    modules = {}
    for file in files:
        relative_path = file.relative_to(repo_root) # get path relative to repo root
        module_id = ".".join(relative_path.parts) # convert path to module id by replacing slashes with dots
        module = ModuleNode(
            module_id=module_id,
            abs_path=file,
            imports=[],
            functions=[],
            classes=[],
            language=file.suffix[1:], # remove the dot
            lines_of_code = count_lines(file)
        )
        if module_id in modules:
            raise ValueError(f"Duplicate module id {module_id} for file {file} and {modules[module_id].abs_path}")
        else:
            modules[module_id] = module
    return modules
    
def build_repo(repo_root: Path, modules: dict[str, ModuleNode]) -> Repo:
    total_lines = sum(module.lines_of_code for module in modules.values())
    total_modules = len(modules)
    return Repo(root=repo_root,
                modules=modules,
                total_lines=total_lines,
                 total_modules=total_modules
            )
    