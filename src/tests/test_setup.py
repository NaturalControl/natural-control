"""Checks that the project is set up: the package imports and runs on a supported Python."""

import sys

import poc


def test_package_imports() -> None:
    assert poc.__doc__


def test_python_version() -> None:
    assert (3, 12) <= sys.version_info[:2] < (3, 14)
