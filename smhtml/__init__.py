#
# Copyright (C) 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
r"""
.. module:: smhtml
   :platform: Unix, Windows
   :synopsis: Simple python library to load, extract and dump MHTML data

python-smhtml is a simple and experimental python library to load MHTML files and
extract files from them, and dump (make) MHTML data from files.

- Home: https://github.com/ssato/python-smhtml

About MHTML format, please refer other web pages such like
https://en.wikipedia.org/wiki/MHTML.
"""
from .api import (
    AUTHOR, VERSION, load, loads, dump, dumps, extract  # flake8: noqa
)

__author__ = AUTHOR
__version__ = VERSION

__all__ = ["load", "load", "extract", "dump", "dumps"]

# vim:sw=4:ts=4:et:
