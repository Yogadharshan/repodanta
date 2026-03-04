import numpy as np

def find_duplicates(chunks, embeddings, threshold=0.95):

    duplicates = []
    similarity_matrix = embeddings @ embeddings.T

    n = len(chunks)

    for i in range(n):
        for j in range (i+1, n):

            if len(chunks[i].content) < 50 or len(chunks[j].content) < 50:
                continue

            # skip if length difference is too large to avoid false positives
            if abs(len(chunks[i].content) - len(chunks[j].content)) > 200:
                continue

            score = similarity_matrix[i, j]
            
            if score > threshold:
                duplicates.append(
                    {
                        "chunk1": chunks[i].chunk_id,
                        "chunk2": chunks[j].chunk_id,
                        "similarity": score
                    }
                )
    return duplicates
