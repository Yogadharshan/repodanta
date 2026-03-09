from repodanta.embedder import embed_query
from repodanta.models import Repo
from repodanta.retriever import retrieve
from repodanta.llm_interface import ask_llm
from repodanta.entity_detector import detect_entities


def build_chunk_context(chunks):
    context = ""
    for c in chunks[:3]:
        if c.function_name is None or c.function_name == "main":
            continue
        context += f"""
module: {c.module_id}
function: {c.function_name}
lines: {c.start_line}-{c.end_line}
code:
{c.content}
"""
    return context.strip()


def build_architecture_summary(repo: Repo) -> str:
    modules = repo.modules.values()
    top_fanout = sorted(modules, key=lambda m: m.fan_out, reverse=True)[:3]
    top_fanin = sorted(modules, key=lambda m: m.fan_in, reverse=True)[:3]

    summary = "repository architecture summary:\n\n"
    summary += "top modules by fan-out (orchestration):\n"
    for m in top_fanout:
        summary += f"- {m.module_id} (fan-out={m.fan_out})\n"
    summary += "\ntop modules by fan-in (core dependencies):\n"
    for m in top_fanin:
        summary += f"- {m.module_id} (fan-in={m.fan_in})\n"
    return summary


def answer_query(query, repo, index, chunks):
    query = query.lower().replace(".py", "")
    entities = detect_entities(query, repo)
    query_vec = embed_query(query)

    # fix: actually use filtered candidates in retrieve
    candidate_chunks = chunks
    if entities["modules"]:
        module_ids = set(entities["modules"])
        candidate_chunks = [c for c in chunks if c.module_id in module_ids]
    elif entities["functions"]:
        func_names = {f[1] for f in entities["functions"]}
        candidate_chunks = [c for c in chunks if c.function_name in func_names]

    retrieved = retrieve(query_vec, index, candidate_chunks, query, top_k=5)

    architecture = build_architecture_summary(repo)
    code_context = build_chunk_context(retrieved)

    prompt = f"""
you are analyzing a software repository called repodanta.
answer the user's question using only the provided code snippets.

rules:
- only explain functions and modules that appear in the snippets.
- do not mention external frameworks unless they appear in the code.
- if snippets lack enough info, say: "not enough information in the retrieved code."
- reference module and function names directly.

user question:
{query}

repository architecture:
{architecture}

relevant code snippets:
{code_context}

explain simply for a developer. mention module and function names involved.
"""
    return ask_llm(prompt)