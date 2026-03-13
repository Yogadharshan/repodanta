from repodanta.commands.core import load_repo
import tomllib
from pathlib import Path

def get_repo_version(path: str) -> str:
    toml_path = Path(path) / "pyproject.toml"
    if toml_path.exists():
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
            return data.get("project", {}).get("version", "unknown")
    return "unknown"

def run_inspect(args):
    repo = load_repo(args.path)
    modules = repo.modules.values()

    total_loc = sum(m.lines_of_code for m in modules)
    total_modules = len(repo.modules)
    total_functions = sum(len(m.functions) for m in modules)
    avg_functions = total_functions / total_modules if total_modules else 0

    version = get_repo_version(args.path)
    largest_module = max(modules, key=lambda m: m.lines_of_code)

    largest_function = None
    for m in modules:
        for f in m.functions:
            size = f.end_line - f.start_line
            if not largest_function or size > largest_function[0]:
                largest_function = (size, m.module_id, f.name)

    hotspots = sorted(modules, key=lambda m: m.fan_in * m.fan_out, reverse=True)[:5]
    top_fanout = sorted(modules, key=lambda m: m.fan_out, reverse=True)[:3]
    top_fanin = sorted(modules, key=lambda m: m.fan_in, reverse=True)[:3]
    top_risk = sorted(modules, key=lambda m: (m.fan_in * 2 + m.fan_out), reverse=True)[:3]

    print("\nrepository overview\n")
    print("-" * 40)
    print(f"version           : {version}")
    print("-" * 40)
    print(f"modules           : {total_modules}")
    print(f"functions         : {total_functions}")
    print(f"lines of code     : {total_loc}")
    print(f"avg funcs/module  : {avg_functions:.2f}")
    print("-" * 40)
    print(f"largest module    : {largest_module.module_id} ({largest_module.lines_of_code} LOC)")
    if largest_function:
        print(f"largest function  : {largest_function[1]}:{largest_function[2]} ({largest_function[0]} lines)")
    print("-" * 40)

    print("\ndependency hotspots")
    for m in hotspots:
        score = m.fan_in * m.fan_out
        print(f"  {m.module_id} (fan-in={m.fan_in}, fan-out={m.fan_out}, score={score})")

    print("\norchestration modules")
    for m in top_fanout:
        print(f"  {m.module_id} (fan-out={m.fan_out})")

    print("\ncore modules")
    for m in top_fanin:
        print(f"  {m.module_id} (fan-in={m.fan_in})")

    print("\nrisky modules")
    for m in top_risk:
        risk = m.fan_in * 2 + m.fan_out
        print(f"  {m.module_id} (risk={risk})")

    print("-" * 40)
    print("end of report\n")