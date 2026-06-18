"""Tests for IR model extensions."""
import tempfile
from pathlib import Path

import pytest
from repodanta.models import (
    Chunk,
    ClassNode,
    Edge,
    FunctionNode,
    ModuleNode,
    Repo,
)


# --- ClassNode ---

def test_class_node_defaults():
    c = ClassNode(name="MyClass", module_id="mymod.py")
    assert c.bases == []
    assert c.methods == []


def test_class_node_with_bases():
    c = ClassNode(name="Child", module_id="mymod.py", bases=["Base", "Mixin"])
    assert c.bases == ["Base", "Mixin"]


def test_class_node_with_methods():
    c = ClassNode(name="Foo", module_id="mymod.py", methods=["__init__", "run"])
    assert c.methods == ["__init__", "run"]


# --- Edge ---

def test_edge_import():
    e = Edge(source="a.py", target="b.py", kind="import")
    assert e.source == "a.py"
    assert e.target == "b.py"
    assert e.kind == "import"


def test_edge_call():
    e = Edge(source="mod.fn", target="mod.other_fn", kind="call")
    assert e.kind == "call"


def test_edge_inherit():
    e = Edge(source="Child", target="Base", kind="inherit")
    assert e.kind == "inherit"


# --- FunctionNode new fields ---

def test_function_node_backward_compat():
    """Existing call sites without new fields must still work."""
    fn = FunctionNode(
        name="foo",
        module_id="mod.py",
        start_line=1,
        end_line=5,
    )
    assert fn.qualified_name == ""
    assert fn.decorators == []
    assert fn.is_async is False
    assert fn.calls == []


def test_function_node_qualified_name():
    fn = FunctionNode(
        name="bar",
        module_id="repodanta/retriever.py",
        start_line=1,
        end_line=3,
        qualified_name="repodanta/retriever.py.bar",
    )
    assert fn.qualified_name == "repodanta/retriever.py.bar"


def test_function_node_decorators():
    fn = FunctionNode(
        name="handler",
        module_id="mod.py",
        start_line=1,
        end_line=5,
        decorators=["staticmethod", "cache"],
    )
    assert fn.decorators == ["staticmethod", "cache"]


def test_function_node_is_async():
    fn = FunctionNode(
        name="fetch",
        module_id="mod.py",
        start_line=1,
        end_line=3,
        is_async=True,
    )
    assert fn.is_async is True


# --- ModuleNode.classes is list[ClassNode] ---

def test_module_node_classes_default_empty():
    tmp = Path(tempfile.mktemp(suffix=".py"))
    tmp.write_text("")
    m = ModuleNode(module_id="mod.py", abs_path=tmp, language="py", lines_of_code=0)
    assert m.classes == []


def test_module_node_classes_accepts_class_nodes():
    tmp = Path(tempfile.mktemp(suffix=".py"))
    tmp.write_text("")
    c = ClassNode(name="Foo", module_id="mod.py")
    m = ModuleNode(
        module_id="mod.py",
        abs_path=tmp,
        language="py",
        lines_of_code=0,
        classes=[c],
    )
    assert len(m.classes) == 1
    assert isinstance(m.classes[0], ClassNode)
    assert m.classes[0].name == "Foo"


# --- Repo.edges ---

def test_repo_edges_default_empty():
    repo = Repo(root=Path("/tmp"), modules={})
    assert repo.edges == []


def test_repo_existing_fields_preserved():
    repo = Repo(root=Path("/tmp"), modules={})
    assert hasattr(repo, "module_graph")
    assert hasattr(repo, "function_graph")
    assert repo.module_graph == {}
    assert repo.function_graph == {}


def test_repo_edges_can_be_populated():
    e1 = Edge(source="a.py", target="b.py", kind="import")
    e2 = Edge(source="a.fn", target="b.fn", kind="call")
    repo = Repo(root=Path("/tmp"), modules={}, edges=[e1, e2])
    assert len(repo.edges) == 2
    assert repo.edges[0].kind == "import"
    assert repo.edges[1].kind == "call"
