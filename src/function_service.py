from models import Repo, FunctionNode
import ast


def extract_functions(repo: Repo) -> None:

    for module in repo.modules.values():

        if module.language != "py":
            continue

        try:

            source = module.abs_path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(source)

            functions = []
            seen_functions = set()

            for node in ast.walk(tree):

                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                    key = (module.module_id, node.name)

                    if key in seen_functions:
                        continue

                    seen_functions.add(key)

                    fn = FunctionNode(
                        name=node.name,
                        module_id=module.module_id,
                        start_line=node.lineno,
                        end_line=node.end_lineno or node.lineno,
                        calls=[]
                    )

                    # scan inside the function body
                    for subnode in ast.walk(node):

                        if isinstance(subnode, ast.Call):

                            if isinstance(subnode.func, ast.Name):
                                fn.calls.append(subnode.func.id)

                            elif isinstance(subnode.func, ast.Attribute):
                                fn.calls.append(subnode.func.attr)

                    # remove duplicate calls
                    fn.calls = list(set(fn.calls))

                    print(
                        f"Extracted function {fn.name} from module {module.module_id} "
                        f"at lines {fn.start_line}-{fn.end_line}"
                    )

                    functions.append(fn)

            module.functions = functions

        except Exception as e:
            print(f"Error processing {module.abs_path}: {e}")