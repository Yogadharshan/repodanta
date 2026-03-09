from repodanta.models import Repo
from ast import Import, ImportFrom, parse, walk


from repodanta.models import Repo
from ast import Import, ImportFrom, parse, walk


def enrich_dependencies(repo: Repo) -> None:
    for module in repo.modules.values():
        if module.language != "py":
            continue
        try:
            with open(module.abs_path, "r", encoding="utf-8", errors="ignore") as file:
                tree = parse(file.read())

            imports = set()

            for node in walk(tree):
                if isinstance(node, Import):
                    for alias in node.names:
                        name = alias.name.split(".")[0] + ".py"
                        match = next((k for k in repo.modules if k == name or k.endswith("." + name)), None)
                        if match:
                            imports.add(match)

                elif isinstance(node, ImportFrom):
                    if node.module:
                        name = node.module.split(".")[-1] + ".py"  # fixed: use node.module not alias
                        match = next((k for k in repo.modules if k == name or k.endswith("." + name)), None)
                        if match:
                            imports.add(match)

            module.imports = list(imports)

        except Exception as e:
            print(f"error processing {module.abs_path}: {e}")