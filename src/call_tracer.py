from models import Repo


def trace_call_chain(repo: Repo, target: str):

    graph = repo.function_graph

    visited = set()
    stack = [target]

    chain = []
    # Perform a depth-first search to find all functions that call the target function
    while stack:
        current = stack.pop()
        for fn, calls in graph.items():
            if any(current in c for c in calls):
                visited.add(fn)
                chain.append((fn, current))
                stack.append(fn)

    return chain