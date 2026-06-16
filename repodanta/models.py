from dataclasses import dataclass, field
from typing import List, Dict
from pathlib import Path


@dataclass
class ClassNode:
    name: str
    module_id: str
    bases: list[str] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)


@dataclass
class Edge:
    source: str
    target: str
    kind: str  # "import" | "call" | "inherit"


@dataclass
class FunctionNode:
    name: str
    module_id: str
    start_line: int
    end_line: int
    calls: list[str] = field(default_factory=list)
    qualified_name: str = ""
    decorators: list[str] = field(default_factory=list)
    is_async: bool = False


@dataclass
class ModuleNode:
    module_id: str
    abs_path: Path
    language: str
    lines_of_code: int
    imports: List[str] = field(default_factory=list)
    functions: List[FunctionNode] = field(default_factory=list)
    classes: list[ClassNode] = field(default_factory=list)
    fan_in: int = 0
    fan_out: int = 0
    risk_score: int = 0


@dataclass
class Repo:
    root: Path
    modules: Dict[str, ModuleNode]
    total_lines: int = 0
    total_modules: int = 0
    module_graph: dict[str, list[str]] = field(default_factory=dict)
    function_graph: dict[str, list[str]] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)


@dataclass
class Chunk:
    chunk_id: str
    module_id: str
    function_name: str
    content: str
    fan_in: int
    fan_out: int
    start_line: int
    end_line: int