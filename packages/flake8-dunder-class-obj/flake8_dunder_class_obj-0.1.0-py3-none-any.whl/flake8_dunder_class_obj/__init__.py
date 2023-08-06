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

    def visit_ClassDef(self: "Visitor", node: ast.ClassDef) -> None:  # noqa: N802
        """
        Visit each ClassDef.

        Search for Assignment to a __ and see if it starts with double underscore.
        :param node: The ast ClassDef node
        """
        for n in node.body:
            if type(n) == ast.Assign:
                for target in n.targets:
                    if (
                        type(target) == ast.Name
                        and str(target.id).startswith("__")
                        and not str(target.id).endswith("__")
                    ):
                        self.problems.append((target.lineno, target.col_offset))
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
