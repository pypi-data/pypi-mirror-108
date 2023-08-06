# -*- coding: utf-8 -*-
"""
Test flake8_dunder_class_obj.

Basic tests for flake8_dunder_class_obj
"""
import ast

import pytest

import flake8_dunder_class_obj


def test_flake8_dunder_class_obj_version():
    """Check __version__."""
    assert flake8_dunder_class_obj.__version__.startswith("0.1.")


def test_flake8_dunder_class_obj_plugin_attrs():
    assert flake8_dunder_class_obj.Plugin.name == "flake8_dunder_class_obj"
    assert flake8_dunder_class_obj.Plugin.version.startswith("0.1.")


message = "DCO100: class objects should not begin with __ unless name mangling desired"
plugin_type = type(flake8_dunder_class_obj.Plugin(ast.parse("")))


@pytest.mark.parametrize(
    ("input_", "expected"),
    [
        ("", set()),
        (
            "class Test:\n    __var = 1",
            {(2, 4, message, plugin_type)},
        ),
        (
            "class Test:\n    def __init__(self):\n        self.__wut_ = 1",
            {(3, 13, message, plugin_type)},
        ),
        ('getattr(self, "__test")', {(1, 14, message, plugin_type)}),
        ('hasattr(self, "__test")', {(1, 14, message, plugin_type)}),
        ("self.__attr", {(1, 5, message, plugin_type)}),
        ("test.__func()", {(1, 5, message, plugin_type)}),
        ("test.__attr.foo", {(1, 5, message, plugin_type)}),
        ("class Test:\n    def __init__(self):\n        self._wut_ = 1", set()),
        ("class Test:\n    pass", set()),
        ("class Test:\n    var = 1", set()),
        ("class Test:\n    __myvar__ = 1", set()),
    ],
)
def test_plugin(input_, expected):
    tree = ast.parse(input_)
    plugin = flake8_dunder_class_obj.Plugin(tree)
    results = set(plugin.run())
    assert results == expected
