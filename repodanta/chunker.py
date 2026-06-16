from repodanta.models import Chunk, Repo, ModuleNode, FunctionNode


def chunk_repo(repo: Repo) -> list[Chunk]:

    MAX_CHUNK_LINES = 80

    chunks = []
    for module in repo.modules.values():
        try:
            lines = module.abs_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception as e:
            print(f"Error reading {module.abs_path}: {e}")
            continue


        # case 1: module has functions, chunk by function
        if module.functions:
            for fn in module.functions:

                if fn.name.startswith("__"):
                    continue

                # python AST lines are 1-indexed
                start = fn.start_line - 1
                end = fn.end_line
                code = lines[start:end]
                code_lines = code[:MAX_CHUNK_LINES]
                if len(code_lines) > MAX_CHUNK_LINES:
                    code_lines = code.splitlines()[:MAX_CHUNK_LINES]

                code = "\n".join(code_lines)

                content = code.strip() # Add more metadata as needed

                chunk_id = f"{module.module_id}:{fn.name}:{fn.start_line}"
                chunk = Chunk(
                    chunk_id=chunk_id,
                    module_id=module.module_id,
                    function_name = fn.name,
                    content=content,
                    fan_in=module.fan_in,
                    fan_out=module.fan_out,
                    start_line=fn.start_line,
                    end_line=fn.end_line
                )
                chunks.append(chunk)
            #case 2: no functions, whole file chunk
        else:
            start = 0
            end = len(lines)
            code = lines[start:end]
            code_lines = code[:MAX_CHUNK_LINES]

            # truncate long files to avoid hitting token limits
            if len(code_lines) > MAX_CHUNK_LINES:
                code_lines = code.splitlines()[:MAX_CHUNK_LINES]
            code = "\n".join(code_lines)

            content = code.strip() # Add more metadata as needed
            if not content:
                continue
            chunk_id = f"{module.module_id}:file"
            chunk = Chunk(
                chunk_id=chunk_id,
                module_id=module.module_id,
                function_name=None,
                content=content,
                fan_in=module.fan_in,
                fan_out=module.fan_out,
                start_line=1,
                end_line=len(lines)
            )
            chunks.append(chunk)
                

            
    return chunks