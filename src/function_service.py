from src.models import Repo, ModuleNode, FunctionNode
import ast

def extract_functions(repo: Repo) -> None:
    for module in repo.modules.values():
        if module.language != "py":
            continue

        try:
            source = module.abs_path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(source)

            functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    fn = FunctionNode(
                        name=node.name,
                        module_id=module.module_id,
                        start_line=node.lineno,
                        end_line=node.end_lineno or node.lineno
                    )
                    print(f"Extracted function {fn.name} from module {module.module_id} at lines {fn.start_line}-{fn.end_line}")
                    functions.append(fn)

                if isinstance(node, ast.AsyncFunctionDef):
                    fn = FunctionNode(
                        name=node.name,
                        module_id=module.module_id,
                        start_line=node.lineno,
                        end_line=node.end_lineno or node.lineno
                    )
                    functions.append(fn)

            module.functions = functions

        except Exception as e:
            print(f"Error processing {module.abs_path}: {e}")