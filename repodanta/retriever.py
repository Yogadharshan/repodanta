from typing import Any
from repodanta.models import Chunk


def retrieve(query_vec: Any, index: Any, chunks: list[Chunk], query: str, top_k: int = 5) -> list[Chunk]:
    scores, indices = index.search(query_vec, top_k * 3)

    candidates = []

    for score, idx in zip(scores[0], indices[0]):

        if idx < 0 or idx >= len(chunks):
            continue

        chunk = chunks[idx]

        final_score = float(score)

        module_name = chunk.module_id.split("/")[-1].replace(".py", "")

        if module_name in query:
            final_score += 0.5

        if chunk.function_name and chunk.function_name in query:
            final_score += 1.0

        candidates.append((final_score, chunk))

    # sort again after boosting
    candidates.sort(key=lambda x: x[0], reverse=True)

    # deduplicate before slicing so duplicates don't consume top_k slots
    seen: set[str] = set()
    unique_candidates = []
    for score, chunk in candidates:
        if chunk.chunk_id not in seen:
            unique_candidates.append((score, chunk))
            seen.add(chunk.chunk_id)

    return [c[1] for c in unique_candidates[:top_k]]