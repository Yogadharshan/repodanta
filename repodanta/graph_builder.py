from repodanta.models import Repo


def build_module_graph(repo: Repo):
    graph = {}
    for module in repo.modules.values():
        graph[module.module_id] = module.imports
    repo.module_graph = graph


def build_function_graph(repo: Repo):
    graph = {}
    for module in repo.modules.values():
        for fn in module.functions:
            key = f"{module.module_id}.{fn.name}"
            graph[key] = list(fn.calls)
    repo.function_graph = graph


def build_graphs(repo: Repo):
    build_module_graph(repo)
    build_function_graph(repo)