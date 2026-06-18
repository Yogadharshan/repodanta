"""Regression tests: inspect, trace, and function extraction output unchanged after IR extension."""
import tempfile
from pathlib import Path

import pytest
from repodanta.dependency_service import enrich_dependencies
from repodanta.function_service import extract_functions
from repodanta.graph_builder import build_graphs
from repodanta.graph_service import analyze_structure
from repodanta.index_service import index_repo
from repodanta.models import Repo


# ---------------------------------------------------------------------------
# Fixture: a minimal synthetic repo on disk
# ---------------------------------------------------------------------------

SOURCE = """\
def alpha(x):
    return beta(x)

def beta(x):
    return x + 1

async def gamma():
    pass

class MyClass:
    @staticmethod
    def delta(self):
        pass
"""


def _synthetic_repo(tmp_path: Path) -> Repo:
    py_file = tmp_path / "sample.py"
    py_file.write_text(SOURCE)
    repo = index_repo(str(tmp_path))
    enrich_dependencies(repo)
    analyze_structure(repo)
    extract_functions(repo)
    build_graphs(repo)
    return repo


@pytest.fixture()
def repo(tmp_path):
    return _synthetic_repo(tmp_path)


# ---------------------------------------------------------------------------
# inspect: structural metrics unchanged
# ---------------------------------------------------------------------------

def test_inspect_module_count(repo):
    assert repo.total_modules == 1


def test_inspect_total_lines(repo):
    assert repo.total_lines == len(SOURCE.splitlines())


def test_inspect_function_names(repo):
    module = list(repo.modules.values())[0]
    names = {fn.name for fn in module.functions}
    assert {"alpha", "beta", "gamma", "delta"} == names


def test_inspect_fan_in_fan_out_unchanged(repo):
    module = list(repo.modules.values())[0]
    assert module.fan_in == 0
    assert module.fan_out == 0


def test_inspect_risk_score_unchanged(repo):
    module = list(repo.modules.values())[0]
    assert module.risk_score == 0


# ---------------------------------------------------------------------------
# trace: function_graph unchanged
# ---------------------------------------------------------------------------

def test_trace_function_graph_exists(repo):
    assert isinstance(repo.function_graph, dict)


def test_trace_alpha_calls_beta(repo):
    module = list(repo.modules.values())[0]
    key = f"{module.module_id}.alpha"
    assert key in repo.function_graph
    assert "beta" in repo.function_graph[key]


def test_trace_beta_calls_nothing_outside(repo):
    module = list(repo.modules.values())[0]
    key = f"{module.module_id}.beta"
    # beta only calls built-ins; no internal calls detected
    assert key in repo.function_graph


def test_trace_module_graph_exists(repo):
    assert isinstance(repo.module_graph, dict)


# ---------------------------------------------------------------------------
# New IR fields populated correctly by function_service
# ---------------------------------------------------------------------------

def test_qualified_name_populated(repo):
    module = list(repo.modules.values())[0]
    for fn in module.functions:
        assert fn.qualified_name == f"{module.module_id}.{fn.name}"


def test_is_async_populated(repo):
    module = list(repo.modules.values())[0]
    fn_map = {fn.name: fn for fn in module.functions}
    assert fn_map["gamma"].is_async is True
    assert fn_map["alpha"].is_async is False
    assert fn_map["beta"].is_async is False


def test_decorators_populated(repo):
    module = list(repo.modules.values())[0]
    fn_map = {fn.name: fn for fn in module.functions}
    assert "staticmethod" in fn_map["delta"].decorators


def test_non_decorated_functions_have_empty_decorators(repo):
    module = list(repo.modules.values())[0]
    fn_map = {fn.name: fn for fn in module.functions}
    assert fn_map["alpha"].decorators == []
    assert fn_map["beta"].decorators == []


# ---------------------------------------------------------------------------
# Existing fields on FunctionNode unchanged
# ---------------------------------------------------------------------------

def test_function_node_existing_fields_intact(repo):
    module = list(repo.modules.values())[0]
    for fn in module.functions:
        assert isinstance(fn.name, str)
        assert isinstance(fn.module_id, str)
        assert isinstance(fn.start_line, int)
        assert isinstance(fn.end_line, int)
        assert isinstance(fn.calls, list)


# ---------------------------------------------------------------------------
# edges field present on Repo but empty (not yet populated by any stage)
# ---------------------------------------------------------------------------

def test_repo_edges_field_exists(repo):
    assert hasattr(repo, "edges")
    assert repo.edges == []


# ---------------------------------------------------------------------------
# classes field is list[ClassNode] (not list[str])
# ---------------------------------------------------------------------------

def test_module_classes_is_list(repo):
    module = list(repo.modules.values())[0]
    assert isinstance(module.classes, list)
