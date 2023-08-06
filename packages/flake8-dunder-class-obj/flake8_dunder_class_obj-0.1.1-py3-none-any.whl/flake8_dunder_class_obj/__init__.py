# -*- coding: utf-8 -*-
"""
Flake8 dunder class object plugin.

Find and report on double underscore class objects
"""
import ast
from typing import Any, Generator, List, Tuple, Type

from .version import version as __version__  # noqa


class Visitor(ast.NodeVisitor):
    """Traverse the tree looking for double underscored variables."""

    def __init__(self: "Visitor") -> None:
        """Traverse the tree looking for double underscored variables."""
        self.problems: List[Tuple[int, int]] = []

    @staticmethod
    def _can_mangle(string_to_check: str) -> bool:
        if string_to_check.startswith("__") and not string_to_check.endswith("__"):
            return True
        return False

    def visit_ClassDef(self: "Visitor", node: ast.ClassDef) -> None:  # noqa: N802
        """
        Visit each ClassDef.

        Search for Assignment to a __ and see if it starts with double underscore.
        :param node: The ast ClassDef node
        """
        for n in node.body:
            if type(n) == ast.Assign:
                for target in n.targets:
                    if type(target) == ast.Name and self._can_mangle(target.id):
                        self.problems.append((target.lineno, target.col_offset))
        self.generic_visit(node)

    def visit_Attribute(self: "Visitor", node: ast.Attribute) -> None:  # noqa: N802
        """
        Visit each Attribute.

        flag double unders
        :param node: the ast Attribute node
        """
        if self._can_mangle(node.attr):
            self.problems.append((node.lineno, node.value.end_col_offset + 1))
        self.generic_visit(node)

    def visit_Call(self: "Visitor", node: ast.Call) -> None:  # noqa: N802
        """
        Visit each Call.

        If the call is getattr(self, "__dundervar_"), flag it
        :param node: The ast Call node
        """
        if type(node.func) == ast.Name and node.func.id in ["getattr", "hasattr"]:
            for arg in node.args:
                if type(arg) == ast.Constant and self._can_mangle(arg.value):
                    self.problems.append((arg.lineno, arg.col_offset))
        self.generic_visit(node)


class Plugin:
    """
    Flake8 dunder class object plugin.

    Find and report on double underscore class objects
    """

    MSG = "DCO100: class objects should not begin with __ unless name mangling desired"

    name = __name__
    version = __version__

    def __init__(self: "Plugin", tree: ast.AST) -> None:
        """
        Create plugin with tree.

        :param tree: The source code ast
        """
        self._tree = tree

    def run(self: "Plugin") -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        """
        Run the code checking.

        :yields: A generator of results. Generator(line, column, message, _)
        """
        visitor = Visitor()
        visitor.visit(self._tree)
        for line, col in visitor.problems:
            yield line, col, self.MSG, type(self)
