from embedder import embed_query
from models import Repo
from retriever import retrieve
from llm_interface import ask_llm

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

    retrieved = retrieve(query_vec, index, chunks, query, top_k=5)

    architecture = build_architecture_summary(repo)

    code_context = build_chunk_context(retrieved)

    prompt = f"""
    Project: Repodanta  
    An open-source repository intelligence tool.

    Role:
    You analyze a software repository. Expert in software architecture and code analysis. Respond directly without conversational phrases.

    Question:
    {query}

    Architecture:
    {architecture}

    Code:
    {code_context}

    Process:
    1. Find relevant modules/files from the architecture.
    2. Identify related classes, functions, or methods in the code.
    3. Explain only the functions directly related to the question.
    4. Ignore unrelated code.

    Rules:
    - Use only the provided architecture and code.
    - Mention module/file and function names.
    - No conversational phrases.
    - No assumptions.
    - No invented history, authors, or companies.
    - If missing: "not found in retrieved code".
    - If unspecified: "not specified in the repository".
    - Keep explanations short and technical.

    Output format:

    modules:
    - <module/file>

    functions:
    - <function/class> (<module>)

    explanation:
    short technical explanation

    answer:
    direct answer
    """
        
    answer = ask_llm(prompt)
    return answer