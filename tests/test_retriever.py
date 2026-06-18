import numpy as np
import pytest
from repodanta.models import Chunk
from repodanta.retriever import retrieve


def _make_chunk(chunk_id: str, module_id: str, function_name: str | None) -> Chunk:
    return Chunk(
        chunk_id=chunk_id,
        module_id=module_id,
        function_name=function_name,
        content="",
        fan_in=0,
        fan_out=0,
        start_line=1,
        end_line=5,
    )


class _MockIndex:
    """Minimal FAISS-compatible mock: search returns preset scores and indices."""

    def __init__(self, scores: list[float], indices: list[int]):
        self._scores = scores
        self._indices = indices

    def search(self, query_vec, k: int):
        n = min(k, len(self._scores))
        return np.array([self._scores[:n]]), np.array([self._indices[:n]])


def _query_vec() -> np.ndarray:
    return np.zeros((1, 384), dtype="float32")


# --- boost tests ---

def test_no_boost_when_no_name_match():
    chunk = _make_chunk("a:fn:1", "embedder.py", "embed_query")
    index = _MockIndex([0.8], [0])
    results = retrieve(_query_vec(), index, [chunk], query="what does the repo do", top_k=1)
    assert results == [chunk]


def test_module_boost_applied():
    chunk_a = _make_chunk("a:fn:1", "embedder.py", "unrelated_fn")
    chunk_b = _make_chunk("b:fn:1", "retriever.py", "unrelated_fn")
    # chunk_b has lower raw score but module name matches query
    index = _MockIndex([0.9, 0.5], [0, 1])
    results = retrieve(_query_vec(), index, [chunk_a, chunk_b], query="retriever logic", top_k=2)
    # chunk_b final = 0.5 + 0.5 = 1.0, chunk_a final = 0.9 — chunk_b wins
    assert results[0] == chunk_b


def test_function_boost_is_one_point_zero():
    """P1-2 regression: old code applied +0.6 + +1.0 = +1.6; fixed code applies +1.0."""
    chunk = _make_chunk("a:embed_query:1", "embedder.py", "embed_query")
    base_score = 0.0
    index = _MockIndex([base_score], [0])
    results = retrieve(_query_vec(), index, [chunk], query="embed_query", top_k=1)
    # Can't inspect internal score directly, but verifying no duplicate boost:
    # If we have two chunks where one matches function name and one doesn't,
    # the matching one should win by exactly +1.0 over a chunk at score +1.05.
    chunk_winner = _make_chunk("w:fn:1", "other.py", "embed_query")
    chunk_loser = _make_chunk("l:fn:1", "other.py", None)
    # loser raw score 1.05, winner raw score 0.0 — winner must overcome via boost
    # +1.0 makes winner 1.0 < loser 1.05 → loser wins (no false +1.6 inflation)
    index2 = _MockIndex([1.05, 0.0], [1, 0])
    results2 = retrieve(_query_vec(), index2, [chunk_winner, chunk_loser], query="embed_query", top_k=2)
    assert results2[0] == chunk_loser  # 1.05 > 1.0


def test_function_boost_wins_at_correct_threshold():
    """Winner with +1.0 boost should beat raw score of 0.95."""
    chunk_winner = _make_chunk("w:fn:1", "other.py", "embed_query")
    chunk_loser = _make_chunk("l:fn:1", "other.py", None)
    # loser raw 0.95, winner raw 0.0 + 1.0 boost = 1.0 → winner wins
    index = _MockIndex([0.95, 0.0], [1, 0])
    results = retrieve(_query_vec(), index, [chunk_winner, chunk_loser], query="embed_query", top_k=2)
    assert results[0] == chunk_winner  # 1.0 > 0.95


def test_deduplication():
    chunk = _make_chunk("a:fn:1", "mod.py", "fn")
    # FAISS returns same index twice (can happen with approximate search)
    index = _MockIndex([0.9, 0.8], [0, 0])
    results = retrieve(_query_vec(), index, [chunk], query="x", top_k=5)
    assert len(results) == 1


def test_top_k_limits_results():
    chunks = [_make_chunk(f"c{i}:fn:1", "mod.py", None) for i in range(10)]
    scores = list(range(10, 0, -1))  # 10, 9, ..., 1
    indices = list(range(10))
    index = _MockIndex(scores, indices)
    results = retrieve(_query_vec(), index, chunks, query="x", top_k=3)
    assert len(results) == 3


def test_out_of_bounds_indices_skipped():
    chunk = _make_chunk("a:fn:1", "mod.py", None)
    # index returns idx=5 but only 1 chunk exists
    index = _MockIndex([0.9, 0.8], [5, 0])
    results = retrieve(_query_vec(), index, [chunk], query="x", top_k=5)
    assert results == [chunk]


def test_negative_faiss_index_skipped():
    # FAISS returns -1 for unfilled result slots; must not be treated as chunks[-1]
    chunk = _make_chunk("a:fn:1", "mod.py", None)
    index = _MockIndex([0.9, 0.8], [-1, 0])
    results = retrieve(_query_vec(), index, [chunk], query="x", top_k=5)
    assert results == [chunk]


def test_duplicate_indices_preserve_top_k_count():
    # When FAISS returns duplicate indices, dedup must happen before top_k slice
    # so that unique result count equals min(top_k, unique_chunks)
    chunks = [_make_chunk(f"c{i}:fn:1", "mod.py", None) for i in range(3)]
    # FAISS returns: idx 0 twice, then 1, then 2 — 3 unique chunks available
    scores = [1.0, 0.9, 0.8, 0.7]
    indices = [0, 0, 1, 2]
    index = _MockIndex(scores, indices)
    results = retrieve(_query_vec(), index, chunks, query="x", top_k=3)
    assert len(results) == 3
    assert len({c.chunk_id for c in results}) == 3
