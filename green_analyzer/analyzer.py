"""AST-based heuristics for selected potentially costly Python patterns."""
import ast
from dataclasses import asdict, dataclass


@dataclass
class Finding:
    rule_id: str
    severity: str
    line: int
    message: str
    explanation: str
    suggestion: str

    def to_dict(self):
        return asdict(self)


class GreenCodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.findings = []
        self.loop_depth = 0

    def visit_For(self, node):
        if self.loop_depth >= 1:
            self.findings.append(Finding(
                "GCA001", "medium", node.lineno, "Nested for-loop detected",
                "Nested loops can multiply work depending on iteration counts.",
                "Check whether a set, dictionary, index, or single-pass algorithm is appropriate."
            ))
        self.loop_depth += 1
        for child in ast.iter_child_nodes(node):
            self.visit(child)
        self.loop_depth -= 1

    def visit_AsyncFor(self, node):
        if self.loop_depth >= 1:
            self.findings.append(Finding(
                "GCA001", "medium", node.lineno, "Nested async for-loop detected",
                "Nested iteration may multiply work; async syntax alone does not make it cheaper.",
                "Review iteration counts and alternative data structures."
            ))
        self.loop_depth += 1
        for child in ast.iter_child_nodes(node):
            self.visit(child)
        self.loop_depth -= 1

    def visit_Compare(self, node):
        if self.loop_depth > 0:
            for op, comparator in zip(node.ops, node.comparators):
                if isinstance(op, (ast.In, ast.NotIn)) and isinstance(comparator, ast.Name):
                    self.findings.append(Finding(
                        "GCA002", "low", node.lineno,
                        f"Membership check against '{comparator.id}' inside a loop",
                        "If the container is a list, membership is linear in its length. "
                        "The analyzer cannot infer the runtime container type.",
                        "If semantics allow, build a set once for repeated membership checks."
                    ))
                    break
        self.generic_visit(node)


def analyze_source(source, filename="<string>"):
    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError as exc:
        raise ValueError(f"Could not parse {filename}: {exc}") from exc
    visitor = GreenCodeVisitor()
    visitor.visit(tree)
    seen, unique = set(), []
    for f in visitor.findings:
        key = (f.rule_id, f.line, f.message)
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


def analyze_file(path):
    from pathlib import Path
    p = Path(path)
    if p.suffix.lower() != ".py":
        raise ValueError("Input must be a .py file.")
    return analyze_source(p.read_text(encoding="utf-8"), str(p))


def findings_as_dicts(findings):
    return [f.to_dict() for f in findings]
