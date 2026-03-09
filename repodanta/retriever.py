# Retriever module: Given a query vector, retrieve relevant code chunks and boost scores based on query relevance
def retrieve(query_vec, index, chunks, query, top_k=5):

    scores, indices = index.search(query_vec, top_k * 3)

    candidates = []

    for score, idx in zip(scores[0], indices[0]):

        if idx >= len(chunks):
            continue

        chunk = chunks[idx]


        final_score = float(score)

        # boost if module name appears in query
        module_name = chunk.module_id.split("/")[-1].replace(".py", "")

        if module_name in query:
            final_score += 0.5
        
        # boost if function name appears in query
        if chunk.function_name and chunk.function_name in query:
            final_score += 0.6

        if chunk.function_name and chunk.function_name in query:
            final_score += 1.0

        candidates.append((final_score, chunk))

    # sort again after boosting
    candidates.sort(key=lambda x: x[0], reverse=True)

    results = [c[1] for c in candidates[:top_k]]

    # deduplicate results based on chunk_id
    seen = set()
    unique = []

    for r in results:
        if r.chunk_id not in seen:
            unique.append(r)
            seen.add(r.chunk_id)
    
    results = unique

    return results