import tempfile
from pathlib import Path

import pytest
from repodanta.chunker import chunk_repo
from repodanta.models import Chunk, FunctionNode, ModuleNode, Repo


def _make_repo(source: str, language: str = "py") -> tuple[Repo, Path]:
    tmp = tempfile.NamedTemporaryFile(suffix=f".{language}", mode="w", delete=False)
    tmp.write(source)
    tmp.flush()
    tmp.close()
    path = Path(tmp.name)
    lines = source.splitlines()
    module = ModuleNode(
        module_id=path.name,
        abs_path=path,
        language=language,
        lines_of_code=len(lines),
    )
    repo = Repo(root=path.parent, modules={path.name: module})
    return repo, path


def test_import_works():
    # P1-2 regression: bare import would raise ImportError when package-imported
    from repodanta.chunker import chunk_repo as _fn
    assert callable(_fn)


def test_chunk_by_function():
    source = "def foo():\n    return 1\ndef bar():\n    return 2\n"
    repo, _ = _make_repo(source)
    module = list(repo.modules.values())[0]
    module.functions = [
        FunctionNode(name="foo", module_id=module.module_id, start_line=1, end_line=2),
        FunctionNode(name="bar", module_id=module.module_id, start_line=3, end_line=4),
    ]
    chunks = chunk_repo(repo)
    names = {c.function_name for c in chunks}
    assert names == {"foo", "bar"}


def test_dunder_functions_skipped():
    source = "def __init__(self):\n    pass\ndef real_fn():\n    return 1\n"
    repo, _ = _make_repo(source)
    module = list(repo.modules.values())[0]
    module.functions = [
        FunctionNode(name="__init__", module_id=module.module_id, start_line=1, end_line=2),
        FunctionNode(name="real_fn", module_id=module.module_id, start_line=3, end_line=4),
    ]
    chunks = chunk_repo(repo)
    names = {c.function_name for c in chunks}
    assert "__init__" not in names
    assert "real_fn" in names


def test_whole_file_chunk_when_no_functions():
    source = "x = 1\ny = 2\n"
    repo, _ = _make_repo(source)
    # no functions set — module.functions == []
    chunks = chunk_repo(repo)
    assert len(chunks) == 1
    assert chunks[0].function_name is None
    assert chunks[0].content.strip() == source.strip()


def test_chunk_id_format_function():
    source = "def myfn():\n    pass\n"
    repo, _ = _make_repo(source)
    module = list(repo.modules.values())[0]
    module.functions = [
        FunctionNode(name="myfn", module_id=module.module_id, start_line=1, end_line=2),
    ]
    chunks = chunk_repo(repo)
    assert chunks[0].chunk_id == f"{module.module_id}:myfn:1"


def test_chunk_id_format_file():
    source = "x = 1\n"
    repo, _ = _make_repo(source)
    module = list(repo.modules.values())[0]
    chunks = chunk_repo(repo)
    assert chunks[0].chunk_id == f"{module.module_id}:file"


def test_empty_file_produces_no_chunk():
    repo, _ = _make_repo("")
    chunks = chunk_repo(repo)
    assert chunks == []


def test_chunk_carries_fan_in_fan_out():
    source = "def fn():\n    pass\n"
    repo, _ = _make_repo(source)
    module = list(repo.modules.values())[0]
    module.fan_in = 3
    module.fan_out = 7
    module.functions = [
        FunctionNode(name="fn", module_id=module.module_id, start_line=1, end_line=2),
    ]
    chunks = chunk_repo(repo)
    assert chunks[0].fan_in == 3
    assert chunks[0].fan_out == 7
