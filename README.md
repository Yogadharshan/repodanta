# repodanta

repository intelligence engine for developers who need to understand large codebases fast.

no docs needed. just point it at a repo.

---

## what it does

repodanta combines structural analysis, dependency graphing, and ai reasoning to answer questions about any codebase.

tested on [fastapi](https://github.com/tiangolo/fastapi) — 1118 modules, 107k lines of code, analyzed in seconds.

---

## commands

### inspect

get a structural overview of any repo.

```bash
repodanta inspect /path/to/repo
```

```
repository overview
----------------------------------------
modules           : 1118
functions         : 4390
lines of code     : 107283
avg funcs/module  : 3.93
----------------------------------------
largest module    : tests.test_include_router_defaults_overrides.py (7304 LOC)
largest function  : tests.test_include_router_defaults_overrides.py:test_openapi (6865 lines)
----------------------------------------
dependency hotspots
  fastapi.testclient.py (fan-in=449, fan-out=1, score=449)
  fastapi.responses.py  (fan-in=74,  fan-out=3, score=222)
  fastapi.routing.py    (fan-in=15,  fan-out=12, score=180)

orchestration modules
  fastapi.applications.py (fan-out=14)
  fastapi.routing.py      (fan-out=12)

core modules
  fastapi.testclient.py (fan-in=449)
  fastapi.responses.py  (fan-in=74)

risky modules
  fastapi.testclient.py (risk=899)
  fastapi.responses.py  (risk=151)
----------------------------------------
```

> fastapi's `testclient.py` has a fan-in of 449 — nearly half the codebase depends on it. you'd never know that just by reading the code.

---

### trace

find how a function is reached in the system.

```bash
repodanta trace /path/to/repo get_request_handler
```

```
call chain
----------------------------------------
fastapi.routing.py:get_route_handler
?:get_request_handler
----------------------------------------
```

---

### query

ask questions about the codebase in plain english.

```bash
repodanta query /path/to/repo "how does request routing work"
```

```
request routing in fastapi flows through routing.py.
get_route_handler determines which endpoint matches
the incoming request and returns the handler function.
```

---

## install
```bash
git clone https://github.com/Yogadharshan/repodanta.git
cd repodanta
pip install -e .
```

**requirements**
- ollama running locally with qwen2.5
```bash
ollama pull qwen2.5
ollama serve
```

> on first run, sentence-transformers will download the embedding model automatically.
> you may see an unauthenticated warning from huggingface — this is harmless.

## how it works

```
structural analysis    →  dependency graph, fan-in/fan-out, hotspot detection
call chain tracing     →  ast-based function call graph traversal
semantic search        →  embeddings + faiss + ai reasoning over retrieved chunks
```

repodanta doesn't just describe code. it understands how the system is connected.

---

## built with
- python ast — static analysis
- sentence-transformers — code embeddings
- faiss — vector search
- ollama (qwen2.5) — local ai reasoning, no api key needed

---

## status

early stage. currently supports python repos only.

built by [Yogadharshan](https://github.com/Yogadharshan).
