repodanta architecture

1 index layer
   scans repository and builds module index

2 analysis layer
   extracts imports, functions, and call graph

3 chunking layer
   splits functions into searchable units

4 embedding layer
   converts code chunks to vectors

5 retrieval layer
   faiss search

6 reasoning layer
   llm explains retrieved code