from src.models import Chunk, Repo, ModuleNode, FunctionNode


def chunk_repo(repo: Repo) -> list[Chunk]:
    chunks = []
    for module in repo.modules.values():
        try:
            lines = module.abs_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception as e:
            print(f"Error reading {module.abs_path}: {e}")
            continue
        # case 1: module has functions, chunk by function
        for fn in module.functions:
            if module.functions:
                for fn in module.functions:
                    # python AST lines are 1-indexed
                    start = fn.start_line - 1
                    end = fn.end_line

                    content = "\n".join(lines[start:end]).strip()

                    chunk_id = f"{module.module_id}:{fn.name}"

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
                content = "\n".join(lines).strip()

                if not content:
                    continue

                chunk_id = f"{module.module_id}:file"

                chunk = Chunk(
                    id=chunk_id,
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