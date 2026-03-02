from dataclasses import dataclass, field
from typing import List, Dict
from pathlib import Path

@dataclass
class ModuleNode:
    module_id: str
    abs_path: Path
    language: str
    lines_of_code: int
    imports: List[str] = field(default_factory=list)
    functions: List["FunctionNode"] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)

@dataclass
class FunctionNode:
    name: str
    module_name: str
    start_line: int
    end_line: int

@dataclass
class Repo:
    root: Path
    modules: Dict[str, ModuleNode]
    total_lines:int = 0
    total_modules:int = 0