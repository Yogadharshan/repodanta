# devvedanta

devvedanta is a local cli tool that analyzes a python codebase using
both structural metrics and semantic retrieval.

it is built as a learning experiment in system design,

---

## what it does

- indexes a python repository
- builds an import dependency graph
- computes fan-in and fan-out metrics
- detects circular imports
- chunks code by function and class
- builds a semantic embedding index
- answers structural and semantic questions using a local llm

---

## why it exists

large codebases are hard to reason about.

most tools do one of the following:

- static analysis (structure only)
- semantic search (meaning only)

devvedanta combines both:

- structure grounds truth
- embeddings capture meaning
- llm explains insights

this project is intentionally minimal.
as the goal is clarity and system understanding.

---

## architecture overview

layers:

1. ingestion layer  
   - file loader  
   - ast parser  

2. structural intelligence layer  
   - import graph  
   - fan-in / fan-out metrics  
   - circular dependency detection  

3. semantic layer  
   - function/class chunking  
   - embeddings  
   - faiss vector index  

4. reasoning layer  
   - hybrid prompt construction  
   - local llm inference  

---

## constraints

- python only
- cli only
- local models only
- no cloud
- no ui

---

## commands (planned)

devvedanta index <path>  
devvedanta analyze-architecture <path>  
devvedanta explain-module <module>  
devvedanta find-duplicates <path>  
devvedanta refactor-plan <path>  

---

## philosophy

deterministic structure first.
probabilistic reasoning second.

metrics are computed, not guessed.
llm explains, not measures.

---

## status

in active development.