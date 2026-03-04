from models import Repo, ModuleNode
from ast import Import, parse, walk, ImportFrom

def enrich_dependencies(repo: Repo) -> None:
    """
    Enrich the Repo object with dependency information.
    This function is a placeholder and should be implemented to analyze the modules
    and populate the imports field of each ModuleNode based on the actual dependencies.
    """

    for module in repo.modules.values():
        if module.language != "py": # Only process Python modules for now
            pass  # TODO: Add support for other languages in the future
        elif module.language == "py": # Process Python modules

            # add logic to parse the module file and extract imports
            try:
                with open(module.abs_path, 'r') as file:
                    tree = parse(file.read())
                    imports = set()  # Use a set to avoid duplicates
                    for node in walk(tree):
                        if isinstance(node, Import):
                            for alias in node.names:
                                imports.add(alias.name + ".py")  # Assuming the imported module is a Python file
                        elif isinstance(node, ImportFrom):
                            module_name = node.module
                            if module_name:
                                normalized_id = module_name + ".py"
                                if normalized_id in repo.modules:
                                    imports.add(normalized_id)  # Add the normalized module name with .py extension
                                else:
                                    imports.add(module_name + ".py")   # Fallback to the full module name with .py extension
                    

                    module.imports = list(imports)
            except Exception as e:
                print(f"Error processing {module.abs_path}: {e}")
        


