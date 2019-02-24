#
# Copyright (C) 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
r"""
.. module:: smhtml
   :platform: Unix, Windows
   :synopsis: Simple MHTML parsing library

python-smhtml is a simple and experimental MHTML parsing library for python.

- Home: https://github.com/ssato/python-smhtml

"""
from .api import (
    AUTHOR, VERSION, load, loads, dump, dumps, extract  # flake8: noqa
)

__author__ = AUTHOR
__version__ = VERSION

__all__ = ["load", "load", "extract", "dump", "dumps"]

# vim:sw=4:ts=4:et:
