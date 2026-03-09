from repodanta.models import Repo


def trace_call_chain(repo: Repo, target_function: str):
    chain = []
    graph = repo.function_graph
    current = target_function
    visited = set()

    while True:
        if current in visited:
            break
        visited.add(current)

        found = False
        for caller, callees in graph.items():
            if current in callees:
                parts = caller.split(".")
                module = ".".join(parts[:-1])
                func = parts[-1]
                chain.insert(0, (module, func))
                current = caller  # use full key, not just func name
                found = True
                break

        if not found:
            break

    # only append target if it was actually found in graph
    if target_function in graph or any(target_function in v for v in graph.values()):
        chain.append(("?", target_function))

    return chain