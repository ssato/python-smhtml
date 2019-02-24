#
# Copyright (C) 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=unused-import
r"""Public APIs of smhtml module.

.. versionadded:: 0.1
"""
from __future__ import absolute_import

from .globals import (
    PACKAGE, AUTHOR, VERSION, LOGGER  # flake8: noqa
)
from .loader import load, loads  # flake8: noqa
from .dumper import dump, dumps  # flake8: noqa


def version():
    """:return: Version info tuple, (major, minor, release), e.g. (0, 8, 2)
    """
    return VERSION.split('.')

# vim:sw=4:ts=4:et:
