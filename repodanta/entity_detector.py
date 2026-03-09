def detect_entities(query, repo):
    query = query.lower()

    modules = []
    functions = []

    query = query.replace(".py", "")

    for module in repo.modules.values():

        module_name = module.module_id.split("/")[-1]
        module_name = module_name.replace(".py", "")

        if module_name.lower() in query:
            modules.append(module.module_id)

        for fn in module.functions:
            if fn.name.lower() in query:
                functions.append((module.module_id, fn.name))

    return {
        "modules": modules,
        "functions": functions
    }