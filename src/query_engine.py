from src.embedder import embed_query
from src.models import Repo
from src.retriever import retrieve
from src.llm_interface import ask_llm

# Given a query vector, retrieve relevant code chunks and generate an answer
def build_chunk_context(chunks):

    context = ""

    for c in chunks[:3]:  # Limit to top 3 chunks for context
        if c.function_name is None:
            continue
        if c.function_name == "main":
            continue
        
        context += f"""
        module: {c.module_id}
        function: {c.function_name}
        lines: {c.start_line}-{c.end_line}

        code:
        {c.content}

    """
        
    return context.strip()

# Use the retrieved context to generate an answer (e.g. using a language model)
def build_architecture_summary(repo: Repo) -> str:

    modules = repo.modules.values()

    # top fan-out modules (orchestrators)
    top_fanout = sorted(modules, key=lambda m: m.fan_out, reverse=True)[:3]

    # top fan-in modules (core infrastructure)
    top_fanin = sorted(modules, key=lambda m: m.fan_in, reverse=True)[:3]

    summary = "Repository architecture summary:\n\n"

    summary += "Top modules by fan-out (orchestration):\n"
    for m in top_fanout:
        summary += f"- {m.module_id} (fan-out={m.fan_out})\n"

    summary += "\nTop modules by fan-in (core dependencies):\n"
    for m in top_fanin:
        summary += f"- {m.module_id} (fan-in={m.fan_in})\n"

    return summary

def answer_query(query, repo, index, chunks):

    query_vec = embed_query(query)

    retrieved = retrieve(query_vec, index, chunks, top_k=5)

    architecture = build_architecture_summary(repo)

    code_context = build_chunk_context(retrieved)

    prompt = f"""
                You are analyzing a software repository.

                User question:
                {query}

                {architecture}

                Relevant code snippets:
                {code_context}

                Explain the answer clearly for a developer.
                Reference the functions and modules where the behavior occurs.
                """
    
    answer = ask_llm(prompt)
    return answer