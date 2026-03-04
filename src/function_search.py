from models import Repo

def find_functions_calling(repo: Repo, symbol: str):

    results = []

    for module in repo.modules.values():

        for fn in module.functions:

            if symbol in fn.calls:

                results.append({
                    "module": module.module_id,
                    "function": fn.name,
                    "line": fn.start_line
                })

    return results
