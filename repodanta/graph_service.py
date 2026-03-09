from repodanta.models import Repo

def analyze_structure(repo: Repo) -> None:
    module_map = {m.module_id: m for m in repo.modules.values()}

    # fan-out: how many modules this one imports
    for module in module_map.values():
        module.fan_out = len(module.imports)

    # fan-in: how many modules import this one
    for module in module_map.values():
        for imp in module.imports:
            if imp in module_map:
                module_map[imp].fan_in += 1

    # risk score: computed after all fan-in and fan-out are finalized
    for module in module_map.values():
        module.risk_score = (module.fan_in * 2) + module.fan_out

