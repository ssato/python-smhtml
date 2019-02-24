#
# -*- coding: utf-8; mode: python -*-
#
# Copyright (C) 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=unused-import
r"""Utility functions.

.. versionadded:: 0.0.1
"""
from __future__ import absolute_import

import chardet


def detect_charset(bmsg, default="ascii"):
    r"""
    :param bmsg: A byte data to detect charset
    :return: A string represents charset such as 'utf-8', 'iso-2022-jp'

    >>> detect_charset(b"a")
    'ascii'
    >>> detect_charset(b"")
    'ascii'
    >>> detect_charset(u"あ".encode("utf-8"))
    'utf-8'
    """
    if not bmsg:
        return default

    return chardet.detect(bmsg)["encoding"]

# vim:sw=4:ts=4:et:
