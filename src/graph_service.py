from src.models import Repo

def analyze_structure(repo: Repo) -> None:
    """
    Analyze the structure of the repository to compute fan-in, fan-out, and risk scores for each module.
    """
    # First, build a mapping of module_id to ModuleNode for easy access
    module_map = {}
    for module in repo.modules.values():
        module_map[module.module_id] = module
    # Calculate fan-in and fan-out for each module
    for module in module_map.values():
        # Fan-out is the number of imports this module has
        module.fan_out = len(module.imports)

            # Fan-in is the number of modules that import this module
        for module in module_map.values():
            for imp in module.imports:
                if imp in module_map:
                    module_map[imp].fan_in += 1

        # Calculate risk score (simple heuristic: fan-in + fan-out)
        module.risk_score = (module.fan_in * 2) + module.fan_out

