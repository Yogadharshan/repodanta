def print_stats(repo):
    total_modules = len(repo.modules)
    total_loc = sum(module.loc for module in repo.modules)

    print(f"Total modules: {total_modules}")
    print(f"Total lines of code: {total_loc}")