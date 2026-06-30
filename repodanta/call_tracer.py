from repodanta.models import Repo


def trace_call_chain(repo: Repo, target_function: str):
    chain = []
    graph = repo.function_graph
    current_name = target_function
    visited = set()

    while True:
        if current_name in visited:
            break
        visited.add(current_name)

        found = False
        for caller_key, callees in graph.items():
            if current_name in callees:
                parts = caller_key.split(".")
                module = ".".join(parts[:-1])
                func = parts[-1]
                chain.insert(0, (module, func))
                current_name = func
                found = True
                break

        if not found:
            break

    if target_function in graph or any(target_function in v for v in graph.values()):
        chain.append(("?", target_function))

    return chain
