# repodanta

repodanta analyzes a python codebase using static analysis and semantic search to help developers understand complex repositories.

## features

- repository indexing
- dependency graph analysis
- function extraction
- call graph tracing
- semantic code search
- duplicate code detection
- sensitive api detection
- local llm explanation via ollama

## usage

```bash
python main.py . --query "where are files read"
```

## example
```
question:
where are files read in this repository?

answer:
src.index_service.scan_files
src.function_service.extract_functions
```

## architecture

repodanta combines
- static code analysis
- vector search
- architecture signals
- llm reasoning

## demo

