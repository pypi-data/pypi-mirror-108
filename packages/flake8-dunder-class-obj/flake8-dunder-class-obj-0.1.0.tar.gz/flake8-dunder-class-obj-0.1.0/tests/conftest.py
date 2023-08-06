# -*- coding: utf-8 -*-
"""Pytest config and global fixtures."""
import pytest


@pytest.fixture(autouse=True)
def _no_requests(request, monkeypatch):
    if request.node.get_closest_marker("requests"):
        return

    def func(*args, **kwargs):
        pytest.fail("External connections not allowed during tests.")

    monkeypatch.setattr("socket.socket", func)
