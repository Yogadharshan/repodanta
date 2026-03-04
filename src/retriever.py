import numpy as np

def retrieve(query_vec, index, chunks, top_k=5):

    scores, indices = index.search(query_vec, top_k)

    results = []

    for i in indices[0]:
        if i == -1:
            continue
        results.append(chunks[i])

    return results